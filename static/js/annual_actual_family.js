
// async function category_view_send(category_view) {
//     const response = await fetch('/expense/monthly_view/category_get_view/', {
//         method: 'POST',
//         headers: {
//             "X-CSRFToken": getCookie("csrftoken"),
//             "Content-Type": "application/json",
//         },
//         body: JSON.stringify({ category_view })
//     })
//     console.log(category_view)
//     window.location.reload();

// }
// const categoryselector = document.getElementById('categoryselector')
// categoryselector.addEventListener('change', () => {
//     const category_view = categoryselector.value;
//     category_view_send(category_view);
// });

// function getCookie(name) {
//     let cookieValue = null;
//     if (document.cookie && document.cookie !== '') {
//         const cookies = document.cookie.split(';');
//         for (let i = 0; i < cookies.length; i++) {
//             const cookie = cookies[i].trim();
//             // Does this cookie string begin with the name we want?
//             if (cookie.substring(0, name.length + 1) === (name + '=')) {
//                 cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//                 break;
//             }
//         }
//     }
//     return cookieValue;
// }






async function fetchData() {
    try {
        const response = await fetch('/expense/annual_view/annual_get_actual');
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


async function fetchSpentData() {
    const response = await fetch('/family/annual_view/annual_spent/');
    const Data = await response.json();
    return Data;
}

async function fetchTargetData() {
    const response = await fetch('/family/annual_view/annual_target/');
    const Data = await response.json();
    return Data;
}

async function fetchIncomeData() {
    const response = await fetch('/family/annual_view/annual_income/');
    const Data = await response.json();
    return Data;
}

async function fetchSavingActualData() {
    const response = await fetch('/family/annual_view/annual_saving/');
    const Data = await response.json();
    return Data;
}

async function fetchSavingTargetData() {
    const response = await fetch('/family/annual_view/annual_saving_target/');
    const Data = await response.json();
    return Data;
}
async function fetchAnnualBalanceData() {
    const response = await fetch('/family/annual_view/balance_track_annual/');
    const Data = await response.json();
    console.log(Data)
    return Data;

}


async function initGrid() {

    const spent_data = await fetchSpentData();
    const target_data = await fetchTargetData();
    const income_data = await fetchIncomeData();
    const saving_actual_data = await fetchSavingActualData();
    const saving_target_data = await fetchSavingTargetData();
    const annual_balance = await fetchAnnualBalanceData();


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
            { field: "Total_Actual", filter: true },
            { field: "Total_Target", filter: true },
            { field: "Status", filter: true },
        ],

    }
    const myGridElement = document.querySelector('#myGridannualviewactual');
    gridApi = agGrid.createGrid(myGridElement, gridOptions);

    fetchData().then((Data) => {
        gridApi.setGridOption('rowData', Data)
    });

    var chartTvsS = new CanvasJS.Chart("chartContainer", {
        exportEnabled: true,
        animationEnabled: true,
        title: {
            text: "Monthly Target Vs Spent Vs Income"
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
            name: "Actual Spent",
            showInLegend: true,
            yValueFormatString: "#,##0.# $",
            dataPoints: spent_data
        },
        {
            type: "line",
            name: "Income",
            showInLegend: true,
            yValueFormatString: "#,##0.## $",
            dataPoints: income_data
        }]
    });
    chartTvsS.render();

    var chartSaving = new CanvasJS.Chart("chartContainerSaving", {
        exportEnabled: true,
        animationEnabled: true,
        title: {
            text: "Monthly Saving Target vs Actual Saving"
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
            name: "Saving target",
            showInLegend: true,
            yValueFormatString: "#,##0.## $",
            dataPoints: saving_target_data
        },
        {
            type: "column",
            name: "Actual Saving",
            showInLegend: true,
            yValueFormatString: "#,##0.## $",
            dataPoints: saving_actual_data
        }]
    });
    chartSaving.render();

    var chartBalance = new CanvasJS.Chart("chartContainerBalance", {
	theme: "light1", // "light1", "ligh2", "dark1", "dark2"
	animationEnabled: true,
	title: {
		text: "Total Accounts Balance"
	},
	axisY: {
		title: "Amount ($)",
		prefix: "$",
		suffix: "k",
		lineThickness: 0,
		includeZero: true
	},
	data: [{
		type: "waterfall",
		indexLabel: "{y}",
		indexLabelFontColor: "#EEEEEE",
		indexLabelPlacement: "inside",
		yValueFormatString: "#,##0k",
		dataPoints: annual_balance, 
	}]
});
    chartBalance.render();


} initGrid();


function toggleDataSeries(e) {
    if (typeof (e.dataSeries.visible) === "undefined" || e.dataSeries.visible) {
        e.dataSeries.visible = false;
    } else {
        e.dataSeries.visible = true;
    }
    e.chartTvsS.render();
}
function toggleDataSeries(e) {
    if (typeof (e.dataSeries.visible) === "undefined" || e.dataSeries.visible) {
        e.dataSeries.visible = false;
    } else {
        e.dataSeries.visible = true;
    }
    e.chartSaving.render();
}

function toggleDataSeries(e) {
    if (typeof (e.dataSeries.visible) === "undefined" || e.dataSeries.visible) {
        e.dataSeries.visible = false;
    }
    else {
        e.dataSeries.visible = true;
    }
    chartBalance.render();
}


window.addEventListener('load', function () {
    const loaderContainer = document.querySelector('.loader');
    // const content = document.querySelector('.main-content');
    setTimeout(() => {
        loaderContainer.style.display = 'none';
        // content.style.display = 'block';
    }, 1000);
});



