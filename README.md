# CareerForge AI 🚀

> AI-powered platform for career guidance, college prediction, and resume analysis — built for Indian students.

![Tech Stack](https://img.shields.io/badge/Stack-FastAPI%20%7C%20React%20%7C%20MongoDB%20%7C%20LangChain-6366f1?style=flat-square)

---

## 📋 Features

| Module | Description |
|--------|-------------|
| 🎯 **Career Guidance** | AI-powered career path recommendations based on interests, skills & scores |
| 🏫 **College Predictor** | NEET/JEE/EAMCET rank-based Safe/Target/Dream college predictions |
| 📄 **Resume Analyzer** | ATS scoring, keyword detection, AI improvement suggestions |
| 💬 **AI Chat Assistant** | Context-aware conversational AI with conversation memory |

---

## 🏗 Architecture

```
CareerForge AI/
├── backend/              # FastAPI Python backend
│   ├── main.py           # App entry point
│   ├── config/           # Settings, DB connection
│   ├── models/           # Pydantic models
│   ├── routers/          # API route handlers
│   ├── services/         # Auth, Cache, Rate Limiter
│   └── middleware/       # Rate limiting middleware
├── ai_services/          # LangChain + OpenAI modules
│   ├── career_ai.py      # Career guidance AI
│   ├── resume_ai.py      # Resume analysis AI
│   └── chat_ai.py        # Chat assistant AI
├── database/
│   └── college_data.json # College dataset (NEET/JEE/EAMCET)
└── frontend/             # React + Tailwind frontend
    └── src/
        ├── pages/        # Landing, Dashboard, Career, College, Resume, Chat
        ├── components/   # Layout, Sidebar
        ├── context/      # Auth context
        └── api/          # Axios API client
```

---

## ⚡ Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- MongoDB (local or Atlas)
- OpenAI API key (optional — rule-based fallback works without it)

### 1. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Configure environment
copy .env.example .env
# Edit .env with your MongoDB URL and OpenAI key

# Start the server
python main.py
# OR
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Backend runs at: http://localhost:8000  
API Docs: http://localhost:8000/docs

### 2. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Configure environment
copy .env.example .env
# Edit VITE_API_URL if backend is not at localhost:8000

# Start dev server
npm run dev
```

Frontend runs at: http://localhost:5173

---

## 🌐 API Documentation

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register` | Register new user |
| POST | `/api/auth/login` | Login and get JWT |
| GET | `/api/auth/me` | Get current user |
| PUT | `/api/auth/me` | Update profile |

### Career Guidance
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/career/analyze` | Analyze career profile |
| GET | `/api/career/history` | Get analysis history |

### College Predictor
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/college/predict` | Predict colleges by rank |
| GET | `/api/college/list` | Browse college dataset |

### Resume Analyzer
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/resume/analyze` | Upload PDF and get analysis |
| GET | `/api/resume/history` | Get past analyses |

### Chat Assistant
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/chat/message` | Send chat message |
| GET | `/api/chat/history` | Get chat sessions |
| DELETE | `/api/chat/session/{id}` | Clear session |

---

## 🔒 Authentication

All protected endpoints require a Bearer JWT token:
```
Authorization: Bearer <your_token>
```

Tokens are issued on `/api/auth/login` and `/api/auth/register`.

---

## 🤖 AI Integration

### With OpenAI (Full AI Mode)
Set `OPENAI_API_KEY` and `AI_ENABLED=true` in `.env`.  
Uses `gpt-3.5-turbo` by default (change via `OPENAI_MODEL`).

### Without OpenAI (Fallback Mode)
Set `AI_ENABLED=false` or leave `OPENAI_API_KEY` blank.  
Rule-based logic provides useful responses without API costs.

### Cost Optimization
- Results are cached for 24 hours (same input = no new API call)
- Rate limiting: 20 AI calls/hour/user
- Prompt optimization to minimize tokens

---

## 🗄 Database Schema

```
MongoDB Collections:
├── users          → User accounts, skills, interests
├── resumes        → Uploaded resume text + analysis
├── career_results → Career analysis history
├── college_data   → College dataset (loaded from JSON)
└── chat_history   → Conversation sessions by user
```

---

## 🚀 Deployment

### Backend → Render / Railway
1. Set all environment variables on the platform
2. Set start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
3. Set build command: `pip install -r requirements.txt`

### Frontend → Vercel
1. Import GitHub repo on Vercel
2. Set `VITE_API_URL` to your deployed backend URL
3. Framework: Vite · Root: `frontend/`

### Database → MongoDB Atlas
1. Create free cluster at atlas.mongodb.com
2. Add your server IP to Network Access
3. Update `MONGODB_URL` in backend `.env`

---

## ⚙️ Environment Variables

See `backend/.env.example` for all backend variables.  
See `frontend/.env.example` for frontend variables.

---

## 🔧 Scalability Design

- **Stateless Backend**: No server-side sessions — JWT based
- **Connection Pooling**: Motor async MongoDB with `maxPoolSize=50`
- **Caching Layer**: Redis primary + in-memory fallback (transparent)
- **Background Tasks**: FastAPI BackgroundTasks for DB writes
- **Rate Limiting**: Per-user sliding window (50 req/hr general, 20 AI calls/hr)
- **Horizontal Scaling**: Multiple Uvicorn workers (`--workers 4`)

---

## 🛠 Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 18, Tailwind CSS, Recharts, React Router v6 |
| Backend | FastAPI, Python 3.10+, Uvicorn |
| AI | LangChain, OpenAI GPT-3.5/4, LangChain-Core |
| Database | MongoDB Atlas, Motor (async driver) |
| Auth | JWT (python-jose), bcrypt (passlib) |
| Cache | Redis / In-memory TTL cache |
| PDF | pdfplumber, PyPDF2 |

---

Built with ❤️ for Indian students navigating NEET, JEE, EAMCET and beyond. 🇮🇳
