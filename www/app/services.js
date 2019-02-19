function start_service() {
    axios.post('http://localhost:3141/endpoints/u2852334499/services/s2292006146/start', {})
        .then(function (response) {
            console.log(response);
        })
        .catch(function (error) {
            console.log(error);
        });
}

function stop_service() {
    axios.post('http://localhost:3141/endpoints/u2852334499/services/s2292006146/stop', {})
        .then(function (response) {
            console.log(response);
        })
        .catch(function (error) {
            console.log(error);
        });
}

function restart_service() {
    axios.post('http://localhost:3141/endpoints/u2852334499/services/s2292006146/restart', {})
        .then(function (response) {
            console.log(response);
        })
        .catch(function (error) {
            console.log(error);
        });
}

function stayDown() {
    var element = document.getElementById("output")
    element.scrollTop = element.scrollHeight;
}

log = document.getElementById('output')
console.log("Connecting to WS")
let connection = new WebSocket('ws://localhost:46079');
connection.onmessage = async function (e) {
    var text = await (new Response(e.data)).text();
    console.log(text)
    log.innerHTML += text + "<br>"
    stayDown()
};