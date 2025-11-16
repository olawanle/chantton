# Crystal Game - Telegram Mini-App

A production-ready Telegram Mini-App clone built with Flask, featuring crystal opening mechanics, tasks, leaderboard, and admin dashboard.

## Features

- 🎮 **Crystal Opening Game** - Randomized prize system with configurable probabilities
- 📋 **Tasks System** - Complete tasks to earn rewards
- 🏆 **Leaderboard** - Compete and climb the ranks
- 👤 **User Profiles** - View collection and activity
- 🛡️ **Admin Dashboard** - Manage claims, prizes, and view audit logs
- 🔐 **Telegram Integration** - Full WebApp API support
- 💰 **TON Payout System** - Placeholder for TON blockchain payouts

## Tech Stack

- **Backend**: Flask (Python)
- **Database**: PostgreSQL (SQLite for local development)
- **Frontend**: Jinja2 templates + vanilla JavaScript
- **Styling**: Custom CSS with starfield animation
- **Deployment**: Docker + Docker Compose

## Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL (or use SQLite for local testing)
- Docker & Docker Compose (optional)

### Local Development (SQLite)

1. **Clone and setup**:
```bash
git clone <repo-url>
cd chant
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. **Configure environment**:
```bash
cp .env.example .env
# Edit .env and set your TELEGRAM_BOT_TOKEN and ADMIN_TOKEN
```

3. **Initialize database**:
```bash
python -m flask shell
>>> from app import create_app
>>> from app.models import db
>>> app = create_app()
>>> app.app_context().push()
>>> db.create_all()
>>> exit()
```

4. **Seed initial data**:
```bash
python scripts/seed_data.py
```

5. **Run the application**:
```bash
python run.py
```

The app will be available at `http://localhost:5000`

### Docker Deployment

1. **Setup environment**:
```bash
cp .env.example .env
# Edit .env with your configuration
```

2. **Start services**:
```bash
docker-compose up -d
```

3. **Seed data** (in a new terminal):
```bash
docker-compose exec web python scripts/seed_data.py
```

4. **Access the app**:
- WebApp: `http://localhost:5000`
- Admin Dashboard: `http://localhost:5000/admin/dashboard`

## Telegram Bot Setup

### 1. Create a Bot

1. Open Telegram and search for [@BotFather](https://t.me/BotFather)
2. Send `/newbot` and follow instructions
3. Save your bot token (you'll need it for `TELEGRAM_BOT_TOKEN`)

### 2. Configure WebApp

1. Send `/newapp` to BotFather
2. Select your bot
3. Provide app details:
   - **Title**: Crystal Game
   - **Description**: Open crystals and win prizes!
   - **Photo**: Upload a 640x360 image (optional)
   - **Web App URL**: `https://your-domain.com` (or use ngrok for testing)

### 3. Add Menu Button (Optional)

Send this to BotFather:
```
/setmenubutton
@your_bot_username
Crystal Game - https://your-domain.com
```

### 4. Set Bot Domain (Required)

Send this to BotFather:
```
/setdomain
@your_bot_username
your-domain.com
```

### 5. Testing with ngrok (Local Development)

1. Install ngrok: https://ngrok.com/download
2. Start your Flask app locally
3. Run: `ngrok http 5000`
4. Copy the HTTPS URL (e.g., `https://abc123.ngrok.io`)
5. Use this URL in BotFather commands above

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Flask secret key | `dev-secret-key-change-in-production` |
| `DATABASE_URL` | Database connection string | `sqlite:///app.db` |
| `TELEGRAM_BOT_TOKEN` | Telegram bot token | (required) |
| `ADMIN_TOKEN` | Admin dashboard token | `admin-token-change-me` |
| `MAX_PLAYS_PER_HOUR` | Rate limit for game plays | `10` |
| `DEFAULT_CRYSTAL_COST` | Cost to open a crystal | `6` |
| `TON_WALLET_PRIVATE_KEY` | TON wallet private key (optional) | - |
| `TON_NETWORK` | TON network (mainnet/testnet) | `testnet` |

## Project Structure

```
chant/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── config.py            # Configuration
│   ├── models.py            # Database models
│   ├── database.py          # DB initialization
│   ├── routes/              # Route blueprints
│   │   ├── main.py         # Main routes (index, leaderboard, profile)
│   │   ├── auth.py         # Telegram authentication
│   │   ├── game.py         # Game play endpoints
│   │   ├── tasks.py        # Tasks endpoints
│   │   └── admin.py        # Admin endpoints
│   ├── services/           # Business logic
│   │   ├── game_service.py # Game play logic
│   │   ├── rate_limiter.py # Rate limiting
│   │   ├── telegram_auth.py # Telegram auth validation
│   │   └── ton_payout.py   # TON payout (placeholder)
│   ├── templates/          # Jinja2 templates
│   │   ├── base.html
│   │   ├── index.html     # Main crystal screen
│   │   ├── tasks.html
│   │   ├── leaderboard.html
│   │   ├── profile.html
│   │   └── admin/
│   │       └── dashboard.html
│   └── static/             # Static files
│       ├── css/
│       ├── js/
│       └── images/        # Place your assets here
├── migrations/             # SQL migrations
├── scripts/               # Utility scripts
│   └── seed_data.py      # Seed prizes and tasks
├── tests/                 # Unit tests
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── run.py
└── README.md
```

## API Endpoints

### Public Endpoints

- `GET /` - Main UI (crystal screen)
- `GET /leaderboard` - Leaderboard UI
- `GET /profile` - Profile UI
- `GET /tasks` - Tasks UI
- `GET /health` - Health check
- `GET /prizes` - List active prizes
- `GET /wins` - Get recent wins for carousel

### Authentication

- `POST /auth/telegram` - Authenticate via Telegram WebApp initData

### Game

- `POST /game/play` - Play a game (open crystal)
- `GET /game/user/<id>/history` - Get user game history
- `POST /game/claim/<game_id>` - Create claim for prize

### Tasks

- `GET /tasks` - List available tasks
- `POST /tasks/check` - Verify and complete a task

### Admin (Protected)

- `GET /admin/dashboard` - Admin dashboard UI
- `GET /admin/claims` - List claims (query param: `?token=...`)
- `POST /admin/payout/<claim_id>` - Process payout
- `POST /admin/claim/<claim_id>/approve` - Approve claim
- `POST /admin/claim/<claim_id>/reject` - Reject claim
- `GET /admin/prizes` - List all prizes
- `POST /admin/prize` - Add/update prize

## Database Schema

### Users
- `id` (BIGINT PRIMARY KEY)
- `tg_user_id` (BIGINT UNIQUE) - Telegram user ID
- `username` (TEXT)
- `display_name` (TEXT)
- `created_at` (TIMESTAMP)

### Games
- `id` (BIGINT PRIMARY KEY)
- `user_id` (BIGINT FOREIGN KEY)
- `result` (JSONB) - Game result data
- `reward_id` (BIGINT FOREIGN KEY, nullable)
- `created_at` (TIMESTAMP)

### Prizes
- `id` (BIGINT PRIMARY KEY)
- `name` (TEXT)
- `type` (TEXT) - 'ton', 'coupon', 'points'
- `meta` (JSONB) - Prize metadata
- `probability` (NUMERIC) - Probability weight (0-1)
- `is_active` (BOOLEAN)

### Claims
- `id` (BIGINT PRIMARY KEY)
- `game_id` (BIGINT FOREIGN KEY)
- `user_id` (BIGINT FOREIGN KEY)
- `status` (TEXT) - 'pending', 'approved', 'paid', 'rejected'
- `payout_tx` (TEXT) - Transaction hash
- `created_at` (TIMESTAMP)
- `updated_at` (TIMESTAMP)

### Tasks
- `id` (BIGINT PRIMARY KEY)
- `name` (TEXT)
- `description` (TEXT)
- `action_type` (TEXT) - 'subscribe', 'boost', 'join'
- `action_meta` (JSONB) - Channel/group IDs
- `reward_points` (INTEGER)
- `is_active` (BOOLEAN)

## Adding Assets

Place your images in `app/static/images/`:
- `crystal-placeholder.png` - Main crystal image
- `scared_cat.png` - Prize image
- `skull_flow.png` - Prize image
- Other prize/character images

Update image paths in:
- Templates (e.g., `index.html`)
- Seed data script (`scripts/seed_data.py`)

## Testing

Run unit tests:
```bash
python -m pytest tests/
```

Or run specific test file:
```bash
python -m pytest tests/test_game_service.py
```

## Deployment to Render

See [RENDER_DEPLOY.md](RENDER_DEPLOY.md) for detailed instructions on deploying to Render.

Quick steps:
1. Push code to GitHub
2. Create PostgreSQL database on Render
3. Create Web Service pointing to your repo
4. Set environment variables
5. Initialize database via Render Shell
6. Configure Telegram bot with your Render URL

## Production Deployment

### Security Checklist

- [ ] Change `SECRET_KEY` to a strong random value
- [ ] Change `ADMIN_TOKEN` to a secure token
- [ ] Use PostgreSQL in production (not SQLite)
- [ ] Set `FLASK_ENV=production` and `FLASK_DEBUG=0`
- [ ] Use HTTPS (required for Telegram WebApp)
- [ ] Store `TON_WALLET_PRIVATE_KEY` securely (use secrets manager)
- [ ] Enable rate limiting at reverse proxy level
- [ ] Set up database backups
- [ ] Configure CORS if needed

### Recommended Stack

- **Web Server**: Nginx (reverse proxy)
- **WSGI Server**: Gunicorn or uWSGI
- **Database**: PostgreSQL 15+
- **Process Manager**: systemd or supervisor
- **SSL**: Let's Encrypt (certbot)

### Gunicorn Example

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 "app:create_app()"
```

## TON Payout Integration

The current `services/ton_payout.py` is a placeholder. To integrate real TON payouts:

1. Install TON SDK: `pip install pytonlib` or use `toncenter` API
2. Update `send_payout()` function in `services/ton_payout.py`
3. Store private keys securely (use environment variables or secrets manager)
4. Test on testnet first

Example integration:
```python
from pytonlib import TonlibClient

async def send_payout(to_address: str, amount: float):
    # Initialize client
    # Sign transaction
    # Broadcast
    # Return tx hash
```

## Troubleshooting

### Telegram WebApp not loading
- Ensure you're using HTTPS (required by Telegram)
- Check domain is set correctly in BotFather
- Verify `TELEGRAM_BOT_TOKEN` is correct
- Check browser console for errors

### Database connection errors
- Verify `DATABASE_URL` is correct
- For PostgreSQL: ensure database exists and user has permissions
- Check PostgreSQL is running: `pg_isready`

### Admin dashboard access denied
- Verify `ADMIN_TOKEN` matches in `.env` and request header
- Check token is passed as query param: `?token=...` or header: `X-Admin-Token`

## License

This project is provided as-is for educational purposes.

## Support

For issues or questions, please open an issue in the repository.

---

**Note**: This is a clone/template project. Replace placeholder images, customize styling, and implement actual Telegram Bot API verification for tasks in production.

