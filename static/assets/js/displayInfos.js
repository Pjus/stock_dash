let list = document.querySelectorAll(".infoType");

let recommand = document.querySelector("#recommand");
let oscill = document.querySelector("#oscill");
let macd = document.querySelector("#macd");
let indicator = document.querySelector("#indicator");

let macd_days = document.querySelector(".macd-days-hidden")
let indi_days = document.querySelector(".indicator-days-hidden")

let indiChart = document.querySelector("#stock-chart-indi")

for(let i=0; i < list.length; i++){
    let curr_btn = list[i]
    curr_btn.addEventListener("click", function(){
        if(curr_btn.value == recommand.id){
            recommand.classList = "stock-infos"
        } else {
            recommand.classList = "stock-infos-hidden"
        }
        if(curr_btn.value == oscill.id){
            oscill.classList = "stock-infos"
        } else {
            oscill.classList = "stock-infos-hidden"
        }
        if(curr_btn.value == macd.id){
            macd.classList = "stock-infos"
            macd_days.classList = "macd-days-show"
        } else {
            macd.classList = "stock-infos-hidden"
            macd_days.classList = "macd-days-hidden"
        }
        if(curr_btn.value == indicator.id){
            indicator.classList = "stock-infos"
            indi_days.classList = "indicator-days-show"

        } else {
            indicator.classList = "stock-infos-hidden"
            indi_days.classList = "indicator-days-hidden"

        }
    })
}


