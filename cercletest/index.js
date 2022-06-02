$.getJSON( "./example.json", function(data) {
    const svg = d3.select('svg');
    const width = +svg.attr('width');
    const height = +svg.attr('height');

    var circles = [];
    data.forEach(e => console.log( e ))

    const circle = svg.append('circle')
        .attr('r', 200)
        .attr('cx', width / 2)
        .attr('cy', height / 2);
    
}).fail(function() {
    console.log( "error" );
});






