# Company-Wise DSA Practice Platform (Backend)

This is the FastAPI backend for a public DSA practice platform focused on company-wise LeetCode questions.

## Architecture

The platform follows a simple architectural rule:
**The server owns the shared question database. Each user's browser owns their personal progress through `localStorage`.**

```text
Frontend (React/Vite - To be implemented)
   ↓
REST API
   ↓
FastAPI Backend
   ↓
Neon PostgreSQL (Questions, Companies, Topics, Relationships)
```

There is **no user authentication**, no sessions, and no server-side tracking of user progress. All state (solved questions, bookmarks, notes) is handled entirely in the frontend using `localStorage`.

## Setup Instructions

### 1. Virtual Environment

Create and activate a virtual environment:

**Windows:**
```bash
python -m venv venv
.\venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Requirements

```bash
pip install -r requirements.txt
```

### 3. Environment Variables

Copy the example environment file:
```bash
cp .env.example .env
```

Edit the `.env` file and configure your Neon PostgreSQL connection string:
```env
DATABASE_URL=postgresql://user:password@your-neon-host/dbname
CORS_ORIGINS=http://localhost:5173
ENVIRONMENT=development
```

> **Warning:** Never expose your `DATABASE_URL` publicly or commit it to version control.

### 4. Database Migrations

Initialize the database schema using Alembic:
```bash
alembic upgrade head
```

### 5. Running Locally

Start the FastAPI development server:
```bash
uvicorn app.main:app --reload
```

The API documentation will be available at:
- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## API Endpoints

The API is fully documented via Swagger UI, but major endpoints include:

- `GET /api/companies` - List companies and search
- `GET /api/companies/{slug}` - Detailed company statistics (question difficulty counts, topics)
- `GET /api/topics` - List topics
- `GET /api/topics/{slug}` - Topic details
- `GET /api/questions` - Primary endpoint for questions (supports filtering, sorting, pagination)
- `GET /api/questions/random` - Fetch random practice questions based on filters
- `GET /api/questions/{id}` / `GET /api/questions/slug/{slug}` - Specific question details

## Dataset Maintenance

The platform database stores only metadata and is populated via datasets. To protect intellectual property, it **does not store** problem descriptions, test cases, or official solutions.

### Import Dataset
To populate the database from a JSON dataset:
```bash
python scripts/import_dataset.py path/to/dataset.json
```
By default, imports use `merge` mode. To completely replace the database:
```bash
python scripts/import_dataset.py path/to/dataset.json --mode=replace --confirm
```

### Export Dataset
To dump the current metadata state to a JSON file:
```bash
python scripts/export_dataset.py
```

## Testing

Run the test suite using `pytest`:
```bash
python -m pytest tests/
```

## Deployment

To deploy in a standard Python hosting environment (like Render, Heroku, or Fly.io):
```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```
Ensure that `DATABASE_URL` is set in your production environment variables.

## Disclaimer

This project is an independent educational tool and is **not affiliated with LeetCode** or any company listed within the dataset.
