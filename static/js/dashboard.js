
async function fetchTotalSpent() {
    const response = await fetch('/expense/dashboard/total_spent');
    const Data = await response.json();
    console.log(Data)
    document.getElementById("total-spent").innerText = Data
    return Data;
}

async function fetchTotalBalance() {
    const response = await fetch('/expense/dashboard/current_balance');
    const Data = await response.json();
    console.log(Data)
    document.getElementById("current-balance").innerText = Data
    return Data;
}

async function fetchTotalremaining() {
    const response = await fetch('/expense/dashboard/fixed_fees_remaining');
    const Data = await response.json();
    console.log(Data)
    document.getElementById("fixed-fees-remaining").innerText = Data
    return Data;
}

async function fetchStatus() {
    const response = await fetch('/expense/dashboard/this_month_status');
    const Data = await response.json();
    console.log(Data)
    document.getElementById("budget-status").innerText = Data
    return Data;
}

async function fetchSpent() {
    const response = await fetch('/expense/dashboard/spent_trend');
    const Data = await response.json();
    console.log(Data)
    return Data;
}
async function fetchSpentPercentage() {
    const response = await fetch('/expense/dashboard/this_month_spent_percentage');
    const Data = await response.json();
    console.log(Data)
    return Data;
}

async function fetchTransData() {
    const response = await fetch('/expense/dashboard/this_month_trans');
    const Data = await response.json();
    console.log(Data)
    return Data;
}

async function fetchsubcatData() {
    const response = await fetch('/expense/dashboard/this_month_spent_sub_categ_percentage');
    const Data = await response.json();
    console.log(Data)
    return Data;
}
async function fetchsubcatDataInverse() {
    const response = await fetch('/expense/dashboard/this_month_spent_sub_categ_percentage_inverse');
    const Data = await response.json();
    console.log(Data)
    return Data;
}


async function initGrid() {
    fetchTotalSpent();
    fetchTotalBalance();
    fetchTotalremaining();
    fetchStatus();
    const Spent_data = await fetchSpent();
    const Spent_Pie = await fetchSpentPercentage();

    const Subcat_spent = await fetchsubcatData();
    const Subcat_spent_inverse = await fetchsubcatDataInverse();

    var chart = new CanvasJS.Chart("chartContainer", {
        animationEnabled: true,
        theme: "light2",
        title: {
            text: "Total Spent"
        },
        axisX: {
            valueFormatString: "DD MMM",
            crosshair: {
                enabled: true,
                snapToDataPoint: true
            }
        },
        axisY: {
            title: "Amount ($)",
            includeZero: true,
            crosshair: {
                enabled: true
            }
        },
        toolTip: {
            shared: true
        },
        legend: {
            cursor: "pointer",
            verticalAlign: "bottom",
            horizontalAlign: "left",
            dockInsidePlotArea: true,
            itemclick: toogleDataSeries
        },
        data: [{
            type: "line",
            markerType: "square",
            xValueFormatString: "DD MMM, YYYY",
            color: "#F08080",
            dataPoints: Spent_data
        }]
    });
    chart.render();


    var chartPie = new CanvasJS.Chart("chartContainerPie", {
        animationEnabled: true,
        title: {
            text: "Spent/Category",
            horizontalAlign: "left"
        },
        data: [{
            type: "doughnut",
            startAngle: 60,
            //innerRadius: 60,
            indexLabelFontSize: 17,
            indexLabel: "{label} - #percent%",
            toolTipContent: "<b>{label}:</b> {y} (#percent%)",
            dataPoints: Spent_Pie
        }]
    });
    chartPie.render();

    var chartbar = new CanvasJS.Chart("chartContainerBar", {
        animationEnabled: true,
        theme: "light2", //"light1", "dark1", "dark2"
        title: {
            text: "Spent Vs Target",
            fontSize: 20,
        },
        axisY: {
            interval: 20,
            suffix: "%"
        },
        axisX: {
			labelAutoFit: true,
            interval: 1
        },
        toolTip: {
            shared: true
        },
        data: [{
            type: "stackedBar100",
            toolTipContent: "{label}<br><b>{name}:</b> {y} (#percent%)",
            showInLegend: true,
            name: "Spent ",
            dataPoints: Subcat_spent
        },
        {
            type: "stackedBar100",
            toolTipContent: "<b>{name}:</b> {y} (#percent%)",
            showInLegend: true,
            name: "Target Remaining",
            dataPoints: Subcat_spent_inverse
        }
        ]
    });
    chartbar.options.height = Subcat_spent.length * 50;
    chartbar.render();



    const gridOptions = {
        // Row Data: The data to be displayed.
        rowData: [],
        // Column Definitions: Defines the columns to be displayed.
        columnDefs: [
            { field: "Date", filter: true},
            { field: "Description", filter: true },
            { field: "Amount", filter: true },
            { field: "In/Out", filter: true },
            { field: "Category", filter: true }
        ]
    };

    const myGridElement = document.querySelector('#myGrid');
    gridApi = agGrid.createGrid(myGridElement, gridOptions);


    fetchTransData().then((Data) => {
        gridApi.setGridOption('rowData', Data)
    });





} initGrid();

function toogleDataSeries(e) {
    if (typeof (e.dataSeries.visible) === "undefined" || e.dataSeries.visible) {
        e.dataSeries.visible = false;
    } else {
        e.dataSeries.visible = true;
    }
    chart.render();
}



window.addEventListener('load', function () {
    const loaderContainer = document.querySelector('.loader');
    // const content = document.querySelector('.main-content');
    setTimeout(() => {
        loaderContainer.style.display = 'none';
        // content.style.display = 'block';
    }, 1000);
});


