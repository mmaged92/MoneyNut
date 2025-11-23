async function fetchData() {
    const response = await fetch('/expense/saving_goal_progress/');
    const Data = await response.json();
    return Data;
}


async function initGrid() {
    const Data_goal =  await fetchData();

    var chart = new CanvasJS.Chart("chartContainer", {
        animationEnabled: true,
        title:{
            text: "Goal Progress",
            horizontalAlign: "left"
        },
        data: [{
            type: "doughnut",
            startAngle: 60,
            //innerRadius: 60,
            indexLabelFontSize: 17,
            indexLabel: "{label} - #percent%",
            toolTipContent: "<b>{label}:</b> {y} (#percent%)",
            dataPoints: Data_goal
        }]
    });
    chart.render();

}initGrid();