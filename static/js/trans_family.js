//fetch all transaction data
async function fetchData() {
    try {
        const response = await fetch('/family/trans_get_family/'); 
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

async function myGridtransview() {


    const gridOptions = {

        rowData: [],

        columnDefs: [
            { field: "User", filter: true},
            { field: "Description", filter: true},
            { field: "Date", filter: true},
            { field: "Amount", filter: true},
            {
                field: "Category",
                filter: true
            },
            { 
                field: "IO", 
                filter: true
            },
            { field: "Bank", filter: true},
            { 
                field: "Account Name", 
                filter: true
            },
            { field: "Account Number", filter: true},
            { field: "Account Type", filter: true},
            { field: "category_id", hide: true },
            { field: "transaction_id", hide: true },
            { field: "Account_id", hide: true },
        ],
    }


    const myGridElement = document.querySelector('#myGridtransview');
    gridApi = agGrid.createGrid(myGridElement, gridOptions);


    fetchData().then((transaction_list)=>{
        gridApi.setGridOption('rowData', transaction_list)
    });

}
myGridtransview();

