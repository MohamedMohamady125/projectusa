# SwimUSA Recruit - Backend API

Complete FastAPI backend for guiding Spanish swimmers through the US college scholarship recruitment process.

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- PostgreSQL 14+
- Redis (optional, for background tasks)

### Installation

1. **Clone and navigate to the backend directory:**
```bash
cd /Users/mohamedmohamady/projectusa/projectusabackend/backend
```

2. **Create virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables:**
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. **Initialize database:**
```bash
# Create database
createdb swimusa_recruit

# Run the SQL schema
psql -U your_username -d swimusa_recruit -f ../dbschema.sql

# Or use Alembic for migrations
alembic init alembic
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

6. **Run the application:**
```bash
# Development mode
python app/main.py

# Or with uvicorn
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

7. **Access the API:**
- API Documentation: http://localhost:8000/api/docs
- Alternative Docs: http://localhost:8000/api/redoc
- Health Check: http://localhost:8000/health

## 📁 Project Structure

```
backend/
├── app/
│   ├── main.py                 # Application entry point
│   ├── core/                   # Core functionality
│   │   ├── config.py          # Settings and configuration
│   │   ├── security.py        # Authentication & security
│   │   ├── dependencies.py    # FastAPI dependencies
│   │   └── exceptions.py      # Custom exceptions
│   ├── db/                     # Database
│   │   ├── base.py            # SQLAlchemy base
│   │   └── session.py         # Database sessions
│   ├── models/                 # SQLAlchemy models
│   ├── schemas/                # Pydantic schemas
│   ├── services/               # Business logic
│   ├── api/                    # API endpoints
│   │   └── v1/
│   │       ├── api.py         # Main router
│   │       └── endpoints/     # Endpoint modules
│   └── utils/                  # Utility functions
├── requirements.txt            # Python dependencies
├── .env.example               # Environment template
└── README.md                  # This file
```

## 🔑 Environment Variables

Key environment variables (see `.env.example` for complete list):

```env
# Database
DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/swimusa_recruit

# Security
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Email
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password

# AWS S3
AWS_ACCESS_KEY_ID=your-aws-key
AWS_SECRET_ACCESS_KEY=your-aws-secret
S3_BUCKET_NAME=swimusa-documents

# Frontend
FRONTEND_URL=http://localhost:3000
CORS_ORIGINS=http://localhost:3000
```

## 📚 API Documentation

Once running, visit http://localhost:8000/api/docs for interactive API documentation.

### Main Endpoints:

**Authentication:**
- POST `/api/v1/auth/register` - Register new user
- POST `/api/v1/auth/login` - Login and get tokens
- POST `/api/v1/auth/verify-email` - Verify email
- GET `/api/v1/auth/me` - Get current user

**Athletes:**
- POST `/api/v1/athletes/profile` - Create profile
- GET `/api/v1/athletes/profile` - Get profile
- PUT `/api/v1/athletes/profile` - Update profile
- POST `/api/v1/athletes/times` - Add swimming time
- GET `/api/v1/athletes/times` - Get swimming times

**Schools:**
- GET `/api/v1/schools` - List schools
- GET `/api/v1/schools/{id}` - Get school details
- GET `/api/v1/schools/{id}/coaches` - Get school coaches

**Tasks:**
- GET `/api/v1/tasks` - Get tasks
- POST `/api/v1/tasks` - Create task

**And more...**

## 🗄️ Database

### Models:
- **User** - Authentication and user management
- **AthleteProfile** - Athlete information and academic data
- **SwimmingTime** - Swimming performance records
- **School** - College/university database
- **Coach** - Coach contact information
- **TeamRanking** - Team rankings by division
- **Task** - Task management system
- **RecruitmentTracking** - School recruitment pipeline
- **Communication** - Communication logs
- **Document** - Document storage
- **VideoTutorial** - Tutorial content
- **Notification** - User notifications

### Enums:
- UserRole: athlete, admin, coach, parent
- DivisionType: D1, D1_MID_MAJOR, D2, D3, NAIA, NJCAA
- TaskStatus: pending, in_progress, completed, cancelled
- RecruitmentStatus: researching, initial_contact, active_communication, etc.
- SwimmingCourse: SCY, SCM, LCM

## 🔒 Authentication

JWT-based authentication with refresh tokens:

1. **Register:** POST `/api/v1/auth/register`
2. **Login:** POST `/api/v1/auth/login` (returns access & refresh tokens)
3. **Use token:** Include in Authorization header: `Bearer <token>`
4. **Verify email:** POST `/api/v1/auth/verify-email`

## 🧪 Testing

```bash
# Run tests
pytest

# With coverage
pytest --cov=app tests/

# Specific test file
pytest tests/test_auth.py
```

## 🐳 Docker (Optional)

```bash
# Build image
docker build -t swimusa-backend .

# Run container
docker run -p 8000:8000 --env-file .env swimusa-backend
```

## 📊 Features

### Core Features:
- ✅ User authentication & authorization
- ✅ Athlete profile management
- ✅ Swimming time tracking & conversion
- ✅ School database & search
- ✅ Task management system
- ✅ Recruitment tracking pipeline
- ✅ Document management
- ✅ Communication logging
- ✅ Video tutorials
- ✅ Notification system

### Technical Features:
- ✅ Async/await throughout
- ✅ JWT authentication
- ✅ Role-based access control
- ✅ Comprehensive error handling
- ✅ Data validation with Pydantic
- ✅ Database migrations
- ✅ API documentation
- ✅ CORS configuration
- ✅ Type hints
- ✅ Modular architecture

## 🛠️ Development

### Code Style:
```bash
# Format code
black app/

# Sort imports
isort app/

# Lint
flake8 app/

# Type check
mypy app/
```

### Database Migrations:
```bash
# Create migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

## 📝 Documentation

- **Full Implementation Report:** See `IMPLEMENTATION_REPORT.md`
- **Database Schema:** See `../dbschema.sql`
- **Application Description:** See `../description.txt`
- **API Docs:** http://localhost:8000/api/docs (when running)

## 🤝 Contributing

1. Create a feature branch
2. Make your changes
3. Write/update tests
4. Submit pull request

## 📄 License

Proprietary - SwimUSA Recruit

## 💡 Support

For issues or questions:
- Check the API documentation
- Review the implementation report
- Contact the development team

---

**Version:** 1.0.0
**Last Updated:** October 15, 2025
**Status:** ✅ Production Ready Foundation
