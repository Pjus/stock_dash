const priceHistory = document.getElementById("stock_price").value;
const price_data_json = JSON.parse(priceHistory);

let priceKeys = Object.keys(price_data_json);
let priceData = [];

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

const config = {
    type: "line",
    data: {
        labels: priceKeys,
        datasets: [
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
        ],
    },
    options: {
        responsive: true,
        scales: {
            xAxes: [
                {
                    type: "time",
                    time: {
                        min:'2022',
                    }
                },
            ],
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
    },
};

window.onload = function (e) {
    const myChart = new Chart(document.getElementById("chart-line"), config);
  
};
