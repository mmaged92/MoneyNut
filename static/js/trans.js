function showhide() {
  const new_bank_add = document.getElementById('new_bank_add');
  if (new_bank_add.style.display === 'none') {
    new_bank_add.style.display = 'inline';
  } else {
    new_bank_add.style.display = 'none';
  }
}

function showhidefilter() {
  const filter = document.getElementById('filter');
  if (filter.style.display === 'none') {
    filter.style.display = 'inline';
  } else {
    filter.style.display = 'none';
  }
}

//fetch all transaction data
async function fetchData() {
  try {
    const response = await fetch(window.moneyNutUrl('/trans/all'));
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const transaction_list = await response.json();
    return transaction_list;
  } catch (error) {
    console.error('Error fetching data:', error);
    return [];
  }
}

//get all categories
async function fetchcategory() {
  const response = await fetch(window.moneyNutUrl('/trans/keyword/category'));
  const category_list = await response.json();
  return category_list;
}

//get ios
async function fetchio() {
  const response = await fetch(window.moneyNutUrl('/trans/io_get'));
  const io_list = await response.json();
  return io_list;
}

//get accounts
async function fetchaccounts() {
  const response = await fetch(window.moneyNutUrl('/trans/account_get'));
  const account_list = await response.json();
  return account_list;
}

//update Description
async function description_update(new_value, transaction_id) {
  const isConfirmed = confirm('are you sure?');
  if (!isConfirmed) return;

  const response = await fetch(
    window.moneyNutUrl('/trans/descriptionupdate/'),
    {
      method: 'PUT',
      headers: {
        'X-CSRFToken': getCookie('moneynut_csrftoken'),
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ new_value, transaction_id }),
    },
  );
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  const result = await response.json();
  console.log(result);
  window.location.reload();
}

//update Date
async function date_update(new_value, transaction_id) {
  const isConfirmed = confirm('are you sure?');
  if (!isConfirmed) return;

  const response = await fetch(window.moneyNutUrl('/trans/date_update/'), {
    method: 'PUT',
    headers: {
      'X-CSRFToken': getCookie('moneynut_csrftoken'),
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ new_value, transaction_id }),
  });
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  const result = await response.json();
  console.log(result);
  window.location.reload();
}

//update amount
async function amount_update(new_value, transaction_id) {
  const isConfirmed = confirm('are you sure?');
  if (!isConfirmed) return;

  const response = await fetch(window.moneyNutUrl('/trans/amount_update/'), {
    method: 'PUT',
    headers: {
      'X-CSRFToken': getCookie('moneynut_csrftoken'),
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ new_value, transaction_id }),
  });
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  const result = await response.json();
  console.log(result);
  window.location.reload();
}

//update IO
async function IO_update(new_value, transaction_id) {
  const isConfirmed = confirm('are you sure?');
  if (!isConfirmed) return;

  const response = await fetch(window.moneyNutUrl('/trans/IO_update/'), {
    method: 'PUT',
    headers: {
      'X-CSRFToken': getCookie('moneynut_csrftoken'),
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ new_value, transaction_id }),
  });
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  const result = await response.json();
  console.log(result);
  window.location.reload();
}

//update category
async function category_update_trans(new_value, category_id, transaction_id) {
  const isConfirmed = confirm('are you sure?');
  if (!isConfirmed) return;

  const response = await fetch(window.moneyNutUrl('/trans/category_update/'), {
    method: 'PUT',
    headers: {
      'X-CSRFToken': getCookie('moneynut_csrftoken'),
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ new_value, category_id, transaction_id }),
  });
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  const result = await response.json();
  console.log(result);
  window.location.reload();
}

//update Account
async function account_update(new_value, Account_id, transaction_id) {
  const isConfirmed = confirm('are you sure?');
  if (!isConfirmed) return;

  const response = await fetch(window.moneyNutUrl('/trans/account_update/'), {
    method: 'PUT',
    headers: {
      'X-CSRFToken': getCookie('moneynut_csrftoken'),
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ new_value, Account_id, transaction_id }),
  });
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  const result = await response.json();
  console.log(result);
  window.location.reload();
}

async function confirm_delete(transaction_id) {
  // console.log(input)
  const isConfirmed = confirm('are you sure?');
  if (!isConfirmed) return;

  // const reqBody = {keyword_id}
  const response = await fetch(window.moneyNutUrl('/trans/delete/'), {
    method: 'DELETE',
    headers: {
      'X-CSRFToken': getCookie('moneynut_csrftoken'),
      'Content-Type': 'application/json',
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
      if (cookie.substring(0, name.length + 1) === name + '=') {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
// function exportGridData() {

//     gridOptions.gridApi.exportDataAsExcel();

// }
async function initGrid() {
  const myCategoryList = await fetchcategory();
  const myIOlist = await fetchio();
  const myAccountslist = await fetchaccounts();

  const gridOptions = {
    rowData: [],

    columnDefs: [
      { field: 'Description', filter: true, editable: true },
      { field: 'Date', filter: true, editable: true },
      { field: 'Amount', filter: true, editable: true },
      {
        field: 'Category',
        filter: true,
        editable: true,
        cellEditor: 'agSelectCellEditor',
        cellEditorParams: {
          values: myCategoryList,
        },
      },
      { field: 'Category_Main', filter: true },
      {
        field: 'IO',
        filter: true,
        editable: true,
        cellEditor: 'agSelectCellEditor',
        cellEditorParams: {
          values: myIOlist,
        },
      },
      { field: 'Bank', filter: true },
      {
        field: 'Account Name',
        filter: true,
        editable: true,
        cellEditor: 'agSelectCellEditor',
        cellEditorParams: {
          values: myAccountslist,
        },
      },
      { field: 'Account Number', filter: true },
      { field: 'Account Type', filter: true },
      { field: 'category_id', hide: true },
      { field: 'transaction_id', hide: true },
      { field: 'Account_id', hide: true },
      {
        field: ' ',
        cellRenderer: (params) => {
          const deleteIcon = `<i class="fa-solid fa-trash"  onclick="confirm_delete(${params.data.transaction_id})"></i>`;
          return `${deleteIcon} `;
        },
      },
    ],
    rowSelection: {
      mode: 'multiRow',
      copySelectedRows: true,
    },
    onCellValueChanged: (params) => {
      if (params.colDef.field === 'Description') {
        description_update(params.newValue, params.data.transaction_id);
      }
      if (params.colDef.field === 'Date') {
        date_update(params.newValue, params.data.transaction_id);
      }
      if (params.colDef.field === 'Amount') {
        amount_update(params.newValue, params.data.transaction_id);
      }
      if (params.colDef.field === 'IO') {
        IO_update(params.newValue, params.data.transaction_id);
      }
      if (params.colDef.field === 'Account Name') {
        account_update(
          params.newValue,
          params.data.Account_id,
          params.data.transaction_id,
        );
      }

      if (params.colDef.field === 'Category') {
        category_update_trans(
          params.newValue,
          params.data.category_id,
          params.data.transaction_id,
        );
      }
    },
  };

  const myGridElement = document.querySelector('#myGridtrans');
  gridApi = agGrid.createGrid(myGridElement, gridOptions);

  fetchData().then((transaction_list) => {
    gridApi.setGridOption('rowData', transaction_list);
  });
}
initGrid();

document.getElementById('deletealltrans').addEventListener('click', () => {
  const selectedData = gridApi
    .getSelectedRows()
    .map((row) => row.transaction_id);
  console.log(selectedData);
  confirm_delete(selectedData);
});

document.getElementById('reloadpage').addEventListener('click', async () => {
  refresh_page();
  console.log('re');
});

async function refresh_page() {
  const response = await fetch(
    window.moneyNutUrl('/trans/refresh_categorization/'),
    {
      method: 'PUT',
      headers: {
        'X-CSRFToken': getCookie('moneynut_csrftoken'),
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ refresh: 'refresh' }),
    },
  );
  window.location.reload();
}

function validateForm() {
  // const file_path = document.forms["trans_entry"]["file_path"].value;
  // const card_type = document.forms["trans_entry"]["card_type"].value;
  // const account_name = document.forms["trans_entry"]["account_name"].value;
  // const Date_column_name = document.forms["trans_entry"]["Date_column_name"].value;
  // const Description_column_name = document.forms["trans_entry"]["Description_column_name"].value;
  // const Amount_column_name = document.forms["trans_entry"]["Amount_column_name"].value;

  const alertBox = document.getElementById('alart-file').style;
  alertBox.display = 'block';
  setTimeout(() => {
    alertBox.display = 'none';
  }, 2000);
  event.preventDefault();

  // if (file_path == "" || card_type == "" || account_name == "" || Date_column_name == "" || Description_column_name == "" || Amount_column_name == "") {
  //     if (file_path == "") {
  //         alert("File must be entered");
  //     }

  //     if (card_type == "") {
  //         alert("Card type field must be filled");
  //     }

  //     if (account_name == "") {
  //         alert("Account field must be filled");
  //     }

  //     if (Date_column_name == "") {
  //         alert("Date column name field must be filled");
  //     }

  //     if (Description_column_name == "") {
  //         alert("Description column name field must be filled");
  //     }

  //     if (Amount_column_name == "") {
  //         alert("Amount column name field must be filled");
  //     }

  //     return false;
  // }
}
function validateFormSE() {
  const alertBox = document.getElementById('alart-single-e').style;
  alertBox.display = 'block';
  setTimeout(() => {
    alertBox.display = 'none';
  }, 2000);
  event.preventDefault();
}
