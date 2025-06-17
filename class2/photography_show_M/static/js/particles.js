function initParticleEffect(canvas, images) {
    const ctx = canvas.getContext('2d');
    let currentIndex = 0;

    function resize() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    }

    function loadImage(index) {
        const img = new Image();
        img.onload = function() {
            // 粒子化处理逻辑
            const particles = [];
            const particleCount = 2000;

            // 这里添加具体的粒子效果实现
            // ...

            function animate() {
                // 粒子动画逻辑
                // ...
                requestAnimationFrame(animate);
            }
            animate();
        };
        img.src = images[index];
    }

    window.nextImage = function() {
        currentIndex = (currentIndex + 1) % images.length;
        loadImage(currentIndex);
    };

    window.prevImage = function() {
        currentIndex = (currentIndex - 1 + images.length) % images.length;
        loadImage(currentIndex);
    };

    window.addEventListener('resize', resize);
    resize();
    loadImage(0);
}