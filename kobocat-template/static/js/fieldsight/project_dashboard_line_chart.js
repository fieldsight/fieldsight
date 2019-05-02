// var margin = {
//     top: 30,
//     right: 0,
//     bottom: 30,
//     left: 5
// };
// var width = 500 - margin.left - margin.right;
// var height = 300;

// var parseDate = d3.time.format("%Y-%m-%d").parse;

// var x = d3.time.scale().range([0, width]);
// var y = d3.scale.linear().range([height, 0]);

// var xAxis = d3.svg.axis().scale(x)
//     .orient("bottom").ticks(6);

// var yAxis = d3.svg.axis().scale(y)
//     .orient("left").ticks(5);

// var valueline = d3.svg.line()
//     .x(function (d) {
//       return x(d.date);
//     })
//     .y(function (d) {
//       return y(d.close);
//     });

// var svg = d3.select("#submission-chart")
//     .append("svg")
//     .attr("width", width + margin.left + margin.right)
//     .attr("height", height + margin.top + margin.bottom)
//     .append("g")
//     .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

// // Get the data

// line_chart_data.forEach(function (d) {
//     d.date = parseDate(d.date);
//     d.close = +d.close;
// });

// // Scale the range of the data
// x.domain(d3.extent(line_chart_data, function (d) {
//     return d.date;
//     }));
// y.domain([0, d3.max(line_chart_data, function (d) {
//     return d.close;
//     })]);

// svg.append("path") // Add the valueline path.
// .attr("d", valueline(line_chart_data));

// svg.append("g") // Add the X Axis
// .attr("class", "x axis")
//     .attr("transform", "translate(15," + height + ")")
//     .call(xAxis);

// svg.append("g") // Add the Y Axis
// .attr("class", "y axis")
//     .call(yAxis);



     

$( document ).ready(function() {
// Chart.defaults.global.defaultFontColor = '#FFF';
height_max = Math.max.apply(Math, cummulative_data) || 10;
height_max = Math.ceil(height_max / 10) * 10;

var ctx = document.getElementById("myChart");
var myChart = new Chart(ctx, {
    type: 'line',
    data: {
        // labels: chartdata.labels,
        // datasets: dataset
        labels: cummulative_labels,
        datasets: [{
            label: 'No of Submissions',
            data: cummulative_data,
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
                    max: height_max
                        },
                        scaleLabel:{
                            display: true,
                            labelString: 'No of Submissions',
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
                            labelString: 'Date',
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