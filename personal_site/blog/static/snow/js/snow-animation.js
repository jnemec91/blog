// storing state in global window object ensures to persist HTMX swaps
if (!window.snowState) {
    window.snowState = {
        snowflakeShapes: [],
        animationRunning: false,
        animationFrameId: null,
        lastFrameTime: Date.now(),
        lastSpawnTime: 0,
        snowflakes: [],
        spawnInterval: 1000 / 100,
        gravity: 0.01,
        wind: 0,
        size: 10,
        rotationSpeed: 0,
        MAX_SNOWFLAKES: 200
    };
}

if (typeof window.toggleNewSnowModal === 'undefined') {
    window.toggleNewSnowModal = () => {
        const backdrop = document.querySelector('.snow-backdrop');
        const modal = document.getElementById('snow-newSnowflakeModal');
        if (backdrop && modal) {
            backdrop.classList.toggle('snow-backdrop-active');
            modal.classList.toggle('snow-modal-active');
        }
    };

    window.toggleSnowButtons = () => {
        const buttons = document.getElementById('snow-buttons');
        const toggler = document.getElementById('snow-buttons-toggler');
        if (buttons) {
            buttons.classList.toggle('snow-buttons-hidden');
        }
        if (toggler && buttons.classList.contains('snow-buttons-hidden')) {
            toggler.innerHTML = 'Ovládací prvky';
        } else if (toggler) {
            toggler.innerHTML = '&#10006;';
        }
    };
}

// always show menu when resizing to large screens
window.addEventListener('resize', () => {
    const buttons = document.getElementById('snow-buttons');
    if (window.innerWidth > 768 && buttons && buttons.classList.contains('snow-buttons-hidden')) {
        buttons.classList.remove('snow-buttons-hidden');
        const toggler = document.getElementById('snow-buttons-toggler');
        if (toggler) {
            toggler.innerHTML = '&#10006;';
        }
    }
});

document.addEventListener('htmx:beforeRequest', function(evt) {
    resetSnowflakes();
});



function resetSnowflakes() {
    // delete existing snowflakes and reset parameters
    window.snowState.snowflakes = [];
    window.snowState.snowflakeShapes = [];
    if (window.snowState.snowflakePool) {
        for (let flake of window.snowState.snowflakePool) {
            flake.active = false;
        }
    }

    window.snowState.gravity = 0.01;
    window.snowState.wind = 0;
    window.snowState.size = 10;
    window.snowState.rotationSpeed = 0;

    const randomSnowflakesCheckbox = document.getElementById('snow-randomSnowflakes');
    if (randomSnowflakesCheckbox) {
        randomSnowflakesCheckbox.checked = false;
    }
}

function drawSnowflake(ctx, centerX, centerY, size, fuzzyness, spanning, spanAngle, branches, rotation = 0, isPreview = false) {
    // draws a snowflake on given context
    const newSnowflakeCanvas = document.getElementById('snow-newSnowflakeCanvas');
    
    if (isPreview && newSnowflakeCanvas) {
        ctx.clearRect(0, 0, newSnowflakeCanvas.width, newSnowflakeCanvas.height);
    } else {
        ctx.lineWidth = 0.5;
    }
    
    ctx.strokeStyle = 'white';
    
    // rotation
    if (rotation !== 0) {
        ctx.save();
        ctx.translate(centerX, centerY);
        ctx.rotate(rotation);
        centerX = 0;
        centerY = 0;
    }
    
    ctx.beginPath();

    for (let i = 0; i < branches; i++) {
        const angle = (i / branches) * Math.PI * 2;
        const cos = Math.cos(angle);
        const sin = Math.sin(angle);

        // main branch
        const mainEndX = centerX + sin * size;
        const mainEndY = centerY - cos * size;
        
        ctx.moveTo(centerX, centerY);
        ctx.lineTo(mainEndX, mainEndY);

        // left and right side branches
        const offsetMultiplier = fuzzyness / 10 * size;
        const sideBranchAngle = (spanAngle * Math.PI / 180);
        const branchCos = Math.cos(sideBranchAngle);
        const branchSin = Math.sin(sideBranchAngle);

        for (let j = 1; j <= spanning; j++) {
            const branchLength = (size / spanning) * j;
            
            // branch starting point
            const branchStartX = centerX + sin * branchLength;
            const branchStartY = centerY - cos * branchLength;
            
            // branch offset
            const offsetX = offsetMultiplier * branchSin;
            const offsetY = offsetMultiplier * branchCos;

            // right branch
            const rightEndX = branchStartX + (cos * offsetX + sin * offsetY);
            const rightEndY = branchStartY + (sin * offsetX - cos * offsetY);
            ctx.moveTo(branchStartX, branchStartY);
            ctx.lineTo(rightEndX, rightEndY);

            // left branch
            const leftEndX = branchStartX - (cos * offsetX - sin * offsetY);
            const leftEndY = branchStartY - (sin * offsetX + cos * offsetY);
            ctx.moveTo(branchStartX, branchStartY);
            ctx.lineTo(leftEndX, leftEndY);
        }
    }
    
    // draw
    ctx.stroke();
    
    // restore context if rotation was applied
    if (rotation !== 0) {
        ctx.restore();
    }
}

function initializeSnowAnimation() {
    // stop previous animation if running
    if (window.snowState.animationFrameId) {
        cancelAnimationFrame(window.snowState.animationFrameId);
    }

    const newSnowflakeCanvas = document.getElementById('snow-newSnowflakeCanvas');
    const newSnowflakeCtx = newSnowflakeCanvas ? newSnowflakeCanvas.getContext('2d') : null;
    const snowCanvas = document.getElementById('snow-snowCanvas');
    const snowCtx = snowCanvas ? snowCanvas.getContext('2d') : null;

    if (!snowCanvas || !snowCtx) return;

    function updateSnowflakePreview() {
        const fuzzySlider = document.getElementById('snow-fuzzyness');
        const spanSlider = document.getElementById('snow-spanning');
        const branchSlider = document.getElementById('snow-branches');
        const angleSlider = document.getElementById('snow-spanAngle');
        const previewSlider = document.getElementById('snow-previewSize');
        
        if (!fuzzySlider || !spanSlider || !branchSlider || !angleSlider || !previewSlider || !newSnowflakeCtx || !newSnowflakeCanvas) return;
        
        const fuzzyness = parseInt(fuzzySlider.value);
        const spanning = parseInt(spanSlider.value);
        const branches = parseInt(branchSlider.value || 6);
        const spanAngle = parseInt(angleSlider.value);
        const previewSize = parseInt(previewSlider.value);
        
        drawSnowflake(newSnowflakeCtx, newSnowflakeCanvas.width / (2 * devicePixelRatio), newSnowflakeCanvas.height / (2 * devicePixelRatio), previewSize, fuzzyness, spanning, spanAngle, branches, 0, true);
    }

    // rmove old event listeners by cloning preview sliders
    ['snow-fuzzyness', 'snow-spanning', 'snow-branches', 'snow-spanAngle', 'snow-previewSize'].forEach(id => {
        const slider = document.getElementById(id);
        if (slider) slider.replaceWith(slider.cloneNode(true));
    });

    // add event listeners to preview sliders
    ['snow-fuzzyness', 'snow-spanning', 'snow-branches', 'snow-spanAngle', 'snow-previewSize'].forEach(id => {
        const slider = document.getElementById(id);
        if (slider) slider.addEventListener('input', updateSnowflakePreview);
    });

    updateSnowflakePreview();

    function addSnowflakeShape() {
        // query current slider elements to get updated references
        const config = {
            fuzzyness: document.getElementById('snow-fuzzyness'),
            spanning: document.getElementById('snow-spanning'),
            branches: document.getElementById('snow-branches'),
            spanAngle: document.getElementById('snow-spanAngle')
        };
        
        if (!Object.values(config).every(el => el)) return;
        
        const shape = {
            fuzzyness: parseInt(config.fuzzyness.value),
            spanning: parseInt(config.spanning.value),
            branches: parseInt(config.branches.value),
            spanAngle: parseInt(config.spanAngle.value)
        };

        // check if shape already exists
        const exists = window.snowState.snowflakeShapes.some(s =>
            s.fuzzyness === shape.fuzzyness &&
            s.spanning === shape.spanning &&
            s.branches === shape.branches &&
            s.spanAngle === shape.spanAngle
        );

        if (!exists) {
            window.snowState.snowflakeShapes.push(shape);
            console.log('Přidána nová vločka:', shape);
        }
    }

    const addShapeButton = document.getElementById('snow-addShape');
    if (addShapeButton) {
        addShapeButton.onclick = () => {
            addSnowflakeShape();
            window.toggleNewSnowModal();
        };
    }

    function resizeNewSnowflakeCanvas() {
        if (!newSnowflakeCanvas || !newSnowflakeCtx) return;
        newSnowflakeCanvas.width = newSnowflakeCanvas.clientWidth * devicePixelRatio;
        newSnowflakeCanvas.height = newSnowflakeCanvas.clientHeight * devicePixelRatio;
        newSnowflakeCtx.scale(devicePixelRatio, devicePixelRatio);
        updateSnowflakePreview();
    }

    window.addEventListener('resize', resizeNewSnowflakeCanvas);
    resizeNewSnowflakeCanvas();

    // initialize snowflake pool if not already done
    if (window.snowState.snowflakePool === undefined) {
        window.snowState.snowflakePool = [];
        for (let i = 0; i < window.snowState.MAX_SNOWFLAKES; i++) {
            window.snowState.snowflakePool.push({
                x: 0, y: 0, size: 0, fuzzyness: 0, spanning: 0, 
                branches: 0, spanAngle: 0, speedY: 0, speedX: 0, 
                rotation: 0, rotationSpeed: 0, active: false
            });
        }
    }

    function resizeSnowCanvas() {
        snowCanvas.width = window.innerWidth * devicePixelRatio;
        snowCanvas.height = window.innerHeight * devicePixelRatio;
        snowCtx.scale(devicePixelRatio, devicePixelRatio);
    }

    window.addEventListener('resize', resizeSnowCanvas);
    resizeSnowCanvas();

    function spawnSnowflake() {
        if (window.snowState.snowflakeShapes.length === 0 || window.snowState.snowflakes.length >= window.snowState.MAX_SNOWFLAKES) return;
        
        let flake = window.snowState.snowflakePool.find(f => !f.active);
        if (!flake) return;
        
        let shape = window.snowState.snowflakeShapes[Math.floor(Math.random() * window.snowState.snowflakeShapes.length)];

        flake.x = Math.random() * window.innerWidth;
        flake.y = -100;
        flake.size = Math.random() * window.snowState.size;
        flake.fuzzyness = shape.fuzzyness;
        flake.spanning = shape.spanning;
        flake.branches = shape.branches;
        flake.spanAngle = shape.spanAngle;
        flake.speedY = 1 + Math.random() * 2;
        flake.speedX = (Math.random() - 0.5) * 0.5;
        flake.rotation = Math.random() * Math.PI * 2;
        flake.rotationSpeed = (Math.random() - 0.5) * window.snowState.rotationSpeed / 100;
        flake.active = true;
        
        window.snowState.snowflakes.push(flake);
    }

    function generateRandomSnowflakeShape() {
        return {
            fuzzyness: Math.floor(1 + Math.random() * 10),
            spanning: Math.floor(1 + Math.random() * 20),
            branches: Math.floor(6 + Math.random() * 4),
            spanAngle: Math.floor(1 + Math.random() * 360)
        };
    }

    function updateSnowflakes(deltaTime) {
        snowCtx.clearRect(0, 0, snowCanvas.width / devicePixelRatio, snowCanvas.height / devicePixelRatio);

        let currentTime = Date.now();
        if (currentTime - window.snowState.lastSpawnTime > window.snowState.spawnInterval) {
            const randomCheckbox = document.getElementById('snow-randomSnowflakes');
            if (randomCheckbox && randomCheckbox.checked) {
                let randomShape = generateRandomSnowflakeShape();
                window.snowState.snowflakeShapes.push(randomShape);
            }
            spawnSnowflake();
            window.snowState.lastSpawnTime = currentTime;
        }

        for (let i = window.snowState.snowflakes.length - 1; i >= 0; i--) {
            let flake = window.snowState.snowflakes[i];
            
            flake.y += flake.speedY + window.snowState.gravity * deltaTime;
            flake.x += flake.speedX + window.snowState.wind * deltaTime;
            flake.rotation += flake.rotationSpeed * deltaTime;

            if (flake.y > window.innerHeight + 50) {
                flake.active = false;
                window.snowState.snowflakes.splice(i, 1);
            } else {
                if (flake.x < -50) {
                    flake.x = window.innerWidth + 50;
                } else if (flake.x > window.innerWidth + 50) {
                    flake.x = -50;
                }
                
                drawSnowflake(snowCtx, flake.x, flake.y, flake.size, flake.fuzzyness, flake.spanning, flake.spanAngle, flake.branches, flake.rotation);
            }
        }
    }

    const TARGET_FPS = 60;
    const FRAME_INTERVAL = 1000 / TARGET_FPS;
    
    function animate() {
        let currentFrameTime = Date.now();
        let deltaTime = currentFrameTime - window.snowState.lastFrameTime;
        
        if (deltaTime >= FRAME_INTERVAL) {
            updateSnowflakes(deltaTime);
            window.snowState.lastFrameTime = currentFrameTime - (deltaTime % FRAME_INTERVAL);
        }
        
        window.snowState.animationFrameId = requestAnimationFrame(animate);
    }

    animate();

    // setup animation control sliders
    const sliderConfig = [
        { id: 'snow-spawnCount', callback: (val) => { window.snowState.spawnInterval = 1000 / parseInt(val); } },
        { id: 'snow-gravity', callback: (val) => { window.snowState.gravity = parseInt(val) / 100; } },
        { id: 'snow-wind', callback: (val) => { window.snowState.wind = parseInt(val) / 100; } },
        { id: 'snow-snowflakeSize', callback: (val) => { window.snowState.size = parseInt(val); } },
        { id: 'snow-rotationSpeed', callback: (val) => { window.snowState.rotationSpeed = parseInt(val); } }
    ];

    sliderConfig.forEach(({ id, callback }) => {
        const slider = document.getElementById(id);
        if (slider) slider.addEventListener('input', (e) => callback(e.target.value));
    });

    window.snowState.animationRunning = true;
}

// initialize on load
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeSnowAnimation);
} else {
    initializeSnowAnimation();
}