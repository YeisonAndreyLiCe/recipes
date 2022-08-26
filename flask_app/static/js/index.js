var formLogin = document.getElementById('formLogin');


formLogin.onsubmit = function(e) {
    e.preventDefault();
    var formData = new FormData(formLogin);
    fetch('/login', {method: 'POST', body: formData})
        .then(response => response.json())
        .then(data => {
            console.log(data);
            if (data.message == 'success') {
                window.location.href = '/recipes';
            }
            var alertMessage = document.getElementById('alertMessage');
            alertMessage.innerText = data.message;
            alertMessage.classList.add('alert');
            alertMessage.classList.add('alert-danger');
        });
    }

var formRegister = document.getElementById('formRegister');

formRegister.onsubmit = function(e) {
    e.preventDefault();
    var formData = new FormData(formRegister);
    fetch('/register', {method: 'POST', body: formData})
        .then(response => response.json())
        .then(data => {
            console.log(data);
            if (data.message == 'success') {
                window.location.href = '/recipes';
            }
            var alertMessage = document.getElementById('alertMessageRegister');
            alertMessage.innerText = data.message;
            alertMessage.classList.add('alert');
            alertMessage.classList.add('alert-danger');
        });
    }