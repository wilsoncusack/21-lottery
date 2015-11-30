
var margin = {top: 50, right: 20, bottom: 30, left: 200},
width = 1000 - margin.left - margin.right,
height = 500 - margin.top - margin.bottom;

// data = {{ data }}
// tempData = []
// for(i = 0; i < data.length; i++) {
//     tempData[i] = {}
//     tempData[i].iteration = data[i][0]
//     if (data[i][1] == -1){
//         tempData[i].winning_bid_number = "secret"
//     }
//     else{
//         tempData[i].winning_bid_number = data[i][1]
//     }

//     tempData[i].potSize = (Math.floor((data[i][2]/100000000) * 10000)/10000)
// }
// data = tempData 

data = [];
 iterations = 20;
 data[0] = {"iteration": 0, "potSize": .0001}; //.0001
 for (i = 1; i <= iterations; i++) {
     randomNumber = (Math.floor(Math.random()*(10*Math.pow(2, i))) + 1)
     acc = randomNumber;
     data[i] = {}
     data[i].potSize = data[i - 1].potSize/2 + (.00001 * randomNumber)
     //data[i].potSize = data[i].potSize/100000000
     data[i].iteration = i;
     data[i].randomNumber = randomNumber;
 }             

//Set the ranges
var x = d3.scale.linear()
    .domain([0, d3.max(data)])
    .range([0, width]);
var y = d3.scale.linear().range([height, 0]);

// Define the axes
var xAxis = d3.svg.axis().scale(x)
    .orient("bottom").ticks(data.length - 1);

var yAxis = d3.svg.axis().scale(y)
    .orient("left").ticks(5);

// Define the line
var valueline = d3.svg.line()
    .x(function(d) { return x(d.iteration); })
    .y(function(d) { return y(d.potSize); });

var tip = d3.tip()
    .attr('class', 'd3-tip')
    .offset([-10, 0])
    .html(function(d) {
    return "<strong>Pot size:</strong> <span style='color:red'>" + Math.floor((d.potSize) * 10000)/10000 + " bitcoins, " +" iteration: " + d.iteration + ", winning bid number: " + d.winning_bid_number + ", max: " + (10  * Math.pow(2, d.iteration)) + "</span>";
    })
    
// Adds the svg canvas
var svg = d3.select("#svg1")
    .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
    .append("g")
        .attr("transform", 
              "translate(" + margin.left + "," + margin.top + ")");

var svg2 = d3.select("#svg2")
    .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
    .append("g")
        .attr("transform", 
              "translate(" + margin.left + "," + margin.top + ")");

svg.call(tip);
svg2.call(tip);

// Scale the range of the data
x.domain(d3.extent(data, function(d) { return d.iteration; }));
y.domain([0, d3.max(data, function(d) { return d.potSize; })]);

// Add the valueline path.
svg.append("path")
    .attr("class", "line")
    .attr("d", valueline(data));


// Add the X Axis
svg.append("g")
    .attr("class", "x axis")
    .attr("transform", "translate(0," + height + ")")
    .call(xAxis);

svg.append("text")      // text label for the x axis
    .attr("x", 400 )
    .attr("y", 450 )
    .attr("class", "label")
    .style("text-anchor", "middle")
    .text("Iteration");

svg.append("text")      // text label for the y axis
    .attr("x", -100 )
    .attr("y", 250 )
    .attr("class", "label")
    .style("text-anchor", "middle")
    .text("Bitcoins");

// Add the Y Axis
svg.append("g")
    .attr("class", "y axis")
    .call(yAxis);


var circle = svg.selectAll("circle")
    .data(data);

var circleEnter = circle.enter()
    .append("circle")
    .on('mouseover', tip.show)
    .on('mouseout', tip.hide);

circleEnter.attr("cy", function(d,i){
    return y(d.potSize)
});
circleEnter.attr("cx", function(d, i) {
    return x(d.iteration); 
});
circleEnter.attr("r", function(d) { return 4; });
circleEnter.attr('style', 'fill: grey')


// Add the valueline path.
svg2.append("path")
    .attr("class", "line")
    .attr("d", valueline(data));


// Add the X Axis
svg2.append("g")
    .attr("class", "x axis")
    .attr("transform", "translate(0," + height + ")")
    .call(xAxis);

svg2.append("text")      // text label for the x axis
    .attr("x", 400 )
    .attr("y", 450 )
    .attr("class", "label")
    .style("text-anchor", "middle")
    .text("Iteration");

svg2.append("text")      // text label for the y axis
    .attr("x", -100 )
    .attr("y", 250 )
    .attr("class", "label")
    .style("text-anchor", "middle")
    .text("Bitcoins");

// Add the Y Axis
svg2.append("g")
    .attr("class", "y axis")
    .call(yAxis);


var circle = svg2.selectAll("circle")
    .data(data);

var circleEnter = circle.enter()
    .append("circle")
    .on('mouseover', tip.show)
    .on('mouseout', tip.hide);

circleEnter.attr("cy", function(d,i){
    return y(d.potSize)
});
circleEnter.attr("cx", function(d, i) {
    return x(d.iteration); 
});
circleEnter.attr("r", function(d) { return 4; });
circleEnter.attr('style', 'fill: grey')