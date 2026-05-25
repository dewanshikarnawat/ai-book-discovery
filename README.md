<div align="center">

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=700&size=32&pause=1000&color=6366F1&center=true&vCenter=true&width=700&lines=📚+AI+Book+Discovery;Find+Your+Next+Favourite+Read;Powered+by+AI+%2B+Open+Data" alt="Typing SVG" />

<br/>

**An AI-powered book recommendation app that understands what you love and surfaces what you'll read next.**

<br/>

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-F7DF1E?style=flat-square&logo=javascript&logoColor=black)
![License](https://img.shields.io/github/license/dewanshikarnawat/ai-book-discovery?style=flat-square&color=6366f1)
![Last Commit](https://img.shields.io/github/last-commit/dewanshikarnawat/ai-book-discovery?style=flat-square&color=10b981)
![Stars](https://img.shields.io/github/stars/dewanshikarnawat/ai-book-discovery?style=flat-square&color=f59e0b)
![Forks](https://img.shields.io/github/forks/dewanshikarnawat/ai-book-discovery?style=flat-square&color=6366f1)

[🚀 Live Demo](#) · [🐛 Report Bug](https://github.com/dewanshikarnawat/ai-book-discovery/issues) · [✨ Request Feature](https://github.com/dewanshikarnawat/ai-book-discovery/issues)

</div>

---

## 📸 Screenshots

> _Add a screenshot or GIF of the running app here — it's the single biggest factor in whether someone stars or bounces._

```
[ Place your app screenshot or demo GIF here ]
```

---

## ✨ Features

- 🤖 **AI-Powered Recommendations** — Describe your mood, a theme, or a book you loved and get instant personalised suggestions
- 🔍 **Smart Search** — Search by title, author, genre, or a natural-language description
- 📖 **Rich Book Details** — Cover art, description, ratings, genre tags, and similar titles
- 🌐 **REST API Backend** — Clean Python API serving structured JSON to any client
- 💅 **Responsive UI** — Works on desktop and mobile without friction
- ⚡ **Fast & Lightweight** — No heavy frameworks, loads instantly

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | Python · Flask / FastAPI |
| **Frontend** | HTML · CSS · Vanilla JavaScript |
| **AI / LLM** | OpenAI API / Google Gemini _(update as applicable)_ |
| **Books Data** | Google Books API / Open Library API |
| **Deployment** | _(e.g. Render, Railway, Vercel — add yours)_ |

---

## 🗂️ Project Structure

```
ai-book-discovery/
├── backend/
│   ├── app.py            ← Main server entry point
│   ├── routes/           ← API route handlers
│   ├── services/         ← AI + books API logic
│   └── requirements.txt  ← Python dependencies
├── frontend/
│   ├── index.html        ← App shell
│   ├── style.css         ← Styles
│   └── script.js         ← Frontend logic & API calls
├── .gitignore
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- API keys for your AI provider and Google Books

### 1 — Clone the repo

```bash
git clone https://github.com/dewanshikarnawat/ai-book-discovery.git
cd ai-book-discovery
```

### 2 — Set up the backend

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3 — Configure environment variables

Create a `.env` file inside `backend/`:

```env
OPENAI_API_KEY=your_openai_key_here
GOOGLE_BOOKS_API_KEY=your_google_books_key_here
```

### 4 — Run the backend

```bash
python app.py
# Server starts at http://localhost:5000
```

### 5 — Open the frontend

```bash
cd ../frontend
python -m http.server 3000
# App available at http://localhost:3000
```

---

## 🔌 API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/recommend?q=<query>` | AI-powered book recommendations |
| `GET` | `/api/search?q=<title>` | Search books by title or author |
| `GET` | `/api/book/<id>` | Details for a specific book |

> FastAPI users: interactive docs are auto-generated at `/docs`.

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repo
2. Create your branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m "Add amazing feature"`
4. Push: `git push origin feature/amazing-feature`
5. Open a Pull Request

---

## 📋 Roadmap

- [ ] User accounts and saved reading lists
- [ ] Goodreads export integration
- [ ] Book rating and review system
- [ ] Chrome extension for one-click recommendations
- [ ] Docker support for easy self-hosting
- [ ] Dark mode

---

## 📬 Connect

<div align="center">

[![LinkedIn](https://img.shields.io/badge/LinkedIn-dewanshikarnawat-0A66C2?style=flat-square&logo=linkedin)](https://linkedin.com/in/dewanshikarnawat)
[![GitHub](https://img.shields.io/badge/GitHub-dewanshikarnawat-181717?style=flat-square&logo=github)](https://github.com/dewanshikarnawat)

</div>

---

## 📄 License

Distributed under the MIT License. See [`LICENSE`](./LICENSE) for details.

---

<div align="center">

If this helped you discover your next favourite book — or helped you build something — please drop a ⭐  
It genuinely helps this project reach more readers and developers!

_Made with 💜 by [Dewanshi Karnawat](https://github.com/dewanshikarnawat)_

</div>
