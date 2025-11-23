
async function category_view_send(category_view) {
    const response = await fetch('/family/monthly_view/category_get_view/', {
        method: 'POST',
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ category_view })
    })
    console.log(category_view)
    window.location.reload();

}
const categoryselector = document.getElementById('categoryselector')
categoryselector.addEventListener('change', () => {
    const category_view = categoryselector.value;
    category_view_send(category_view);
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}






async function fetchData() {
    try {
        const response = await fetch('/family/monthly_view/monthly_get');
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

async function fetchCategorySpentData() {
    const response = await fetch('/family/monthly_view/category_spent/');
    const Data = await response.json();
    return Data;
}
async function fetchCategorySpentDataamounts() {
    const response = await fetch('/family/monthly_view/category_spent_amounts/');
    const Data = await response.json();
    return Data;
}

async function fetchdailyspent() {
    const response = await fetch('/family/monthly_view/category_spent_daily/');
    const Data = await response.json();
    return Data;
}


async function spentvstarget() {
    const response = await fetch('/family/monthly_view/spentvstarget/');
    const Data = await response.json();
    return Data;
}


async function incomeVSspent() {
    const response = await fetch('/family/monthly_view/incomevsspent/');
    const Data = await response.json();
    return Data;
}

async function targetVSsaving() {
    const response = await fetch('/family/monthly_view/savingvstarget/');
    const Data = await response.json();
    return Data;
}

async function Balance() {
    const response = await fetch('/family/monthly_view/balance_track_monthly/');
    const Data = await response.json();
    return Data;
}

async function initGrid() {

    const category_date = await fetchCategorySpentData();
    const data_category_spent = await fetchCategorySpentDataamounts();
    const dailyspent = await fetchdailyspent();
    const spentvstargetchart = await spentvstarget();
    const incomevsspentchart = await incomeVSspent();
    const targetsaving = await targetVSsaving();
    const balance_data = await Balance();

    const gridOptions = {

        rowData: [],

        columnDefs: [

            { field: "category", filter: true },
            { field: "Total_spent", filter: true },
            { field: "Total_Target", filter: true },
            { field: "Remianing", filter: true },
            { field: "Status", filter: true },

        ],

    }
    const myGridElement = document.querySelector('#myGridmonthlyview');
    gridApi = agGrid.createGrid(myGridElement, gridOptions);

    fetchData().then((Data) => {
        gridApi.setGridOption('rowData', Data)
    });


    var chartbar = new CanvasJS.Chart("chartContainerbar", {
        animationEnabled: true,
        exportEnabled: true,
        height: 400,
        title: {
            text: "Monthly Spent"
        },
        axisX: {
            interval: 1,
        },
        axisY2: {
            titleFontSize: 14,
            interlacedColor: "rgba(1,77,101,.2)",
            gridColor: "rgba(1,77,101,.1)",
            title: "Spent Amount ($)"
        },
        data: [{
            type: "bar",
            name: "Categories",
            color: "#014D65",
            axisYType: "secondary",
            dataPoints: data_category_spent
        }]
    });
    chartbar.render();

    var chart = new CanvasJS.Chart("chartContainer", {
        exportEnabled: true,
        animationEnabled: true,
        title: {
            text: "Monthly Status",
            fontSize: 20,
        },
        legend: {
            cursor: "pointer",
            itemclick: explodePie
        },
        data: [{
            type: "pie",
            
            toolTipContent: "{name}: <strong>{y}%</strong>",
            indexLabel: "{name} - {y}%",
            dataPoints: category_date
        }]
    });
    chart.render();

    var chartbardaily = new CanvasJS.Chart("chartContainerbardaily", {
        animationEnabled: true,
        theme: "light2", // "light1", "light2", "dark1", "dark2"
        title: {
            text: "Daily Spent",
            fontSize: 20,
        },
        axisY: {
            title: "Spent Amount ($)"
        },
        data: [{
            type: "column",
            color: "#B0D0B0",
            legendMarkerColor: "grey",
            dataPointWidth: 5,
            yValueFormatString: "#,##0.## $",
            legendText: "Date",
            dataPoints: dailyspent

        }]
    });
    chartbardaily.render();

    var chartspentVSTarget = new CanvasJS.Chart("chartspentVSTarget", {
        animationEnabled: true,
        theme: "light2", // "light1", "light2", "dark1", "dark2"
        title: {
            text: "Actual Monthly Spent Vs Target",
            fontSize: 20,
        },
        axisY: {
            title: "Amount ($)",
            minimum: 0,
            interval: 2000
        },
        data: [{
            type: "column",
            yValueFormatString: "#,##0.## $",
            dataPoints: spentvstargetchart
        }]
    });
    chartspentVSTarget.render();

    var chartIncomeVSSpent = new CanvasJS.Chart("chartIncomeVSSpent", {
        animationEnabled: true,
        theme: "light2", // "light1", "light2", "dark1", "dark2"
        title: {
            text: "Monthly Income Vs Monthly Actual Spent",
            fontSize: 20,
        },
        axisY: {
            title: "Amount ($)",
            minimum: 0,
            interval: 2000
        },
        data: [{
            type: "column",
            yValueFormatString: "#,##0.## $",
            dataPoints: incomevsspentchart
        }]
    });
    chartIncomeVSSpent.render();

    var chartSavingVSTargetSaving = new CanvasJS.Chart("chartSavingVSTargetSaving", {
        theme: "light2", // "light1", "light2", "dark1", "dark2"
        title: {
            text: "Actual Monthly Saving Vs Target Saving",
            fontSize: 20,
        },
        axisY: {
            title: "Amount ($)",
            minimum: 0,
            interval: 2000
        },
        data: [{
            type: "column",
            yValueFormatString: "#,##0.## $",
            dataPoints: targetsaving
        }]
    });
    chartSavingVSTargetSaving.render();

    var chartBalance = new CanvasJS.Chart("chartContainerBalance", {
        animationEnabled: true,
        exportEnabled: true,
        title: {
            text: "Monthly Accounts Balance",
            fontSize: 20,
        },
        axisY: {
            title: "Amount ($)",
            prefix: "$",
            suffix: "k",
            lineThickness: 0,
            includeZero: true
        },
        data: [{
            type: "stepLine",
            yValueFormatString: "#,##0k",
            markerSize: 5,
            dataPoints: balance_data
        }]
    });
    chartBalance.render();

} initGrid();


function explodePie(e) {
    if (typeof (e.dataSeries.dataPoints[e.dataPointIndex].exploded) === "undefined" || !e.dataSeries.dataPoints[e.dataPointIndex].exploded) {
        e.dataSeries.dataPoints[e.dataPointIndex].exploded = true;
    } else {
        e.dataSeries.dataPoints[e.dataPointIndex].exploded = false;
    }
    e.chart.render();
}



window.addEventListener('load', function () {
    const loaderContainer = document.querySelector('.loader');
    // const content = document.querySelector('.main-content');
    setTimeout(() => {
        loaderContainer.style.display = 'none';
        // content.style.display = 'block';
    }, 1000);
});



