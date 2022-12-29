const monthlyReturns = document.getElementById("monthly-returns").value;
const portHistory = document.getElementById("port_history").value;

const profit_data_json = JSON.parse(monthlyReturns);
const portHistory_data_json = JSON.parse(portHistory);

let profitKeys = Object.keys(profit_data_json);
let profitData = [];

let historyKeys = Object.keys(portHistory_data_json);
let historyData = [];

for (let i = 0; i < Object.keys(profitKeys).length; i++) {
    profitData.push(parseFloat(profit_data_json[profitKeys[i]]));
}

for (let i = 0; i < Object.keys(historyKeys).length; i++) {
    historyData.push(parseFloat(portHistory_data_json[historyKeys[i]]));
}

var colors = [];
for (var i = 0; i < profitData.length; i++) {
    var color;
    if (profitData[i] > 0) {
        color = "green";
    } else {
        color = "red";
    }
    colors[i] = color;
}

var ctx = document.getElementById("chart-bars").getContext("2d");

new Chart(ctx, {
    type: "bar",
    data: {
        labels: profitKeys,
        datasets: [
            {
                label: "Profit $",
                tension: 0.4,
                borderWidth: 0,
                borderRadius: 4,
                borderSkipped: false,
                backgroundColor: colors,
                data: profitData,
                maxBarThickness: 6,
            },
        ],
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                display: false,
            },
        },
        interaction: {
            intersect: false,
            mode: "index",
        },
        scales: {
            y: {
                grid: {
                    drawBorder: false,
                    display: false,
                    drawOnChartArea: false,
                    drawTicks: false,
                },
                ticks: {
                    suggestedMin: -500,
                    suggestedMax: 500,
                    beginAtZero: true,
                    padding: 15,
                    font: {
                        size: 14,
                        family: "Open Sans",
                        style: "normal",
                        lineHeight: 2,
                    },
                    color: "#fff",
                },
            },
            x: {
                grid: {
                    drawBorder: false,
                    display: false,
                    drawOnChartArea: false,
                    drawTicks: false,
                },
                ticks: {
                    display: false,
                },
            },
        },
    },
});

var ctx2 = document.getElementById("chart-line").getContext("2d");

var gradientStroke1 = ctx2.createLinearGradient(0, 230, 0, 50);

gradientStroke1.addColorStop(1, "rgba(203,12,159,0.2)");
gradientStroke1.addColorStop(0.2, "rgba(72,72,176,0.0)");
gradientStroke1.addColorStop(0, "rgba(203,12,159,0)"); //purple colors

var gradientStroke2 = ctx2.createLinearGradient(0, 230, 0, 50);

gradientStroke2.addColorStop(1, "rgba(20,23,39,0.2)");
gradientStroke2.addColorStop(0.2, "rgba(72,72,176,0.0)");
gradientStroke2.addColorStop(0, "rgba(20,23,39,0)"); //purple colors

new Chart(ctx2, {
    type: "line",
    data: {
        labels: historyKeys,
        datasets: [
            {
                label: "Portfolio Value",
                tension: 0.4,
                borderWidth: 0,
                pointRadius: 0,
                borderColor: "#cb0c9f",
                borderWidth: 3,
                backgroundColor: gradientStroke1,
                fill: true,
                data: historyData,
                maxBarThickness: 6,
            },

        ],
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                display: false,
            },
        },
        interaction: {
            intersect: false,
            mode: "index",
        },
        scales: {
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
        },
    },
});
