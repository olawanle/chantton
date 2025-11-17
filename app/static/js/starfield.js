// Starfield animation
(function() {
    function initStarfield() {
        const canvas = document.getElementById('starfield');
        if (!canvas) {
            // Retry after a short delay if canvas doesn't exist yet
            setTimeout(initStarfield, 100);
            return;
        }
        
        const ctx = canvas.getContext('2d');
        if (!ctx) {
            console.warn('Could not get 2d context for starfield');
            return;
        }
        
        const stars = [];
        const numStars = 300; // More stars for better effect
        
        function resizeCanvas() {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        }
        
        function initStars() {
            stars.length = 0;
            const width = canvas.width || window.innerWidth;
            const height = canvas.height || window.innerHeight;
            for (let i = 0; i < numStars; i++) {
                stars.push({
                    x: Math.random() * width,
                    y: Math.random() * height,
                    radius: Math.random() * 1.5,
                    opacity: Math.random(),
                    speed: Math.random() * 0.5 + 0.1
                });
            }
        }
        
        function animate() {
            try {
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                
                stars.forEach(star => {
                    star.opacity += star.speed * 0.01;
                    if (star.opacity > 1) {
                        star.opacity = 0;
                        star.x = Math.random() * canvas.width;
                        star.y = Math.random() * canvas.height;
                    }
                    
                    ctx.beginPath();
                    ctx.arc(star.x, star.y, star.radius, 0, Math.PI * 2);
                    // Use golden/yellow-orange colors like in the design
                    const intensity = star.opacity * 0.8;
                    const green = Math.floor(200 + Math.sin(star.opacity * Math.PI) * 55);
                    const blue = Math.floor(100 + Math.sin(star.opacity * Math.PI) * 50);
                    ctx.fillStyle = `rgba(255, ${green}, ${blue}, ${intensity})`;
                    ctx.fill();
                });
                
                requestAnimationFrame(animate);
            } catch (error) {
                console.error('Error in starfield animation:', error);
            }
        }
        
        resizeCanvas();
        initStars();
        animate();
        
        window.addEventListener('resize', () => {
            resizeCanvas();
            initStars();
        });
    }
    
    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initStarfield);
    } else {
        initStarfield();
    }
})();

