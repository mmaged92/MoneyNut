
async function fetchData() {
    const reponse = await fetch('/saving/income/income_get', { method: 'GET' });
    const target_list = await reponse.json();
    return target_list
}

async function fetchfreq() {
    const reponse = await fetch('/saving/income/income_freq_get', { method: 'GET' });
    const data = await reponse.json();
    return data
}

async function confirm_delete_income(income_id) {
    // console.log(input) 
    const isConfirmed = confirm('are you sure?');
    if (!isConfirmed) return;
    console.log(income_id)
    // const reqBody = {keyword_id}

    const response = await fetch('/saving/income/delete_income', {
        method: 'DELETE',
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ income_id }),
    });
    window.location.reload();
}

async function income_update(newValue, income_id) {
    const response = await fetch('/saving/income/income_update', {
        method: 'PUT',
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ newValue, income_id }),
    })
    const result = await response.json();
    const rowNode = gridOptions.api.getRowNode(String(income_id));
    if (rowNode) {
            rowNode.setDataValue("income", data.new_value);
    }
}

async function freq_update(newValue, income_id, year, month) {
    const isConfirmed = confirm('are you sure?');
    if (!isConfirmed) return;

    const response = await fetch('/saving/income/income_freq_update', {
        method: 'PUT',
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ newValue, income_id, year, month }),
    })
    const result = await response.json();
    const rowNode = gridOptions.api.getRowNode(String(income_id));
    if (rowNode) {
            rowNode.setDataValue("frequency", data.new_value);
    }
}

async function date_update(newValue, income_id) {
    const isConfirmed = confirm('are you sure?');
    if (!isConfirmed) return;

    const response = await fetch('/saving/income/income_date_update', {
        method: 'PUT',
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ newValue, income_id}),
    })
    const result = await response.json();
    const rowNode = gridOptions.api.getRowNode(String(income_id));
    if (rowNode) {
            rowNode.setDataValue("date", data.new_value);
    }
}


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


async function initGrid() {

    const freq = await fetchfreq();
    const gridOptions = {

        rowData: [],

        columnDefs: [

            {
                field: "year", filter: true
            },
            {
                field: "month", filter: true
            },
            { field: "income", filter: true, editable: true },
            {
                field: "frequency", filter: true, editable: true,
                cellEditor: "agSelectCellEditor",
                cellEditorParams: {
                    values: freq
                }
            },
            { field: "date", filter: true, editable: true },
            { field: "income_id", hide: true },

            {
                field: " ", cellRenderer: params => {
                    const deleteIcon = `<i class="fa-solid fa-trash"  onclick="confirm_delete_income(${params.data.income_id})"></i>`
                    return `${deleteIcon} `;
                }
            }
        ],
        rowSelection: {
            mode: 'multiRow'
        },
        onCellValueChanged: params => {

            if (params.colDef.field === 'frequency') {
                freq_update(params.newValue, params.data.income_id, params.data.year, params.data.month)
            }
            if (params.colDef.field === 'income') {
                saving_tagert_update(params.newValue, params.data.income_id)
            }

            if (params.colDef.field === 'date') {
                date_update(params.newValue, params.data.income_id)
            }
        }

    }


    const myGridElement = document.querySelector('#myGridtincome');
    gridApi = agGrid.createGrid(myGridElement, gridOptions);


    fetchData().then((Data) => {
        gridApi.setGridOption('rowData', Data)
    });

}
initGrid();


document.getElementById('deleteallincomes').addEventListener('click', () => {
    const selectedData = gridApi.getSelectedRows().map(row => row.income_id);
    console.log(selectedData);
    confirm_delete_income(selectedData);
});