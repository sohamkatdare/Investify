
async function getStocks() {
    const response = await fetch(`https://www.alphavantage.co/query?function=TOP_GAINERS_LOSERS&apikey=9J4GJJ2IXM4PJX5M`).then((response) => {
        if(response.status !== 200) {
            onFail(ticker);
        }
        return response.json();
    })
    
}

function onFail(ticker) {
    // If stock ticker not found or data not available, then reload the page with flash message.
    console.log("error="+ticker);
}