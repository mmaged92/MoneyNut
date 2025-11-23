async function fetchData() {
    const response = await fetch('/accounts/add_bank/get_banks/', { method: 'GET' });
    const data = await response.json();
    return data

}

async function confirm_delete_bank(BanK_id) {
    // console.log(input) 
    const isConfirmed = confirm('are you sure?');
    console.log(BanK_id)
    if (!isConfirmed) return;

    // const reqBody = {keyword_id}
    const response = await fetch('/accounts/add_bank/delete_banks/', {
        method: 'DELETE',
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            "Content-Type": "application/json",
        },
        body: JSON.stringify({BanK_id}),
        
    });
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }

    const result = await response.json();
    console.log(result);
    window.location.reload();
}


async function Bank_update(newValue, Bank_id) {

    const response = await fetch('/accounts/add_bank/update_banks/', {
        method: 'PUT',
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            "Content-Type": "application/json",
        },
        body: JSON.stringify({newValue, Bank_id}),
        
    })

    const result = await response.json();
    const rowNode = gridOptions.api.getRowNode(String(Bank_id));
    if (rowNode) {
            rowNode.setDataValue("Bank", data.new_value);
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
    const gridOptions = {

        rowData: [],

        columnDefs: [

            {
                field: "Bank", filter: true, editable: true,
            },

            { field: "Bank_id", hide: true },
            {
                field: " ", cellRenderer: params => {
                    const deleteIcon = `<i class="fa-solid fa-trash"  onclick="confirm_delete_bank(${params.data.Bank_id})"></i>`
                    return `${deleteIcon} `;
                }
            }

        ],
        rowSelection: {
            mode: 'multiRow'
        },
        onCellValueChanged: params => {

            if (params.colDef.field === 'Bank') {
                Bank_update(params.newValue, params.data.Bank_id)
            }
        }

    }


    const myGridElement = document.querySelector('#myGridabank');
    gridApi = agGrid.createGrid(myGridElement, gridOptions);


    fetchData().then((Data) => {
        gridApi.setGridOption('rowData', Data)
    });

}
initGrid();


document.getElementById('deletebanks').addEventListener('click', () => {
    const selectedData = gridApi.getSelectedRows().map(row => row.Bank_id);
    confirm_delete_bank(selectedData);
});