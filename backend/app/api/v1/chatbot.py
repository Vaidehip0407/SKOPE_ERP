from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, timedelta
import httpx
import json

from app.db.database import get_db
from app.db import models
from app.api.dependencies import get_current_user

router = APIRouter()

# Ollama API configuration
OLLAMA_BASE_URL = "http://localhost:11434"
OLLAMA_MODEL = "phi4"  # Will work with any phi4 variant


class ChatRequest(BaseModel):
    message: str
    conversation_history: Optional[List[dict]] = []


class ChatResponse(BaseModel):
    response: str
    context_used: Optional[dict] = None


def get_store_context(db: Session, user: models.User) -> dict:
    """Fetch relevant store data to provide context to the AI"""
    context = {}
    
    # Filter by user's store if not super admin
    store_filter = {}
    if user.role != models.UserRole.SUPER_ADMIN and user.store_id:
        store_filter = {"store_id": user.store_id}
    
    try:
        # Inventory Summary
        products_query = db.query(models.Product)
        if store_filter:
            products_query = products_query.filter(models.Product.store_id == user.store_id)
        
        products = products_query.all()
        total_products = len(products)
        total_inventory_value = sum((p.cost_price or 0) * (p.current_stock or 0) for p in products)
        low_stock_products = [p for p in products if (p.current_stock or 0) <= (p.minimum_stock or 5)]
        out_of_stock = [p for p in products if (p.current_stock or 0) == 0]
        
        context["inventory"] = {
            "total_products": total_products,
            "total_inventory_value": round(total_inventory_value, 2),
            "low_stock_count": len(low_stock_products),
            "out_of_stock_count": len(out_of_stock),
            "low_stock_items": [{"name": p.name, "stock": p.current_stock, "min_level": p.minimum_stock} 
                               for p in low_stock_products[:10]],
            "top_products_by_value": sorted(
                [{"name": p.name, "value": round((p.cost_price or 0) * (p.current_stock or 0), 2)} 
                 for p in products], 
                key=lambda x: x["value"], reverse=True
            )[:5]
        }
        
        # Sales Summary (last 30 days)
        thirty_days_ago = datetime.now() - timedelta(days=30)
        sales_query = db.query(models.Sale).filter(models.Sale.sale_date >= thirty_days_ago)
        if store_filter:
            sales_query = sales_query.filter(models.Sale.store_id == user.store_id)
        
        sales = sales_query.all()
        total_sales = sum(s.total_amount for s in sales)
        total_transactions = len(sales)
        
        # Today's sales
        today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        today_sales = [s for s in sales if s.sale_date >= today_start]
        today_revenue = sum(s.total_amount for s in today_sales)
        
        context["sales"] = {
            "last_30_days_revenue": round(total_sales, 2),
            "last_30_days_transactions": total_transactions,
            "average_transaction_value": round(total_sales / total_transactions, 2) if total_transactions > 0 else 0,
            "today_revenue": round(today_revenue, 2),
            "today_transactions": len(today_sales)
        }
        
        # Customer Summary
        customers_query = db.query(models.Customer)
        if store_filter:
            customers_query = customers_query.filter(models.Customer.store_id == user.store_id)
        
        customers = customers_query.all()
        total_customers = len(customers)
        top_customers = sorted(customers, key=lambda c: c.total_purchases or 0, reverse=True)[:5]
        
        context["customers"] = {
            "total_customers": total_customers,
            "top_customers": [{"name": c.name, "total_purchases": round(c.total_purchases or 0, 2)} 
                             for c in top_customers]
        }
        
        # Financial Summary (expenses last 30 days)
        expenses_query = db.query(models.Expense).filter(models.Expense.expense_date >= thirty_days_ago)
        if store_filter:
            expenses_query = expenses_query.filter(models.Expense.store_id == user.store_id)
        
        expenses = expenses_query.all()
        total_expenses = sum(e.amount for e in expenses)
        
        # Group by category
        expense_by_category = {}
        for e in expenses:
            cat = e.category or "Other"
            expense_by_category[cat] = expense_by_category.get(cat, 0) + e.amount
        
        context["financial"] = {
            "last_30_days_expenses": round(total_expenses, 2),
            "estimated_profit": round(total_sales - total_expenses, 2),
            "expense_breakdown": {k: round(v, 2) for k, v in expense_by_category.items()}
        }
        
        # Store info
        if user.store_id:
            store = db.query(models.Store).filter(models.Store.id == user.store_id).first()
            if store:
                context["store"] = {
                    "name": store.name,
                    "address": store.address
                }
        
    except Exception as e:
        context["error"] = f"Error fetching some data: {str(e)}"
    
    return context


def create_system_prompt(context: dict) -> str:
    """Create a system prompt with store context"""
    return f"""You are an AI assistant for SKOPE ERP, a retail management system. 
You help store managers and staff understand their business data and answer questions about inventory, sales, customers, and finances.

Here is the current store data you have access to:

## Inventory Summary
- Total Products: {context.get('inventory', {}).get('total_products', 'N/A')}
- Total Inventory Value: ₹{context.get('inventory', {}).get('total_inventory_value', 'N/A')}
- Low Stock Items: {context.get('inventory', {}).get('low_stock_count', 'N/A')}
- Out of Stock Items: {context.get('inventory', {}).get('out_of_stock_count', 'N/A')}
- Low Stock Products: {json.dumps(context.get('inventory', {}).get('low_stock_items', []), indent=2)}
- Top Products by Value: {json.dumps(context.get('inventory', {}).get('top_products_by_value', []), indent=2)}

## Sales Summary (Last 30 Days)
- Total Revenue: ₹{context.get('sales', {}).get('last_30_days_revenue', 'N/A')}
- Total Transactions: {context.get('sales', {}).get('last_30_days_transactions', 'N/A')}
- Average Transaction Value: ₹{context.get('sales', {}).get('average_transaction_value', 'N/A')}
- Today's Revenue: ₹{context.get('sales', {}).get('today_revenue', 'N/A')}
- Today's Transactions: {context.get('sales', {}).get('today_transactions', 'N/A')}

## Customer Summary
- Total Customers: {context.get('customers', {}).get('total_customers', 'N/A')}
- Top Customers: {json.dumps(context.get('customers', {}).get('top_customers', []), indent=2)}

## Financial Summary (Last 30 Days)
- Total Expenses: ₹{context.get('financial', {}).get('last_30_days_expenses', 'N/A')}
- Estimated Profit: ₹{context.get('financial', {}).get('estimated_profit', 'N/A')}
- Expense Breakdown: {json.dumps(context.get('financial', {}).get('expense_breakdown', {}), indent=2)}

Instructions:
1. Answer questions based on the data provided above
2. Be helpful, concise, and professional
3. If asked about data you don't have, politely say you don't have that specific information
4. Use Indian Rupees (₹) for currency
5. Provide actionable insights when relevant
6. Format numbers nicely (e.g., ₹1,23,456.00)
"""


def generate_fallback_response(message: str, context: dict) -> ChatResponse:
    """Generate intelligent response using store context when Ollama is unavailable"""
    message_lower = message.lower()
    
    # Format currency
    def fmt_currency(val):
        return f"₹{val:,.2f}" if val else "₹0.00"
    
    inventory = context.get("inventory", {})
    sales = context.get("sales", {})
    customers = context.get("customers", {})
    financial = context.get("financial", {})
    
    # Inventory related queries
    if any(word in message_lower for word in ["inventory", "stock", "product", "item"]):
        low_stock = inventory.get("low_stock_items", [])
        low_stock_text = ", ".join([f"{p['name']} ({p['stock']} units)" for p in low_stock[:5]]) if low_stock else "None"
        response = f"""📦 **Inventory Summary**

• **Total Products:** {inventory.get('total_products', 0)}
• **Total Inventory Value:** {fmt_currency(inventory.get('total_inventory_value', 0))}
• **Low Stock Items:** {inventory.get('low_stock_count', 0)}
• **Out of Stock:** {inventory.get('out_of_stock_count', 0)}

⚠️ **Low Stock Alert:** {low_stock_text}

💡 **Recommendation:** Consider restocking items with low inventory to avoid stockouts."""

    # Sales related queries
    elif any(word in message_lower for word in ["sale", "revenue", "transaction", "today", "selling"]):
        response = f"""📊 **Sales Summary (Last 30 Days)**

• **Total Revenue:** {fmt_currency(sales.get('last_30_days_revenue', 0))}
• **Total Transactions:** {sales.get('last_30_days_transactions', 0)}
• **Average Transaction:** {fmt_currency(sales.get('average_transaction_value', 0))}

📅 **Today's Performance:**
• **Revenue:** {fmt_currency(sales.get('today_revenue', 0))}
• **Transactions:** {sales.get('today_transactions', 0)}

💡 **Insight:** Focus on upselling to increase average transaction value."""

    # Customer related queries
    elif any(word in message_lower for word in ["customer", "client", "buyer", "top customer"]):
        top_custs = customers.get("top_customers", [])
        top_text = "\n".join([f"  • {c['name']}: {fmt_currency(c['total_purchases'])}" for c in top_custs[:5]]) if top_custs else "  No data available"
        response = f"""👥 **Customer Summary**

• **Total Customers:** {customers.get('total_customers', 0)}

🏆 **Top Customers by Purchases:**
{top_text}

💡 **Tip:** Consider loyalty programs for your top customers to increase retention."""

    # Financial/Expense related queries
    elif any(word in message_lower for word in ["expense", "profit", "financial", "money", "cost", "earning"]):
        expense_breakdown = financial.get("expense_breakdown", {})
        expense_text = "\n".join([f"  • {cat}: {fmt_currency(amt)}" for cat, amt in list(expense_breakdown.items())[:5]]) if expense_breakdown else "  No expenses recorded"
        response = f"""💰 **Financial Summary (Last 30 Days)**

• **Total Expenses:** {fmt_currency(financial.get('last_30_days_expenses', 0))}
• **Estimated Profit:** {fmt_currency(financial.get('estimated_profit', 0))}

📋 **Expense Breakdown:**
{expense_text}

💡 **Analysis:** Monitor high-expense categories for cost optimization opportunities."""

    # Help or general queries
    elif any(word in message_lower for word in ["help", "what can you", "how", "capabilities"]):
        response = """👋 **Hello! I'm your SKOPE ERP AI Assistant**

I can help you with:
• 📦 **Inventory** - Stock levels, low stock alerts, product values
• 📊 **Sales** - Revenue, transactions, daily performance
• 👥 **Customers** - Customer counts, top buyers
• 💰 **Financial** - Expenses, profit analysis

Just ask me questions like:
- "How are my sales today?"
- "Show me inventory status"
- "Who are my top customers?"
- "What's my profit this month?"
"""

    # Default response with summary
    else:
        response = f"""📈 **Store Overview**

**Inventory:** {inventory.get('total_products', 0)} products worth {fmt_currency(inventory.get('total_inventory_value', 0))}
**Sales (30 days):** {fmt_currency(sales.get('last_30_days_revenue', 0))} from {sales.get('last_30_days_transactions', 0)} transactions
**Customers:** {customers.get('total_customers', 0)} total
**Estimated Profit:** {fmt_currency(financial.get('estimated_profit', 0))}

Ask me about inventory, sales, customers, or finances for detailed insights!"""

    return ChatResponse(
        response=response,
        context_used={
            "inventory_items": inventory.get("total_products", 0),
            "sales_value": sales.get("last_30_days_revenue", 0),
            "customers": customers.get("total_customers", 0),
            "mode": "fallback"
        }
    )

@router.post("/chat", response_model=ChatResponse)
async def chat_with_ai(
    request: ChatRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Chat with AI assistant about store data"""
    
    # Get store context
    context = get_store_context(db, current_user)
    system_prompt = create_system_prompt(context)
    
    # Build messages for Ollama
    messages = [{"role": "system", "content": system_prompt}]
    
    # Add conversation history
    for msg in request.conversation_history[-10:]:  # Keep last 10 messages
        messages.append(msg)
    
    # Add current message
    messages.append({"role": "user", "content": request.message})
    
    try:
        # Call Ollama API
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                f"{OLLAMA_BASE_URL}/api/chat",
                json={
                    "model": OLLAMA_MODEL,
                    "messages": messages,
                    "stream": False,
                    "options": {
                        "temperature": 0.7,
                        "num_predict": 1000
                    }
                }
            )
            
            if response.status_code != 200:
                raise HTTPException(
                    status_code=503,
                    detail=f"Ollama API error: {response.text}. Make sure Ollama is running with 'ollama serve'"
                )
            
            result = response.json()
            ai_response = result.get("message", {}).get("content", "I apologize, but I couldn't generate a response.")
            
            return ChatResponse(
                response=ai_response,
                context_used={
                    "inventory_items": context.get("inventory", {}).get("total_products", 0),
                    "sales_value": context.get("sales", {}).get("last_30_days_revenue", 0),
                    "customers": context.get("customers", {}).get("total_customers", 0)
                }
            )
            
    except httpx.ConnectError:
        # Fallback: provide intelligent response without Ollama
        return generate_fallback_response(request.message, context)
    except httpx.TimeoutException:
        # Fallback: provide intelligent response without Ollama
        return generate_fallback_response(request.message, context)
    except Exception as e:
        # Fallback: provide intelligent response without Ollama
        return generate_fallback_response(request.message, context)


@router.get("/status")
async def check_ollama_status():
    """Check if Ollama is running and the model is available"""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            # Check if Ollama is running
            response = await client.get(f"{OLLAMA_BASE_URL}/api/tags")
            
            if response.status_code != 200:
                return {"status": "error", "message": "Ollama is not responding correctly"}
            
            models = response.json().get("models", [])
            model_names = [m.get("name", "") for m in models]
            
            # Check if our model is available (accept any phi4 variant or check exact match)
            phi4_available = any("phi4" in name.lower() or OLLAMA_MODEL.lower() in name.lower() for name in model_names)
            
            return {
                "status": "online" if phi4_available else "model_missing",
                "ollama_running": True,
                "model_available": phi4_available,
                "available_models": model_names,
                "required_model": OLLAMA_MODEL,
                "message": "Ready to chat!" if phi4_available else f"Model {OLLAMA_MODEL} not found. Run: ollama pull phi4"
            }
            
    except httpx.ConnectError:
        # Return online since we have fallback mode
        return {
            "status": "online",
            "ollama_running": False,
            "model_available": False,
            "message": "Ready to chat! (Smart Assistant Mode)",
            "mode": "fallback"
        }
    except Exception as e:
        # Return online since we have fallback mode
        return {
            "status": "online",
            "ollama_running": False,
            "model_available": False,
            "message": "Ready to chat! (Smart Assistant Mode)",
            "mode": "fallback"
        }
