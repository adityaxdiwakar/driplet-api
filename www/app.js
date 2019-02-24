const express = require('express')
const cookieParser = require('cookie-parser');
const axios = require('axios')
const app = express()
const port = 80
app.engine('html', require('ejs').renderFile);
app.set('view engine', 'html');
app.use(cookieParser());

app.get('/', (req, res) => {
    console.log(req.cookies)
    res.render("index.ejs")
})

app.get('/login', (req, res) => {
    res.render('login.ejs')
})

app.get('/:clientid/services', (req, res) => {
    var clientid = req.params.clientid;

})

app.get('/:clientid/services/:serviceid', async (req, res) => {
    var clientid = req.params.clientid;
    var serviceid = req.params.serviceid;
    if (req.cookies.userid != clientid) {
        res.render('unavailable.ejs')
    }
    else if (req.cookies.token == undefined) {
        res.render('unavailable.ejs')
    }
    else {
        try {
            const request = await axios('http://localhost:3141/endpoints/' + clientid + '/services/' + serviceid,
                {
                    "headers": {
                        authorization: req.cookies.token
                    }
                }
            )
            res.render('service.ejs', {
                serviceid: serviceid,
                clientid: clientid,
                servicename: request.data.name,
                token: req.cookies.token,
                logservice: request.data.log_command
            })
        }
        catch (e) {
            console.error(e)
            res.render('unavailable.ejs')
        }
    }
})

app.listen(port, () => console.log("STARTED"))