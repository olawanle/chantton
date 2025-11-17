// Icon SVG definitions
const Icons = {
    diamond: `<svg class="icon icon-diamond" viewBox="0 0 24 24" fill="currentColor">
        <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/>
    </svg>`,
    
    bat: `<svg class="icon icon-bat" viewBox="0 0 24 24" fill="currentColor">
        <path d="M12 2C8 2 5 5 5 9c0 2 1 4 2 5v6h10v-6c1-1 2-3 2-5 0-4-3-7-7-7zm0 2c3 0 5 2 5 5 0 1.5-.7 3-1.5 4h-7C7.7 12 7 10.5 7 9c0-3 2-5 5-5z"/>
    </svg>`,
    
    crown: `<svg class="icon icon-crown" viewBox="0 0 24 24" fill="currentColor">
        <path d="M5 16L3 5l5.5 5L12 4l3.5 6L21 5l-2 11H5zm2.7-2h8.6l.9-6.4-2.1 2.1L12 6l-3.1 3.6-2.1-2.1L7.7 14z"/>
    </svg>`,
    
    home: `<svg class="icon icon-home" viewBox="0 0 24 24" fill="currentColor">
        <path d="M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z"/>
    </svg>`,
    
    inventory: `<svg class="icon icon-inventory" viewBox="0 0 24 24" fill="currentColor">
        <path d="M20 6h-2.18c.11-.31.18-.65.18-1a2.996 2.996 0 0 0-5.5-1.65l-.5.67-.5-.68C10.96 2.54 10 2 9 2 7.34 2 6 3.34 6 5c0 .35.07.69.18 1H4c-1.11 0-1.99.89-1.99 2L2 19c0 1.11.89 2 2 2h16c1.11 0 2-.89 2-2V8c0-1.11-.89-2-2-2zm-5-2c.55 0 1 .45 1 1s-.45 1-1 1-1-.45-1-1 .45-1 1-1zM9 4c.55 0 1 .45 1 1s-.45 1-1 1-1-.45-1-1 .45-1 1-1zm11 15H4v-2h16v2zm0-5H4V8h5.08L7 10.83 8.62 12 11 8.76l1-1.36 1 1.36L15.38 12 17 10.83 14.92 8H20v6z"/>
    </svg>`,
    
    target: `<svg class="icon icon-target" viewBox="0 0 24 24" fill="currentColor">
        <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm.31-8.86c-1.77-.45-2.34-.94-2.34-1.67 0-.84.79-1.43 2.1-1.43 1.38 0 1.9.66 1.94 1.64h1.71c-.05-1.34-.87-2.57-2.49-2.97V5H10.9v1.69c-1.51.32-2.72 1.3-2.72 2.81 0 1.79 1.49 2.69 3.66 3.21 1.95.46 2.34 1.12 2.34 1.87 0 .53-.39 1.39-2.1 1.39-1.6 0-2.23-.72-2.32-1.64H8.04c.1 1.7 1.36 2.66 2.86 2.97V19h2.34v-1.67c1.52-.29 2.72-1.16 2.72-2.81 0-1.79-1.49-2.69-3.66-3.21z"/>
    </svg>`,
    
    close: `<svg class="icon icon-close" viewBox="0 0 24 24" fill="currentColor">
        <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/>
    </svg>`,
    
    chevronDown: `<svg class="icon icon-chevron-down" viewBox="0 0 24 24" fill="currentColor">
        <path d="M7.41 8.59L12 13.17l4.59-4.58L18 10l-6 6-6-6 1.41-1.41z"/>
    </svg>`,
    
    menu: `<svg class="icon icon-menu" viewBox="0 0 24 24" fill="currentColor">
        <path d="M3 18h18v-2H3v2zm0-5h18v-2H3v2zm0-7v2h18V6H3z"/>
    </svg>`,
    
    airplane: `<svg class="icon icon-airplane" viewBox="0 0 24 24" fill="currentColor">
        <path d="M21 16v-2l-8-5V3.5c0-.83-.67-1.5-1.5-1.5S10 2.67 10 3.5V9l-8 5v2l8-2.5V19l-2 1.5V22l3.5-1 3.5 1v-1.5L13 19v-5.5l8 2.5z"/>
    </svg>`,
    
    check: `<svg class="icon icon-check" viewBox="0 0 24 24" fill="currentColor">
        <path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/>
    </svg>`,
    
    crystal: `<svg class="icon icon-crystal" viewBox="0 0 24 24" fill="currentColor">
        <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/>
        <path d="M12 2v5M12 12v5M2 7l10 5M12 7l10 5"/>
    </svg>`,
    
    ton: `<svg class="icon icon-ton" viewBox="0 0 24 24" fill="currentColor">
        <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
    </svg>`,
    
    coupon: `<svg class="icon icon-coupon" viewBox="0 0 24 24" fill="currentColor">
        <path d="M20 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 14H4v-6h16v6zm0-10H4V6h16v2z"/>
        <path d="M7 8h2v2H7zm0 4h2v2H7zm4-4h2v2h-2zm0 4h2v2h-2zm4-4h2v2h-2zm0 4h2v2h-2z"/>
    </svg>`,
    
    points: `<svg class="icon icon-points" viewBox="0 0 24 24" fill="currentColor">
        <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
    </svg>`,
    
    globe: `<svg class="icon icon-globe" viewBox="0 0 24 24" fill="currentColor">
        <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.94-.5-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z"/>
    </svg>`,
    
    arrowLeft: `<svg class="icon icon-arrow-left" viewBox="0 0 24 24" fill="currentColor">
        <path d="M15.41 7.41L14 6l-6 6 6 6 1.41-1.41L10.83 12z"/>
    </svg>`,
    
    arrowRight: `<svg class="icon icon-arrow-right" viewBox="0 0 24 24" fill="currentColor">
        <path d="M10 6L8.59 7.41 13.17 12l-4.58 4.59L10 18l6-6z"/>
    </svg>`,
    
    chevronUp: `<svg class="icon" viewBox="0 0 24 24" fill="currentColor">
        <path d="M7.41 15.41L12 10.83l4.59 4.58L18 14l-6-6-6 6z"/>
    </svg>`,
    
    star: `<svg class="icon icon-star" viewBox="0 0 24 24" fill="currentColor">
        <path d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"/>
    </svg>`,
    
    celebration: `<svg class="icon icon-celebration" viewBox="0 0 24 24" fill="currentColor">
        <path d="M5 8c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2zm7-3C10.9 5 10 5.9 10 7s.9 2 2 2 2-.9 2-2-.9-2-2-2zm7 0c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2zm-7 4c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2zm-7 1c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2zm14 0c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2zm-7 3c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2zm-7 1c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2zm14 0c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2z"/>
    </svg>`,
    
    dice: `<svg class="icon icon-dice" viewBox="0 0 24 24" fill="currentColor">
        <path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zM7.5 18C6.67 18 6 17.33 6 16.5S6.67 15 7.5 15 9 15.67 9 16.5 8.33 18 7.5 18zm0-9C6.67 9 6 8.33 6 7.5S6.67 6 7.5 6 9 6.67 9 7.5 8.33 9 7.5 9zm4.5 4.5c-.83 0-1.5-.67-1.5-1.5s.67-1.5 1.5-1.5 1.5.67 1.5 1.5-.67 1.5-1.5 1.5zm4.5 4.5c-.83 0-1.5-.67-1.5-1.5s.67-1.5 1.5-1.5 1.5.67 1.5 1.5-.67 1.5-1.5 1.5zm0-9c-.83 0-1.5-.67-1.5-1.5S15.67 6 16.5 6 18 6.67 18 7.5 17.33 9 16.5 9z"/>
    </svg>`,
    
    money: `<svg class="icon icon-money" viewBox="0 0 24 24" fill="currentColor">
        <path d="M11.8 10.9c-2.27-.59-3-1.2-3-2.15 0-1.09 1.01-1.85 2.7-1.85 1.78 0 2.44.85 2.5 2.1h2.21c-.07-1.72-1.12-3.3-3.21-3.81V3h-3v2.16c-1.94.42-3.5 1.68-3.5 3.61 0 2.31 1.91 3.46 4.7 4.13 2.5.6 3 1.48 3 2.41 0 .69-.49 1.79-2.7 1.79-2.06 0-2.87-.92-2.98-2.1h-2.2c.12 2.19 1.76 3.42 3.68 3.83V21h3v-2.15c1.95-.37 3.5-1.5 3.5-3.55 0-2.84-2.43-3.81-4.7-4.4z"/>
    </svg>`,
    
    sparkle: `<svg class="icon icon-sparkle" viewBox="0 0 24 24" fill="currentColor">
        <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
    </svg>`,
    
    percent: `<svg class="icon icon-percent" viewBox="0 0 24 24" fill="currentColor">
        <path d="M7.5 4C5.57 4 4 5.57 4 7.5S5.57 11 7.5 11 11 9.43 11 7.5 9.43 4 7.5 4zm0 5C6.67 9 6 8.33 6 7.5S6.67 6 7.5 6 9 6.67 9 7.5 8.33 9 7.5 9zm9 4c-1.93 0-3.5 1.57-3.5 3.5s1.57 3.5 3.5 3.5 3.5-1.57 3.5-3.5-1.57-3.5-3.5-3.5zm0 5c-.83 0-1.5-.67-1.5-1.5s.67-1.5 1.5-1.5 1.5.67 1.5 1.5-.67 1.5-1.5 1.5zM5.41 20L4 18.59 18.59 4 20 5.41 5.41 20z"/>
    </svg>`,
    
    users: `<svg class="icon icon-users" viewBox="0 0 24 24" fill="currentColor">
        <path d="M16 11c1.66 0 2.99-1.34 2.99-3S17.66 5 16 5c-1.66 0-3 1.34-3 3s1.34 3 3 3zm-8 0c1.66 0 2.99-1.34 2.99-3S9.66 5 8 5C6.34 5 5 6.34 5 8s1.34 3 3 3zm0 2c-2.33 0-7 1.17-7 3.5V19h14v-2.5c0-2.33-4.67-3.5-7-3.5zm8 0c-.29 0-.62.02-.97.05 1.16.84 1.97 1.97 1.97 3.45V19h6v-2.5c0-2.33-4.67-3.5-7-3.5z"/>
    </svg>`
};

// Function to render icon
function renderIcon(name) {
    return Icons[name] || '';
}

// Export to global scope
window.renderIcon = renderIcon;

// Function to replace emoji with icons in DOM
function replaceEmojisWithIcons() {
    // First, replace elements with data-icon attribute
    document.querySelectorAll('[data-icon]').forEach(el => {
        const iconName = el.getAttribute('data-icon');
        if (Icons[iconName] && !el.querySelector('svg')) {
            el.innerHTML = renderIcon(iconName);
        }
    });
    
    // Replace emojis in text content throughout the document
    const replacements = {
        '💎': 'diamond',
        '🦇': 'bat',
        '👑': 'crown',
        '🏠': 'home',
        '📦': 'inventory',
        '🎯': 'target',
        '✕': 'close',
        '✈️': 'airplane',
        '✓': 'check',
        '🌐': 'globe',
        '‹': 'arrowLeft',
        '›': 'arrowRight',
        '^': 'chevronUp',
        '▼': 'chevronDown',
        '⋯': 'menu',
        '⭐': 'star',
        '🎉': 'celebration',
        '🎲': 'dice',
        '💰': 'money',
        '🎫': 'coupon',
        '✨': 'sparkle'
    };
    
    // Walk through all text nodes and replace emojis
    function walkTextNodes(node) {
        if (node.nodeType === 3) { // Text node
            let text = node.textContent;
            let replaced = false;
            
            for (const [emoji, iconName] of Object.entries(replacements)) {
                if (text.includes(emoji)) {
                    const parent = node.parentNode;
                    if (parent && !parent.hasAttribute('data-icon')) {
                        const parts = text.split(emoji);
                        const fragment = document.createDocumentFragment();
                        
                        parts.forEach((part, index) => {
                            if (part) {
                                fragment.appendChild(document.createTextNode(part));
                            }
                            if (index < parts.length - 1) {
                                const iconSpan = document.createElement('span');
                                iconSpan.setAttribute('data-icon', iconName);
                                iconSpan.innerHTML = renderIcon(iconName);
                                fragment.appendChild(iconSpan);
                            }
                        });
                        
                        parent.replaceChild(fragment, node);
                        replaced = true;
                        break;
                    }
                }
            }
        } else if (node.nodeType === 1) { // Element node
            // Skip script and style tags
            if (node.tagName !== 'SCRIPT' && node.tagName !== 'STYLE') {
                // Check if element itself has emoji text
                if (node.childNodes.length === 1 && node.childNodes[0].nodeType === 3) {
                    const text = node.textContent.trim();
                    if (replacements[text] && !node.hasAttribute('data-icon') && !node.querySelector('svg')) {
                        node.setAttribute('data-icon', replacements[text]);
                        node.innerHTML = renderIcon(replacements[text]);
                    }
                } else {
                    // Recursively process children
                    Array.from(node.childNodes).forEach(walkTextNodes);
                }
            }
        }
    }
    
    // Process the entire document
    walkTextNodes(document.body);
    
    // Also handle specific icon containers
    document.querySelectorAll('.currency-icon, .nav-icon, .task-icon, .prize-icon, .item-icon, .activity-icon, .banner-icon, .crown-icon, .diamond-icon').forEach(el => {
        if (!el.hasAttribute('data-icon') && !el.querySelector('svg')) {
            const text = el.textContent.trim();
            if (replacements[text]) {
                el.setAttribute('data-icon', replacements[text]);
                el.innerHTML = renderIcon(replacements[text]);
            }
        }
    });
}

// Export to global scope
window.replaceEmojisWithIcons = replaceEmojisWithIcons;

// Initialize immediately and on DOM ready
function initIcons() {
    replaceEmojisWithIcons();
    // Run again after a short delay to catch any late-loading content
    setTimeout(replaceEmojisWithIcons, 100);
    setTimeout(replaceEmojisWithIcons, 500);
}

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initIcons);
} else {
    initIcons();
}

// Re-run when new content is added (for dynamically loaded content)
const observer = new MutationObserver((mutations) => {
    mutations.forEach((mutation) => {
        if (mutation.addedNodes.length) {
            mutation.addedNodes.forEach((node) => {
                if (node.nodeType === 1) { // Element node
                    // Check if node or its children have data-icon
                    if (node.hasAttribute && node.hasAttribute('data-icon')) {
                        const iconName = node.getAttribute('data-icon');
                        if (Icons[iconName]) {
                            node.innerHTML = renderIcon(iconName);
                        }
                    }
                    // Check children
                    const iconElements = node.querySelectorAll ? node.querySelectorAll('[data-icon]') : [];
                    iconElements.forEach(el => {
                        const iconName = el.getAttribute('data-icon');
                        if (Icons[iconName]) {
                            el.innerHTML = renderIcon(iconName);
                        }
                    });
                }
            });
        }
    });
});

// Start observing
observer.observe(document.body, {
    childList: true,
    subtree: true
});

