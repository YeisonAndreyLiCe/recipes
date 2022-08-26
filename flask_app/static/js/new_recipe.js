
form = document.getElementById('form');
form.onsubmit = function(e) {
    e.preventDefault();
    var formData = new FormData(form);
    fetch('/create/recipe', {method: 'POST', body: formData})
        .then(response => response.json())
        .then(data => {
            console.log(data);
            if (data.message == 'success') {
                window.location.href = '/recipes';
            }
            alert(data.message);
            /* var alertMessage = document.getElementById('alertMessage');
            alertMessage.innerText = data.message;
            alertMessage.classList.add('alert');
            alertMessage.classList.add('alert-danger'); */
        });
    }
