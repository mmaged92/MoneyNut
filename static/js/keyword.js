
async function confirm_delete(keyword_id) {
    // console.log(input) 
    const isConfirmed = confirm('are you sure?');
    if (!isConfirmed) return;

    // const reqBody = {keyword_id}
    const response = await fetch('/trans/keyword/delete', {
        method: 'DELETE',
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ keyword_id }),
    });
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }

    const result = await response.json();
    console.log(result);
    window.location.reload();
}

async function keyword_update(new_value, keyword_id) {
    const isConfirmed = confirm('are you sure?');
    if (!isConfirmed) return;

    const response = await fetch('/trans/keyword/update', {
        method: 'PUT',
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ new_value, keyword_id }),
    });
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }

    const result = await response.json();
    const rowNode = gridOptions.api.getRowNode(String(keyword_id));
    if (rowNode) {
            rowNode.setDataValue("keyword", data.new_value);
    }
}

async function category_update(new_value, category_id, keyword_id) {
    const isConfirmed = confirm('are you sure?');
    if (!isConfirmed) return;

    const response = await fetch('/trans/keyword/categoryupdate', {
        method: 'PUT',
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ new_value, category_id, keyword_id }),
    });
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }

    const result = await response.json();
    const rowNode = gridOptions.api.getRowNode(String(keyword_id));
    if (rowNode) {
            rowNode.setDataValue("category", data.new_value);
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
async function fetchData() {
    try {
        const response = await fetch('/trans/keyword/all');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error("Error fetching data:", error);
        return []; // Return empty array on error
    }
}

async function fetchcategory() {

    const response = await fetch('/trans/keyword/category');
    const category_list = await response.json();
    return category_list;
}

async function initGrid() {
    const myCategoryList = await fetchcategory();

    const gridOptions = {

        rowData: [
        ],
        columnDefs: [

            { field: "keyword", filter: true, editable: true },
            {
                field: "category",
                filter: true,
                editable: true,
                cellEditor: "agSelectCellEditor",
                cellEditorParams: {
                    values: myCategoryList
                }
            },
            { field: "category_id", hide: true },
            { field: "keyword_id", hide: true },
            {
                field: " ", cellRenderer: params => {
                    const deleteIcon = `<i class="fa-solid fa-trash"  onclick="confirm_delete(${params.data.keyword_id})"></i>`
                    return `${deleteIcon} `;
                }
            }
        ],
        rowSelection: {
            mode: 'multiRow'
        },
        onCellValueChanged: params => {

            if (params.colDef.field === 'keyword') {
                keyword_update(params.newValue, params.data.keyword_id)
            }

            if (params.colDef.field === 'category') {
                category_update(params.newValue, params.data.category_id, params.data.keyword_id)
            }
        }

    }


    const myGridElement = document.querySelector('#myGrid');
    gridApi = agGrid.createGrid(myGridElement, gridOptions);


    function updateRowData(data) {

        gridApi.setGridOption('rowData', data)

    }
    fetchData().then(updateRowData);





}
initGrid();

document.getElementById('deleteall').addEventListener('click', () => {
    const selectedData = gridApi.getSelectedRows().map(row => row.keyword_id);
    console.log(selectedData); 
    confirm_delete(selectedData)
});