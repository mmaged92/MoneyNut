//fetch all transaction data
async function fetchData() {
    try {
        const response = await fetch('/family/get_family_members/'); 
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

async function delete_member(id) {
    // console.log(input) 
    const isConfirmed = confirm('are you sure?');
    if (!isConfirmed) return;
    console.log(id)


    const response = await fetch('/family/remove_family_member/', {
        method: 'DELETE',
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ id }),
    });
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


    const gridOptions = {

        rowData: [],

        columnDefs: [
            { field: "user", filter: true},
            { field: "name", filter: true},
            { field: "email", filter: true},
            { field: "Status", filter: true},
            { field: "id", hide: true },
            {
                field: " ", cellRenderer: params => {
                    const deleteIcon = `<i class="fa-solid fa-delete-left"  onclick="delete_member(${params.data.id})"></i>`
                    return `${deleteIcon} `;
                }
            }
        ],
        rowSelection: {
            mode: 'multiRow'
        },

    }


    const myGridElement = document.querySelector('#myGridFamily');
    gridApi = agGrid.createGrid(myGridElement, gridOptions);


    fetchData().then((transaction_list)=>{
        gridApi.setGridOption('rowData', transaction_list)
    });

}
myGridtransview();

