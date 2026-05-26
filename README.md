# Armoire 🧥

**A modern wardrobe and style tracking application**  
Built with FastAPI, React, Flutter, PostgreSQL, and Kubernetes.

---

## 🚧 Work in Progress

_Armoire_ is an ongoing personal project designed to showcase my skills in full-stack development, infrastructure automation, and cloud-native architecture. It's a practical implementation of modern dev tools and engineering practices.

---

## 🧠 Purpose

The goal of Armoire is to provide a platform for:
- Tracking and organizing clothing and accessories
- Visualizing wardrobe composition by season, category, brand, and fit
- Managing personal measurements and clothing sizes
- Integrating weather data for daily recommendations
- Supporting mobile and web interfaces with real-time sync

---

## ⚙️ Tech Stack

| Layer       | Technology                             |
|------------|-----------------------------------------|
| Frontend   | React (web), Flutter (mobile)           |
| Backend    | FastAPI (Python), Pydantic, SQLAlchemy  |
| Database   | PostgreSQL (via Kubernetes service)     |
| Cloud Infra| Kubernetes, Skaffold, Argo CD           |
| DevOps     | GitHub Actions, Docker, dotenv          |
| Storage    | S3-compatible object storage — MinIO (local), AWS S3 (prod) |
| API        | OpenWeather API (climate-based insights)|

---

## 📂 Project Structure

```bash
armoire/
│
├── backend/              # FastAPI backend
│   └── app/
│       ├── api/          # API routes (image upload/list)
│       ├── core/         # Settings / config
│       ├── db/           # SQLAlchemy session & engine
│       ├── services/     # Storage (S3/MinIO) and other services
│       └── main.py       # FastAPI entry point
│
├── frontend/             # React web client
├── k8s/                  # Kubernetes manifests
├── argo/                 # Argo CD application
├── docker-compose.yml    # Local full-stack (api + web + Postgres + MinIO)
└── README.md
```

---

## 🚀 Getting Started (Local Dev)

The full stack runs locally with Docker Compose — FastAPI backend, React frontend, PostgreSQL, and a MinIO (S3-compatible) object store:

```bash
docker compose up --build
```

| Service        | URL                                              |
|----------------|--------------------------------------------------|
| Frontend       | http://localhost:3000                            |
| Backend API    | http://localhost:8000                            |
| API docs       | http://localhost:8000/docs                       |
| MinIO console  | http://localhost:9001 (minioadmin / minioadmin)  |

On startup, a one-shot job creates the `armoire` bucket and grants read access. Open the **Wardrobe** page in the frontend to upload an item photo — images are stored in MinIO and served back through the gallery. The same code targets AWS S3 in production by changing the `S3_*` environment variables.

---

## 📱 Mobile App (Flutter)

A Flutter client in [`mobile/`](mobile/) lists and adds wardrobe items through the same API.

```bash
cd mobile
flutter pub get
# Android emulator reaches the host backend at 10.0.2.2; override for other targets:
flutter run --dart-define=API_BASE_URL=http://localhost:8000
```

---

## 🧪 Kubernetes Dev Loop

Using [Skaffold](https://skaffold.dev/) and [kind](https://kind.sigs.k8s.io/) for local Kubernetes deployments.

```bash
skaffold dev
```

This loads Docker images into your kind cluster and watches for changes in source files.

---

## ✅ Features (Planned)

- [x] PostgreSQL DB models with SQLAlchemy
- [x] FastAPI endpoints with dependency injection
- [x] React frontend UI
- [x] Dockerized services
- [x] Image upload backed by S3-compatible object storage (MinIO / AWS S3)
- [x] Wardrobe item catalog — CRUD, category/brand/season filtering, composition summary
- [x] Skaffold & kind setup
- [x] Flutter mobile app — browse and add wardrobe items via the API
- [x] OAuth2 password flow with JWT auth (register / login / current user)
- [x] Weather-based daily outfit recommendations (OpenWeather; set `OPENWEATHER_API_KEY`)
- [x] CI pipeline (GitHub Actions: backend tests, frontend build, compose validation)
- [x] Real-time wardrobe sync over WebSockets
- [x] AI outfit recommendations (Claude / Anthropic API; set `ANTHROPIC_API_KEY`)
- [ ] Production-ready Helm charts & CI/CD with Argo CD

---

## 📸 Screenshots

_(Coming soon...)_

---

## 👋 Author

**Russ Carroll**  
Site Reliability Engineer | DevOps | Cloud & Web Systems  
📍 Central Florida  
🔗 [LinkedIn](https://www.linkedin.com/in/russ-carroll/)  
🔧 [GitHub](https://github.com/SoWrongImRight)

---

## 📝 License

This project is under the MIT License. See `LICENSE` file for details.
