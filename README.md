# 🪞 WitMirror — Turn Negativity into Wisdom  

**WitMirror** is a web app that detects rude or negative comments online and responds with clever, proverb-style wisdom.  
Instead of arguing, WitMirror reflects the critic’s tone back with calm wit — revealing their bad manners through elegance, not anger.  

---

## ✨ Features

- 🔍 **Tone Detection:** Uses AI sentiment and intent analysis to detect sarcasm, hostility, or negativity.  
- 🧘 **Proverb Generator:** Crafts original, wise phrases inspired by world proverbs and modern wit.  
- 💬 **Smart Reply Builder:** Creates subtle, context-aware responses that fit platform tone (Reddit, X, etc).  
- 🧩 **Mirror Mode:** Optionally rephrases your own draft into a composed, witty reflection.  
- 🌐 **Browser Plugin (planned):** Highlight a comment, click *Reflect*, and let WitMirror respond.  

---

## 🧠 Example

**Negative comment:**  
> “This screams AI slop.”  

**WitMirror reply:**  
> “The mirror often blames the face it reflects.”  

or  

> “Politeness is free; rudeness always collects interest.”  

---

## 🧩 Tech Stack

| Layer | Technology |
|-------|-------------|
| Frontend | SvelteKit / TailwindCSS |
| Backend | FastAPI / Python |
| AI Models | OpenAI GPT-4 / local LLM |
| Database | SQLite or Supabase |
| Hosting | Vercel / Fly.io |

---

## 🚀 Run Locally

```bash
git clone https://github.com/makalin/witmirror
cd witmirror
npm install
npm run dev
````

Backend (optional):

```bash
cd api
pip install -r requirements.txt
uvicorn main:app --reload
```

---

## 🧭 Roadmap

* [ ] Browser extension (Chrome + Firefox)
* [ ] “Wisdom Styles” (Sufi, Stoic, Zen, Sarcastic)
* [ ] Comment history and reflection analytics
* [ ] API for integrations (Discord, Reddit bots)

---

## 💡 Philosophy

WitMirror believes wisdom always wins over noise.
It doesn’t fight trolls — it enlightens them.

> “When a wise man points at the moon, the fool looks at the finger.”

---

**Author:** [Mehmet Akalın](https://github.com/makalin)
**License:** MIT
**Project Type:** Experimental AI / NLP / Satire
