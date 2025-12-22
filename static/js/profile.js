

document.getElementById("sumbit_button").addEventListener("click", ()=>{
    const first_name_data = document.getElementById("first_name_new").value;
    const last_name_data = document.getElementById("last_name_new").value;
    // const BD = document.getElementById("BD").value;
    const MS = document.getElementById("MS").value;
    const GENDER = document.getElementById("GENDER").value;
    const JT = document.getElementById("JT").value;
    const PN = document.getElementById("PN").value;
    const AD = document.getElementById("AD").value;
    const country = document.getElementById("country").value;
    const Region = document.getElementById("Region").value;
    const ZPC = document.getElementById("ZPC").value;
    const email = document.getElementById("email").value;
    console.log(GENDER)
    console.log(last_name_data)
    User_date_update(first_name_data,last_name_data,MS,GENDER,JT,PN,AD,country,Region,ZPC,email);
});




async function User_date_update(first_name_data,last_name_data,MS,GENDER,JT,PN,AD,country,Region,ZPC,email) {
    const response = await fetch('/profile/user_update/', {
        method: 'PUT',
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            "Content-Type": "application/json",
        },
        body: JSON.stringify({first_name_data,last_name_data,MS,GENDER,JT,PN,AD,country,Region,ZPC,email}),
    })
    console.log(last_name_data)
    
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


const bd = document.getElementById('BD');

bd.addEventListener('focus', () => {
    bd.type = 'date';
});