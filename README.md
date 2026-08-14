# Company Wise DSA

A company-wise DSA practice platform that helps developers prepare for technical interviews by exploring coding questions by company, topic, difficulty, and relative frequency.

The platform:
- contains 3,430 questions
- covers 737 companies
- contains 24 curated DSA topics
- supports company/topic filtering
- supports difficulty filtering
- supports search
- supports pagination
- supports random practice
- tracks solved questions locally
- supports bookmarks
- supports personal notes
- supports progress import/export
- supports light and dark themes
- requires no account/sign-up for personal progress

---

## Features

- Company-wise question discovery
- Topic-wise question discovery
- Difficulty filtering
- Question search
- Relative frequency information
- Random practice sessions
- Local progress tracking
- Solved/bookmarked questions
- Personal notes
- Progress export/import
- Light / dark / system theme
- Responsive desktop/tablet/mobile UI
- FastAPI backend
- PostgreSQL database

---

## Tech Stack

**Frontend:**
- React (v19)
- Vite
- React Router (v7)

**Backend:**
- FastAPI
- SQLAlchemy
- PostgreSQL / psycopg2
- Alembic
- Pydantic

---

## Architecture

```text
Frontend
    ↓
FastAPI REST API
    ↓
PostgreSQL Database
```

Personal progress is intentionally stored in the browser's `localStorage` rather than server-side user accounts to ensure privacy and eliminate friction.

**Backend (Source of Truth):**
- question metadata
- companies
- topics
- relationships
- frequency information

**Browser/localStorage (User State):**
- solved questions
- bookmarks
- notes
- timestamps
- theme preference / progress data

---

## Dataset

- The canonical dataset contains 3,430 unique questions.
- Questions are deduplicated using normalized LeetCode URLs.
- Company/question relationships are deduplicated.
- Time-period files were used for question discovery where applicable, but the final application does NOT expose the original time-period dimension.
- Frequency is represented as a merged relative signal and is NOT an official LeetCode statistic.
- Premium-only questions were filtered according to the dataset preparation rules.
- The final dataset contains titles, difficulty, links, company relationships, topic relationships, and relative frequency information.
- No problem statements, editorials, test cases, or solution code are included in the application dataset.



## Disclaimer

This project is an independent educational project and is not affiliated
with, endorsed by, or sponsored by LeetCode or any company referenced on
this platform.

The platform provides links, titles, difficulty information, company
associations, topics, and other metadata derived from publicly available
third-party sources.

No LeetCode problem statements, solutions, editorials, test cases, or
proprietary content are reproduced or distributed by this project.

Dataset sources and attribution are documented separately. Third-party
data remains subject to the respective licenses and terms of its original
sources.

If you believe any content or attribution in this repository requires
correction or removal, please open an issue or contact the maintainer.

---

## License

The original source code of this project is licensed under the MIT License.

The MIT License applies only to original code authored for this project.
Third-party data, repositories, trademarks, and other external materials
are NOT covered by this license and remain subject to their respective
licenses and terms.

See [DATA_SOURCES.md](DATA_SOURCES.md) for source attribution and licensing information.

---

## Getting Started

### Prerequisites
- Node.js (v18+)
- Python (v3.10+)
- PostgreSQL Database (e.g., Neon)

### Backend

Create and activate a virtual environment:
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux
```

Install dependencies:
```bash
pip install -r requirements.txt
```

Configure `.env` (copy from `.env.example`):
```bash
DATABASE_URL="postgresql://user:password@host/dbname"
ENVIRONMENT="development"
```

Start the FastAPI server:
```bash
fastapi dev app/main.py
# or
uvicorn app.main:app --reload
```

### Frontend

Install dependencies:
```bash
cd frontend
npm install
```

Start the Vite development server:
```bash
npm run dev
```

Build for production:
```bash
npm run build
```

---

## Environment Variables

The backend relies on the following environment variables (defined in `backend/.env`):

```env
DATABASE_URL="postgresql://..."
ENVIRONMENT="development" # or "production"
CORS_ORIGINS="http://localhost:5173"
```

Secrets must never be committed to Git.

---

## API

The backend exposes several REST API routes:

- **GET `/api/companies`**: List all companies.
- **GET `/api/companies/{slug}`**: Get details for a specific company.
- **GET `/api/topics`**: List all topics.
- **GET `/api/topics/{slug}`**: Get details for a specific topic.
- **GET `/api/questions`**: Fetch paginated questions with filtering:
  - `?company=google`
  - `?topic=array`
  - `?difficulty=medium`
  - `?search=two+sum`
  - `?slugs=two-sum,binary-search`
  - `?page=1&limit=50`
- **GET `/api/questions/random`**: Fetch random questions with filters (`?limit=5`).
- **GET `/api/questions/slug/{slug}`**: Lookup a specific question by slug.

---

## Local Progress

Local progress requires no account to function. Progress is stored entirely within your browser's `localStorage`.

- Solved questions and bookmarks are persisted securely on your device.
- Personal notes and solved timestamps are tracked locally.
- The platform supports importing and exporting your progress as JSON, allowing you to back up your data or move between devices.
- **Note:** Clearing your browser's site data or storage will erase this progress unless you have exported a backup.

---

## Project Structure

```text
company-wise-dsa/
├── backend/
│   ├── alembic/            # Database migrations
│   ├── app/                # FastAPI application
│   │   ├── api/            # Route handlers
│   │   ├── db/             # Database connection & setup
│   │   ├── models/         # SQLAlchemy ORM models
│   │   ├── schemas/        # Pydantic validation schemas
│   │   └── services/       # Business logic
│   ├── data/               # Raw dataset files
│   ├── scripts/            # Parsing & seeding scripts
│   ├── tests/              # Pytest suites
│   ├── alembic.ini         # Database configuration
│   └── requirements.txt    # Python dependencies
├── frontend/
│   ├── public/             # Static assets (favicon)
│   ├── src/
│   │   ├── components/     # Reusable React components
│   │   ├── context/        # Progress Context (localStorage logic)
│   │   ├── pages/          # Application routes
│   │   ├── App.jsx         # Main router entry
│   │   ├── index.css       # Global styles and theme
│   │   └── main.jsx        # React root
│   ├── index.html          # HTML template
│   └── package.json        # Node dependencies
├── LICENSE                 # MIT License (Original Source Code)
└── README.md               # Project documentation
```

---

## Development

**Run the backend locally:**
```bash
cd backend
uvicorn app.main:app --reload
```

**Run the frontend locally:**
```bash
cd frontend
npm run dev
```

**Run backend tests:**
```bash
cd backend
pytest
```

---

## Roadmap

- Additional dataset sources for newer questions.
- Improved and fuzzy search.
- Additional practice modes and mock interviews.
- Advanced local analytics and progress charts.

---

## 📌 Disclaimer

This project is an independent educational project and is not affiliated with,
endorsed by, or sponsored by LeetCode or any company referenced on this platform.

The platform provides links, titles, difficulty information, company associations,
and other metadata derived from publicly available third-party sources.

No LeetCode problem statements, solutions, editorials, test cases, or proprietary
content are reproduced or distributed by this project.

Dataset sources and attribution are documented in the repository. Each third-party
source remains subject to its respective license and terms of use.

If you believe any content or attribution in this repository requires correction
or removal, please open an issue or contact the maintainer.

---

## Author

**Ashutosh Shukla**  
Portfolio: [https://ashutosh-shukla-portfolio.vercel.app/](https://ashutosh-shukla-portfolio.vercel.app/)
