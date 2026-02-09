/**
 * Universal Line Graph Renderer
 * Renders line graphs with customizable colors, fills, and axes
 */

class LineGraphRenderer {
    constructor() {
        this.charts = {};
        this.defaultOptions = {
            lineColor: '#8b7355',
            backgroundColor: 'rgba(139, 115, 85, 0.1)',
            fillColor: 'rgba(139, 115, 85, 0.15)',
            pointColor: '#8b7355',
            pointSize: 5,
            lineWidth: 2,
            tension: 0.4
        };
    }

    /**
     * Render a universal line graph
     * @param {string} canvasId - Canvas element ID
     * @param {Array} data - Array of tuples [[x1, y1], [x2, y2], ...]
     * @param {string} unitX - Unit label for X axis
     * @param {string} unitY - Unit label for Y axis
     * @param {string} title - Graph title
     * @param {Object} options - Customization options
     * @param {Array} importantMoments - Array of important moments [{x: 'date', label: 'description', color: '#color'}, ...]
     */
    render(canvasId, data, unitX, unitY, title, options = {}, importantMoments = []) {
        const ctx = document.getElementById(canvasId);
        if (!ctx) {
            console.error(`Canvas element not found: ${canvasId}`);
            return null;
        }

        // Merge options with defaults
        const settings = { ...this.defaultOptions, ...options };

        // Destroy existing chart if it exists
        if (this.charts[canvasId]) {
            this.charts[canvasId].destroy();
        }

        // Parse data - handle both array of arrays and array of objects
        const dataPoints = new Map();

        data.forEach(point => {
            if (Array.isArray(point)) {
                dataPoints.set(String(point[0]), point[1]);
            } else if (typeof point === 'object' && 'x' in point && 'y' in point) {
                dataPoints.set(String(point.x), point.y);
            }
        });

        // Add important moments that don't have data with placeholder null
        importantMoments.forEach(moment => {
            const dateStr = String(moment.x);
            if (!dataPoints.has(dateStr)) {
                dataPoints.set(dateStr, null);
            }
        });

        // Sort all dates chronologically
        const sortedEntries = Array.from(dataPoints.entries()).sort((a, b) => {
            return new Date(a[0]) - new Date(b[0]);
        });

        const labels = sortedEntries.map(entry => entry[0]);
        const values = sortedEntries.map(entry => entry[1]);

        // Interpolate Y values for important moments that don't have data
        for (let i = 0; i < values.length; i++) {
            if (values[i] === null) {
                // Find previous and next non-null values
                let prevIndex = i - 1;
                let nextIndex = i + 1;
                
                while (prevIndex >= 0 && values[prevIndex] === null) prevIndex--;
                while (nextIndex < values.length && values[nextIndex] === null) nextIndex++;
                
                if (prevIndex >= 0 && nextIndex < values.length) {
                    // Linear interpolation
                    const prevDate = new Date(labels[prevIndex]);
                    const currDate = new Date(labels[i]);
                    const nextDate = new Date(labels[nextIndex]);
                    
                    const totalDiff = nextDate - prevDate;
                    const currDiff = currDate - prevDate;
                    const ratio = currDiff / totalDiff;
                    
                    values[i] = values[prevIndex] + (values[nextIndex] - values[prevIndex]) * ratio;
                } else if (prevIndex >= 0) {
                    // Use previous value if no next value
                    values[i] = values[prevIndex];
                } else if (nextIndex < values.length) {
                    // Use next value if no previous value
                    values[i] = values[nextIndex];
                }
            }
        }

        // Create point styles array for important moments
        const pointRadiusArray = [];
        const pointBackgroundColorArray = [];
        const pointBorderWidthArray = [];
        
        labels.forEach((label, index) => {
            const moment = importantMoments.find(m => String(m.x) === label);
            if (moment) {
                pointRadiusArray.push(settings.pointSize + 3);
                pointBackgroundColorArray.push(moment.color || '#f39c12');
                pointBorderWidthArray.push(3);
            } else {
                pointRadiusArray.push(settings.pointSize);
                pointBackgroundColorArray.push(settings.pointColor);
                pointBorderWidthArray.push(2);
            }
        });

        const chartData = {
            labels: labels,
            datasets: [{
                label: `${unitY}`,
                data: values,
                borderColor: settings.lineColor,
                backgroundColor: settings.fillColor,
                fill: true,
                borderWidth: settings.lineWidth,
                tension: settings.tension,
                pointRadius: pointRadiusArray,
                pointBackgroundColor: pointBackgroundColorArray,
                pointBorderColor: '#fff',
                pointBorderWidth: pointBorderWidthArray,
                pointHoverRadius: settings.pointSize + 4,
                spanGaps: true // Enable line interpolation across null values (important moments without data)
            }]
        };

        const chartOptions = {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false,
                    position: 'top',
                    labels: {
                        usePointStyle: true,
                        padding: 15,
                        font: {
                            size: 13,
                            family: "'Arial', sans-serif"
                        }
                    }
                },
                title: {
                    display: true,
                    text: title,
                    font: {
                        size: 15,
                        weight: 'bold'
                    },
                    padding: 10,
                    margin: 30
                },
                tooltip: {
                    mode: 'index',
                    intersect: false,
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    padding: 12,
                    titleFont: { size: 13 },
                    bodyFont: { size: 12 },
                    callbacks: {
                        label: function(context) {
                            return `${context.dataset.label}: ${context.parsed.y.toFixed(2)} ${unitY}`;
                        },
                        afterLabel: function(context) {
                            const label = context.label;
                            const moment = importantMoments.find(m => String(m.x) === label);
                            if (moment) {
                                return `⭐ ${moment.label}`;
                            }
                            return '';
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: false,
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)'
                    },
                    ticks: {
                        font: { size: 11 },
                        callback: function(value) {
                            return value + ' ' + unitY;
                        }
                    },
                    title: {
                        display: true,
                        text: unitY,
                        font: { size: 12, weight: 'bold' }
                    }
                },
                x: {
                    grid: {
                        display: false
                    },
                    ticks: {
                        font: { size: 11 }
                    },
                    title: {
                        display: true,
                        text: unitX,
                        font: { size: 12, weight: 'bold' }
                    }
                }
            }
        };

        this.charts[canvasId] = new Chart(ctx, {
            type: 'line',
            data: chartData,
            options: chartOptions
        });

        return this.charts[canvasId];
    }

    /**
     * Update chart data
     * @param {string} canvasId - Canvas element ID
     * @param {Array} data - New data array
     */
    updateData(canvasId, data) {
        if (!this.charts[canvasId]) {
            console.error(`Chart not found: ${canvasId}`);
            return;
        }

        const labels = [];
        const values = [];

        data.forEach(point => {
            if (Array.isArray(point)) {
                labels.push(String(point[0]));
                values.push(point[1]);
            } else if (typeof point === 'object' && 'x' in point && 'y' in point) {
                labels.push(String(point.x));
                values.push(point.y);
            }
        });

        this.charts[canvasId].data.labels = labels;
        this.charts[canvasId].data.datasets[0].data = values;
        this.charts[canvasId].update();
    }

    /**
     * Update chart options
     * @param {string} canvasId - Canvas element ID
     * @param {Object} options - New options
     */
    updateOptions(canvasId, options) {
        if (!this.charts[canvasId]) {
            console.error(`Chart not found: ${canvasId}`);
            return;
        }

        const dataset = this.charts[canvasId].data.datasets[0];
        if (options.lineColor) dataset.borderColor = options.lineColor;
        if (options.backgroundColor) dataset.backgroundColor = options.backgroundColor;
        if (options.fillColor) dataset.backgroundColor = options.fillColor;
        if (options.pointColor) dataset.pointBackgroundColor = options.pointColor;
        if (options.lineWidth) dataset.borderWidth = options.lineWidth;
        if (options.pointSize) {
            dataset.pointRadius = options.pointSize;
            dataset.pointHoverRadius = options.pointSize + 2;
        }

        this.charts[canvasId].update();
    }

    /**
     * Destroy a specific chart
     * @param {string} canvasId - Canvas element ID
     */
    destroy(canvasId) {
        if (this.charts[canvasId]) {
            this.charts[canvasId].destroy();
            delete this.charts[canvasId];
        }
    }

    /**
     * Destroy all charts
     */
    destroyAll() {
        Object.keys(this.charts).forEach(canvasId => {
            this.charts[canvasId].destroy();
        });
        this.charts = {};
    }
}

// Create global instance
window.lineGraphRenderer = new LineGraphRenderer();
