$.getJSON("./example.json", function (json) {
    var width = 960,
        height = 500;

    console.log(json)
    
    var nodes = d3.range(200).map(function () { return {
            radius: Math.random() * 12 + 4,
            image: 'url("https://static.wikia.nocookie.net/logopedia/images/c/c6/Wii_Sports_Resort.jpg")'
        }; }),
        color = d3.scale.category10();

    var force = d3.layout.force()
        .gravity(0.05)
        .charge(function (d, i) { return -10; })
        .nodes(nodes)
        .size([width, height]);

    force.start();

    var svg = d3.select("svg")
        .attr("width", width)
        .attr("height", height);

    svg.selectAll("circle")
        .data(nodes.slice(1))
        .enter().append("circle")
        .attr("r", function (d) { return d.radius; })
        //.style("fill", function (d, i) { return color(i % 3); });
        .style("fill", function (d, i) { return 'url("#img1")'; });

    force.on("tick", function (e) {
        var q = d3.geom.quadtree(nodes),
            i = 0,
            n = nodes.length;

        while (++i < n) q.visit(collide(nodes[i]));

        svg.selectAll("circle")
            .attr("cx", function (d) { return d.x; })
            .attr("cy", function (d) { return d.y; });
    });

    function collide(node) {
        var r = node.radius + 16,
            nx1 = node.x - r,
            nx2 = node.x + r,
            ny1 = node.y - r,
            ny2 = node.y + r;
        return function (quad, x1, y1, x2, y2) {
            if (quad.point && (quad.point !== node)) {
                var x = node.x - quad.point.x,
                    y = node.y - quad.point.y,
                    l = Math.sqrt(x * x + y * y),
                    r = node.radius + quad.point.radius;
                if (l < r) {
                    l = (l - r) / l * .5;
                    node.x -= x *= l;
                    node.y -= y *= l;
                    quad.point.x += x;
                    quad.point.y += y;
                }
            }
            return x1 > nx2 || x2 < nx1 || y1 > ny2 || y2 < ny1;
        };
    }

}).fail(function () {
    console.log("error");
});