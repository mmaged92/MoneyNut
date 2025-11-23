

async function fetchData() {
    try {
        const response = await fetch('/expense/annual_view/annual_get_target');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const Data = await response.json();
        console.log(Data)
        return Data;
    } catch (error) {
        console.error("Error fetching data:", error);
        return [];
    }
}

async function fetchTargetData() {
    const response = await fetch('/expense/annual_view/annual_target/');
    const Data = await response.json();
    return Data;
}

async function fetchExpectedIncomeData() {
    const response = await fetch('/expense/annual_view/annual_Expected_income/');
    const Data = await response.json();
    return Data;
}

async function fetchExpectedSavingData() {
    const response = await fetch('/expense/annual_view/annual_Expected_Saving/');
    const Data = await response.json();
    return Data;
}

async function initGrid() {

    const target_data = await fetchTargetData();
    const Expected_Income = await fetchExpectedIncomeData();
    const Expected_Saving = await fetchExpectedSavingData();


    const gridOptions = {

        rowData: [],

        columnDefs: [

            { field: "category", filter: true, pinned: "left" },
            { field: "JAN", filter: true },
            { field: "FEB", filter: true },
            { field: "MAR", filter: true },
            { field: "APR", filter: true },
            { field: "MAY", filter: true },
            { field: "JUN", filter: true },
            { field: "JUL", filter: true },
            { field: "AUG", filter: true },
            { field: "SEP", filter: true },
            { field: "OCT", filter: true },
            { field: "NOV", filter: true },
            { field: "DEC", filter: true },
            { field: "Total_Target", filter: true },
        ],

    }
    const myGridElement = document.querySelector('#myGridannualview');
    gridApi = agGrid.createGrid(myGridElement, gridOptions);

    fetchData().then((Data) => {
        gridApi.setGridOption('rowData', Data)
    });

    var chartTvsEI = new CanvasJS.Chart("chartTargetvsIncomevsSaving", {
        exportEnabled: true,
        animationEnabled: true,
        title: {
            text: "Target Vs Expected Income Vs Expected Saving"
        },
        axisX: {

        },
        axisY: {
            title: "Amount ($)",
            titleFontColor: "#4F81BC",
            lineColor: "#4F81BC",
            labelFontColor: "#4F81BC",
            tickColor: "#4F81BC",
            includeZero: true
        },
        axisY2: {
            title: "Clutch - Units",
            titleFontColor: "#C0504E",
            lineColor: "#C0504E",
            labelFontColor: "#C0504E",
            tickColor: "#C0504E",
            includeZero: true
        },
        toolTip: {
            shared: true
        },
        legend: {
            cursor: "pointer",
            itemclick: toggleDataSeries
        },
        data: [{
            type: "column",
            name: "Budget target",
            showInLegend: true,
            yValueFormatString: "#,##0.## $",
            dataPoints: target_data
        },
        {
            type: "column",
            name: "Expected Saving",
            showInLegend: true,
            yValueFormatString: "#,##0.# $",
            dataPoints: Expected_Saving
        },
        {
            type: "line",
            name: "Expected Income",
            showInLegend: true,
            yValueFormatString: "#,##0.## $",
            dataPoints: Expected_Income
        }]
    });
    chartTvsEI.render();

    function toggleDataSeries(e) {
        if (typeof (e.dataSeries.visible) === "undefined" || e.dataSeries.visible) {
            e.dataSeries.visible = false;
        } else {
            e.dataSeries.visible = true;
        }
        e.chartTvsEI.render();
    }

} initGrid();



window.addEventListener('load', function () {
    const loaderContainer = document.querySelector('.loader');
    // const content = document.querySelector('.main-content');
    setTimeout(() => {
        loaderContainer.style.display = 'none';
        // content.style.display = 'block';
    }, 1000);
});





