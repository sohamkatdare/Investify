// Call the backend APIs for the search results.
// All requests are asynchronous.
// The results are populated in the search.html page.

// TODO: Style search.html page
// ticker = document.getElementById("ticker");
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

async function getHighcharts(ticker, id="candle_div") {
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
    await Highcharts.stockChart(id, {
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
    const peRatio = document.getElementById("pe-ratio");
    const epsRatio = document.getElementById("eps-ratio");
    peRatio.innerHTML = `<div class="skeleton w-full h-4 mb-1 rounded-sm last:w-4/5 last:mb-0"></div>`;
    epsRatio.innerHTML = `<div class="skeleton w-full h-4 mb-1 rounded-sm last:w-4/5 last:mb-0"></div>`;
    // Get the PE and EPS data from the backend asychronously
    // and populate the PE and EPS in the search.html page.
    const response = await fetch('/search/pe-and-eps?ticker=' + ticker);
    const data = await response.json();

    // TODO: Formatting for PE and EPS.
    peRatio.innerHTML = data["pe_ratio"];
    epsRatio.innerHTML = data["eps"];    
}

async function getCompositeScore(ticker) {
    const compositeScore = document.getElementById("composite-score");
    compositeScore.innerHTML = `<div class="skeleton w-full h-4 mb-1 rounded-sm last:w-4/5 last:mb-0"></div>`;
    // Get the composite score data from the backend asychronously
    // and populate the composite score in the search.html page.
    const response = await fetch('/search/composite-score?ticker=' + ticker);
    const data = await response.json();

    // TODO: Formatting for Composite Score.
    compositeScore.textContent = data["composite_score"];
}

async function getNews(ticker) {
    // Create skeleton cards

    const skeletonHTML = `
    <div class="h-full sm:shadow-[-1rem_0_3rem_#000]  transition-all duration-700 rounded-lg overflow-hidden relative text-white flex flex-col w-96 group left-0 sm:[&:not(:first-child)]:ml-[-100px] stack-card shrink-0 grow">
    <figure class="grow overflow-hidden"><div class="grow w-full h-full object-cover group-hover:scale-110 transition-all brightness-[0.6] group-hover:brightness-100 duration-700 rounded-t-lg skeleton"></div></figure>
    <div class="py-4 h-max overflow-visible bg-[#1b1726] grow-0">
        <h2 class="px-6 text-2xl font-semibold hover:underline mb-2">
            <div class="skeleton w-4/5 h-4 mb-2 rounded-sm"></div>
            <div class="skeleton w-1/2 h-4 mb-2 rounded-sm"></div>
        </h2>
        <h3 class="px-6 text-slate-500 text-sm mb-4">
            <div class="skeleton w-full h-4 mb-2 rounded-sm"></div>
        </h3>
        <div class="bar w-full relative h-1.5  overflow-hidden bg-white/25 mb-4"></div>
        <div class="px-2 flex flex-wrap flex-row justify-center items-center gap-x-4 gap-y-2">
            <span class="text-center">
                <div class="skeleton w-8 h-3 rounded-lg"></div>
            </span>
            <span class="text-center">
                <div class="skeleton w-8 h-3 rounded-lg"></div>
            </span>
            <span class="text-center">
                <div class="skeleton w-8 h-3 rounded-lg"></div>
            </span>
            <span class="text-center">
                <div class="skeleton w-8 h-3 rounded-lg"></div>
            </span>
        </div>
        </div>
    </div>
  
    `
    const skeletonHTML2 = `
    <div class="h-full sm:shadow-[-1rem_0_3rem_#000]  transition-all duration-700 rounded-lg overflow-hidden relative text-white flex flex-col w-96 group left-0 sm:[&:not(:first-child)]:ml-[-100px] stack-card shrink-0 grow">
    <figure class="grow overflow-hidden"><div class="grow w-full h-full object-cover group-hover:scale-110 transition-all brightness-[0.6] group-hover:brightness-100 duration-700 rounded-t-lg skeleton"></div></figure>
    <div class="py-4 h-max overflow-visible bg-[#1b1726] grow-0">
        <h2 class="px-6 text-2xl font-semibold hover:underline mb-2">
            <div class="skeleton w-4/5 h-4 mb-2 rounded-sm"></div>
            <div class="skeleton w-1/2 h-4 mb-2 rounded-sm"></div>
            <div class="skeleton w-1/2 h-4 mb-2 rounded-sm"></div>
            <div class="skeleton w-1/2 h-4 mb-2 rounded-sm"></div>
            <div class="skeleton w-1/2 h-4 mb-2 rounded-sm"></div>
            <div class="skeleton w-1/2 h-4 mb-2 rounded-sm"></div>
            <div class="skeleton w-1/2 h-4 mb-2 rounded-sm"></div>
            <div class="skeleton w-1/2 h-4 mb-2 rounded-sm"></div>
            <div class="skeleton w-1/2 h-4 mb-2 rounded-sm"></div>
            <div class="skeleton w-1/2 h-4 mb-2 rounded-sm"></div>
            <div class="skeleton w-1/2 h-4 mb-2 rounded-sm"></div>
            <div class="skeleton w-1/2 h-4 mb-2 rounded-sm"></div>
            <div class="skeleton w-1/2 h-4 mb-2 rounded-sm"></div>
            <div class="skeleton w-1/2 h-4 mb-2 rounded-sm"></div>
            <div class="skeleton w-1/2 h-4 mb-2 rounded-sm"></div>
            <div class="skeleton w-1/2 h-4 mb-2 rounded-sm"></div>
        </h2>
        <h3 class="px-6 text-slate-500 text-sm mb-4">
            <div class="skeleton w-full h-4 mb-2 rounded-sm"></div>
        </h3>
        <div class="bar w-full relative h-1.5  overflow-hidden bg-white/25 mb-4"></div>
        <div class="px-2 flex flex-wrap flex-row justify-center items-center gap-x-4 gap-y-2">
            <span class="text-center">
                <div class="skeleton w-16 h-3 rounded-lg"></div>
            </span>
            <span class="text-center">
                <div class="skeleton w-8 h-3 rounded-lg"></div>
            </span>
            <span class="text-center">
                <div class="skeleton w-8 h-3 rounded-lg"></div>
            </span>
            <span class="text-center">
                <div class="skeleton w-8 h-3 rounded-lg"></div>
            </span>
        </div>
        </div>
    </div>
  
    `
    const skeletonCount = 6;

    document.getElementById("news").innerHTML = skeletonHTML.repeat(skeletonCount) + skeletonHTML2;
    // Get the news data from the backend asychronously
    // and populate the news in the search.html page.
    const response = await fetch('/search/news?ticker=' + ticker).catch(onFail);
    const data = await response.json();
    console.log(data)

    returnHTML = ""
    
    counter = 0


    data.forEach((element) => {   
        if(!element.hasOwnProperty("thumbnail")) return;
        tickerList = `<div class="px-2 flex flex-wrap flex-row justify-center items-center gap-x-4 gap-y-2">`
        tickerCount = 0
        for (i = 1; i < element.relatedTickers.length; i++) {
            // Make sure ticker is only letters.
            if(element.relatedTickers[i] != ticker){
                const href = element.relatedTickers[i].match(/^[a-zA-Z]+$/) ? "" : `/search?ticker=${element.relatedTickers[i]}` //if ticker has special characters, then don't add href
                tickerList += `
                <a class="flex justify-center items-center text-white text-base font-medium hover:bg-white/[0.075] bg-transparent border-2 border-white/25 hover:border-transparent rounded-full min-w-64 h-8 p-4 px-2 mb-2 text-center" href=${href}>
                    <span class="text-center">${element.relatedTickers[i]}</span>
                </a>`
                tickerCount += 1
            }
            if (tickerCount == 3) {
                break
            }
        };
        
        if (tickerCount == 0) {
            tickerList += `<a class="invisible flex justify-center items-center text-white text-base font-medium hover:bg-white/[0.075] bg-transparent border-2 border-white/25 hover:border-transparent rounded-full min-w-64 h-8 p-4 px-2 mb-2 text-center">
                <span class="text-center">NO TICKERS FOUND</span>
            </a>`
        }

        tickerList += `</div>`
        console.log(tickerList)

        returnHTML += 
        `<div class="h-full max-sm:hover:shadow-xl max-sm:hover:drop-shadow-xl max-sm:hover:-translate-y-[10%] sm:shadow-[-1rem_0_3rem_#000]  transition-all duration-700 rounded-lg overflow-hidden relative text-white flex flex-col w-96 group left-0 sm:[&:not(:first-child)]:ml-[-100px] stack-card shrink-0 grow">
            <figure class="grow overflow-hidden">
                <a href="${element.link}" target="_blank" class="grow">
                    <img src=${element.thumbnail.resolutions[0].url} class="grow w-full h-full object-cover group-hover:scale-110 transition-all brightness-[0.6] group-hover:brightness-100 duration-700 rounded-t-lg skeleton">
                </a>
            </figure>
            <div class="py-4 px-6 h-max overflow-visible bg-[#1b1726] grow-0">
                <a class="text-2xl font-semibold hover:underline mb-4" href="${element.link}">${element.title}</a>
                <h3 class="text-slate-500 text-sm mb-4">${element.publisher}</h3>
                <div class="bar relative h-1.5  overflow-hidden bg-white/25 mb-4">
                    <div class="w-0 h-full absolute top-0 left-0 bg-gradient-to-r from-pink-500 via-purple-500 to-pink-500 transition-all duration-700 hover:w-full group-hover:w-full"></div>
                </div>
                ${tickerList}
            </div>
        </div>`
    })



    document.getElementById("news").innerHTML = returnHTML;
}

async function getInsiderTrading(ticker) {
    // Create skeleton cards
    const skeletonHTML = `<div class="card card-compact w-96 bg-[#1b1726] shadow-xl" data-link>
            <div class="card-body">
                <div class="flex flex-row justify-between">
                    <div class="flex flex-row gap-x-2">
                        <span><svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="inline w-4 h-4">
                            <path class="inline" stroke-linecap="round" stroke-linejoin="round" d="M15.75 6a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0zM4.501 20.118a7.5 7.5 0 0114.998 0A17.933 17.933 0 0112 21.75c-2.676 0-5.216-.584-7.499-1.632z" />
                        </svg></span> <span class="inline skeleton w-4/5 h-4 mb-2 rounded-sm"></span>
                    </div>
                    <div class="flex flex-row gap-x-2">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-4 h-4">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M6.75 3v2.25M17.25 3v2.25M3 18.75V7.5a2.25 2.25 0 012.25-2.25h13.5A2.25 2.25 0 0121 7.5v11.25m-18 0A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75m-18 0v-7.5A2.25 2.25 0 015.25 9h13.5A2.25 2.25 0 0121 11.25v7.5m-9-6h.008v.008H12v-.008zM12 15h.008v.008H12V15zm0 2.25h.008v.008H12v-.008zM9.75 15h.008v.008H9.75V15zm0 2.25h.008v.008H9.75v-.008zM7.5 15h.008v.008H7.5V15zm0 2.25h.008v.008H7.5v-.008zm6.75-4.5h.008v.008h-.008v-.008zm0 2.25h.008v.008h-.008V15zm0 2.25h.008v.008h-.008v-.008zm2.25-4.5h.008v.008H16.5v-.008zm0 2.25h.008v.008H16.5V15z" />
                        </svg>
                        <span class="inline skeleton w-4/5 h-4 mb-2 rounded-sm"></span>
                    </div>
                </div>
                <div class="flex justify-between w-full">
                    <h2 class="card-title text-4xl mr-6 font-bold skeleton w-4/5 h-4 mb-2 rounded-sm data-title></h2>
                    <h2 class="card-title text-4xl ml-6 font-bold skeleton w-4/5 h-4 mb-2 rounded-sm"></h2>
                </div>
                <div class="flex justify-between">
                    <p class="skeleton w-4/5 h-4 mb-2 rounded-sm"></p>
                    <p class="text-end skeleton w-4/5 h-4 mb-2 rounded-sm"></p>
                </div>
            </div>
        </div>`

    document.getElementById("insider-trading").innerHTML = skeletonHTML.repeat(2);
    // Get the news data from the backend asychronously
    // and populate the news in the search.html page.
    const response = await fetch('/search/insider-trading?ticker=' + ticker).catch(onFail);
    const data = await response.json();
    console.log(data)

    insiderHTML = ""
    count = 0

    data.forEach((element) => {
        count += 1
        color = ""

        if (element.action == "Sold") {
            color = "red";
        } else if (element.action == "Bought") {
            color = "green"
        }

        insiderHTML += 
        `<div class="card card-compact w-max bg-[#1b1726] shadow-xl" data-link>
            <div class="card-body">
                <div class="flex flex-row justify-between">
                    <div class="flex flex-row gap-x-2">
                        <span><svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="inline w-4 h-4">
                            <path class="inline" stroke-linecap="round" stroke-linejoin="round" d="M15.75 6a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0zM4.501 20.118a7.5 7.5 0 0114.998 0A17.933 17.933 0 0112 21.75c-2.676 0-5.216-.584-7.499-1.632z" />
                        </svg></span> <span class="inline">${element.name}</span>
                    </div>
                    <div class="flex flex-row gap-x-2">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-4 h-4">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M6.75 3v2.25M17.25 3v2.25M3 18.75V7.5a2.25 2.25 0 012.25-2.25h13.5A2.25 2.25 0 0121 7.5v11.25m-18 0A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75m-18 0v-7.5A2.25 2.25 0 015.25 9h13.5A2.25 2.25 0 0121 11.25v7.5m-9-6h.008v.008H12v-.008zM12 15h.008v.008H12V15zm0 2.25h.008v.008H12v-.008zM9.75 15h.008v.008H9.75V15zm0 2.25h.008v.008H9.75v-.008zM7.5 15h.008v.008H7.5V15zm0 2.25h.008v.008H7.5v-.008zm6.75-4.5h.008v.008h-.008v-.008zm0 2.25h.008v.008h-.008V15zm0 2.25h.008v.008h-.008v-.008zm2.25-4.5h.008v.008H16.5v-.008zm0 2.25h.008v.008H16.5V15z" />
                        </svg>
                        <span class="inline">${element.trade_date}</span>
                    </div>
                </div>
                <div class="flex justify-between w-full">
                    <h2 class="card-title text-4xl mr-6 font-bold text-${color}-500" data-title>${element.action}</h2>
                    <h2 class="card-title text-4xl ml-6 font-bold">${element.total} USD</h2>
                </div>
                <div class="flex justify-between">
                    <p>${element.stock_type}</p>
                    <p class="text-end">Qty: ${element.quantity}</p>
                </div>
            </div>
        </div>`
        // }
    })


    if (count == 0) {
        document.getElementById("insider-heading").classList.add("hidden")
        document.getElementById("insider-trading").classList.add("hidden")
    }

    if (count != 0) {
        document.getElementById("insider-heading").classList.remove("hidden")
        document.getElementById("insider-trading").classList.remove("hidden")
    }

    document.getElementById("insider-trading").innerHTML = insiderHTML;
    
}

// TODO: Add other functions to get the other data from the backend.

function onFail(ticker) {
    // If stock ticker not found or data not available, then reload the page with flash message.
    window.location.href = "/search?" + "error="+ticker;
}

form = document.getElementById("search-form");
form.addEventListener("submit", search);

favButton = document.getElementById("favorite-button")
if (favButton) {
    favButton.addEventListener("click", toggleFavorite);
}

// If url has query params, then populate the search bar with the ticker and submit the form.
const urlParams = new URLSearchParams(window.location.search);
const ticker = urlParams.get('ticker');
if (ticker) {
    document.getElementById("ticker").value = ticker;
    document.getElementById("search-form-submit").click();
}