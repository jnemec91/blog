
async function renderGraphs() {
    // Load data from JSON file
    const response = await fetch('/static/blog/js/medicalData.json');
    const medicalData = await response.json();
    
    // Initialize carousel
    const carousel = new GraphCarousel('#medicalGraphCarousel');

    /* =========================
    HEMATOLOGIE – GRAFY
    ========================= */

    // Add all graphs from JSON configuration
    medicalData.graphs.forEach(graphConfig => {
        carousel.addGraph({
            canvas: graphConfig.canvas,
            data: medicalData.hematology[graphConfig.dataKey],
            unitX: graphConfig.unitX,
            unitY: graphConfig.unitY,
            title: graphConfig.title,
            options: graphConfig.options,
            importantMoments: medicalData.importantMoments,
        });
    });

    // Render initial graph
    const initialGraph = carousel.getCurrentGraph();
    lineGraphRenderer.render(
        initialGraph.canvas,
        initialGraph.data,
        initialGraph.unitX,
        initialGraph.unitY,
        initialGraph.title,
        initialGraph.options,
        initialGraph.importantMoments
    );

    // Listen for carousel changes and render appropriate graph
    document.getElementById('medicalGraphCarousel').addEventListener('carouselGraphChanged', function(event) {
        const { graph } = event.detail;
        setTimeout(() => {
            lineGraphRenderer.render(
                graph.canvas,
                graph.data,
                graph.unitX,
                graph.unitY,
                graph.title,
                graph.options,
                graph.importantMoments
            );
        }, 100);
    });    
}
