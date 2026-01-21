# Docker Setup for SKOPE ERP

This guide explains how to run the SKOPE ERP application using Docker.

## Prerequisites

- Docker Desktop installed
- Docker Compose installed

## Quick Start

### Development Environment

1. **Start all services:**
   ```bash
   docker-compose up -d
   ```

2. **Access the application:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - Database: localhost:5432

3. **Stop all services:**
   ```bash
   docker-compose down
   ```

### Production Environment

1. **Start production services:**
   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```

2. **Access the application:**
   - Frontend: http://localhost
   - Backend API: http://localhost:8000

## Services

### PostgreSQL Database
- **Image:** postgres:15-alpine
- **Port:** 5432
- **Database:** skope_erp
- **Username:** postgres
- **Password:** password (development) / configurable (production)

### Backend (FastAPI)
- **Port:** 8000
- **Technology:** Python FastAPI
- **Features:** Auto-reload in development

### Frontend (React)
- **Development Port:** 3000
- **Production Port:** 80
- **Technology:** React + Vite
- **Features:** Hot reload in development, Nginx in production

## Environment Variables

Create a `.env` file in the root directory for production:

```env
POSTGRES_PASSWORD=your_secure_password
DATABASE_URL=postgresql://postgres:your_secure_password@postgres:5432/skope_erp
VITE_API_URL=http://localhost:8000
```

## Docker Commands

### Build specific service:
```bash
docker-compose build backend
docker-compose build frontend
```

### View logs:
```bash
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Execute commands in containers:
```bash
docker-compose exec backend bash
docker-compose exec frontend sh
```

### Reset database:
```bash
docker-compose down -v
docker-compose up -d
```

## Volumes

- **postgres_data:** Persistent database storage
- **backend_uploads:** File uploads storage
- **Frontend source:** Mounted for development hot reload

## Network

All services communicate through the `skope_network` bridge network.

## Troubleshooting

1. **Port conflicts:** Change ports in docker-compose.yml if needed
2. **Database connection:** Ensure PostgreSQL is running before backend
3. **Frontend not loading:** Check if backend is accessible at the API URL
4. **Permission issues:** Run `docker-compose down -v` to reset volumes

## Production Considerations

- Use environment variables for sensitive data
- Set up proper SSL/TLS certificates
- Configure proper backup strategies for PostgreSQL
- Monitor resource usage and scale as needed