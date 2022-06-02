max = (a, b) => a > b ? a : b;
min = (a, b) => a < b ? a : b;
abs = (a) => a < 0 ? -a : a;
const rad = 100;
const plus = 250;


function draw(json, svg_) {
    let width = $(document).width() - 5;
    let height = $(document).height() - 75;

    let clear = function () { }

    let svg = svg_ == null ? d3.select("svg")
        .style("background-color", 'lightgray')
        : svg_;

    json.max = 0;
    let i = 0;
    let n = json.children.length;
    while (i < n) {
        json.max = Math.sqrt(max(json.max, json.children[i].value));
        i++;
    }

    json.nodes = d3.range(json.children.length).map(function (i) {
        const radius = Math.sqrt(json.children[i].value) / json.max * 100;
        const src = json.children[i].img;
        const name = json.children[i].name
            .replaceAll(" ", "_")
            .replaceAll("/", "_")
            .replaceAll("\\", "_")
            .replaceAll(".", "");
        const color = json.children[i].color;

        const img = new Image();
        const j = i;
        img.onload = function () {
            json.nodes[j].width = this.width;
            json.nodes[j].height = this.height;
        }
        img.src = src;

        return {
            width: -1,
            height: -1,
            color: color,
            radius: radius,
            true_radius: radius,
            name: name,
            image: src
        };
    });

    var force = d3.layout.force()
        .gravity(0.05)
        .charge(function (d, i) { return -1; })
        .nodes(json.nodes)
        .size([width, height]);

    force.start();

    svg.selectAll("circle")
        .data(json.nodes.slice(0))
        .enter()
        .append("pattern")
        .attr("id", function (d, i) { return 'img_' + d.name; })
        .attr("patternUnits", "userSpaceOnUse")
        .attr("width", function (d) { return 2 * rad; })
        .attr("height", function (d) { return 2 * rad; })
        .append("image")
        .attr("href", function (d, i) { return d.image; });

    const g = svg.selectAll("circle")
        .data(json.nodes.slice(0))
        .enter()
        .append("g")
        .attr("id", function (d, i) { return 'g_' + d.name; });

    g.append("circle")
        .attr("r", rad)
        .attr("cx", rad)
        .attr("cy", rad)
        .style("fill", function (d, i) { return d.color; });

    g.append("circle")
        .attr("r", rad)
        .attr("cx", rad)
        .attr("cy", rad)
        .style("fill", function (d, i) { return 'url(#img_' + d.name + ')'; })
        .on("click", function (d, i) {
            if (!play) {
                let i = 0;
                let n = json.nodes.length;
                while (i < n) {
                    json.nodes[i].fixed = false;
                    ++i;
                }
            }
            play = true;
            if (focus == i) {
                d3.select('#g_' + json.nodes[focus].name)
                    .selectAll("circle")
                    .style("fill", function (d, i) { return i ? 'url(#img_' + d.name + ')' : d.color; });
                clear();
                focus = -1;
            }
            else {
                focus = i;
                d3.select('#g_' + json.nodes[focus].name)
                    .selectAll("circle")
                    .style("fill", function (d, i) { return d.color; });
            }
        });

    let focus = -1;
    let play = true;

    let nb = 0
    force.on("tick", function (e) {
        if (play) {
            width = $(document).width() - 5;
            height = $(document).height() - 75;

            force.size([width, height]);

            if (svg_ == null)
                svg.attr("width", width)
                    .attr("height", height);

            if (focus >= 0) {
                let dif = 0;
                let i = 0;
                let n = json.nodes.length;

                while (i < n) {
                    root = json.nodes[i];
                    if (focus == i) {
                        dif = abs(root.radius - (min(width, height) + plus)) + abs(root.x - width / 2) + abs(root.y - height / 2);
                        root.x -= .2 * (root.x - width / 2);
                        root.y -= .2 * (root.y - height / 2);
                    }
                    else {
                        root.x += .2 * (root.x - width / 2);
                        root.y += .2 * (root.y - height / 2);
                    }
                    ++i;
                }
                if (dif < 10) {
                    let i = 0;
                    while (i < n) {
                        json.nodes[i].fixed = true;
                        ++i;
                    }
                    play = false;
                    if (json.children[focus].children) {
                        let sub_svg = svg
                            .append("g")
                            .attr("id", 'gc_' + json.nodes[focus].name);
                        clear = draw(json.children[focus], sub_svg);
                    }
                    else {
                        console.log("ICI")
                    }
                }
            }

            let q = d3.geom.quadtree(json.nodes);
            let i = 0;
            let n = json.nodes.length;

            while (i < n) {
                root = json.nodes[i];
                if (focus == i)
                    root.radius -= .2 * (root.radius - (min(width, height) + plus));
                else if (focus < 0)
                    root.radius -= .5 * (root.radius - root.true_radius);
                else
                    root.radius -= .01 * root.radius;
                ++i;
            }

            i = 0;
            while (i < n) {
                q.visit(collide(json.nodes[i]));
                ++i;
            }

            if (focus < 0) {
                i = 0;
                while (i < n) {
                    json.nodes[i].x = max(json.nodes[i].radius, min(json.nodes[i].x, width - json.nodes[i].radius));
                    json.nodes[i].y = max(json.nodes[i].radius, min(json.nodes[i].y, height - json.nodes[i].radius));
                    ++i;
                }
            }

            svg.selectAll("image")
                .attr("x", function (d) { return d.width < d.height ? ((2 * rad) - d.width) / 2 : 0; })
                .attr("y", function (d) { return d.width > d.height ? ((2 * rad) - d.height) / 2 : 0; });

            g.style("transform", function (d, i) {
                return "translate(" +
                    (d.x - d.radius) + "px, " +
                    (d.y - d.radius) + "px) scale(" +
                    (d.radius / rad) + ")"
            })
        }
    });


    svg.on("mousemove", function () {
        force.resume();
    });

    function collide(node) {
        var r = node.radius * 1.2,
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
                    l = (l - r) / l * .2;
                    node.x -= x *= l;
                    node.y -= y *= l;
                    quad.point.x += x;
                    quad.point.y += y;
                }
            }
            return x1 > nx2 || x2 < nx1 || y1 > ny2 || y2 < ny1;
        };
    }
    return function () {
        svg.remove();
        force.stop();
    }
}


$.getJSON("example.json", function (json) {
    draw(json, null);
}
).fail(function () {
    console.log("error");
});