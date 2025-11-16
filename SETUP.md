# Quick Setup Guide

## For Termux (Android)

1. **Install dependencies**:
```bash
pkg update && pkg upgrade
pkg install python python-pip postgresql
pip install -r requirements.txt
```

2. **Setup SQLite (easier for Termux)**:
```bash
# Edit .env and set:
DATABASE_URL=sqlite:///app.db
```

3. **Initialize database**:
```bash
python -c "from app import create_app; from app.models import db; app = create_app(); app.app_context().push(); db.create_all()"
python scripts/seed_data.py
```

4. **Run server**:
```bash
python run.py
```

5. **Expose with ngrok** (install from https://ngrok.com):
```bash
ngrok http 5000
```

6. **Configure Telegram bot** (see README.md BotFather section)

## For Docker

```bash
docker-compose up -d
docker-compose exec web python scripts/seed_data.py
```

Access at `http://localhost:5000`

## For Local Development

See README.md for detailed instructions.

## Testing Without Telegram

The app can run in a regular browser for testing, but some features require Telegram WebApp API:
- Authentication will fail (you can mock it)
- Telegram popups won't work (use `alert()` fallback)

To test game logic without Telegram:
1. Comment out Telegram auth checks temporarily
2. Use browser dev tools to set session manually
3. Test endpoints directly with curl/Postman

