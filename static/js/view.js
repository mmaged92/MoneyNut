//fetch all transaction data
async function fetchData() {
    try {
        const response = await fetch('/trans/all'); 
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const transaction_list = await response.json();
        return transaction_list;
    } catch (error) {
        console.error("Error fetching data:", error);
        return []; 
    }
}

//get all categories
async function fetchcategory() {

    const response = await fetch('/trans/keyword/category');
    const category_list = await response.json();
    return category_list;
}

//get ios
async function fetchio() {

    const response = await fetch('/trans/io_get');
    const io_list = await response.json();
    return io_list;
}

//get accounts
async function fetchaccounts() {

    const response = await fetch('/trans/account_get');
    const account_list = await response.json();
    return account_list;
}


//update Description
async function description_update(new_value, transaction_id) {
    const response = await fetch('/trans/descriptionupdate/', {
        method: 'PUT',
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ new_value, transaction_id }),
    });
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }

    const result = await response.json();
    const rowNode = gridOptions.api.getRowNode(String(transaction_id));
    if (rowNode) {
            rowNode.setDataValue("Description", data.new_value);
    }
}

//update Date
async function date_update(new_value, transaction_id) {
    const response = await fetch('/trans/date_update/', {
        method: 'PUT',
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ new_value, transaction_id }),
    });
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }

    const result = await response.json();
    const rowNode = gridOptions.api.getRowNode(String(transaction_id));
    if (rowNode) {
            rowNode.setDataValue("Date", data.new_value);
    }
}

//update amount
async function amount_update(new_value, transaction_id) {
    const response = await fetch('/trans/amount_update/', {
        method: 'PUT',
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ new_value, transaction_id }),
    });
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }

    const result = await response.json();
    const rowNode = gridOptions.api.getRowNode(String(transaction_id));
    if (rowNode) {
            rowNode.setDataValue("Amount", data.new_value);
    }
}

//update IO
async function IO_update(new_value, transaction_id) {
    const response = await fetch('/trans/IO_update/', {
        method: 'PUT',
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ new_value, transaction_id }),
    });
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }

    const result = await response.json();
    const rowNode = gridOptions.api.getRowNode(String(transaction_id));
    if (rowNode) {
            rowNode.setDataValue("IO", data.new_value);
    }
}

//update category
async function category_update_trans(new_value, category_id, transaction_id) {
    const response = await fetch('/trans/category_update/', {
        method: 'PUT',
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ new_value, category_id, transaction_id }),
    });
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }

    const result = await response.json();
    const rowNode = gridOptions.api.getRowNode(String(transaction_id));
    if (rowNode) {
            rowNode.setDataValue("Category", data.new_value, data.main_cat);
    }
}

//update Account
async function account_update(new_value, Account_id, transaction_id) {
    const response = await fetch('/trans/account_update/', {
        method: 'PUT',
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ new_value, Account_id, transaction_id }),
    });
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }

    const result = await response.json();
    const rowNode = gridOptions.api.getRowNode(String(transaction_id));
    if (rowNode) {
            rowNode.setDataValue("Account Name", data.new_value);
    }
}

async function confirm_delete(transaction_id) {
    // console.log(input) 
    const isConfirmed = confirm('are you sure?');
    if (!isConfirmed) return;

    // const reqBody = {keyword_id}
    const response = await fetch('/trans/delete/', {
        method: 'DELETE',
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ transaction_id }),
    });
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }

    const result = await response.json();
    console.log(result);
    window.location.reload();
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

async function myGridtransview() {
    const myCategoryList = await fetchcategory();
    const myIOlist = await fetchio();
    const myAccountslist = await fetchaccounts();

    const gridOptions = {

        rowData: [],

        columnDefs: [
            
            { field: "Description", filter: true, editable: true },
            { field: "Date", filter: true, editable: true },
            { field: "Amount", filter: true, editable: true },
            {
                field: "Category",
                filter: true,
                editable: true,
                cellEditor: "agSelectCellEditor",
                cellEditorParams: {
                    values: myCategoryList
                }
            },
            {
                field: "Category_Main",
                filter: true
            },
            { 
                field: "IO", 
                filter: true, 
                editable: true,
                cellEditor: "agSelectCellEditor",
                cellEditorParams: {
                    values: myIOlist
                } 
            },
            { field: "Bank", filter: true},
            { 
                field: "Account Name", 
                filter: true, 
                editable: true,
                cellEditor: "agSelectCellEditor",
                cellEditorParams: {
                    values: myAccountslist
                }
            },
            { field: "Account Number", filter: true},
            { field: "Account Type", filter: true},
            { field: "category_id", hide: true },
            { field: "transaction_id", hide: true },
            { field: "Account_id", hide: true },
            {
                field: " ", cellRenderer: params => {
                    const deleteIcon = `<i class="fa-solid fa-trash"  onclick="confirm_delete(${params.data.transaction_id})"></i>`
                    return `${deleteIcon} `;
                }
            }
        ],
        rowSelection: {
            mode: 'multiRow'
        },
        onCellValueChanged: params => {

            if (params.colDef.field === 'Description') {
                description_update(params.newValue, params.data.transaction_id)
            }
            if (params.colDef.field === 'Date') {
                date_update(params.newValue, params.data.transaction_id)
            }
            if (params.colDef.field === 'Amount') {
                amount_update(params.newValue, params.data.transaction_id)
            }
            if (params.colDef.field === 'IO') {
                IO_update(params.newValue, params.data.transaction_id)
            }
            if (params.colDef.field === 'Account Name') {
                account_update(params.newValue,params.data.Account_id, params.data.transaction_id)
            }

            if (params.colDef.field === 'Category') {
                category_update_trans(params.newValue, params.data.category_id, params.data.transaction_id)
            }
        }

    }


    const myGridElement = document.querySelector('#myGridtransview');
    gridApi = agGrid.createGrid(myGridElement, gridOptions);


    fetchData().then((transaction_list)=>{
        gridApi.setGridOption('rowData', transaction_list)
    });

}
myGridtransview();


document.getElementById('deletealltransview').addEventListener('click', () => {
    const selectedData = gridApi.getSelectedRows().map(row => row.transaction_id);
    console.log(selectedData); 
    confirm_delete(selectedData);
});
