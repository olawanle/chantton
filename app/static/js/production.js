// Production utilities and optimizations

// Error tracking (integrate with your error tracking service)
function trackError(error, context = {}) {
    if (window.Telegram && window.Telegram.WebApp) {
        // Log to console in development
        console.error('Error:', error, context);
        
        // In production, send to error tracking service
        // Example: Sentry, LogRocket, etc.
        if (typeof window.trackError === 'function') {
            window.trackError(error, context);
        }
    }
}

// Performance monitoring
function measurePerformance(name, fn) {
    if ('performance' in window && 'mark' in window.performance) {
        const startMark = `${name}-start`;
        const endMark = `${name}-end`;
        window.performance.mark(startMark);
        
        const result = fn();
        
        window.performance.mark(endMark);
        window.performance.measure(name, startMark, endMark);
        
        const measure = window.performance.getEntriesByName(name)[0];
        console.log(`${name} took ${measure.duration.toFixed(2)}ms`);
        
        return result;
    }
    return fn();
}

// Retry logic for failed requests
async function fetchWithRetry(url, options = {}, maxRetries = 3) {
    let lastError;
    for (let i = 0; i < maxRetries; i++) {
        try {
            const response = await fetch(url, options);
            if (response.ok) {
                return response;
            }
            // Retry on 5xx errors
            if (response.status >= 500 && i < maxRetries - 1) {
                await new Promise(resolve => setTimeout(resolve, 1000 * (i + 1)));
                continue;
            }
            return response;
        } catch (error) {
            lastError = error;
            if (i < maxRetries - 1) {
                await new Promise(resolve => setTimeout(resolve, 1000 * (i + 1)));
            }
        }
    }
    throw lastError;
}

// Debounce function for performance
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Throttle function for performance
function throttle(func, limit) {
    let inThrottle;
    return function(...args) {
        if (!inThrottle) {
            func.apply(this, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// Global error handler
window.addEventListener('error', (event) => {
    trackError(event.error, {
        message: event.message,
        filename: event.filename,
        lineno: event.lineno,
        colno: event.colno
    });
});

// Unhandled promise rejection handler
window.addEventListener('unhandledrejection', (event) => {
    trackError(event.reason, {
        type: 'unhandledrejection'
    });
});

