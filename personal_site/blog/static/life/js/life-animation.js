
if (typeof window.toggleLifeButtons === 'undefined') {
    window.toggleLifeButtons = () => {
        const buttons = document.getElementById('life-buttons');
        const toggler = document.getElementById('life-buttons-toggler');
        if (buttons) {
            buttons.classList.toggle('life-buttons-hidden');
        }
        if (toggler && buttons.classList.contains('life-buttons-hidden')) {
            toggler.innerHTML = 'Ovládací prvky';
        } else if (toggler) {
            toggler.innerHTML = '&#10006;';
        }
    };
}

function resetGameOfLife() {
    if (window.gameOfLifeState && window.gameOfLifeState.intervalId) {
        clearInterval(window.gameOfLifeState.intervalId);
    }
    window.gameOfLifeState = null;
    initializeGameOfLife();
    drawGameOfLife();
    document.getElementById('life-startStop').innerText = 'Start';
}

function initializeGameOfLife() {
    window.gameOfLifeState = null;
    
    if (!window.gameOfLifeState) {    
        window.gameOfLifeState = {
            gameOfLifeArray: [],
            isRunning: false,
            lifeCanvas: document.getElementById('life-canvas'),
            cellSize: Math.floor(Math.min(window.innerWidth, window.innerHeight) / 180),
            lastCellClicked: null,
            intervalId: null,
        };

        
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
                    // newX >= 0 && newX < grid.length && newY >= 0 && newY < grid[0].length
                    if (newX >= 0 && newY >= 0 && newX < grid.length && newY < grid[0].length) {
                        this.neighbors.push(grid[newX][newY]);
                    } else {
                        if (newX >= grid.length) {
                            newX = newX % grid.length;
                        }
                        if (newY >= grid[0].length) {
                            newY = newY % grid[0].length;
                        }
                        if (newX < 0) {
                            newX = grid.length + newX;
                        }
                        if (newY < 0) {
                            newY = grid[0].length + newY;
                        }
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

        if (window.gameOfLifeState) {
        const rows = Math.floor(window.gameOfLifeState.lifeCanvas.height) / window.gameOfLifeState.cellSize;
        const cols = Math.floor(window.gameOfLifeState.lifeCanvas.width) / window.gameOfLifeState.cellSize;


        for (let i = 0; i < rows; i++) {
            const row = [];
            for (let j = 0; j < cols; j++) {
                row.push(new Cell(false));
            }
            window.gameOfLifeState.gameOfLifeArray.push(row);
        }

        }
    }
    drawGameOfLife();
}

initializeGameOfLife();


function drawGameOfLife() {
    const state = window.gameOfLifeState;
    const canvas = state.lifeCanvas;
    const ctx = canvas.getContext('2d');
    const speed = document.getElementById('life-gameSpeed').value;

    if (state.intervalId) {
        clearInterval(state.intervalId);
        state.intervalId = setInterval(gameOfLifeStep, 1000 - speed);
    }
    
    
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Draw cells
    for (let c = 0; c < state.gameOfLifeArray.length; c++) {
        for (let r = 0; r < state.gameOfLifeArray[c].length; r++) {
            const cell = state.gameOfLifeArray[c][r];
            const x = r * state.cellSize;
            const y = c * state.cellSize;
            
            if (cell.isAlive) {
                ctx.fillStyle = 'rgba(0, 180, 0, 0.2)';
                ctx.fillRect(x, y, state.cellSize, state.cellSize);
                ctx.fillStyle = 'rgba(0, 255, 0, 0.8)';
                ctx.fillRect(x, y, state.cellSize, state.cellSize);
            }

            if (cell.cursorHover) {
                ctx.fillStyle = 'rgba(255, 255, 255, 0.5)';
                ctx.fillRect(x, y, state.cellSize, state.cellSize);
            }
            ctx.strokeStyle = '#111111';
            ctx.strokeRect(x, y, state.cellSize, state.cellSize);
        }
    }
}

window.gameOfLifeState.lifeCanvas.addEventListener('mousemove', (event) => {
    const rect = window.gameOfLifeState.lifeCanvas.getBoundingClientRect();
    const x = (event.clientX - rect.left) * (window.gameOfLifeState.lifeCanvas.width / rect.width);
    const y = (event.clientY - rect.top) * (window.gameOfLifeState.lifeCanvas.height / rect.height);
    const cellSize = window.gameOfLifeState.cellSize;

    // calculate cell indices
    const row = Math.floor(y / cellSize);
    const col = Math.floor(x / cellSize);

    // draw cell hover effect
    
    // reset previous hover states
    for (let c = 0; c < window.gameOfLifeState.gameOfLifeArray.length; c++) {
        for (let r = 0; r < window.gameOfLifeState.gameOfLifeArray[c].length; r++) {
            window.gameOfLifeState.gameOfLifeArray[c][r].cursorHover = false;
        }
    }
    if (row >= 0 && row < window.gameOfLifeState.gameOfLifeArray.length &&
        col >= 0 && col < window.gameOfLifeState.gameOfLifeArray[row].length) {
        window.gameOfLifeState.gameOfLifeArray[row][col].cursorHover = true;
        window.gameOfLifeState.lifeCanvas.style.cursor = 'pointer';
    }

    if (!window.gameOfLifeState.isRunning) {
        drawGameOfLife();
    }

});

// Track mouse state for drag functionality
window.gameOfLifeState.isMouseDown = false;

window.gameOfLifeState.lifeCanvas.addEventListener('click', (event) => {
    toggleCellAtEvent(event);
});

window.gameOfLifeState.lifeCanvas.addEventListener('mousedown', (event) => {
    window.gameOfLifeState.isMouseDown = true;
});

window.gameOfLifeState.lifeCanvas.addEventListener('mousemove', (event) => {
    if (window.gameOfLifeState.isMouseDown) {
        toggleCellAtEvent(event);
    }
});

window.gameOfLifeState.lifeCanvas.addEventListener('mouseup', () => {
    window.gameOfLifeState.isMouseDown = false;
    window.gameOfLifeState.lastCellClicked = null;
});

window.gameOfLifeState.lifeCanvas.addEventListener('mouseleave', () => {
    window.gameOfLifeState.isMouseDown = false;
    window.gameOfLifeState.lastCellClicked = null;
});

function toggleCellAtEvent(event) {
    const rect = window.gameOfLifeState.lifeCanvas.getBoundingClientRect();
    const x = (event.clientX - rect.left) * (window.gameOfLifeState.lifeCanvas.width / rect.width);
    const y = (event.clientY - rect.top) * (window.gameOfLifeState.lifeCanvas.height / rect.height);
    const cellSize = window.gameOfLifeState.cellSize;
    const row = Math.floor(y / cellSize);
    const col = Math.floor(x / cellSize);


    if (row >= 0 && row < window.gameOfLifeState.gameOfLifeArray.length &&
        col >= 0 && col < window.gameOfLifeState.gameOfLifeArray[row].length) {
        if (window.gameOfLifeState.lastCellClicked &&
            window.gameOfLifeState.lastCellClicked.row === row &&
            window.gameOfLifeState.lastCellClicked.col === col) {
            return; // prevent toggling the same cell multiple times during drag
        }
        window.gameOfLifeState.gameOfLifeArray[row][col].toggle();
        window.gameOfLifeState.lastCellClicked = {row, col};
    }

    drawGameOfLife();
}


function gameOfLifeStep() {
    const state = window.gameOfLifeState;
    const grid = state.gameOfLifeArray;

    for (let c=0; c < grid.length; c++) {
        for (let r=0; r < grid[c].length; r++) {
            grid[c][r].getNeighbors(c, r, grid);
            grid[c][r].computeNextState();
        }
    }

    for (let c=0; c < grid.length; c++) {
        for (let r=0; r < grid[c].length; r++) {
            grid[c][r].update();
        }
    }
    drawGameOfLife();
}

function toggleGameOfLife() {
    const state = window.gameOfLifeState;

    state.isRunning = !state.isRunning;
    if (state.isRunning) {
        state.intervalId = setInterval(gameOfLifeStep, 430);
        document.getElementById('life-startStop').innerText = 'Stop';
    } else {
        clearInterval(state.intervalId);
        document.getElementById('life-startStop').innerText = 'Start';
        state.intervalId = null;
        state.isRunning = false;
    }
}

document.getElementById('life-startStop').addEventListener('click', toggleGameOfLife);

// initialize on load
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeGameOfLife);
} else {
    initializeGameOfLife();
}

// reset on htmx request
document.addEventListener('htmx:beforeRequest', function(evt) {
    clearInterval(window.gameOfLifeState.intervalId);
    resetGameOfLife();
});