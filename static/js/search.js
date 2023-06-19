// Call the backend APIs for the search results.
// All requests are asynchronous.
// The results are populated in the search.html page.

ticker = document.getElementById("ticker");

async function search(event) {
    // Prevent the form from submitting
    event.preventDefault();

    document.getElementById("flex-1").style.display = "none";

    // API Calls
    getHighcharts();
}

async function getHighcharts() {
    // Get the highcharts data from the backend asychronously
    // and populate the highcharts in the search.html page.
    // document.getElementById("candle_div").style.display = "block";
    const response = await fetch('/search/highcharts?ticker=' + ticker.value, 
        headers={
            'Content-Type': 'application/json',
        }
    );
    const data = await response.json();
    console.log(data);
    // split the data set into ohlc and volume
    var ohlc = [],
        volume = [],
        dataLength = data.length,
        // set the allowed units for data grouping
        groupingUnits = [
            [
                "week", // unit name
                [1] // allowed multiples
            ],
            ["month", [1, 2, 3, 4, 6]]
        ],
        i = 0;

    for (i; i < dataLength; i += 1) {
        ohlc.push([
        data[i][0], // the date
        data[i][1], // open
        data[i][2], // high
        data[i][3], // low
        data[i][4] // close
        ]);

        volume.push([
        data[i][0], // the date
        data[i][5] // the volume
        ]);
    }
    console.log(ohlc);
    console.log(volume);

    // create the chart      
    Highcharts.stockChart("candle_div", {
        chart: {
            backgroundColor: "#171212",
            style: {
            fontFamily: "'Unica One', sans-serif"
            },
            events: {
            load: function () {
                var chart = this;
                chart.xAxis[0].setExtremes(
                chart.xAxis[0].dataMin,
                chart.xAxis[0].dataMax
                ); // This line is added to fix a bug with the scrollbar
                chart.scrollbar.track.attr({
                stroke: "transparent",
                "stroke-width": 0
                });
                chart.scrollbar.scrollbarGroup.attr({
                stroke: "transparent",
                "stroke-width": 0
                });
            }
            }
        },
    
        rangeSelector: {
            selected: 2,
            buttonTheme: {
            fill: "#69ff33",
            states: {
                select: {
                fill: "#299900",
                style: {
                    color: "white"
                }
                }
            }
            }
        },
    
        xAxis: {
            labels: {
            style: {
                color: "#FFFFFF"
            }
            }
        },
    
        yAxis: [
            {
            labels: {
                align: "right",
                x: -3,
                style: {
                color: "#E0E0E3"
                }
            },
            title: {
                text: "Price",
                style: {
                color: "#E0E0E3"
                }
            },
            height: "60%",
            lineWidth: 2,
            resize: {
                enabled: true
            },
            gridLineColor: "#707073",
            gridLineWidth: 0.5,
            tickInterval: 5,
            tickColor: "#707073"
            },
            {
            labels: {
                align: "right",
                x: -3,
                style: {
                color: "#E0E0E3"
                }
            },
            title: {
                text: "Volume",
                style: {
                color: "#E0E0E3"
                }
            },
            top: "65%",
            height: "35%",
            offset: 0,
            lineWidth: 2,
            gridLineColor: "#707073",
            gridLineWidth: 0.5,
            tickInterval: 10000000,
            tickColor: "#707073"
            }
        ],
    
        tooltip: {
            split: true,
            backgroundColor: "rgba(0, 0, 0, 0.85)",
            style: {
            color: "#F0F0F0"
            }
        },
    
        plotOptions: {
            candlestick: {
            lineColor: "#4CAF50",
            color: "#4CAF50",
            upLineColor: "#F44336",
            upColor: "#F44336"
            },
            column: {
            color: "#2196F3"
            }
        },
    
        series: [
            {
            type: "candlestick",
            name: "AAPL",
            id: "aapl",
            zIndex: 2,
            data: ohlc
            },
            {
            type: "column",
            name: "Volume",
            id: "volume",
            data: volume,
            yAxis: 1
            }
        ],
    
        credits: {
            enabled: false
        },
    
        exporting: {
            buttons: {
            contextButton: {
                enabled: false
            },
            fullscreen: {
                text: "Maximize",
                fill: "#69ff33",
                onclick: function () {
                var chart = this;
                chart.fullscreen.toggle();
                }
            }
            }
        }
    });
}

form = document.getElementById("search-form");
form.addEventListener("submit", search);