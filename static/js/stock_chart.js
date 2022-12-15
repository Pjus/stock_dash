const btn_search = document.getElementById("btn_search");
btn_search.addEventListener("click", function () {
    document.getElementById("ticker").value =
        document.getElementById("search_ticker").value;
    document.getElementById("searchForm").submit();
});
document
    .querySelector("#search_ticker")
    .addEventListener("keypress", function (e) {
        if (e.key === "Enter") {
            document.getElementById("ticker").value =
                document.getElementById("search_ticker").value;
            document.getElementById("searchForm").submit();
        }
    });

const stock_ticker = document.getElementById("stock_ticker").value;

let priceDataPoints = [];
let volumeDataPoints = [];
let closeDataPoints = [];


let financialDataPoints = [];
let balancePoints = [];
let cashPoints = [];

let selectedSubject = ''
const accountSubjects = document.getElementsByClassName('accountSubject')

let fsData = [];
let bsData = [];
let cfData = [];

let fsSub = '';
let bsSub = '';
let cfSub = '';


let stockChart = new CanvasJS.StockChart("chartContainer",{
        exportEnabled: true,
        theme: "light2",
        title:{
        text: `${stock_ticker.toUpperCase()} Stock Price`,
        },
        charts: [{
        toolTip: {
            shared: true
        },
        axisX: {
            lineThickness: 5,
            tickLength: 0,
            labelFormatter: function(e) {
            return "";
            },
            crosshair: {
            enabled: true,
            snapToDataPoint: true,
            labelFormatter: function(e) {
                return ""
            }
            }
        },
        axisY2: {
            title: `${stock_ticker.toUpperCase()} Price`,
            prefix: "$"
        },
        legend: {
            verticalAlign: "top",
            horizontalAlign: "left"
        },
        data: [
            {
                name: "Price (in USD)",
                yValueFormatString: "$#,###.##",
                axisYType: "secondary",
                type: "candlestick",
                risingColor: "red",
                fallingColor: "blue",
                dataPoints : priceDataPoints
            },
            {
                type: "line",
                showInLegend: true,
                name: "Total Revenue",
                axisYType: "secondary",
                yValueFormatString: "$#,##0.00bn",
                xValueFormatString: "YYYY-MM-DD",
                dataPoints: financialDataPoints,
            },
            {
                type: "line",
                showInLegend: true,
                name: "Cash",
                axisYType: "secondary",
                yValueFormatString: "$#,##0.00bn",
                xValueFormatString: "YYYY-MM-DD",
                dataPoints: balancePoints,
            },
            {
                type: "line",
                showInLegend: true,
                name: "Net Income",
                axisYType: "secondary",
                yValueFormatString: "$#,##0.00bn",
                xValueFormatString: "YYYY-MM-DD",
                dataPoints: cashPoints,
            },
        ]
        },{
        height: 100,
        toolTip: {
            shared: true
        },
        axisX: {
            crosshair: {
            enabled: true,
            snapToDataPoint: true
            }
        },
        axisY2: {
            prefix: "",
            title: "Volume"
        },
        legend: {
            horizontalAlign: "left"
        },
        data: [{
            yValueFormatString: "#,###.##",
            axisYType: "secondary",
            name: "Volume",
            dataPoints : volumeDataPoints
        }]
        }],
        navigator: {
        data: [{
            color: "grey",
            dataPoints: closeDataPoints
        }],
        slider: {
            minimum: new Date(2021, 10, 01),
            maximum: new Date(2022, 12, 31)
        }
    }
});

const price_data = document.getElementById("stock_price").value;
const price_data_json = JSON.parse(price_data);
let priceKeys = Object.keys(price_data_json);

const fs_data = document.getElementById("stock_fs").value;
const fs_data_json = JSON.parse(fs_data);
let fsKeys = Object.keys(fs_data_json);

const bs_data = document.getElementById("stock_bs").value;
const bs_data_json = JSON.parse(bs_data);
let bsKeys = Object.keys(bs_data_json);

const cf_data = document.getElementById("stock_cf").value;
const cf_data_json = JSON.parse(cf_data);
let cfKeys = Object.keys(cf_data_json);

function getPriceData() {
    for (let i = 0; i < Object.keys(priceKeys).length; i++) {
        priceDataPoints.push({
            x: new Date(priceKeys[i]),
            y: [
                parseFloat(price_data_json[priceKeys[i]]["Open"]),
                parseFloat(price_data_json[priceKeys[i]]["High"]),
                parseFloat(price_data_json[priceKeys[i]]["Low"]),
                parseFloat(price_data_json[priceKeys[i]]["Close"]),
            ],
        });
        volumeDataPoints.push({
            x: new Date(priceKeys[i]),
            y: parseFloat(price_data_json[priceKeys[i]]["Volume"]),
            color: parseFloat(price_data_json[priceKeys[i]]["Open"]) < parseFloat(price_data_json[priceKeys[i]]["Close"]) ? "green" : "red"
        });
        closeDataPoints.push({
            x: new Date(priceKeys[i]),
            y: parseFloat(price_data_json[priceKeys[i]]["Close"]),

        })
    }
    for (let i = 0; i < Object.keys(fs_data_json).length; i++) {
        financialDataPoints.push({
            x: new Date(fsKeys[i]),
            y:
                parseFloat(fs_data_json[fsKeys[i]]["Total Revenue"]) /
                1000000000,
        });
        balancePoints.push({
            x: new Date(bsKeys[i]),
            y: parseFloat(bs_data_json[bsKeys[i]]["Cash"]) / 1000000000,
        });
        cashPoints.push({
            x: new Date(cfKeys[i]),
            y: parseFloat(cf_data_json[cfKeys[i]]["Net Income"]) / 1000000000,
        });
    }
}


window.onload = function () {
    getPriceData();
    stockChart.render()
};


function update(subject) {
    
    if(Object.keys(fs_data_json[fsKeys[0]]).includes(subject)){
        if(fsData.length > 0){
            fsData = []
            fsSub = ''
        }
        fsSub = subject
        for (let i = 0; i < Object.keys(fs_data_json).length; i++) {
            fsData.push({
                x: new Date(fsKeys[i]),
                y:
                    parseFloat(fs_data_json[fsKeys[i]][subject]) /
                    1000000000,
            });
        }
    }

    if(Object.keys(bs_data_json[bsKeys[0]]).includes(subject)){
        if(bsData.length > 0){
            bsData = []
            bsSub = ''

        }
        bsSub = subject
        for (let i = 0; i < Object.keys(bs_data_json).length; i++) {
            bsData.push({
                x: new Date(bsKeys[i]),
                y:
                    parseFloat(bs_data_json[bsKeys[i]][subject]) /
                    1000000000,
            });
        }
    }

    if(Object.keys(cf_data_json[cfKeys[0]]).includes(subject)){
        if(cfData.length > 0){
            cfData = []
            cfSub = ''
        }
        cfSub = subject
        for (let i = 0; i < Object.keys(cf_data_json).length; i++) {
            cfData.push({
                x: new Date(cfKeys[i]),
                y:
                    parseFloat(cf_data_json[cfKeys[i]][subject]) /
                    1000000000,
            });
        }
    }


    var stockChart = new CanvasJS.StockChart("chartContainer",{
        exportEnabled: true,
        theme: "light2",
        title:{
        text: `${stock_ticker.toUpperCase()} Stock Price`,
        },
        charts: [{
        toolTip: {
            shared: true
        },
        axisX: {
            lineThickness: 5,
            tickLength: 0,
            labelFormatter: function(e) {
            return "";
            },
            crosshair: {
            enabled: true,
            snapToDataPoint: true,
            labelFormatter: function(e) {
                return ""
            }
            }
        },
        axisY2: {
            title: `${stock_ticker.toUpperCase()} Price`,
            prefix: "$"
        },
        legend: {
            verticalAlign: "top",
            horizontalAlign: "left"
        },
        data: [
            {
                name: "Price (in USD)",
                yValueFormatString: "$#,###.##",
                axisYType: "secondary",
                type: "candlestick",
                risingColor: "red",
                fallingColor: "blue",
                dataPoints : priceDataPoints
            },
            {
                type: "line",
                showInLegend: true,
                name: "Total Revenue",
                axisYType: "secondary",
                yValueFormatString: "$#,##0.00bn",
                xValueFormatString: "YYYY-MM-DD",
                dataPoints: fsData,
            },
            {
                type: "line",
                showInLegend: true,
                name: "Cash",
                axisYType: "secondary",
                yValueFormatString: "$#,##0.00bn",
                xValueFormatString: "YYYY-MM-DD",
                dataPoints: bsData,
            },
            {
                type: "line",
                showInLegend: true,
                name: "Net Income",
                axisYType: "secondary",
                yValueFormatString: "$#,##0.00bn",
                xValueFormatString: "YYYY-MM-DD",
                dataPoints: cfData,
            },
        ]
        },{
        height: 100,
        toolTip: {
            shared: true
        },
        axisX: {
            crosshair: {
            enabled: true,
            snapToDataPoint: true
            }
        },
        axisY2: {
            prefix: "",
            title: "Volume"
        },
        legend: {
            horizontalAlign: "left"
        },
        data: [{
            yValueFormatString: "#,###.##",
            axisYType: "secondary",
            name: "Volume",
            dataPoints : volumeDataPoints
        }]
        }],
        navigator: {
        data: [{
            color: "grey",
            dataPoints: closeDataPoints
        }],
        slider: {
            minimum: new Date(2021, 10, 01),
            maximum: new Date(2022, 12, 31)
        }
    }
});
    stockChart.render()
}

for(let i=0; i < accountSubjects.length; i++){
    accountSubjects[i].addEventListener("click", function(e){
        selectedSubject = this.innerText;
        update(selectedSubject)
    })
}

let chartTypeName = ''
const chartTypes = document.getElementsByClassName('chartType')
for(let i=0; i < chartTypes.length; i++){
    chartTypes[i].addEventListener("click", function(e){
        chartTypeName = this.innerText;
        if(chartTypeName=='Candle Chart'){
            console.log(chartTypeName);
        }else if(chartTypeName=='Line Chart'){
            console.log(chartTypeName);           
        } 
    })
}
