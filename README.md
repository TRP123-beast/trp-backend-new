# TRP Backend

Toronto Regional Properties (TRP) Backend API - A FastAPI-based real estate platform integrating MLS data and Supabase authentication.

## Features

- **Properties Module**: Search, retrieve, and manage property listings from MLS
- **Users Module**: Complete authentication system with Supabase integration
- **Page Load Module**: Merged APIs for efficient frontend data loading
- **Async Operations**: All endpoints use async/await for optimal performance

## Setup

### Prerequisites

- Python 3.9+
- Virtual environment (recommended)

### Installation

1. Clone the repository
2. Create and activate virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables:
   ```bash
   cp env.template .env
   # Edit .env with your actual API keys
   ```

### Environment Variables

Create a `.env` file with the following variables:

```env
MLS_URL=https://query.ampre.ca/odata
MLS_AUTHTOKEN=your_mls_auth_token
SUPABASE_URL=your_supabase_url
SUPABASE_ANON_KEY=your_supabase_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_supabase_service_role_key
RESOURCE_RECORD_KEY_MAPPING={"X8311912": "N8102234"}
```

## Running the Application

### Development

```bash
uvicorn main:app --reload
```

### Production

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

## API Documentation

Once running, access the interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Properties

- `POST /properties/search` - Search properties with filters
- `GET /properties/get/{listing_key}` - Get specific property details
- `GET /properties/media/{resource_record_key}` - Get property media
- `GET /properties/media/mapping/{listing_key}` - Get media using mapping

### Users

- `POST /users/auth/signup` - User registration
- `POST /users/auth/token` - User login
- `POST /users/auth/refresh` - Refresh access token
- `POST /users/auth/create` - Create user (admin)
- `GET /users/auth/all` - Get all users (admin)
- `GET /users/auth/{user_id}` - Get specific user
- `PATCH /users/auth/{user_id}` - Update user
- `DELETE /users/auth/{user_id}` - Delete user

### Page Load

- `GET /page_load/home` - Get merged home page data

## Project Structure

```
trp-backend/
├── modules/
│   ├── properties/
│   │   ├── search/
│   │   ├── get/
│   │   └── media/
│   ├── users/
│   │   └── authentication/
│   └── page_load/
│       └── home/
├── main.py
├── requirements.txt
├── .env
└── README.md
```

## Development

### Code Style

- Follow PEP 8 guidelines
- Use type hints
- Use async/await for all I/O operations
- Document endpoints with docstrings

### Testing

Test endpoints using:
- FastAPI's built-in Swagger UI
- Postman
- curl commands

## Security

- API keys stored in environment variables
- CORS middleware configured
- Input validation with Pydantic models
- Error handling with appropriate HTTP status codes

## License

[Add your license here] 