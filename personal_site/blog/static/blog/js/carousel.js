/**
 * Graph Carousel Component
 * Manages navigation between multiple graphs
 */

class GraphCarousel {
    constructor(containerSelector = '.graph-carousel') {
        this.containerSelector = containerSelector;
        this.currentIndex = 0;
        this.graphs = [];
        this.init();
    }

    init() {
        const container = document.querySelector(this.containerSelector);
        if (!container) {
            console.warn(`Carousel container not found: ${this.containerSelector}`);
            return;
        }

        this.container = container;
        this.createCarouselStructure();
        this.attachEventListeners();
    }

    createCarouselStructure() {
        this.container.innerHTML = '';

        const wrapper = document.createElement('div');
        wrapper.className = 'carousel-wrapper';

        const graphContainer = document.createElement('div');
        graphContainer.className = 'carousel-graphs';
        graphContainer.id = 'carouselGraphs';

        const navPrev = document.createElement('button');
        navPrev.className = 'carousel-nav carousel-nav-prev';
        navPrev.innerHTML = '&laquo;';

        const navNext = document.createElement('button');
        navNext.className = 'carousel-nav carousel-nav-next';
        navNext.innerHTML = '&raquo;';

        const indicators = document.createElement('div');
        indicators.className = 'carousel-indicators';

        wrapper.appendChild(navPrev);
        wrapper.appendChild(graphContainer);
        wrapper.appendChild(navNext);

        this.container.appendChild(wrapper);
        this.container.appendChild(indicators);

        this.graphContainer = graphContainer;
        this.navPrev = navPrev;
        this.navNext = navNext;
        this.indicators = indicators;
    }

    attachEventListeners() {
        this.navPrev.addEventListener('click', () => this.previousGraph());
        this.navNext.addEventListener('click', () => this.nextGraph());
    }

    /**
     * Add a graph to the carousel
     * @param {Object} graphConfig - Configuration object with canvas, data, units, title, and options
     */
    addGraph(graphConfig) {
        this.graphs.push(graphConfig);
        this.renderGraphs();
        this.updateIndicators();
    }

    renderGraphs() {
        this.graphContainer.innerHTML = '';
        
        this.graphs.forEach((graphConfig, index) => {
            const slide = document.createElement('div');
            slide.className = 'carousel-slide';
            if (index === this.currentIndex) {
                slide.classList.add('active');
            }

            const graphWrapper = document.createElement('div');
            graphWrapper.className = 'graph-slide-content';

            const canvasWrapper = document.createElement('div');
            canvasWrapper.className = 'graph-canvas-wrapper';

            let canvas;
            if (typeof graphConfig.canvas === 'string') {
                canvas = document.createElement('canvas');
                canvas.id = graphConfig.canvas;
            } else {
                canvas = graphConfig.canvas;
            }

            canvasWrapper.appendChild(canvas);
            graphWrapper.appendChild(canvasWrapper);
            slide.appendChild(graphWrapper);
            this.graphContainer.appendChild(slide);
        });
    }

    updateIndicators() {
        this.indicators.innerHTML = '';
        
        this.graphs.forEach((_, index) => {
            const dot = document.createElement('button');
            dot.className = 'carousel-indicator-dot';
            if (index === this.currentIndex) {
                dot.classList.add('active');
            }
            dot.addEventListener('click', () => this.goToGraph(index));
            this.indicators.appendChild(dot);
        });
    }

    nextGraph() {
        if (this.graphs.length === 0) return;
        this.currentIndex = (this.currentIndex + 1) % this.graphs.length;
        this.updateCarousel();
    }

    previousGraph() {
        if (this.graphs.length === 0) return;
        this.currentIndex = (this.currentIndex - 1 + this.graphs.length) % this.graphs.length;
        this.updateCarousel();
    }

    goToGraph(index) {
        if (index >= 0 && index < this.graphs.length) {
            this.currentIndex = index;
            this.updateCarousel();
        }
    }

    updateCarousel() {
        const slides = this.graphContainer.querySelectorAll('.carousel-slide');
        const dots = this.indicators.querySelectorAll('.carousel-indicator-dot');

        slides.forEach((slide, index) => {
            slide.classList.remove('active');
            if (index === this.currentIndex) {
                slide.classList.add('active');
            }
        });

        dots.forEach((dot, index) => {
            dot.classList.remove('active');
            if (index === this.currentIndex) {
                dot.classList.add('active');
            }
        });

        this.dispatchChangeEvent();
    }

    dispatchChangeEvent() {
        const event = new CustomEvent('carouselGraphChanged', {
            detail: { 
                index: this.currentIndex, 
                graph: this.graphs[this.currentIndex] 
            }
        });
        this.container.dispatchEvent(event);
    }

    getCurrentGraph() {
        return this.graphs[this.currentIndex];
    }

    getCurrentIndex() {
        return this.currentIndex;
    }
}

window.GraphCarousel = GraphCarousel;
