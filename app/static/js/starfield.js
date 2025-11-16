// Starfield animation
(function() {
    const canvas = document.getElementById('starfield');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    const stars = [];
    const numStars = 200;
    
    function resizeCanvas() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    }
    
    function initStars() {
        stars.length = 0;
        for (let i = 0; i < numStars; i++) {
            stars.push({
                x: Math.random() * canvas.width,
                y: Math.random() * canvas.height,
                radius: Math.random() * 1.5,
                opacity: Math.random(),
                speed: Math.random() * 0.5 + 0.1
            });
        }
    }
    
    function animate() {
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
            ctx.fillStyle = `rgba(255, 255, 200, ${star.opacity})`;
            ctx.fill();
        });
        
        requestAnimationFrame(animate);
    }
    
    resizeCanvas();
    initStars();
    animate();
    
    window.addEventListener('resize', () => {
        resizeCanvas();
        initStars();
    });
})();

