// Get the input field
var password_input = document.getElementById("login-password-field");

password_input.addEventListener("keyup", function (event) {
  if (event.keyCode === 13) {
    event.preventDefault();
    document.getElementById("login-button").click();
  }
});

var registration_input = document.getElementById("reg-password-field")

registration_input.addEventListener("keyup", function (event) {
  if (event.keyCode === 13) {
    event.preventDefault();
    document.getElementById("register-button").click()
  }
})

function login() {
  username = document.getElementById('login-username').value;
  password = document.getElementById('login-password-field').value;
  if (username == "" || password == "") {
    alert("Please fill out the fields entirely")
    return
  }
  axios.post('http://localhost:3141/endpoints/login', {
    username: username,
    password: password
  })
    .then((response) => {
      document.cookie = "userid=" + String(response['data']['id']);
      document.cookie = "token=" + String(response['data']['token']);
    })
    .catch(function (error) {
      console.log(error);
    });
}

function register() {
  email = document.getElementById('reg-email-address').value;
  username = document.getElementById('reg-username').value;
  password = document.getElementById('reg-password-field').value;
  if (email == "" || username == "" || password == "") {
    alert("Please fill out the fields entirely.")
    return
  }
  axios.post('http://localhost:3141/endpoints/register', {
    email: email,
    username: username,
    password: password
  })
    .then(function (response) {
      document.cookie = "userid=" + String(response['id']);
      document.cookie = "token=" + String(response['token']);
      console.log(response);
    })
    .catch(function (error) {
      console.log(error);
    });
}