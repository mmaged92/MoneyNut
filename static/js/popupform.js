function togglePopup() {
    const overlay = document.getElementById('popupOverlay');
    overlay.classList.toggle('show');
}


document.getElementById("save_btn").addEventListener("click", () => {
    const Date_column_name = document.getElementById("Date_column_name").value;
    const Description_column_name = document.getElementById("Description_column_name").value;
    const Amount_column_name = document.getElementById("Amount_column_name").value;
    const account_name_mapping = document.getElementById("account_name_mapping").value;
    file_mapping_fn(Date_column_name, Description_column_name, Amount_column_name, account_name_mapping);
});

async function file_mapping_fn(Date_column_name, Description_column_name, Amount_column_name, account_name_mapping) {
    const response = await fetch('/trans/file_mapping/', {
        method: 'POST',
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ Date_column_name, Description_column_name, Amount_column_name, account_name_mapping }),
    })

    


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

// async function mapping_required(){
    
//     const reponse = await fetch('trans/', { method: 'GET' });

//     if (data.mapping_required) {
//         togglePopup();
//         return;
//     }

// }