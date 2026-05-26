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
- [ ] Mobile app with Flutter
- [ ] OAuth2 login integration
- [ ] AI-based outfit recommendations
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
