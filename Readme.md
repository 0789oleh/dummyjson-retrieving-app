# Dummyjson retrieving app


**Live Demo**: http://localhost:3000 (after `docker compose up --build`)  
**Repository**: Open source · Clean code · Production-ready


![frontend](/screenshots/image.png )


---

### Implemented Features (All + Extra)

| Requirement                                    | Status | Notes |
|------------------------------------------------|--------|-------|
| FastAPI backend + PostgreSQL                   | Done   | SQLAlchemy 2.0, async, lifespan |
| React + TypeScript frontend (1–2 pages)        | Done   | 2 beautiful pages with navigation |
| Data from https://dummyjson.com                | Done   | Auto-loaded on first start |
| View / Sort / Edit / Delete products           | Done   | Full CRUD with persistence |
| Store edited/deleted data in PostgreSQL        | Done   | All changes saved |
| At least 2 related entities                    | Done   | User → Cart → Product |
| Docker Compose (frontend + backend + db)       | Done   | One command: `docker compose up --build` |
| Code formatted (Flake8 + Prettier)              | Done   | Clean and consistent |
| Unit tests (pytest)                            | Done   | Schema + CRUD tests |
| Open GitHub repo + detailed README             | Done   | You’re reading it |

### Bonus Features (Senior Level)

- Modern UI with Tailwind CSS + gradient navbar
- React Router + proper SPA routing in Docker (nginx fallback)
- Pagination, sorting (by title/price), hover effects
- Dashboard: Users with their carts and total prices
- Clean architecture: CRUD layer, Pydantic schemas, response models
- N+1 queries eliminated using `selectinload`
- Graceful handling of dummyjson data + idempotent loading

---

### Tech Stack

**Backend**
- Python 3.12
- FastAPI
- SQLAlchemy 2.0 (async)
- PostgreSQL
- Pydantic v2

**Frontend**
- React 18 + TypeScript
- Vite
- Tailwind CSS
- React Router DOM

**DevOps**
- Docker + Docker Compose
- Nginx (SPA fallback for client-side routing)

---

### How to Run

```bash
# Clone and run (one command!)
git clone https://github.com/your-username/synergyway-test.git
cd synergyway-test

docker compose up --build
```

Swagger is available at http://localhost:3000/docs

![swagger](/screenshots/image_docs.png )
