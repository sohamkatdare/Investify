// Call the backend APIs for the search results.
// All requests are asynchronous.
// The results are populated in the search.html page.

// TODO: Style search.html page
// ticker = document.getElementById("ticker");
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById("flex-1").style.display = "none";
})



async function search(event) {
    // Prevent the form from submitting
    event.preventDefault();

    // Get the ticker from the form
    const ticker = document.getElementById("ticker").value;

    // Hide flex-1 div. REMOVE THIS LATER IF NOT NEEDED.
    document.getElementById("flex-1").style.display = "none";
    document.getElementById("search-results").style.display = "block";
    document.querySelectorAll(".search-appear").forEach((element) => {
        element.style.display = "flex";
    });

    // Async API Calls
    favoriteButtonState(ticker);
    getHighcharts(ticker);
    getPeAndEPS(ticker);
    getCompositeScore(ticker);
    getNews(ticker);
    getInsiderTrading(ticker);
}

let maximize;


let favoriteState = false;
let f_stocks;
async function favoriteButtonState(ticker) {
    // Get the favorite button state from the backend asychronously
    f_stocks = await getFavoriteStocks();
    if (favoriteState != f_stocks.includes(ticker)) { // State does not match.
        document.getElementById("favorite-button").click();
        favoriteState = f_stocks.includes(ticker);
    }
}

async function toggleFavorite(e) {
    // Toggle the favorite button state in the backend asychronously
    favoriteState = !favoriteState;
    const ticker = document.getElementById("ticker").value;
    if (favoriteState) {
        if (!f_stocks.includes(ticker)) {
            addFavoriteStock(ticker);
        }
    } else {
        if (f_stocks.includes(ticker)) {
            removeFavoriteStock(ticker);
        }
    }
}

async function getHighcharts(ticker) {
    // Get the highcharts data from the backend asychronously
    // and populate the highcharts in the search.html page.
    // document.getElementById("candle_div").style.display = "block";
    const response = await fetch('/search/highcharts?ticker=' + ticker).then((response) => {
        if (response.status !== 200) {
            onFail(ticker);
        }
        return response;
    });
    const data = await response.json();

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

    // create the chart      
    await Highcharts.stockChart("candle_div", {
        chart: {
            backgroundColor: "#1b1726",
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
            fill: "#7f6eff",
            states: {
                select: {
                    fill: "#523bff",
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
            name: ticker.toUpperCase(),
            id: ticker.toLowerCase(),
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

    document.getElementById("candle_div").classList.remove("skeleton");
    document.getElementById("candle_div").classList.add("lg:outline");
    document.getElementById("candle_div").classList.add("lg:outline-offset-2");
    document.getElementById("candle_div").classList.add("lg:outline-2");
    document.getElementById("candle_div").classList.add("lg:outline-pink-600/50");
}

async function getPeAndEPS(ticker) {
    // Get the PE and EPS data from the backend asychronously
    // and populate the PE and EPS in the search.html page.
    const response = await fetch('/search/pe-and-eps?ticker=' + ticker).catch(onFail);
    const data = await response.json();

    // TODO: Formatting for PE and EPS.
    document.getElementById("pe-ratio").textContent = data["pe_ratio"];
    document.getElementById("eps-ratio").textContent = data["eps"];    
}

async function getCompositeScore(ticker) {
    // Get the composite score data from the backend asychronously
    // and populate the composite score in the search.html page.
    const response = await fetch('/search/composite-score?ticker=' + ticker).catch(onFail);
    const data = await response.json();

    // TODO: Formatting for Composite Score.
    document.getElementById("composite-score").textContent = data["composite_score"];
}

async function getNews(ticker) {
    // Create skeleton cards

    const skeletonHTML = `
        <a class="card card-compact w-96 bg-[#1b1726] shadow-xl" data-link href="">
            <figure class="h-20 aspect-square skeleton">
                <img class="h-30 aspect-square skeleton" data-img src=""/>
            </figure>
            <div class="card-body">
                <h2 class="card-title hover:underline text-xl font-semibold inline" data-title>
                    <div class="skeleton w-full h-7 mb-2 rounded-sm last:w-4/5"></div>
                    <div class="skeleton w-full h-7 mb-2 rounded-sm last:w-4/5"></div>
                </h2> 
                <span class="text-slate-500" data-publisher>
                    <div class="skeleton w-2/5 h-2 mb-1 rounded-sm"></div>
                    <div class="skeleton w-2/5 h-2 mb-1 rounded-sm"></div>
                    <div class="skeleton w-2/5 h-2 mb-1 rounded-sm"></div>
                </span>
            </div>
        </a>
    `
    const skeletonCount = 6;

    // document.getElementById("news").innerHTML = skeletonHTML.repeat(skeletonCount);
    // Get the news data from the backend asychronously
    // and populate the news in the search.html page.
    const response = await fetch('/search/news?ticker=' + ticker).catch(onFail);
    const data = await response.json();

    returnHTML = ""
    
    // counter = 0


    data.forEach((element) => {
        // counter += 1
        // if (counter <= 6){
        returnHTML += 
        `<a class="card card-compact w-96 bg-[#1b1726] shadow-xl" data-link href="${element.link}">
            <figure>
                <img class="h-30 skeleton" data-img src="${element.thumbnail.resolutions[0].url}"/>
            </figure>
            <div class="card-body">
                <h2 class="card-title hover:underline text-xl font-semibold inline" data-title>${element.title}</h2> 
                <span class="text-slate-500" data-publisher>— ${element.publisher}</span>
            </div>
        </a>`
        // }
    })
    // TODO: Formatting for News. Probably will use cards, but not sure yet.
    // document.getElementById("news").innerHTML = returnHTML;
}

async function getInsiderTrading(ticker) {
    // Get the news data from the backend asychronously
    // and populate the news in the search.html page.
    const response = await fetch('/search/insider-trading?ticker=' + ticker).catch(onFail);
    const data = await response.json();

    data.forEach((element) => {
        // counter += 1
        // if (counter <= 6){
        returnHTML += 
        `<div class="card card-compact w-96 bg-[#1b1726] shadow-xl" data-link>
            <div class="card-body">
                <span><svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 6a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0zM4.501 20.118a7.5 7.5 0 0114.998 0A17.933 17.933 0 0112 21.75c-2.676 0-5.216-.584-7.499-1.632z" />
                </svg></span> <span>${element.name}</span>
                <h2 class="card-title hover:underline text-xl font-semibold inline" data-title>${element.action} ${element.quantity} ${element.stock_type}</h2> 
                <span class="text-slate-500" data-publisher>— ${element.publisher}</span>
            </div>
        </div>`
        // }
    })
    
    // TODO: Formatting for News. Probably will use cards, but not sure yet.
    document.getElementById("insider-trading").textContent = data;
}

// TODO: Add other functions to get the other data from the backend.

function onFail(ticker) {
    // If stock ticker not found or data not available, then reload the page with flash message.
    // window.location.href = "/search?" + "&error="+ticker;
}

form = document.getElementById("search-form");
form.addEventListener("submit", search);

document.getElementById("favorite-button").addEventListener("click", toggleFavorite);

// If url has query params, then populate the search bar with the ticker and submit the form.
const urlParams = new URLSearchParams(window.location.search);
const ticker = urlParams.get('ticker');
if (ticker) {
    document.getElementById("ticker").value = ticker;
    document.getElementById("search-form-submit").click();
}

// Remove all the query params from the url.
window.history.replaceState({}, document.title, "/" + "search");