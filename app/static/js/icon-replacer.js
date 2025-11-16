// Aggressive emoji replacement - runs continuously to catch all emojis
(function() {
    'use strict';
    
    const emojiMap = {
        '💎': {icon: 'diamond', selector: '.currency-icon, .diamond-icon'},
        '🦇': {icon: 'bat', selector: '.currency-icon'},
        '👑': {icon: 'crown', selector: '.nav-icon, .crown-icon'},
        '🏠': {icon: 'home', selector: '.nav-icon'},
        '📦': {icon: 'inventory', selector: '.nav-icon'},
        '🎯': {icon: 'target', selector: '.nav-icon'},
        '✕': {icon: 'close', selector: '.btn-close, .btn-close-small'},
        '✈️': {icon: 'airplane', selector: '.task-icon'},
        '✓': {icon: 'check', selector: '.btn-check'},
        '🌐': {icon: 'globe', selector: '.lang-selector'},
        '⭐': {icon: 'star', selector: '.prize-icon, .rank-scores'},
        '🎉': {icon: 'celebration', selector: '.activity-icon'},
        '🎲': {icon: 'dice', selector: '.activity-icon'},
        '💰': {icon: 'money', selector: '.prize-icon, .item-icon'},
        '🎫': {icon: 'coupon', selector: '.prize-icon, .item-icon'},
        '✨': {icon: 'sparkle', selector: '.banner-icon'},
        '▼': {icon: 'chevronDown', selector: '.icon-btn'},
        '^': {icon: 'chevronUp', selector: '.chevron'},
        '⋯': {icon: 'menu', selector: '.icon-btn'},
        '‹': {icon: 'arrowLeft', selector: '.nav-arrow-left'},
        '›': {icon: 'arrowRight', selector: '.nav-arrow-right'}
    };
    
    function replaceAllEmojis() {
        if (typeof renderIcon !== 'function') {
            return; // Icons.js not loaded yet
        }
        
        // Replace in all elements
        Object.entries(emojiMap).forEach(([emoji, config]) => {
            const elements = document.querySelectorAll(config.selector);
            elements.forEach(el => {
                if (el.textContent.includes(emoji) && !el.querySelector('svg')) {
                    if (!el.hasAttribute('data-icon')) {
                        el.setAttribute('data-icon', config.icon);
                    }
                    if (typeof replaceEmojisWithIcons === 'function') {
                        // Use the main replacement function
                        const iconName = el.getAttribute('data-icon');
                        if (iconName && typeof renderIcon === 'function') {
                            el.innerHTML = renderIcon(iconName);
                        }
                    }
                }
            });
        });
        
        // Also replace any standalone emoji text nodes
        const walker = document.createTreeWalker(
            document.body,
            NodeFilter.SHOW_TEXT,
            null,
            false
        );
        
        let node;
        const textNodes = [];
        while (node = walker.nextNode()) {
            if (node.textContent.trim()) {
                textNodes.push(node);
            }
        }
        
        textNodes.forEach(textNode => {
            const text = textNode.textContent;
            for (const [emoji, config] of Object.entries(emojiMap)) {
                if (text.includes(emoji)) {
                    const parent = textNode.parentNode;
                    if (parent && parent.tagName !== 'SCRIPT' && parent.tagName !== 'STYLE') {
                        const parts = text.split(emoji);
                        const fragment = document.createDocumentFragment();
                        
                        parts.forEach((part, index) => {
                            if (part) {
                                fragment.appendChild(document.createTextNode(part));
                            }
                            if (index < parts.length - 1) {
                                const span = document.createElement('span');
                                span.setAttribute('data-icon', config.icon);
                                if (typeof renderIcon === 'function') {
                                    span.innerHTML = renderIcon(config.icon);
                                }
                                fragment.appendChild(span);
                            }
                        });
                        
                        parent.replaceChild(fragment, textNode);
                        break;
                    }
                }
            }
        });
    }
    
    // Run immediately and on various events
    function runReplacement() {
        if (document.body) {
            replaceAllEmojis();
        }
    }
    
    // Run on multiple events to catch all cases
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', runReplacement);
    } else {
        runReplacement();
    }
    
    window.addEventListener('load', runReplacement);
    
    // Also run periodically to catch dynamically added content
    setInterval(runReplacement, 1000);
    
    // Observe DOM changes
    if (window.MutationObserver) {
        const observer = new MutationObserver(() => {
            setTimeout(runReplacement, 50);
        });
        
        observer.observe(document.body, {
            childList: true,
            subtree: true,
            characterData: true
        });
    }
    
    // Export function for manual calls
    window.replaceAllEmojis = replaceAllEmojis;
})();

