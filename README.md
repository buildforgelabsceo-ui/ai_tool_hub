# AIToolHub

A production-ready AI tools discovery platform built with Flask, SQLite, and vanilla JavaScript.

## Features

- 🔍 **Search** — Real-time search across tool names, categories, and tags
- 📁 **Categories** — Browse tools by category (Writing, Coding, Image, Video, etc.)
- 📄 **Tool Pages** — SEO-friendly individual pages for every tool (`/tools/chatgpt`)
- ➕ **Submit Tools** — Community form to add new tools
- 📱 **Responsive** — Works on mobile, tablet, and desktop

## Quick Start

```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
python app.py
```

Visit **http://localhost:5000**

## Project Structure

```
aitoolhub/
├── app.py                  # Entry point
├── config.py               # Configuration
├── requirements.txt
├── Procfile                # Heroku/Render deployment
├── aitoolhub/
│   ├── __init__.py         # App factory
│   ├── models/
│   │   ├── __init__.py     # SQLAlchemy instance
│   │   └── tool.py         # Tool model
│   ├── routes/
│   │   ├── __init__.py
│   │   └── main.py         # All route handlers
│   ├── data/
│   │   └── seed.py         # 18 pre-loaded AI tools
│   ├── templates/
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── tools.html
│   │   ├── tool_detail.html
│   │   ├── categories.html
│   │   ├── submit.html
│   │   └── 404.html
│   └── static/
│       ├── css/style.css
│       └── js/main.js
└── aitoolhub.db            # SQLite database (auto-created)
```

## Adding Tools

### Via the web UI
Visit `/submit` and fill in the form.

### Via seed data
Edit `aitoolhub/data/seed.py` and add entries to `SEED_TOOLS`.

### Via Python shell
```python
from aitoolhub import create_app
from aitoolhub.models import db
from aitoolhub.models.tool import Tool

app = create_app()
with app.app_context():
    tool = Tool(
        name="New Tool",
        slug="new-tool",
        description="Full description...",
        short_description="One-liner",
        website_url="https://example.com",
        category="AI Writing Tools",
        # logo_url="https://example.com/logo.png",
        pricing="Freemium",
        tags="writing,productivity",
        featured=False
    )
    db.session.add(tool)
    db.session.commit()
```

## Deployment

### Render / Railway / Heroku
```bash
# Set env vars:
SECRET_KEY=your-secret-key
FLASK_ENV=production
```

The `Procfile` handles the gunicorn server command.

## Pages

| Route | Description |
|-------|-------------|
| `/` | Homepage with featured tools |
| `/tools` | All tools with search & filter |
| `/tools/<slug>` | Individual tool detail page |
| `/categories` | All categories overview |
| `/categories/<name>` | Tools in a category |
| `/submit` | Submit a new tool |
| `/api/search?q=...` | JSON search API |
