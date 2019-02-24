const express = require('express')
const app = express()
const port = 80
app.engine('html', require('ejs').renderFile);
app.set('view engine', 'html');

app.get('/', (req, res) => {
    res.render("index.ejs")
})

app.get('/login', (req, res) => {
    res.render('login.ejs')
})

app.get('/:clientid/services', (req, res) => {
    var clientid = req.params.clientid;
    
})

app.get('/:clientid/services/:serviceid', (req, res) => {
    var clientid = req.params.clientid;
    var serviceid = req.params.serviceid;
    res.render('service.ejs', {clientid: clientid, serviceid: serviceid})
})

app.listen(port, () => console.log("STARTED"))