// Telegram WebApp utilities
(function() {
    if (!window.Telegram || !window.Telegram.WebApp) {
        console.warn('Telegram WebApp API not available');
        return;
    }
    
    const tg = window.Telegram.WebApp;
    
    // Initialize
    tg.ready();
    tg.expand();
    
    // Set theme colors (optional)
    tg.setHeaderColor('#000000');
    tg.setBackgroundColor('#000000');
    
    // Enable closing confirmation
    tg.enableClosingConfirmation();
    
    // Export for use in other scripts
    window.TelegramWebApp = tg;
})();

