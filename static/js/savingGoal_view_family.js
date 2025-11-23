async function fetchData() {
    const response = await fetch('/family/saving_goal_progress_family/');
    const Data = await response.json();
    console.log(Data)
    return Data;
}


async function initGrid() {
    const Data_goal =  await fetchData();

    var chart = new CanvasJS.Chart("chartContainerf", {
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