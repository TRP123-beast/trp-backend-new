# TRP Backend API

Toronto Regional Properties (TRP) Backend API - A FastAPI-based real estate platform integrating MLS data and Supabase authentication.

## 🏗️ Architecture

This project follows a clean, modular FastAPI architecture with clear separation of concerns:

```
app/
├── core/                 # Core configurations and utilities
│   ├── config.py        # Environment variables and settings
│   ├── security.py      # JWT handling and password hashing
│   └── dependencies.py  # Reusable FastAPI dependencies
├── schemas/             # Pydantic models for API validation
│   ├── user.py         # User request/response models
│   └── property.py     # Property request/response models
├── services/           # Business logic layer
│   ├── user_service.py     # User-related business logic
│   ├── property_service.py # Property-related business logic
│   └── page_load_service.py # Merged data services
├── api/                # API endpoints (routes)
│   └── v1/
│       ├── endpoints/  # Individual endpoint modules
│       │   ├── users.py
│       │   ├── properties.py
│       │   └── page_load.py
│       └── api.py      # API router aggregator
└── main.py             # FastAPI application entry point
```

## 🚀 Features

- **Property Search**: Filter and retrieve MLS property listings
- **Property Details**: Get detailed property information
- **Property Media**: Fetch property images and media
- **User Authentication**: Signup, login, and token management via Supabase
- **Page Load APIs**: Merged data endpoints for frontend consumption
- **JWT Authentication**: Secure token-based authentication
- **CORS Support**: Cross-origin resource sharing enabled
- **API Documentation**: Auto-generated Swagger/OpenAPI docs

## 📋 Prerequisites

- Python 3.9+
- FastAPI
- Uvicorn
- aiohttp
- python-dotenv
- python-jose[cryptography]
- passlib[bcrypt]
- email-validator

## 🔧 Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd trp-backend-new
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp env.template .env
   # Edit .env with your actual values
   ```

## ⚙️ Configuration

Create a `.env` file with the following variables:

```env
# MLS Configuration
MLS_URL=your_mls_api_url
MLS_AUTHTOKEN=your_mls_auth_token

# Supabase Configuration
SUPABASE_URL=your_supabase_url
SUPABASE_ANON_KEY=your_supabase_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_supabase_service_role_key

# JWT Configuration
JWT_SECRET_KEY=your_jwt_secret_key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## 🏃‍♂️ Running the Application

### Local Development
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production (Render)
The application is configured for Render deployment with the provided `Procfile`.

## 📚 API Endpoints

### Base URL
- **Local**: `http://localhost:8000`
- **Production**: `https://trp-backend-new.onrender.com`

### API Documentation
- **Swagger UI**: `/docs`
- **ReDoc**: `/redoc`

### Available Endpoints

#### Properties
- `POST /api/v1/properties/search` - Search properties with filters
- `GET /api/v1/properties/get/{property_id}` - Get property details
- `GET /api/v1/properties/media/{property_id}` - Get property media

#### Users
- `POST /api/v1/users/auth/signup` - Create user account
- `POST /api/v1/users/auth/login` - User login
- `POST /api/v1/users/auth/refresh` - Refresh JWT token
- `GET /api/v1/users/me` - Get current user info (authenticated)

#### Page Load
- `GET /api/v1/page_load/home` - Get merged home page data

## 🔒 Authentication

The API uses JWT tokens for authentication. To access protected endpoints:

1. **Login** to get a JWT token
2. **Include the token** in the Authorization header:
   ```
   Authorization: Bearer <your_jwt_token>
   ```

## 🧪 Testing

### Using Postman

1. **Test the docs endpoint**:
   ```
   GET https://trp-backend-new.onrender.com/docs
   ```

2. **Test property search**:
   ```
   POST https://trp-backend-new.onrender.com/api/v1/properties/search
   Content-Type: application/json
   
   {
     "MLS_TOP_LIMIT": 5
   }
   ```

3. **Test user signup**:
   ```
   POST https://trp-backend-new.onrender.com/api/v1/users/auth/signup
   Content-Type: application/json
   
   {
     "email": "test@example.com",
     "password": "yourpassword"
   }
```

## 🏗️ Project Structure Benefits

- **Separation of Concerns**: Each module has a single responsibility
- **Maintainability**: Easy to locate and modify specific functionality
- **Testability**: Services can be tested independently
- **Scalability**: New features can be added without affecting existing code
- **FastAPI Synergy**: Leverages FastAPI's dependency injection and Pydantic validation

## 🔄 Migration from Old Structure

The project has been restructured from the original `modules/` structure to follow FastAPI best practices:

- **Old**: `modules/properties/search/search.py`
- **New**: `app/api/v1/endpoints/properties.py` + `app/services/property_service.py`

This provides better separation between API routes and business logic.

## 📝 License

This project is proprietary to Toronto Regional Properties. 