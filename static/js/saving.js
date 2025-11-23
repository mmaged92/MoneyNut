
async function fetchData() {
    const reponse = await fetch('/saving/saving_target_get', { method: 'GET' });
    const target_list = await reponse.json();
    return target_list
}

async function fetchfreq() {
    const reponse = await fetch('/saving/freq_get', { method: 'GET' });
    const data = await reponse.json();
    return data
}

async function confirm_delete_saving(target_id) {
    // console.log(input) 
    const isConfirmed = confirm('are you sure?');
    if (!isConfirmed) return;
    console.log(target_id)
    // const reqBody = {keyword_id}

    const response = await fetch('/saving/delete_saving', {
        method: 'DELETE',
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ target_id }),
    });
    window.location.reload();
}

async function saving_tagert_update(newValue, saving_target_id) {

    const response = await fetch('/saving/saving_target_update', {
        method: 'PUT',
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ newValue, saving_target_id }),
    })
    const result = await response.json();
    const rowNode = gridOptions.api.getRowNode(String(saving_target_id));
    if (rowNode) {
            rowNode.setDataValue("Saving_target", data.new_value);
    }
}

async function freq_update(newValue, saving_target_id, year, month) {

    const response = await fetch('/saving/freq_update', {
        method: 'PUT',
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ newValue, saving_target_id, year, month }),
    })
    const rowNode = gridOptions.api.getRowNode(String(saving_target_id));
    if (rowNode) {
            rowNode.setDataValue("frequency", data.new_value);
    }
}

async function date_update(newValue, saving_target_id) {

    const response = await fetch('/saving/date_update', {
        method: 'PUT',
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ newValue, saving_target_id}),
    })
    const rowNode = gridOptions.api.getRowNode(String(saving_target_id));
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
            { field: "Saving_target", filter: true, editable: true },
            {
                field: "frequency", filter: true, editable: true,
                cellEditor: "agSelectCellEditor",
                cellEditorParams: {
                    values: freq
                }
            },
            { field: "date", filter: true, editable: true },
            { field: "saving_target_id", hide: true },
            {
                field: " ", cellRenderer: params => {
                    const deleteIcon = `<i class="fa-solid fa-trash"  onclick="confirm_delete_saving(${params.data.saving_target_id})"></i>`
                    return `${deleteIcon} `;
                }
            }
        ],
        rowSelection: {
            mode: 'multiRow'
        },
        onCellValueChanged: params => {

            if (params.colDef.field === 'frequency') {
                freq_update(params.newValue, params.data.saving_target_id, params.data.year, params.data.month)
            }
            if (params.colDef.field === 'Saving_target') {
                saving_tagert_update(params.newValue, params.data.saving_target_id)
            }
            if (params.colDef.field === 'date') {
                date_update(params.newValue, params.data.saving_target_id)
            }
        }

    }


    const myGridElement = document.querySelector('#myGridtsavingtargets');
    gridApi = agGrid.createGrid(myGridElement, gridOptions);


    fetchData().then((Data) => {
        gridApi.setGridOption('rowData', Data)
    });

}
initGrid();


document.getElementById('deletealltarget').addEventListener('click', () => {
    const selectedData = gridApi.getSelectedRows().map(row => row.saving_target_id);
    console.log(selectedData);
    confirm_delete_saving(selectedData);
});