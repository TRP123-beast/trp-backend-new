# TRP Backend API

A FastAPI-based backend for Toronto Regional Properties (TRP) application, providing a modular API for property management, user authentication, and real estate data integration.

## 🏗️ Project Structure

```
trp-backend-new/
├── 📄 .env                          # Environment variables (not in git)
├── 📄 .env.example                  # Environment template
├── 📄 .gitignore                    # Git ignore rules
├── 📄 README.md                     # Project documentation
├── 📄 main.py                       # FastAPI application entry point
├── 📄 requirements.txt              # Python dependencies
├── 🎯 venv/                         # Virtual environment
├── 📁 core/                         # Core configuration
│   ├── 📄 config.py                 # Settings and configuration
│   └── 📄 security.py               # Security utilities
└── 📁 app/                          # Main application code
    ├── 📄 __init__.py
    ├── 📁 auth/                     # Authentication module
    │   └── 📄 deps.py               # JWT auth dependencies
    ├── 📁 property/                 # Property management module
    │   ├── 📄 __init__.py
    │   ├── 📄 api.py                # 🚀 Property API endpoints
    │   ├── 📄 cart.py               # 🛒 User cart functionality
    │   ├── 📄 wishlist.py           # ❤️ User wishlist functionality
    │   ├── 📄 clients.py            # 🌐 MLS API client
    │   ├── 📄 models.py             # 📊 Pydantic data models
    │   └── 📄 services.py           # ⚙️ Business logic services
    ├── 📁 user/                     # User management module
    │   ├── 📄 __init__.py
    │   ├── 📄 api.py                # User API endpoints
    │   ├── 📄 models.py             # User data models
    │   └── 📄 services.py           # User business logic
    ├── 📁 flags/                    # Flags management module
    │   ├── 📄 __init__.py
    │   ├── 📄 api.py                # Flags API endpoints
    │   ├── 📄 models.py             # Flags data models
    │   └── 📄 services.py           # Flags business logic
    ├── 📁 questions/                # Questions management module
    │   ├── 📄 __init__.py
    │   ├── 📄 api.py                # Questions API endpoints
    │   ├── 📄 models.py             # Questions data models
    │   └── 📄 services.py           # Questions business logic
    └── 📁 responses/                # Responses management module
        ├── 📄 __init__.py
        ├── 📄 api.py                # Responses API endpoints
        ├── 📄 models.py             # Responses data models
        └── 📄 services.py           # Responses business logic
```

## 🚀 Features

### Property Management
- **MLS Integration**: Direct integration with MLS OData API for real estate data
- **Property Search**: Advanced filtering and search capabilities
- **Media Management**: Property image and media handling
- **Cart System**: User shopping cart for properties
- **Wishlist**: User wishlist functionality

### User Management
- **Authentication**: JWT-based user authentication
- **User Profiles**: Complete user profile management
- **Authorization**: Role-based access control

### Data Management
- **Flags**: System flags and configuration
- **Questions**: Dynamic question management
- **Responses**: User response tracking

## 🛠️ Technology Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **Pydantic**: Data validation and settings management
- **Supabase**: Backend-as-a-Service for database operations
- **aiohttp**: Asynchronous HTTP client for external API calls
- **JWT**: JSON Web Tokens for authentication
- **PostgreSQL**: Database (via Supabase)

## 📋 API Endpoints

### Properties
- `GET /api/v1/properties/search` - Search properties with filters
- `GET /api/v1/properties/selected-fields` - Get properties with selected fields
- `GET /api/v1/properties/get/{property_id}` - Get specific property details
- `GET /api/v1/properties/media/{property_id}` - Get property media with fields
- `GET /api/v1/properties/media-simple/{property_id}` - Get property media (simple)

### Cart
- `POST /api/v1/cart/add/{property_id}` - Add property to cart
- `GET /api/v1/cart/` - Get user's cart
- `DELETE /api/v1/cart/remove/{property_id}` - Remove property from cart
- `DELETE /api/v1/cart/clear` - Clear user's cart

### Wishlist
- `POST /api/v1/wishlist/add/{property_id}` - Add property to wishlist
- `GET /api/v1/wishlist/` - Get user's wishlist
- `DELETE /api/v1/wishlist/remove/{property_id}` - Remove property from wishlist
- `DELETE /api/v1/wishlist/clear` - Clear user's wishlist

### Users
- `POST /api/v1/users/signup` - Create new user account
- `POST /api/v1/users/login` - User authentication
- `GET /api/v1/users/me` - Get current user info
- `GET /api/v1/users/` - Get all users (admin)
- `GET /api/v1/users/{user_id}` - Get specific user
- `PUT /api/v1/users/{user_id}` - Update user
- `DELETE /api/v1/users/{user_id}` - Delete user

### Flags
- `GET /api/v1/flags/` - List all flags
- `GET /api/v1/flags/{flag_id}` - Get specific flag
- `POST /api/v1/flags/` - Create new flag
- `PUT /api/v1/flags/{flag_id}` - Update flag
- `DELETE /api/v1/flags/{flag_id}` - Delete flag

### Questions
- `GET /api/v1/questions/` - List all questions
- `GET /api/v1/questions/{question_id}` - Get specific question
- `POST /api/v1/questions/` - Create new question
- `PUT /api/v1/questions/{question_id}` - Update question
- `DELETE /api/v1/questions/{question_id}` - Delete question

### Responses
- `GET /api/v1/responses/` - List all responses
- `GET /api/v1/responses/{response_id}` - Get specific response
- `POST /api/v1/responses/` - Create new response
- `PUT /api/v1/responses/{response_id}` - Update response
- `DELETE /api/v1/responses/{response_id}` - Delete response

## 🔧 Setup and Installation

### Prerequisites
- Python 3.10+
- Supabase account
- MLS API access

### Environment Variables
Create a `.env` file based on `.env.example`:

```bash
# MLS Configuration
MLS_URL=https://query.ampre.ca/odata
MLS_AUTHTOKEN=your_mls_token
MLS_PROPERTY_TYPE=Residential Freehold
MLS_RENTAL_APPLICATION=true
MLS_ORIFINATING_SYSTEM_NAME=Toronto Regional Real Estate Board
MLS_TOP_LIMIT=10
MLS_PPROPERTY_FILTER_FIELDS=BathroomsTotalInteger,BedroomsTotal,BuildingAreaTotal,City,CityRegion,CrossStreet,ListingKey,ListPrice,ParkingSpaces,UnparsedAddress
MLS_PROPERTY_IMAGE_FILTER_FIELDS=ImageHeight,ImageSizeDescription,ImageWidth,MediaKey,MediaObjectID,MediaType,MediaURL,Order,ResourceRecordKey

# Supabase Configuration
SUPABASE_URL=your_supabase_url
SUPABASE_ANON_KEY=your_supabase_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_supabase_service_role_key

# JWT Configuration
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS Configuration
ALLOWED_ORIGINS=["*"]
```

### Installation
```bash
# Clone the repository
git clone <repository-url>
cd trp-backend-new

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
uvicorn main:app --reload
```

### Database Setup
1. Create a Supabase project
2. Set up the required tables (users, flags, questions, responses)
3. Configure environment variables with your Supabase credentials

## 🧪 Testing

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=app
```

## 📚 API Documentation

Once the server is running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 🚀 Deployment

### Render Deployment
1. Connect your GitHub repository to Render
2. Configure environment variables in Render dashboard
3. Deploy as a Web Service

### Environment Variables for Production
Ensure all required environment variables are set in your deployment platform.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For support and questions, please contact the development team. 