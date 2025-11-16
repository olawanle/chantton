// Main app JavaScript
(function() {
    // Utility functions
    window.showToast = function(message, type = 'info') {
        if (window.Telegram && window.Telegram.WebApp) {
            window.Telegram.WebApp.showPopup({
                title: type === 'success' ? 'Success' : type === 'error' ? 'Error' : 'Info',
                message: message,
                buttons: [{type: 'ok'}]
            });
        } else {
            alert(message);
        }
    };
    
    window.closeApp = function() {
        if (window.Telegram && window.Telegram.WebApp) {
            window.Telegram.WebApp.close();
        }
    };
    
    window.navigateTo = function(path) {
        window.location.href = path;
    };
})();

