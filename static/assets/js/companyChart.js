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

let colors = ["#fc0f0f", "#ffffff", "#55ffff", "#322bff", "#ffff66", "#ffffff"]

for (let i = 0; i < priceKeys.length; i++) {
    priceData.push(price_data_json[priceKeys[i]]["Close"]);
}

var ctx2 = document.getElementById("chart-line").getContext("2d");

var gradientStroke1 = ctx2.createLinearGradient(0, 230, 0, 50);

gradientStroke1.addColorStop(1, "rgba(203,12,159,0.2)");
gradientStroke1.addColorStop(0.2, "rgba(72,72,176,0.0)");
gradientStroke1.addColorStop(0, "rgba(203,12,159,0)"); //purple colors

var gradientStroke2 = ctx2.createLinearGradient(0, 230, 0, 50);

gradientStroke2.addColorStop(1, "rgba(20,23,39,0.2)");
gradientStroke2.addColorStop(0.2, "rgba(72,72,176,0.0)");
gradientStroke2.addColorStop(0, "rgba(20,23,39,0)"); //purple colors

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

let totalDatasets = [
    {
        label: "Close Price",
        tension: 0.4,
        borderWidth: 0,
        pointRadius: 0,
        pointBorderWidth: 1,
        borderColor: "#cb0c9f",
        borderWidth: 3,
        backgroundColor: gradientStroke1,
        fill: true,
        data: priceData,
        maxBarThickness: 6,
    },
    {
        label: "MACD1",
        tension: 0.4,
        borderWidth: 0,
        pointRadius: 0,
        pointBorderWidth: 1,
        borderColor: "#fc0f0f",
        borderWidth: 3,
        backgroundColor: gradientStroke1,
        fill: true,
        data: macdData1,
        maxBarThickness: 6,
    },
    {
        label: "MACD2",
        tension: 0.4,
        borderWidth: 0,
        pointRadius: 0,
        pointBorderWidth: 1,
        borderColor: "#ffffff",
        borderWidth: 3,
        backgroundColor: gradientStroke1,
        fill: true,
        data: macdData2,
        maxBarThickness: 6,
    },
    {
        label: "MACD3",
        tension: 0.4,
        borderWidth: 0,
        pointRadius: 0,
        pointBorderWidth: 1,
        borderColor: "#55ffff",
        borderWidth: 3,
        backgroundColor: gradientStroke1,
        fill: true,
        data: macdData3,
        maxBarThickness: 6,
    },
    {
        label: "MACD4",
        tension: 0.4,
        borderWidth: 0,
        pointRadius: 0,
        pointBorderWidth: 1,
        borderColor: "#322bff",
        borderWidth: 3,
        backgroundColor: gradientStroke1,
        fill: true,
        data: macdData4,
        maxBarThickness: 6,
    },
    {
        label: "MACD5",
        tension: 0.4,
        borderWidth: 0,
        pointRadius: 0,
        pointBorderWidth: 1,
        borderColor: "#ffff66",
        borderWidth: 3,
        backgroundColor: gradientStroke1,
        fill: true,
        data: macdData5,
        maxBarThickness: 6,
    },
    {
        label: "MACD6",
        tension: 0.4,
        borderWidth: 0,
        pointRadius: 0,
        pointBorderWidth: 1,
        borderColor: "#ffffff",
        borderWidth: 3,
        backgroundColor: gradientStroke1,
        fill: true,
        data: macdData6,
        maxBarThickness: 6,
    },
];

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
        label: `MACD ${num}`,
        tension: 0.4,
        borderWidth: 0,
        pointRadius: 0,
        pointBorderWidth: 1,
        borderColor: colors[num-1],
        borderWidth: 3,
        backgroundColor: gradientStroke1,
        fill: true,
        data: macdData,
        maxBarThickness: 6,
    }

    myChart.data.datasets[num] = tempData

    
}

window.onload = function () {
    let macd_btns = document.querySelectorAll(".macd");
    const ticker = document.querySelector("#stock_ticker").value;

    for (let i = 0; i < macd_btns.length; i++) {
        let curr_btn = macd_btns[i];
        curr_btn.addEventListener("click", getMACD);
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
};
