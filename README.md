# 🪞 WitMirror — Turn Negativity into Wisdom  

**WitMirror** is a web app that detects rude or negative comments online and responds with clever, proverb-style wisdom.  
Instead of arguing, WitMirror reflects the critic's tone back with calm wit — revealing their bad manners through elegance, not anger.  

---

## ✨ Features

### 🧠 **Core AI Features**
- 🔍 **Advanced Tone Detection:** Multi-layered sentiment analysis with emotion recognition
- 🧘 **8 Wisdom Styles:** Classic, Stoic, Zen, Sufi, Sarcastic, Poetic, Scientific, Humorous
- 💬 **Smart Reply Builder:** Context-aware responses for different platforms
- 🤖 **Multiple AI Providers:** OpenAI GPT-4, Anthropic Claude, Ollama (local)
- 🧩 **Mirror Mode:** Reflect negativity with elegant wisdom responses

### 🔗 **API Integrations**
- 📱 **Reddit Integration:** Analyze Reddit comments and posts
- 🐦 **Twitter Integration:** Process tweets and mentions
- 💬 **Discord Webhooks:** Send wisdom to Discord channels
- 📊 **Social Sentiment Analysis:** Cross-platform sentiment monitoring
- 🔄 **Real-time Data:** Live social media content analysis

### 📚 **Comment History & Analysis**
- 📖 **Complete History:** Track all your wisdom generations
- 🔍 **Advanced Search:** Filter by sentiment, platform, style, date
- ⭐ **Favorites System:** Save your most effective responses
- 📈 **Trending Topics:** Discover what topics you analyze most
- 📊 **Personal Analytics:** Your usage patterns and preferences
- 💾 **Export/Import:** Backup and restore your data

### 👤 **User Management**
- 🔐 **Authentication:** Secure JWT-based user system
- 👥 **User Profiles:** Personalized settings and preferences
- 🎛️ **Admin Dashboard:** System administration and monitoring
- 📊 **Usage Analytics:** Comprehensive user statistics
- 🔒 **Privacy Controls:** Granular privacy settings

### 🛠️ **Professional Tools**
- 📈 **Advanced Analytics:** Detailed usage insights and reporting
- 🚦 **Rate Limiting:** API protection and abuse prevention
- 🔧 **Admin Panel:** User management and system monitoring
- 📤 **Bulk Processing:** Analyze multiple texts simultaneously
- 🎨 **Custom Templates:** Create your own wisdom templates
- 📊 **Real-time Monitoring:** System health and performance metrics  

---

## 🧠 Example

**Negative comment:**  
> "This screams AI slop."  

**WitMirror reply:**  
> "The mirror often blames the face it reflects."  

or  

> "Politeness is free; rudeness always collects interest."  

---

## 🧩 Tech Stack

| Layer | Technology |
|-------|-------------|
| Frontend | SvelteKit / TailwindCSS |
| Backend | FastAPI / Python |
| AI Models | OpenAI GPT-4 / local LLM |
| Database | SQLite |
| Hosting | Vercel / Fly.io |

---

## 🚀 Quick Start

### Option 1: Automated Setup
```bash
git clone https://github.com/makalin/witmirror
cd witmirror
chmod +x scripts/setup.sh
./scripts/setup.sh
```

### Option 2: Manual Setup

**Frontend:**
```bash
npm install
npm run dev
```

**Backend:**
```bash
cd api
pip install -r requirements.txt
uvicorn main:app --reload
```

### Environment Setup
1. Copy `api/env.example` to `api/.env`
2. Add your OpenAI API key (optional - fallback wisdom will be used if not provided)
3. Start both servers

---

## 🌐 Access Points

- **Frontend:** http://localhost:5173
- **Backend API:** http://localhost:8000
- **API Documentation:** http://localhost:8000/docs
- **API Stats:** http://localhost:8000/stats

---

## 🐳 Docker Setup

```bash
# Build and run with Docker Compose
docker-compose up --build

# Or run individual services
docker-compose up frontend
docker-compose up backend
```

---

## 📁 Project Structure

```
witmirror/
├── src/                    # SvelteKit frontend
│   ├── routes/            # Pages and API routes
│   ├── app.html           # HTML template
│   └── app.css            # Global styles
├── api/                   # FastAPI backend
│   ├── main.py           # Main API application
│   ├── requirements.txt  # Python dependencies
│   └── env.example       # Environment template
├── static/               # Static assets
├── scripts/              # Setup and utility scripts
├── package.json          # Node.js dependencies
├── tailwind.config.js    # Tailwind configuration
└── README.md             # This file
```

---

## 🔧 API Endpoints

### POST `/api/analyze`
Analyze a comment and generate wisdom response.

**Request:**
```json
{
  "text": "This screams AI slop.",
  "platform": "reddit",
  "style": "classic"
}
```

**Response:**
```json
{
  "analysis": {
    "sentiment": "negative",
    "confidence": 0.85,
    "detected_emotions": ["anger", "contempt"],
    "toxicity_score": 0.3
  },
  "wisdom": "The mirror often blames the face it reflects.",
  "style": "classic",
  "platform": "reddit"
}
```

### GET `/api/stats`
Get usage statistics and analytics.

---

## 🎨 Wisdom Styles

- **Classic:** Traditional proverbs and wise sayings
- **Stoic:** Ancient Stoic philosophy wisdom
- **Zen:** Buddhist-inspired mindfulness wisdom
- **Sufi:** Mystical Sufi wisdom
- **Sarcastic:** Witty, slightly sarcastic responses

---

## 🧭 Roadmap

### ✅ **Completed Features**
* [x] **8 Wisdom Styles** (Classic, Stoic, Zen, Sufi, Sarcastic, Poetic, Scientific, Humorous)
* [x] **Comment History & Analytics** - Complete tracking and analysis
* [x] **API Integrations** - Reddit, Twitter, Discord webhooks
* [x] **User Authentication** - JWT-based user system
* [x] **Admin Dashboard** - System administration
* [x] **Advanced Analytics** - Comprehensive reporting
* [x] **Rate Limiting** - API protection
* [x] **Bulk Processing** - Multiple text analysis
* [x] **Export/Import** - Data management
* [x] **Social Sentiment Analysis** - Cross-platform monitoring

### 🚀 **Upcoming Features**
* [ ] **Browser Extension** (Chrome + Firefox) - Highlight comments and get instant wisdom
* [ ] **Mobile App** - iOS and Android applications
* [ ] **Advanced AI Models** - GPT-4 Turbo, Claude-3.5, local models
* [ ] **Real-time Notifications** - Push notifications for new mentions
* [ ] **Team Collaboration** - Shared workspaces and team analytics
* [ ] **Custom AI Training** - Train models on your specific wisdom style
* [ ] **API Marketplace** - Third-party integrations and plugins
* [ ] **Advanced Analytics** - Machine learning insights and predictions

---

## 🛠️ Development

### Frontend Development
```bash
npm run dev          # Start dev server
npm run build        # Build for production
npm run preview      # Preview production build
npm run check        # Type checking
```

### Backend Development
```bash
cd api
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Database
The app uses SQLite for simplicity. Database file: `api/witmirror.db`

---

## 🚀 Deployment

### Vercel (Frontend)
```bash
npm run build
# Deploy to Vercel
```

### Fly.io (Backend)
```bash
cd api
fly deploy
```

### Docker
```bash
docker-compose up --build
```

---

## 💡 Philosophy

WitMirror believes wisdom always wins over noise.
It doesn't fight trolls — it enlightens them.

> "When a wise man points at the moon, the fool looks at the finger."

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

---

**Author:** [Mehmet T. AKALIN](https://github.com/makalin)  
**Project Type:** Experimental AI / NLP / Satire  
**Version:** 1.0.0
