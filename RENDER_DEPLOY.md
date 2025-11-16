# Deploying to Render

This guide will help you deploy the Crystal Game Telegram Mini-App to Render.

## Prerequisites

1. A Render account (sign up at https://render.com)
2. Your Telegram Bot Token
3. A GitHub repository (optional, but recommended)

## Step 1: Prepare Your Repository

1. **Push your code to GitHub** (if not already done):
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin <your-github-repo-url>
   git push -u origin main
   ```

2. **Create a `.env` file locally** (don't commit this):
   - Copy `.env.example` to `.env`
   - Fill in your values

## Step 2: Deploy via Render Dashboard

### Option A: Using render.yaml (Recommended)

1. Go to https://dashboard.render.com
2. Click **"New +"** → **"Blueprint"**
3. Connect your GitHub repository
4. Render will automatically detect `render.yaml`
5. Review the configuration and click **"Apply"**

### Option B: Manual Setup

#### Create PostgreSQL Database

1. Go to https://dashboard.render.com
2. Click **"New +"** → **"PostgreSQL"**
3. Configure:
   - **Name**: `crystal-game-db`
   - **Database**: `crystal_game`
   - **User**: `crystal_game_user`
   - **Plan**: Free (or paid for production)
4. Click **"Create Database"**
5. Copy the **Internal Database URL** (you'll need this)

#### Create Web Service

1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub repository
3. Configure the service:

   **Basic Settings:**
   - **Name**: `crystal-game`
   - **Environment**: `Python 3`
   - **Region**: Choose closest to your users
   - **Branch**: `main` (or your default branch)
   - **Root Directory**: Leave empty (or `./` if needed)

   **Build & Deploy:**
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn -w 4 -b 0.0.0.0:$PORT --timeout 120 --access-logfile - --error-logfile - "app:create_app()"`

   **Environment Variables:**
   ```
   PYTHON_VERSION=3.11.0
   DATABASE_URL=<from PostgreSQL service>
   SECRET_KEY=<generate a strong random string>
   TELEGRAM_BOT_TOKEN=<your-telegram-bot-token>
   ADMIN_TOKEN=<generate a strong random string>
   FLASK_ENV=production
   FLASK_DEBUG=0
   SESSION_COOKIE_SECURE=True
   MAX_PLAYS_PER_HOUR=10
   DEFAULT_CRYSTAL_COST=6
   ```

4. Click **"Create Web Service"**

## Step 3: Generate Secure Keys

Generate secure values for `SECRET_KEY` and `ADMIN_TOKEN`:

```bash
# On Linux/Mac
python -c "import secrets; print(secrets.token_hex(32))"

# Or use online generator: https://randomkeygen.com/
```

Add these to your Render environment variables.

## Step 4: Initialize Database

After the first deployment:

1. Go to your web service in Render dashboard
2. Click **"Shell"** tab
3. Run:
   ```bash
   python -c "from app import create_app; from app.models import db; app = create_app(); app.app_context().push(); db.create_all()"
   python scripts/seed_data.py
   ```

Or use the Render Shell:
```bash
# Initialize database
python -c "from app import create_app; from app.models import db; app = create_app(); app.app_context().push(); db.create_all()"

# Seed data
python scripts/seed_data.py
```

## Step 5: Configure Telegram Bot

1. Get your Render app URL (e.g., `https://crystal-game.onrender.com`)
2. Open Telegram and go to [@BotFather](https://t.me/BotFather)
3. Send `/newapp` and select your bot
4. Provide:
   - **Title**: Crystal Game
   - **Description**: Open crystals and win prizes!
   - **Photo**: (optional)
   - **Web App URL**: `https://your-app-name.onrender.com`
5. Send `/setdomain` and set your domain to `your-app-name.onrender.com`

## Step 6: Update Environment Variables

If you need to update environment variables later:

1. Go to your service in Render dashboard
2. Click **"Environment"** tab
3. Add/edit variables
4. Click **"Save Changes"**
5. Service will automatically redeploy

## Step 7: Custom Domain (Optional)

1. Go to your service → **"Settings"**
2. Scroll to **"Custom Domains"**
3. Add your domain
4. Follow DNS configuration instructions
5. Update Telegram Bot domain setting

## Troubleshooting

### Database Connection Issues

- Check that `DATABASE_URL` is set correctly
- Ensure database is in the same region as web service
- Use **Internal Database URL** (not external) for better performance

### Build Failures

- Check build logs in Render dashboard
- Ensure `requirements.txt` has all dependencies
- Verify Python version matches (3.11.0)

### App Not Starting

- Check logs in Render dashboard
- Verify `PORT` environment variable is used (Render sets this automatically)
- Check that gunicorn is in requirements.txt

### Icons Not Showing

- Clear browser cache
- Check that static files are being served correctly
- Verify `app/static` directory structure

## Monitoring

- **Logs**: View real-time logs in Render dashboard
- **Metrics**: Monitor CPU, memory, and request metrics
- **Alerts**: Set up alerts for errors or downtime

## Scaling

For production with higher traffic:

1. Upgrade to a paid plan
2. Increase gunicorn workers: `-w 8` (adjust based on CPU)
3. Use a paid PostgreSQL plan
4. Enable auto-scaling if needed

## Backup Strategy

1. **Database Backups**: Render provides automatic backups for paid plans
2. **Manual Backup**: Use pg_dump via Render Shell
3. **Code Backup**: Your code is in GitHub

## Environment Variables Reference

| Variable | Description | Required |
|----------|-------------|----------|
| `DATABASE_URL` | PostgreSQL connection string | Yes |
| `SECRET_KEY` | Flask secret key | Yes |
| `TELEGRAM_BOT_TOKEN` | Telegram bot token | Yes |
| `ADMIN_TOKEN` | Admin dashboard token | Yes |
| `FLASK_ENV` | Set to `production` | Yes |
| `FLASK_DEBUG` | Set to `0` | Yes |
| `SESSION_COOKIE_SECURE` | Set to `True` | Yes |
| `MAX_PLAYS_PER_HOUR` | Rate limit | No |
| `DEFAULT_CRYSTAL_COST` | Crystal cost | No |
| `TON_WALLET_PRIVATE_KEY` | TON wallet (if using) | No |

## Post-Deployment Checklist

- [ ] Database initialized
- [ ] Seed data loaded
- [ ] Telegram bot configured
- [ ] WebApp URL set in BotFather
- [ ] Domain set in BotFather
- [ ] Test authentication
- [ ] Test game play
- [ ] Test admin dashboard
- [ ] Monitor logs for errors
- [ ] Set up alerts

## Support

- Render Docs: https://render.com/docs
- Render Status: https://status.render.com
- Render Community: https://community.render.com

---

**Note**: Free tier services on Render spin down after 15 minutes of inactivity. For production, consider upgrading to a paid plan.

