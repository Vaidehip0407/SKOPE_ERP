# 🔧 API Testing Guide

## ✅ Quick API Test

### **Test Backend is Running:**

Open your browser and visit:
```
http://localhost:8000/docs
```

You should see the **Swagger UI** with all API endpoints!

---

## 🧪 **Test Sales API:**

### **Method 1: Browser**
```
http://localhost:8000/api/v1/sales/
```

### **Method 2: Command Line (PowerShell)**
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/sales/" -Headers @{"Authorization"="Bearer YOUR_TOKEN"}
```

### **Method 3: Direct Test**
1. Go to http://localhost:8000/docs
2. Click on `/api/v1/sales/` endpoint
3. Click "Try it out"
4. Click "Execute"
5. See the response!

---

## 🔐 **Get Auth Token:**

### **Step 1: Login First**
```
POST http://localhost:8000/api/v1/auth/login
Body: {
  "username": "admin",
  "password": "admin123"
}
```

### **Step 2: Copy the Token**
From response, copy the `access_token`

### **Step 3: Use Token in Headers**
```
Authorization: Bearer YOUR_TOKEN_HERE
```

---

## 📊 **Expected Sales Response:**

```json
[
  {
    "id": 1,
    "invoice_number": "INV120241217001",
    "customer_id": 1,
    "store_id": 1,
    "subtotal": 1999.98,
    "gst_amount": 359.996,
    "discount": 0.0,
    "total_amount": 2359.976,
    "payment_mode": "cash",
    "payment_status": "completed",
    "sale_date": "2024-12-17T10:30:00",
    "items": [...]
  }
]
```

---

## 🐛 **Common Issues:**

### **1. CORS Error**
- Backend should allow localhost:3000
- Check `app/main.py` CORS settings

### **2. Authentication Error**
- Frontend needs valid token
- Token stored in localStorage
- Check browser DevTools → Application → Local Storage

### **3. Database Empty**
- Run: `python seed_data.py` again
- Verify data exists

### **4. Backend Not Running**
- Check: `netstat -ano | findstr :8000`
- Restart: `uvicorn app.main:app --reload --port 8000`

---

## 🔍 **Debug Steps:**

### **1. Check Browser Console (F12)**
```
Network Tab → Look for failed requests
Console Tab → Look for errors
```

### **2. Check Backend Logs**
Look at the terminal where backend is running

### **3. Test API Directly**
Use Swagger UI at http://localhost:8000/docs

---

## ✅ **Quick Fix:**

### **If Sales Still Not Loading:**

1. **Refresh browser** (Ctrl + Shift + R)
2. **Clear cache** (Ctrl + Shift + Del)
3. **Logout and login again**
4. **Check console for errors** (F12)

---

## 📞 **Still Having Issues?**

Check:
- ✅ Backend running on port 8000
- ✅ Frontend running on port 3000
- ✅ Database has data (207 sales)
- ✅ Login successful
- ✅ Token in localStorage

