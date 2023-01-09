
var ctx2 = document.getElementById("chart-line").getContext("2d");

var gradientStroke1 = ctx2.createLinearGradient(0, 230, 0, 50);

gradientStroke1.addColorStop(1, "rgba(203,12,159,0.2)");
gradientStroke1.addColorStop(0.2, "rgba(72,72,176,0.0)");
gradientStroke1.addColorStop(0, "rgba(203,12,159,0)"); //purple colors

var gradientStroke2 = ctx2.createLinearGradient(0, 230, 0, 50);

gradientStroke2.addColorStop(1, "rgba(20,23,39,0.2)");
gradientStroke2.addColorStop(0.2, "rgba(72,72,176,0.0)");
gradientStroke2.addColorStop(0, "rgba(20,23,39,0)"); //purple colors



const priceHistory = document.getElementById("stock_price").value;
const price_data_json = JSON.parse(priceHistory);

let priceKeys = Object.keys(price_data_json);


let priceData = [];
let macdData1 = [];
let macdData2 = [];
let macdData3 = [];
let macdData4 = [];
let macdData5 = [];
let macdData6 = [];

let bbandMiddleData = [];
let bbandUpperData = [];
let bbandLowerData = [];

let bbandDataset = [
    bbandMiddleData,
    bbandUpperData,
    bbandLowerData,
]

let dataArray = [
    priceData,
    macdData1,
    macdData2,
    macdData3,
    macdData4,
    macdData5,
    macdData6,
    bbandMiddleData,
    bbandUpperData,
    bbandLowerData,
]


let colors = [
    "#cb0c9f", 
    "#fc0f0f", 
    "#8338eb", 
    "#55ffff", 
    "#322bff", 
    "#ffff66", 
    "#fb8500", 
    '#ACC6DF', 
    '#1B98E0', 
    '#1B98E0', 
]

let labels = [
    'Price', 
    '10D', 
    '20D', 
    '30D', 
    '50D', 
    '100D', 
    '200D', 
    'Middle', 
    'Upper', 
    'Lower'
]


const scales = {
    y: {
        grid: {
            drawBorder: false,
            display: true,
            drawOnChartArea: true,
            drawTicks: false,
            borderDash: [5, 5],
        },
        ticks: {
            display: true,
            padding: 10,
            color: "#b2b9bf",
            font: {
                size: 11,
                family: "Open Sans",
                style: "normal",
                lineHeight: 2,
            },
        },
    },
    x: {
        grid: {
            drawBorder: false,
            display: false,
            drawOnChartArea: false,
            drawTicks: false,
            borderDash: [5, 5],
        },
        ticks: {
            display: true,
            color: "#b2b9bf",
            padding: 20,
            font: {
                size: 11,
                family: "Open Sans",
                style: "normal",
                lineHeight: 2,
            },
        },
    },
};

for (let i = 0; i < priceKeys.length; i++) {
    priceData.push(price_data_json[priceKeys[i]]["Close"]);
}

let totalDatasets = []

for(let i = 0; i < colors.length; i++){
    totalDatasets.push(
        {
            label: labels[i],
            tension: 0.4,
            borderWidth: 0,
            pointRadius: 0,
            pointBorderWidth: 1,
            borderColor: colors[i],
            borderWidth: 3,
            backgroundColor: gradientStroke1,
            fill: true,
            data: dataArray[i],
            maxBarThickness: 6,
        }
    )
    
}


const config = {
    type: "line",
    data: {
        labels: priceKeys,
        datasets: totalDatasets,
    },
    options: {
        responsive: true,
        scales: {
            xAxes: [
                {
                    type: "time",
                    time: {
                        min: "2022",
                    },
                },
            ],
            y: {
                type: "linear",
                display: true,
                position: "left",
            },
            y1: {
                type: "linear",
                display: true,
                position: "right",

                // grid line settings
                grid: {
                    drawOnChartArea: false, // only want the grid lines for one axis to show up
                },
            },
        },
        pan: {
            enabled: true,
            mode: "x",
        },
        zoom: {
            enabled: true,
            mode: "x", // or 'x' for "drag" version
        },
        legend: {
            display: false,
        },
        tooltips: {
            mode: "index",
            intersect: false,
            callbacks: {
                label: function(tooltipItem, data) {
                    return `${data.datasets[tooltipItem.datasetIndex].label} ${tooltipItem.yLabel.toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,')}`;
                }
            }
        },
        hover: {
            mode: "index",
            intersect: false,
        },
    },
};

let myChart = new Chart(document.getElementById("chart-line"), config);

function fillDataset(macdData, macdKeys, macd_data_json, myChart, num) {
    for (let i = 0; i < macdKeys.length; i++) {
        macdData.push(macd_data_json[macdKeys[i]]);
    }
    let tempData = {
        label: labels[num],
        tension: 0.4,
        borderWidth: 0,
        pointRadius: 0,
        pointBorderWidth: 1,
        borderColor: colors[num],
        borderWidth: 3,
        backgroundColor: gradientStroke1,
        fill: true,
        data: macdData,
        maxBarThickness: 6,
    }

    myChart.data.datasets[num] = tempData

    
}

function fillBBAND(bbandKeys, bband_data_json){
    for(let i=0; i < bbandKeys.length; i++){
        let currentBand = bbandKeys[i]
        let currentData = bband_data_json[currentBand]
        let dateKeys = Object.keys(currentData);

        for(let date=0; date < dateKeys.length; date++){
            bbandDataset[i].push(currentData[dateKeys[date]])
        }

        let tempData = {
            label: labels[7 + i],
            tension: 0.4,
            borderWidth: 0,
            pointRadius: 0,
            pointBorderWidth: 1,
            borderColor: colors[7 + i],
            borderWidth: 3,
            backgroundColor: gradientStroke1,
            fill: true,
            data: bbandDataset[i],
            maxBarThickness: 6,
        }
        myChart.data.datasets[7 + i] = tempData

    }


}

window.onload = function () {
    let macd_btns = document.querySelectorAll(".macd");
    let indi_btns = document.querySelectorAll(".indi");

    const ticker = document.querySelector("#stock_ticker").value;

    for (let i = 0; i < macd_btns.length; i++) {
        let curr_btn = macd_btns[i];
        curr_btn.addEventListener("click", getMACD);
    }

    for (let i = 0; i < indi_btns.length; i++) {
        let curr_btn = indi_btns[i];
        curr_btn.addEventListener("click", getINDI);
    }


    async function getMACD() {
        if (this.clicked == true) {
            this.clicked = false;
            switch (this.value) {
                case "10":
                    macdData1.length = 0;
                    myChart.data.datasets[1] = macdData1;
                    myChart.update();

                    break;
                case "20":
                    macdData2.length = 0;
                    myChart.data.datasets[2] = macdData2;
                    myChart.update();
                    break;

                case "30":
                    macdData3.length = 0;
                    myChart.data.datasets[3] = macdData3;
                    myChart.update();
                    break;
                case "50":
                    macdData4.length = 0;
                    myChart.data.datasets[4] = macdData4;
                    myChart.update();
                    break;
                case "100":
                    macdData5.length = 0;
                    myChart.data.datasets[5] = macdData5;
                    myChart.update();
                    break;
                case "200":
                    macdData6.length = 0;
                    myChart.data.datasets[6] = macdData6;
                    myChart.update();
                    break;
            }
        } else {
            this.clicked = true;
            let obj;
            const res = await fetch(
                `/analysis/indicator/macd/${ticker}/${this.value}`
            );
            obj = await res.json();
            const macd_data_json = JSON.parse(obj["result"]);
            let macdKeys = Object.keys(macd_data_json);
            switch (this.value) {
                case "10":
                    fillDataset(
                        macdData1,
                        macdKeys,
                        macd_data_json,
                        myChart,
                        1
                    );
                    myChart.update();
                    break;
                case "20":
                    fillDataset(
                        macdData2,
                        macdKeys,
                        macd_data_json,
                        myChart,
                        2
                    );
                    myChart.update();
                    break;
                case "30":
                    fillDataset(
                        macdData3,
                        macdKeys,
                        macd_data_json,
                        myChart,
                        3
                    );
                    myChart.update();
                    break;
                case "50":
                    fillDataset(
                        macdData4,
                        macdKeys,
                        macd_data_json,
                        myChart,
                        4
                    );
                    myChart.update();
                    break;
                case "100":
                    fillDataset(
                        macdData5,
                        macdKeys,
                        macd_data_json,
                        myChart,
                        5
                    );
                    myChart.update();
                    break;
                case "200":
                    fillDataset(
                        macdData6,
                        macdKeys,
                        macd_data_json,
                        myChart,
                        6
                    );
                    myChart.update();

                    break;
            }
        }myChart.update(config);
    }

    async function getINDI(){
        if (this.clicked == true) {
            this.clicked = false;
            switch (this.value) {
                case "bband":

                    break;

                case "20":
                    break;

                case "30":
                    break;

                case "50":
                    break;

                case "100":
                    break;

                case "200":
                    break;
            }
        } else {
            this.clicked = true;
            let obj;
            const res = await fetch(
                `/analysis/indicator/bband/${ticker}`
            );
            obj = await res.json();
            const bband_data_json = JSON.parse(obj["result"]);
            let bbandKeys = Object.keys(bband_data_json);
            switch (this.value) {
                case "bband":

                    fillBBAND(bbandKeys, bband_data_json)
 


                    break;

                case "20":
                    break;

                case "30":
                    break;

                case "50":
                    break;

                case "100":
                    break;

                case "200":
                    break;
            }
        }myChart.update(config);
    }
};
