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