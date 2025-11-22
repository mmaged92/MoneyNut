
async function fetchcategories() {

    const response = await fetch('/target/category_get/');
    const category_list = await response.json();
    return category_list;
}
async function fetchmaincategories() {

    const response = await fetch('/target/main_category_get/');
    const category_list = await response.json();
    console.log(category_list)
    return category_list;
}

async function fetchmaincategorieslist() {

    const response = await fetch('/target/main_category_get_list/');
    const category_list = await response.json();
    console.log(category_list)
    return category_list;
}


async function main_category_update_main(new_value, category_id) {

    const response = await fetch('/target/main_category_update/', {
        method: 'PUT',
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ new_value, category_id }),
    });
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }

    const result = await response.json();
    const rowNode = gridOptions.api.getRowNode(String(category_id));
    if (rowNode) {
            rowNode.setDataValue("Category", data.new_value);
    }
}
async function main_category_update(new_value, category_id) {

    const response = await fetch('/target/category_main_category_update/', {
        method: 'PUT',
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ new_value, category_id }),
    });
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }

    const result = await response.json();
    const rowNode = gridOptions.api.getRowNode(String(category_id));
    if (rowNode) {
            rowNode.setDataValue("main_category", data.new_value);
    }
}

async function fixed_fees_update(new_value, category_id) {

    console.log(new_value)
    const response = await fetch('/target/fixed_fees_update/', {
        method: 'PUT',
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ new_value, category_id }),

    });
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }

    const result = await response.json();
    const rowNode = gridOptions.api.getRowNode(String(category_id));
    if (rowNode) {
            rowNode.setDataValue("fixed_fees", data.new_value);
    }
}


async function confirm_delete(category_id) {
    // console.log(input) 
    const isConfirmed = confirm('are you sure?');
    if (!isConfirmed) return;

    // const reqBody = {keyword_id}
    const response = await fetch('/target/delete/', {
        method: 'DELETE',
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ category_id }),
    });
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }

    const result = await response.json();
    console.log(result);
    window.location.reload();
}

async function main_confirm_delete(category_id) {
    // console.log(input) 
    const isConfirmed = confirm('are you sure?');
    if (!isConfirmed) return;

    // const reqBody = {keyword_id}
    const response = await fetch('/target/main_category_delete/', {
        method: 'DELETE',
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ category_id }),
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


async function initGrid() {
    const categorymain_list = await fetchmaincategorieslist();
    const gridOptions = {

        rowData: [],

        columnDefs: [
            { field: "Category", filter: true, editable: true },
            {
                field: "main_category",
                filter: true,
                editable: true,
                cellEditor: "agSelectCellEditor",
                cellEditorParams: {
                    values: categorymain_list
                }
            },
            {
                field: "fixed_fees", filter: true, editable: true,
                cellDataType: "boolean",
                valueGetter: params => {
                    // Assuming params.data.isActive can be 'True', 'False', or actual booleans
                    console.log(params.data.fixed_fees)
                    if (params.data.fixed_fees === null) {
                        console.log(params.data.fixed_fees)
                        return params.data.fixed_fees === 'false';
                    }
                    else if (params.data.fixed_fees === 'True' || params.data.fixed_fees === 'true') {
                        console.log(params.data.fixed_fees)
                        return params.data.fixed_fees = true // Return as is if already a boolean
                    }
                    else if (params.data.fixed_fees === "False" || params.data.fixed_fees === 'false') {
                        console.log(params.data.fixed_fees)
                        return params.data.fixed_fees = false; // Return as is if already a boolean
                    }
                },
            },
            { field: "category_id", hide: true },
            {
                field: " ", cellRenderer: params => {
                    const deleteIcon = `<i class="fa-solid fa-trash"  onclick="confirm_delete(${params.data.category_id})"></i>`
                    return `${deleteIcon} `;
                }
            }
        ],
        rowSelection: {
            mode: 'multiRow'
        },
        onCellValueChanged: params => {
            if (params.colDef.field === 'Category') {
                category_update_cat(params.newValue, params.data.category_id)
            }
            if (params.colDef.field === 'fixed_fees') {
                fixed_fees_update(params.newValue, params.data.category_id)
            }
            if (params.colDef.field === 'main_category') {
                main_category_update(params.newValue, params.data.category_id)
            }
        }

    }

    const gridOptionMainCategories = {

        rowData: [],

        columnDefs: [
            { field: "Category", filter: true, editable: true },
    
            { field: "category_id", hide: true },
            {
                field: " ", cellRenderer: params => {
                    const deleteIcon = `<i class="fa-solid fa-trash"  onclick="main_confirm_delete(${params.data.category_id})"></i>`
                    return `${deleteIcon} `;
                }
            }
        ],
        rowSelection: {
            mode: 'multiRow'
        },
        onCellValueChanged: params => {
            if (params.colDef.field === 'Category') {
                main_category_update_main(params.newValue, params.data.category_id)
            }

        }

    }


    const myGridElement = document.querySelector('#myGridcategories');
    gridApi = agGrid.createGrid(myGridElement, gridOptions, gridOptionMainCategories);


    fetchcategories().then((category_list) => {
        gridApi.setGridOption('rowData', category_list)
    });


    const myGridElementMainCategories = document.querySelector('#myGridmaincategories');
    gridApiMainCategories = agGrid.createGrid(myGridElementMainCategories, gridOptionMainCategories);


    fetchmaincategories().then((category_list) => {
        gridApiMainCategories.setGridOption('rowData', category_list)
    });
}
initGrid();


document.getElementById('deleteallcategory').addEventListener('click', () => {
    const selectedData = gridApi.getSelectedRows().map(row => row.category_id);
    console.log(selectedData);
    confirm_delete(selectedData);
});

document.getElementById('deleteallmaincategory').addEventListener('click', () => {
    const selectedData = gridApiMainCategories.getSelectedRows().map(row => row.category_id);
    console.log(selectedData);
    main_confirm_delete(selectedData);
});


async function submitmaincategory(newCategory){
    
    const response = await fetch('/target/main_category_add/', {
        method: 'PUT',
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            "Content-Type": "application/json",
        },
        
        body: JSON.stringify({newCategory}),
    });
    console.log(newCategory)
    window.location.reload();
}

document.getElementById('sendButton').addEventListener('click',()=>{
    const main_category_get = document.getElementById('main-category-value').value;
    submitmaincategory(main_category_get)
})