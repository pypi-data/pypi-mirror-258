var express = require('express');
var router = express.Router();
var bodyParser = require('body-parser')
var fetch = require('node-fetch')

var app = express()
var jsonParser = bodyParser.json()
const https = require('https');
const config = require('../config');

const httpsAgent = new https.Agent({
      rejectUnauthorized: false,
    });

router.post('/', jsonParser, function(req, res, next) {

   const input = req.body;

   try {
       json = { 'status': 'ok'} ;
       res.json(json);

   } catch (err) {
     console.log(err);
     res.status(500).send(err);
   }
});

module.exports = router;
