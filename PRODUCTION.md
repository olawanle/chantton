# Production Deployment Guide

## Pre-Deployment Checklist

### 1. Environment Variables
- [ ] Set strong `SECRET_KEY` (use `python -c "import secrets; print(secrets.token_hex(32))"`)
- [ ] Set strong `ADMIN_TOKEN`
- [ ] Configure `TELEGRAM_BOT_TOKEN`
- [ ] Set `DATABASE_URL` to PostgreSQL connection string
- [ ] Set `FLASK_DEBUG=0` or remove it
- [ ] Set `SESSION_COOKIE_SECURE=True` (for HTTPS)
- [ ] Configure `TON_WALLET_PRIVATE_KEY` if using TON payouts

### 2. Database
- [ ] Use PostgreSQL (not SQLite)
- [ ] Run migrations: `python -c "from app import create_app; from app.models import db; app = create_app(); app.app_context().push(); db.create_all()"`
- [ ] Seed initial data: `python scripts/seed_data.py`
- [ ] Set up database backups
- [ ] Configure connection pooling

### 3. Security
- [ ] Enable HTTPS (required for Telegram WebApp)
- [ ] Verify security headers are set (see `app/middleware.py`)
- [ ] Review and test rate limiting
- [ ] Test input validation
- [ ] Verify admin endpoints are protected
- [ ] Set up firewall rules

### 4. Monitoring & Logging
- [ ] Configure logging to file (see `app/middleware.py`)
- [ ] Set up log rotation
- [ ] Configure error tracking (Sentry, etc.)
- [ ] Set up uptime monitoring
- [ ] Configure alerts for errors

### 5. Performance
- [ ] Use production WSGI server (Gunicorn/uWSGI)
- [ ] Configure worker processes
- [ ] Set up reverse proxy (Nginx)
- [ ] Enable static file caching
- [ ] Configure database connection pooling
- [ ] Set up CDN for static assets (optional)

## Deployment Options

### Option 1: Docker (Recommended)

```bash
# Build and run
docker-compose -f docker-compose.prod.yml up -d

# View logs
docker-compose logs -f web

# Update
docker-compose pull
docker-compose up -d --build
```

### Option 2: Gunicorn + Nginx

#### Install Gunicorn
```bash
pip install gunicorn
```

#### Run with Gunicorn
```bash
gunicorn -w 4 -b 0.0.0.0:5000 --timeout 120 --access-logfile - --error-logfile - "app:create_app()"
```

#### Nginx Configuration
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    # Security headers
    add_header X-Frame-Options "DENY" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    
    # Static files
    location /static {
        alias /path/to/app/static;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
    
    # Proxy to Gunicorn
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }
}
```

### Option 3: systemd Service

Create `/etc/systemd/system/crystal-game.service`:

```ini
[Unit]
Description=Crystal Game Flask Application
After=network.target postgresql.service

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/app
Environment="PATH=/path/to/venv/bin"
Environment="DATABASE_URL=postgresql://user:pass@localhost/db"
Environment="SECRET_KEY=your-secret-key"
Environment="TELEGRAM_BOT_TOKEN=your-token"
Environment="ADMIN_TOKEN=your-admin-token"
ExecStart=/path/to/venv/bin/gunicorn -w 4 -b 127.0.0.1:5000 --timeout 120 "app:create_app()"
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable crystal-game
sudo systemctl start crystal-game
sudo systemctl status crystal-game
```

## Production Configuration

### Environment Variables Template

```bash
# Flask
SECRET_KEY=your-strong-secret-key-here
FLASK_ENV=production
FLASK_DEBUG=0

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/crystal_game

# Telegram
TELEGRAM_BOT_TOKEN=your-bot-token

# Admin
ADMIN_TOKEN=your-strong-admin-token

# Security
SESSION_COOKIE_SECURE=True

# Game Settings
MAX_PLAYS_PER_HOUR=10
DEFAULT_CRYSTAL_COST=6

# TON (if using)
TON_WALLET_PRIVATE_KEY=your-private-key
TON_NETWORK=mainnet
```

## Monitoring

### Health Check Endpoint
```bash
curl https://your-domain.com/health
```

### Logs
```bash
# Application logs
tail -f logs/app.log

# Gunicorn logs
journalctl -u crystal-game -f

# Nginx logs
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log
```

## Backup Strategy

### Database Backup
```bash
# Daily backup script
pg_dump -U postgres crystal_game > backup_$(date +%Y%m%d).sql

# Restore
psql -U postgres crystal_game < backup_20240101.sql
```

### Automated Backups
Set up cron job:
```bash
0 2 * * * /path/to/backup-script.sh
```

## Scaling

### Horizontal Scaling
- Use load balancer (Nginx, HAProxy)
- Multiple Gunicorn workers
- Shared session storage (Redis)
- Database read replicas

### Vertical Scaling
- Increase Gunicorn workers: `-w 8`
- Increase database connection pool
- Add more RAM/CPU

## Security Hardening

1. **Firewall**: Only allow ports 80, 443, and SSH
2. **Fail2ban**: Protect against brute force
3. **SSL/TLS**: Use Let's Encrypt with auto-renewal
4. **Updates**: Keep system and dependencies updated
5. **Secrets**: Use secrets manager (AWS Secrets Manager, HashiCorp Vault)
6. **Rate Limiting**: Configure at reverse proxy level
7. **WAF**: Consider Web Application Firewall

## Troubleshooting

### High Memory Usage
- Reduce Gunicorn workers
- Check for memory leaks
- Enable database query logging

### Slow Response Times
- Check database queries (use EXPLAIN)
- Enable caching (Redis)
- Optimize static files
- Check network latency

### Database Connection Errors
- Check connection pool settings
- Verify database is running
- Check firewall rules
- Review connection limits

## Maintenance

### Regular Tasks
- [ ] Review logs weekly
- [ ] Update dependencies monthly
- [ ] Test backups monthly
- [ ] Review security alerts
- [ ] Monitor disk space
- [ ] Check error rates

### Updates
```bash
# Update dependencies
pip install --upgrade -r requirements.txt

# Run migrations if needed
# Test in staging first
# Deploy to production
```

## Support

For production issues:
1. Check logs first
2. Review error tracking
3. Check database status
4. Verify environment variables
5. Test health endpoint

