// var margin = {top: 0, right: 0, bottom: 73, left: 0},
//     width = 400 - margin.left - margin.right,
//     height = 315;

// var formatPercent = d3.format(".0%");

// var x = d3.scale.ordinal()
//     .rangeRoundBands([0, width], .1);

// var y = d3.scale.linear()
//     .range([height, 0]);

// var xAxis = d3.svg.axis()
//     .scale(x)
//     .orient("bottom");

// var yAxis = d3.svg.axis()
//     .scale(y)
//     .orient("left");

// var tip = d3.tip()
//   .attr('class', 'd3-tip')
//   .offset([-10, 0])
//   .html(function(d) {
//     return "<strong>No of Sites </strong> <span style='color:red'>" + d.frequency + "</span>";
//   })

// var svg = d3.select("#progress-bar").append("svg")
//     .attr("width", width + margin.left + margin.right)
//     .attr("height", height + margin.top + margin.bottom)
//   .append("g")
//     .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

// svg.call(tip);


// x.domain(dict_bar_data.map(function(d) { return d.letter; }));
// y.domain([0, d3.max(dict_bar_data, function(d) { return d.frequency; })]);

// svg.append("g")
//     .attr("class", "x axis")
//     .attr("transform", "translate(0," + height + ")")
//     .call(xAxis)
//     .append("text")
//     .attr("y", 15)
//     .attr("x",465)
//     .attr("dy", ".71em")
//     .style("text-anchor", "end")
//     .text("Progress %");


// svg.append("g")
//     .attr("class", "y axis")
//     .call(yAxis)
//   .append("text")
//     .attr("transform", "rotate(-90)")
//     .attr("y", -20)
//     .attr("dy", ".71em")
//     .style("text-anchor", "end")
//     .text("Sites");

// svg.selectAll(".bar")
//     .data(dict_bar_data)
//   .enter().append("rect")
//     .attr("class", "bar")
//     .attr("x", function(d) { return x(d.letter); })
//     .attr("width", x.rangeBand())
//     .attr("y", function(d) { return y(d.frequency); })
//     .attr("height", function(d) { return height - y(d.frequency); })
//     .on('mouseover', tip.show)
//     .on('mouseout', tip.hide)

// function type(d) {
//   d.frequency = +d.frequency;
//   return d;
// }


$( document ).ready(function() {
// Chart.defaults.global.defaultFontColor = '#FFF';
bar_height_max = Math.max.apply(Math, progress_data) || 10;
bar_height_max = Math.ceil(bar_height_max / 10) * 10;

var ctx = document.getElementById("myBar");
var myChart = new Chart(ctx, {
    type: 'bar',
    data: {
        // labels: chartdata.labels,
        // datasets: dataset
        labels: progress_labels,
        datasets: [{
            label: 'No of Sites',
            data: progress_data,
            backgroundColor: 'rgba(41,128,185,0.5)',
            borderColor: 'rgba(0,99,132,0.2)',
            borderWidth: 1
        }]
    },
    options: {
        scales: {
    yAxes: [
                    {
                        id: 'y-axis-1',
                        display: true,
                        position: 'left',
                        ticks: {
                            callback: function(value, index, values) {
                                return value;
                            },
                             min: 0,
                    sepSize: 1,
                    max: bar_height_max
                        },
                        scaleLabel:{
                            display: true,
                            labelString: 'No of Sites',
                            backgroundColor: 'rgba(0,0,0,0.2)',
                            fontColor: "#000"
                        }
                    }   
                ],
    xAxes: [
                    {
                        id: 'x-axis-1',
                        display: true,
                        position: 'bottom',
                        ticks: {
                            callback: function(value, index, values) {
                                return value;
                            }
                        },
                        scaleLabel:{
                            display: true,
                            labelString: 'Progress Percentage',
                            backgroundColor: 'rgba(255,255,255,0.2)',
                            fontColor: "#000"
                        }
                    }   
                ]
  },
        title: {
            display: false,
            text: 'Custom Chart Title'
        },
        legend: {
            display: false,
        },
        tooltips: {
            mode: 'label',


        },
        hover: {
            mode: 'label'
        },
    }

});
       
});
