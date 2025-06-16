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
| Storage    | AWS S3 (for storing images)             |
| API        | OpenWeather API (climate-based insights)|

---

## 📂 Project Structure

```bash
armoire/
│
├── app/              # FastAPI backend
│   ├── db/           # DB models, sessions, migrations
│   ├── api/          # API routes and logic
│   └── main.py       # FastAPI entry point
│
├── frontEnd/         # React frontend app
│
├── infra/            # Kubernetes manifests, Skaffold config
│
├── .env              # Environment variables (local only)
└── README.md
```

---

## 🚀 Getting Started (Local Dev)

```bash
# Backend (FastAPI)
cd app
uvicorn app.main:app --reload

# Frontend (React)
cd frontEnd
npm install
npm start
```

> Note: Backend and frontend communicate over ports 8000 and 3000 respectively.

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
