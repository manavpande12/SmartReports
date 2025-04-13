let barCtx = document.getElementById('vesselLevelChart').getContext('2d');

let act_qty1 = 0, act_qty2 = 0;
let set_qty1 = 1000;
let set_qty2 = 1000;
let emptyVessel1 = set_qty1, emptyVessel2 = set_qty2;
let vesselLevelChart;

function isDarkMode() {
    return document.body.classList.contains("dark-mode");
}
function getChartBackgroundColor() {
    return isDarkMode() ? "#000" : "#fff";
}
function getChartGridColor() {
    return isDarkMode() ? "rgba(255, 255, 255, 0.1)" : "rgba(0, 0, 0, 0.25)";
}
function getChartLabelColor() {
    return isDarkMode() ? "white" : "black"; 
}
function getChartEmptyColor() {
    return isDarkMode() ? "black" : "lightgrey"; 
}





function createVesselChart() {
    if (vesselLevelChart) {
        vesselLevelChart.destroy();
    }

    vesselLevelChart = new Chart(barCtx, {
        type: 'bar',
        data: {
            labels: ["Vessel 1", "Vessel 2"],
            datasets: [
                {
                    label: 'Filled Vessel (kg)',
                    data: [act_qty1, act_qty2],
                    backgroundColor: "#324A84",
                    borderWidth: 1,
                    barThickness: 60,
                },
                {
                    label: 'Empty Capacity (kg)',
                    data: [emptyVessel1, emptyVessel2],
                    backgroundColor: getChartEmptyColor(),
                    borderWidth: 1,
                    barThickness: 60,
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    stacked: true,
                    title: { display: true, text: 'Weight (kg)', color: getChartLabelColor() },
                    grid: { display: true, color: getChartGridColor() },
                    ticks: { color: getChartLabelColor() }
                },
                x: {
                    stacked: true,
                    title: { display: false },
                    grid: { color: getChartGridColor() },
                    ticks: { color: getChartLabelColor() }
                }
            },
            plugins: {
                legend: {
                    labels: { color: getChartLabelColor() }
                }
            },
            backgroundColor: getChartBackgroundColor()
        }
    });
}

function updateIndicator(vessel1,vessel2,pause1,pause2) {
    let Indicator1 = document.getElementById('Indicator1');
    let Indicator2 = document.getElementById('Indicator2');
    if (Indicator1) {
        // Start
        if(vessel1 && !pause1){
            Indicator1.style.backgroundColor = '#66FF00';
            Indicator1.style.boxShadow = '0 0 15px rgba(0, 255, 0, 0.9)';
        }
        //Stop
        if(!vessel1 && !pause1){
            Indicator1.style.backgroundColor = '#EF0107';
            Indicator1.style.boxShadow = '0 0 10px rgba(255, 0, 0, 0.7)';
        }
        //Pause
        if(vessel1 && pause1){
            Indicator1.style.backgroundColor = '#FFFF00';
            Indicator1.style.boxShadow = '0 0 10px rgba(255, 255, 0, 0.7)';
        }
        
    }
    if (Indicator2) {
        // Start
        if(vessel2 && !pause2){
            Indicator2.style.backgroundColor = '#66FF00';
            Indicator2.style.boxShadow = '0 0 15px rgba(0, 255, 0, 0.9)';
        }
        //Stop
        if(!vessel2 && !pause2){
            Indicator2.style.backgroundColor = '#EF0107';
            Indicator2.style.boxShadow = '0 0 10px rgba(255, 0, 0, 0.7)';
        }
        //Pause
        if(vessel2 && pause2){
            Indicator2.style.backgroundColor = '#FFFF00';
            Indicator2.style.boxShadow = '0 0 10px rgba(255, 255, 0, 0.7)';
        }
        
    }
}

function noIndicator() {
    let Indicator1 = document.getElementById('Indicator1');
    let Indicator2 = document.getElementById('Indicator2');
    if(Indicator1){
        Indicator1.style.backgroundColor = '#EF0107';
        Indicator1.style.boxShadow = '0 0 10px rgba(255, 0, 0, 0.7)';
    }
    if(Indicator2){
        Indicator2.style.backgroundColor = '#EF0107';
        Indicator2.style.boxShadow = '0 0 10px rgba(255, 0, 0, 0.7)';
    }
}

async function updateVesselChart() {
    try {
        const response = await fetch('/api/data'); 
        const jsonData = await response.json();

        if (jsonData.length > 0) {  
            let latestData = jsonData[jsonData.length - 1];

            //Qty
            act_qty1 = latestData.act_qty1;  
            act_qty2 = latestData.act_qty2;  
            set_qty1 = latestData.set_qty1;
            set_qty2 = latestData.set_qty2;

            //Status
            let vessel1 = latestData.vessel1
            let vessel2 = latestData.vessel2
            let pause1 = latestData.pause1;
            let pause2 = latestData.pause2;
         

            emptyVessel1 = Math.max(0, set_qty1 - act_qty1);
            emptyVessel2 = Math.max(0, set_qty2 - act_qty2);
            vesselLevelChart.data.datasets[0].data = [act_qty1, act_qty2]; 
            vesselLevelChart.data.datasets[1].data = [emptyVessel1, emptyVessel2];
            vesselLevelChart.update(); 


            updateIndicator(vessel1,vessel2,pause1,pause2);
        }
        else{
            noIndicator();
        }
    } catch (error) {
        console.error("Error fetching vessel data:", error);
        noIndicator();
    }
}

const observer = new MutationObserver(() => {
    createVesselChart();
});

observer.observe(document.body, { attributes: true, attributeFilter: ["class"] });

document.addEventListener("DOMContentLoaded", () => {
    createVesselChart();
    updateVesselChart();
});

setInterval(updateVesselChart, 1000);
