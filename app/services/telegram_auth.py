import hmac
import hashlib
import json
import urllib.parse
from app.config import Config

def validate_telegram_auth(init_data: str) -> dict:
    """
    Validate Telegram WebApp initData.
    Returns user data if valid, None otherwise.
    """
    if not Config.TELEGRAM_BOT_TOKEN:
        # In development, allow without validation
        try:
            params = dict(urllib.parse.parse_qsl(init_data))
            user_str = params.get('user', '{}')
            user_data = json.loads(user_str)
            return user_data
        except:
            return None
    
    try:
        # Parse init_data
        params = dict(urllib.parse.parse_qsl(init_data))
        
        # Get hash
        received_hash = params.pop('hash', '')
        if not received_hash:
            return None
        
        # Create data check string
        data_check_string = '\n'.join(f"{k}={v}" for k, v in sorted(params.items()))
        
        # Calculate secret key
        secret_key = hmac.new(
            key=b"WebAppData",
            msg=Config.TELEGRAM_BOT_TOKEN.encode(),
            digestmod=hashlib.sha256
        ).digest()
        
        # Calculate hash
        calculated_hash = hmac.new(
            key=secret_key,
            msg=data_check_string.encode(),
            digestmod=hashlib.sha256
        ).hexdigest()
        
        # Verify
        if calculated_hash != received_hash:
            return None
        
        # Parse user data
        user_str = params.get('user', '{}')
        user_data = json.loads(user_str)
        
        return user_data
    except Exception as e:
        print(f"Telegram auth validation error: {e}")
        return None

