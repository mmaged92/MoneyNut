
async function fetchData() {
    const reponse = await fetch('/saving/goal/goal_get', { method: 'GET' });
    const target_list = await reponse.json();
    return target_list
}


async function getAccounts() {
    const response = await fetch('/saving/goal/get_accounts', { method: 'GET' });
    const data = await response.json();
    return data

}



async function confirm_delete_goal(goal_id) {
    // console.log(input) 
    const isConfirmed = confirm('are you sure?');
    if (!isConfirmed) return;
    console.log(goal_id)
    // const reqBody = {keyword_id}

    const response = await fetch('/saving/goal/delete_goal', {
        method: 'DELETE',
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ goal_id }),
    });
    window.location.reload();
}

async function goal_name_update(newValue, goal_id) {
    const response = await fetch('/saving/goal/goal_name_update', {
        method: 'PUT',
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ newValue, goal_id }),
    })
    const result = await response.json();
    const rowNode = gridOptions.api.getRowNode(String(goal_id));
    if (rowNode) {
            rowNode.setDataValue("Goal_name", data.new_value);
    }
}
async function goal_account_update(newValue, goal_id) {
    const response = await fetch('/saving/goal/goal_account_update', {
        method: 'PUT',
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ newValue, goal_id }),
    })
    const rowNode = gridOptions.api.getRowNode(String(goal_id));
    if (rowNode) {
            rowNode.setDataValue("Account", data.new_value);
    }
}

async function goal_target_update(newValue, goal_id) {


    const response = await fetch('/saving/goal/goal_target_update', {
        method: 'PUT',
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ newValue, goal_id }),
    })
    const rowNode = gridOptions.api.getRowNode(String(goal_id));
    if (rowNode) {
            rowNode.setDataValue("Goal_target", data.new_value);
    }
}

async function goal_due_date_update(newValue, goal_id) {
    const isConfirmed = confirm('are you sure?');
    if (!isConfirmed) return;

    const response = await fetch('/saving/goal/goal_due_date_update', {
        method: 'PUT',
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ newValue, goal_id }),
    })
    const rowNode = gridOptions.api.getRowNode(String(goal_id));
    if (rowNode) {
            rowNode.setDataValue("Due_date", data.new_value);
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
    const accounts = await getAccounts();
    const gridOptions = {

        rowData: [],

        columnDefs: [

            { field: "Goal_name", filter: true, editable: true },
            { field: "Goal_target", filter: true, editable: true },
            { field: "Due_date", filter: true, editable: true },
            { field: "Goal_created_on", filter: true },
            { field: "goal_id", hide: true },
            {
                field: "Account", filter: true, editable: true,
                cellEditor: "agSelectCellEditor",
                cellEditorParams: {
                values: accounts
                }
            },
            {
                field: " ", cellRenderer: params => {
                    const deleteIcon = `<i class="fa-solid fa-trash"  onclick="confirm_delete_goal(${params.data.goal_id})"></i>`
                    return `${deleteIcon} `;
                }
            }
        ],
        rowSelection: {
            mode: 'multiRow'
        },
        onCellValueChanged: params => {

            if (params.colDef.field === 'Goal_name') {
                goal_name_update(params.newValue, params.data.goal_id)
            }
            if (params.colDef.field === 'Goal_target') {
                goal_target_update(params.newValue, params.data.goal_id)
            }
            if (params.colDef.field === 'Due_date') {
                goal_due_date_update(params.newValue, params.data.goal_id)
            }
            if (params.colDef.field === 'Account') {
                goal_account_update(params.newValue, params.data.goal_id)
            }
        }

    }


    const myGridElement = document.querySelector('#myGridtsavingGoal');
    gridApi = agGrid.createGrid(myGridElement, gridOptions);


    fetchData().then((Data) => {
        gridApi.setGridOption('rowData', Data)
    });

}
initGrid();


document.getElementById('deleteallgoals').addEventListener('click', () => {
    const selectedData = gridApi.getSelectedRows().map(row => row.goal_id);
    console.log(selectedData);
    confirm_delete_goal(selectedData);
});