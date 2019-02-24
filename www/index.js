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

app.listen(port, () => console.log("STARTED"))