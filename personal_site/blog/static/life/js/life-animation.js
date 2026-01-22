
window.toggleLifeButtons = () => {
    const buttons = document.getElementById('life-buttons');
    const toggler = document.getElementById('life-buttons-toggler');
    if (buttons) {
        buttons.classList.toggle('life-buttons-hidden');
    }
    if (toggler) {
        if (buttons && buttons.classList.contains('life-buttons-hidden')) {
            toggler.innerHTML = 'Ovládací prvky';
        } else {
            toggler.innerHTML = '&#10006;';
        }
    }
};

// Handle HTMX page swaps
document.addEventListener('htmx:afterSwap', () => {
    // Check if we're on the life page
    const canvas = document.getElementById('life-canvas');
    if (canvas) {
        GameOfLifeManager.init();
    } else {
        GameOfLifeManager.cleanup();
    }
});

// Handle HTMX before request
document.addEventListener('htmx:beforeRequest', () => {
    GameOfLifeManager.cleanup();
});

// Initialize on first load
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', GameOfLifeManager.init);
} else {
   GameOfLifeManager.init();;
}