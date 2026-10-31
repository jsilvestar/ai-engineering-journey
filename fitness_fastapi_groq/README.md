#1 Fitness Planner

FastAPI examples: Fitness plan app using LLM-powered generator via Groq.
you have option to download the weekly plan.

## Setup

### 🔑 Getting a Groq API key

You only need to do this once.

1. Go to **[console.groq.com](https://console.groq.com/keys)** and sign up — email, Google, or GitHub all work. No credit card needed.
2. In the left sidebar, click **API Keys** → **Create API Key**.
3. Give it a name (e.g. `my-groq-key`) and click **Create**.
4. **Copy the key immediately** — Groq shows it to you exactly once. If you lose it, you'll have to create a new one.
5. Paste it into your `.env` file (copy `.env.sample` to `.env` first):
   ```
   GROQ_API_KEY=your_key_here
   ```
6. Never commit `.env` to git or paste your key into a shared notebook cell, this project's `.gitignore` already excludes it, keep it that way.

### 🔄 Syncing dependencies

```bash
uv sync
```

## Scripts

2. Start FastAPI backend
Open Terminal 1 in VS Code and run:
```bash
 uv run uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

3. Start Streamlit frontend
Open Terminal 2 using the + icon in VS Code.

```bash
uv run streamlit run frontend/app.py
```

4 . Open URL  in the browser
```bash
http://localhost:8501/
```