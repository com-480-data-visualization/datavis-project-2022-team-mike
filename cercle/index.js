max = (a, b) => a > b ? a : b;
min = (a, b) => a < b ? a : b;
abs = (a) => a < 0 ? -a : a;
const rad = 100;
const color_range = d3.scale.linear()
    .domain([-1, 0, 25, 50, 75, 100])
    .range(['black', 'red', 'orange', 'yellow', 'green', 'blue']);

const move_speed = .2;
const growth_speed = .2;
const normal_speed = .5;

const box_width = 450;
const box_height = 270;
var top_text = null;
var top_text_root = null;

function add_text(svg, dx, dy, text) {
    return svg.append("text")
        .attr("dx", dx)
        .attr("dy", dy)
        .attr("font-family", "impact")
        .attr("font-size", "20")
        .attr("fill", "white")
        .attr("stroke", "black")
        .attr("stroke-width", "1")
        .html(text)
}

function draw(json, svg_, value_, score_) {
    let width = window.innerWidth;
    let height = window.innerHeight - 75;

    let clear = function () { }

    let svg = svg_ == null ? d3.select("svg")
        .style("background-color", 'lightgray')
        : svg_;
    if (top_text == null) {
        top_text_root = svg;
        top_text = add_text(top_text_root, 20, 30, "")
    }
    let sum = 0;
    let i = 0;
    let n = json.children.length;
    while (i < n) {
        sum += value_(json.children[i]);
        i++;
    }

    json.nodes = d3.range(json.children.length).map(function (i) {
        const radius = Math.sqrt(value_(json.children[i]));
        const src = json.children[i].img.length > 0 ? json.children[i].img : "default.png";
        const name = json.children[i].Name
            .replaceAll(" ", "_")
            .replaceAll("(", "_")
            .replaceAll(")", "_")
            .replaceAll("[", "_")
            .replaceAll("]", "_")
            .replaceAll("/", "_")
            .replaceAll("\\", "_")
            .replaceAll("'", "_")
            .replaceAll(":", "_")
            .replaceAll(".", "");
        const color = json.children[i].img.length > 0 ? json.children[i].color : "rgb(84,84,84)";

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
            score: score_(json.children[i]),
            text: json.children[i].Name,
            name: name,
            image: src
        };
    });

    var force = d3.layout.force()
        .gravity(0.03)
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

    function onclick(d, i) {
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

            d3.select('#t_' + json.nodes[focus].name)
                .html(function (d, i) { return d.text; })

            let last_html = top_text.html();
            top_text.remove();
            top_text = add_text(top_text_root, 20, 30, last_html.substring(0, last_html.length - json.children[focus].Name.length - 1));

            focus = -1;
        }
        else {
            focus = i;
            d3.select('#g_' + json.nodes[focus].name)
                .selectAll("circle")
                .style("fill", function (d, i) { return d.color; });

            d3.select('#t_' + json.nodes[focus].name)
                .html("");

            let last_html = top_text.html();
            top_text.remove();
            top_text = add_text(top_text_root, 20, 30, last_html + "/" + json.children[focus].Name);
        }
    }

    const g = svg.selectAll("circle")
        .data(json.nodes.slice(0))
        .enter()
        .append("g")
        .attr("id", function (d, i) { return 'g_' + d.name; });

    g.append("circle")
        .attr("r", rad)
        .attr("cx", rad)
        .attr("cy", rad)
        .style("fill", function (d, i) { return d.color; })
        .attr("stroke", function (d, i) { return color_range(d.score); })
        .attr("stroke-width", "2")
        .on("click", onclick);

    g.append("circle")
        .attr("r", rad)
        .attr("cx", rad)
        .attr("cy", rad)
        .style("fill", function (d, i) { return 'url(#img_' + d.name + ')'; })
        .attr("stroke", function (d, i) { return color_range(d.score); })
        .attr("stroke-width", "2")
        .on("click", onclick);

    add_text(g, rad, rad * 2 / 5, function (d, i) { return d.text; })
        .attr("id", function (d, i) { return 't_' + d.name; })
        .attr("dominant-baseline", "middle")
        .attr("text-anchor", "middle")
        .on("click", onclick);


    let focus = -1;
    let play = true;

    function smooth_move(curent, target, speed, direction = 1) {
        return curent - speed * direction * (curent - target);
    }

    function show_radius(radius, width, height) {
        return max(radius * Math.sqrt((width * height) / (sum * 20)), 10);
    }

    let sub_svg = null

    force.on("tick", function (e) {
        width = smooth_move(width, window.innerWidth, move_speed);
        height = smooth_move(height, window.innerHeight - 75, move_speed);

        force.size([width, height]);

        if (svg_ == null)
            svg.attr("width", width)
                .attr("height", height);

        if (sub_svg != null) {
            sub_svg.style("transform", function (d, i) {
                let x = (width - 200) / box_width
                let y = (height - 200) / box_height
                let b = x < y
                return `translate(${b ? 100 : (width - box_width * y) / 2}px, ${b ? (height - box_height * x) / 2 : 100}px) scale(${b ? x : y})`
            })
        }

        if (play) {
            if (focus >= 0) {
                let dif = 0;
                let i = 0;
                let n = json.nodes.length;

                while (i < n) {
                    root = json.nodes[i];
                    if (focus == i) {
                        dif = abs(root.radius - max(width, height)) + abs(root.x - width / 2) + abs(root.y - height / 2);
                        root.x = smooth_move(root.x, width / 2, move_speed);
                        root.y = smooth_move(root.y, height / 2, move_speed);
                    }
                    else {
                        root.x = smooth_move(root.x, width / 2, move_speed, -1);
                        root.y = smooth_move(root.y, height / 2, move_speed, -1);
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
                        clear = draw(
                            json.children[focus],
                            svg.append("g").attr("id", 'gc_' + json.nodes[focus].name),
                            value_,
                            score_);
                    }
                    else {
                        let root = json.children[focus]
                        sub_svg = svg
                            .append("g")
                            .attr("id", 'gc_' + json.nodes[focus].name)
                            .on("tick", function (e) {

                            });

                        sub_svg.append("rect")
                            .attr("width", box_width)
                            .attr("height", box_height)
                            .attr("fill", "white")
                            .attr("stroke", "black")
                            .attr("stroke-width", "1");

                        add_text(sub_svg, 20, 40, root.Name);
                        add_text(sub_svg, 35, 70, `User_score : \t ${(root.User_score >= 0 ? root.User_score + "%" : "")}`);
                        add_text(sub_svg, 35, 100, `Meta_score : \t ${(root.Meta_score >= 0 ? root.Meta_score + "%" : "")}`);
                        add_text(sub_svg, 35, 130, `Global_Sales : \t ${(root.Global_Sales >= 0 ? root.Global_Sales + " millions" : "")}`);
                        add_text(sub_svg, 35, 160, `NA_Sales : \t ${(root.NA_Sales >= 0 ? root.NA_Sales + " millions" : "")}`);
                        add_text(sub_svg, 35, 190, `EU_Sales : \t ${(root.EU_Sales >= 0 ? root.EU_Sales + " millions" : "")}`);
                        add_text(sub_svg, 35, 220, `JP_Sales : \t ${(root.JP_Sales >= 0 ? root.JP_Sales + " millions" : "")}`);
                        add_text(sub_svg, 35, 250, `Other_Sales : \t ${(root.Meta_score >= 0 ? root.Other_Sales + " millions" : "")}`);
                        clear = function () {
                            sub_svg.remove();
                            sub_svg = null;
                        }
                    }
                }
            }

            let q = d3.geom.quadtree(json.nodes);
            let i = 0;
            let n = json.nodes.length;

            while (i < n) {
                root = json.nodes[i];
                if (focus == i)
                    root.radius = smooth_move(root.radius, max(width, height), growth_speed);
                else if (focus < 0)
                    root.radius = smooth_move(root.radius, root.true_radius, normal_speed);
                else
                    root.radius = smooth_move(root.radius, 0, normal_speed);
                ++i;
            }

            i = 0;
            while (i < n) {
                q.visit(collide(json.nodes[i], width, height));
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
                let cr = show_radius(d.radius, width, height)
                return "translate(" +
                    (d.x - cr) + "px, " +
                    (d.y - cr) + "px) scale(" +
                    (cr / rad) + ")"
            })
        }
    });


    svg.on("mousemove", function () {
        force.resume();
    });

    function collide(node, width, height) {
        var r = show_radius(node.radius, width, height) * 10,
            nx1 = node.x - r,
            nx2 = node.x + r,
            ny1 = node.y - r,
            ny2 = node.y + r;
        return function (quad, x1, y1, x2, y2) {
            if (quad.point && (quad.point !== node)) {
                var x = node.x - quad.point.x,
                    y = node.y - quad.point.y,
                    l = Math.sqrt(x * x + y * y),
                    r = show_radius(node.radius, width, height) + show_radius(quad.point.radius, width, height);
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


$.getJSON("../data/bubble.json", function (json) {
    draw(json, null, function (child) { return child.Global_Sales }, function (child) { return child.NB ? child.Meta_score / child.NB : child.Meta_score });
}
).fail(function () {
    console.log("error");
});