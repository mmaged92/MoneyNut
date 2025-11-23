
async function fetchData() {
    const response = await fetch('/accounts/getaccounts', { method: 'GET' });
    const data = await response.json();
    return data

}
async function fetchBank() {
    const response = await fetch('/accounts/bank_get', { method: 'GET' });
    const data = await response.json();
    return data

}
async function fetchAccountsTypes() {
    const response = await fetch('/accounts/accounttype_get', { method: 'GET' });
    const data = await response.json();
    return data

}


async function initGrid() {
    const banks = await fetchBank();
    const accountTypes = await fetchAccountsTypes();

    const gridOptions = {

        rowData: [],

        columnDefs: [

            {
                field: "Bank", filter: true
            },
            {
                field: "account_type", filter: true
            },
            {
                field: "account_name",
                filter: true

            },
            { field: "account_number", filter: true, editable: true },
            { field: "Starting_balance", filter: true, editable: true },
            { field: "account_balance_start_date", filter: true, editable: true},
            { field: "account_balance", filter: true },

            { field: "account_id", hide: true },


        ],
    }


    const myGridElement = document.querySelector('#myGridaccounts');
    gridApi = agGrid.createGrid(myGridElement, gridOptions);


    fetchData().then((Data) => {
        gridApi.setGridOption('rowData', Data)
    });

}
initGrid();
