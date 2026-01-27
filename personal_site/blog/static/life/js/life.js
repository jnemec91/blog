
class Cell {
    constructor(isAlive = false) {
        this.isAlive = isAlive;
        this.neighbors = [];
        this.willBeAlive = false;
        this.cursorHover = false;
    }

    toggle() {
        this.isAlive = !this.isAlive;
    }

    getNeighbors(x, y, grid) {
        this.neighbors = [];
        const directions = [
            [-1, -1], [-1, 0], [-1, 1],
            [0, -1],           [0, 1],
            [1, -1],  [1, 0],  [1, 1],
        ];

        directions.forEach(([dx, dy]) => {
            let newX = x + dx;
            let newY = y + dy;
            
            if (newX >= 0 && newY >= 0 && newX < grid.length && newY < grid[0].length) {
                this.neighbors.push(grid[newX][newY]);
            } else {
                if (newX >= grid.length) newX = newX % grid.length;
                if (newY >= grid[0].length) newY = newY % grid[0].length;
                if (newX < 0) newX = grid.length + newX;
                if (newY < 0) newY = grid[0].length + newY;
                this.neighbors.push(grid[newX][newY]);
            }
        });
    }

    computeNextState() {
        const aliveNeighbors = this.neighbors.filter(neighbor => neighbor.isAlive).length;
        if (this.isAlive) {
            this.willBeAlive = aliveNeighbors === 2 || aliveNeighbors === 3;
        } else {
            this.willBeAlive = aliveNeighbors === 3;
        }
    }
    
    update() {
        this.isAlive = this.willBeAlive;
    }
}

// State
const GameOfLifeManager = {
    state: null,
    eventListeners: [],
    animationId: null,

    init() {
        this.cleanup();
        
        const canvas = document.getElementById('life-canvas');
        if (!canvas) return;

        const rect = canvas.getBoundingClientRect();
        canvas.width = rect.width;
        canvas.height = rect.height;

        const desiredCellSize = 10;
        const cols = Math.floor(canvas.width / desiredCellSize);
        const rows = Math.floor(canvas.height / desiredCellSize);
        
        const cellSize = Math.min(
            canvas.width / cols,
            canvas.height / rows
        );

        this.state = {
            gameOfLifeArray: [],
            isRunning: false,
            lifeCanvas: canvas,
            cellSize: cellSize,
            lastCellClicked: null,
            isMouseDown: false,
            framesSinceStep: 0,
        };

        this.setupGrid();
        this.attachEventListeners();
        this.startRenderLoop();
    },

    setupGrid() {
        if (!this.state || !this.state.lifeCanvas) return;

        const rows = Math.floor(this.state.lifeCanvas.height / this.state.cellSize);
        const cols = Math.floor(this.state.lifeCanvas.width / this.state.cellSize);

        for (let i = 0; i < rows; i++) {
            const row = [];
            for (let j = 0; j < cols; j++) {
                row.push(new Cell(false));
            }
            this.state.gameOfLifeArray.push(row);
        }
    },

    attachEventListeners() {
        if (!this.state) return;

        const canvas = this.state.lifeCanvas;
        const startStopBtn = document.getElementById('life-startStop');

        const handleCanvasMouseMove = (event) => this.handleCanvasMouseMove(event);
        canvas.addEventListener('mousemove', handleCanvasMouseMove);
        this.eventListeners.push({ element: canvas, event: 'mousemove', handler: handleCanvasMouseMove });

        const handleCanvasClick = (event) => this.toggleCellAtEvent(event);
        canvas.addEventListener('click', handleCanvasClick);
        this.eventListeners.push({ element: canvas, event: 'click', handler: handleCanvasClick });

        const handleCanvasMouseDown = () => {
            this.state.isMouseDown = true;
        };
        canvas.addEventListener('mousedown', handleCanvasMouseDown);
        this.eventListeners.push({ element: canvas, event: 'mousedown', handler: handleCanvasMouseDown });

        const handleCanvasMouseDrag = (event) => {
            if (this.state.isMouseDown) {
                this.toggleCellAtEvent(event);
            }
        };
        canvas.addEventListener('mousemove', handleCanvasMouseDrag);
        this.eventListeners.push({ element: canvas, event: 'mousemove', handler: handleCanvasMouseDrag });

        const handleCanvasMouseUp = () => {
            this.state.isMouseDown = false;
            this.state.lastCellClicked = null;
        };
        canvas.addEventListener('mouseup', handleCanvasMouseUp);
        this.eventListeners.push({ element: canvas, event: 'mouseup', handler: handleCanvasMouseUp });

        const handleCanvasMouseLeave = () => {
            this.state.isMouseDown = false;
            this.state.lastCellClicked = null;
        };
        canvas.addEventListener('mouseleave', handleCanvasMouseLeave);
        this.eventListeners.push({ element: canvas, event: 'mouseleave', handler: handleCanvasMouseLeave });

        if (startStopBtn) {
            const handleToggle = () => this.toggleGameOfLife();
            startStopBtn.addEventListener('click', handleToggle);
            this.eventListeners.push({ element: startStopBtn, event: 'click', handler: handleToggle });
        }

        const stepBtn = document.getElementById('life-step');
        if (stepBtn) {
            const handleStep = () => this.gameOfLifeStep();
            stepBtn.addEventListener('click', handleStep);
            this.eventListeners.push({ element: stepBtn, event: 'click', handler: handleStep });
        }

        const resetBtn = document.getElementById('life-reset');
        if (resetBtn) {
            const handleReset = () => this.reset();
            resetBtn.addEventListener('click', handleReset);
            this.eventListeners.push({ element: resetBtn, event: 'click', handler: handleReset });
        }

        const togglerBtn = document.getElementById('life-buttons-toggler');
        if (togglerBtn) {
            const handleToggleButtons = () => window.toggleLifeButtons();
            togglerBtn.addEventListener('click', handleToggleButtons);
            this.eventListeners.push({ element: togglerBtn, event: 'click', handler: handleToggleButtons });
        }

        // touch controls
        canvas.addEventListener('touchstart', (e) => {
            this.state.isMouseDown = true;
            this.toggleCellAtEvent(e.touches[0]);
            e.preventDefault();
        });

        canvas.addEventListener('touchmove', (e) => {
            if (this.state.isMouseDown) {
                this.toggleCellAtEvent(e.touches[0]);
            }
            e.preventDefault();
        });

        canvas.addEventListener('touchend', (e) => {
            this.state.isMouseDown = false;
            this.state.lastCellClicked = null;
            e.preventDefault();
        });

    },

    handleCanvasMouseMove(event) {
        if (!this.state) return;

        const rect = this.state.lifeCanvas.getBoundingClientRect();
        const x = (event.clientX - rect.left) * (this.state.lifeCanvas.width / rect.width);
        const y = (event.clientY - rect.top) * (this.state.lifeCanvas.height / rect.height);
        const cellSize = this.state.cellSize;

        const row = Math.floor(y / cellSize);
        const col = Math.floor(x / cellSize);

        for (let c = 0; c < this.state.gameOfLifeArray.length; c++) {
            for (let r = 0; r < this.state.gameOfLifeArray[c].length; r++) {
                this.state.gameOfLifeArray[c][r].cursorHover = false;
            }
        }

        if (row >= 0 && row < this.state.gameOfLifeArray.length &&
            col >= 0 && col < this.state.gameOfLifeArray[row].length) {
            this.state.gameOfLifeArray[row][col].cursorHover = true;
            this.state.lifeCanvas.style.cursor = 'pointer';
        } else {
            this.state.lifeCanvas.style.cursor = 'default';
        }

        if (!this.state.isRunning) {
            this.draw();
        }
    },

    toggleCellAtEvent(event) {
        if (!this.state) return;

        const rect = this.state.lifeCanvas.getBoundingClientRect();
        const x = (event.clientX - rect.left) * (this.state.lifeCanvas.width / rect.width);
        const y = (event.clientY - rect.top) * (this.state.lifeCanvas.height / rect.height);
        const cellSize = this.state.cellSize;
        const row = Math.floor(y / cellSize);
        const col = Math.floor(x / cellSize);

        if (row >= 0 && row < this.state.gameOfLifeArray.length &&
            col >= 0 && col < this.state.gameOfLifeArray[row].length) {
            
            // prevent toggling the same cell multiple times
            if (this.state.lastCellClicked &&
                this.state.lastCellClicked.row === row &&
                this.state.lastCellClicked.col === col) {
                return;
            }

            this.state.gameOfLifeArray[row][col].toggle();
            this.state.lastCellClicked = { row, col };
        }

        this.draw();
    },

    draw() {
        if (!this.state) return;

        const canvas = this.state.lifeCanvas;
        const ctx = canvas.getContext('2d');
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // draw cells
        for (let c = 0; c < this.state.gameOfLifeArray.length; c++) {
            for (let r = 0; r < this.state.gameOfLifeArray[c].length; r++) {
                const cell = this.state.gameOfLifeArray[c][r];
                const x = r * this.state.cellSize;
                const y = c * this.state.cellSize;
                
                if (cell.isAlive) {
                    ctx.fillStyle = 'rgba(0, 180, 0, 0.2)';
                    ctx.fillRect(x, y, this.state.cellSize, this.state.cellSize);
                    ctx.fillStyle = 'rgba(0, 255, 0, 0.8)';
                    ctx.fillRect(x, y, this.state.cellSize, this.state.cellSize);
                }

                if (cell.cursorHover) {
                    ctx.fillStyle = 'rgba(255, 255, 255, 0.5)';
                    ctx.fillRect(x, y, this.state.cellSize, this.state.cellSize);
                }

                ctx.strokeStyle = '#111111';
                ctx.strokeRect(x, y, this.state.cellSize, this.state.cellSize);
            }
        }
    },

    startRenderLoop() {
        const render = () => {
            this.draw();

            if (this.state && this.state.isRunning) {
                this.state.framesSinceStep += 1;
                if (this.state.framesSinceStep >= this.getFramesPerStep()) {
                    this.gameOfLifeStep();
                    this.state.framesSinceStep = 0;
                }
            }

            this.animationId = window.requestAnimationFrame(render);
        };

        if (!this.animationId) {
            this.animationId = window.requestAnimationFrame(render);
        }
    },

    getFramesPerStep() {
        const speedControl = document.getElementById('life-gameSpeed');
        if (speedControl) {
            let speed = parseInt(speedControl.value, 10);
            speed = 31 - speed;
            if (speed < 1) speed = 1;
            return speed;
        }
    },

    gameOfLifeStep() {
        if (!this.state) return;

        const grid = this.state.gameOfLifeArray;

        // clculate next state
        for (let c = 0; c < grid.length; c++) {
            for (let r = 0; r < grid[c].length; r++) {
                grid[c][r].getNeighbors(c, r, grid);
                grid[c][r].computeNextState();
            }
        }

        // update grid
        for (let c = 0; c < grid.length; c++) {
            for (let r = 0; r < grid[c].length; r++) {
                grid[c][r].update();
            }
        }

    },

    toggleGameOfLife() {
        if (!this.state) return;

        this.state.isRunning = !this.state.isRunning;
        const startStopBtn = document.getElementById('life-startStop');

        if (this.state.isRunning) {
            if (startStopBtn) startStopBtn.innerText = 'Stop';
            this.state.framesSinceStep = 0;
        } else {
            if (startStopBtn) startStopBtn.innerText = 'Start';
        }
    },

    reset() {
        this.cleanup();
        this.init();
    },

    cleanup() {
        if (this.animationId) {
            window.cancelAnimationFrame(this.animationId);
            this.animationId = null;
        }

        // remove event listeners
        this.eventListeners.forEach(({ element, event, handler }) => {
            element.removeEventListener(event, handler);
        });
        this.eventListeners = [];

        this.state = null;

        let startStopBtn = document.getElementById('life-startStop');
        if (startStopBtn) startStopBtn.innerText = 'Start';
    },
};
