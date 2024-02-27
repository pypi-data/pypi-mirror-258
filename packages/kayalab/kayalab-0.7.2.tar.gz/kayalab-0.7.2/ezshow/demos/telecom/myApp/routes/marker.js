var fs = require('fs');
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

   let imput = req.body;
   let url = config.db.url + '/api/v2/table/%2Fukcloud%2Fmarkers%2F';
   console.log(url);
   try {
        fetch( url, {
            method: 'GET',
            agent: httpsAgent,
            headers: {
              'Content-Type': 'application/json',
              'Authorization': 'Basic ' + Buffer.from(config.db.user).toString('base64')
            }
        })
        .then( response => response.json() )
        .then ( json => res.json(json) )
        .catch(err => console.error(err));

   } catch (err) {
     console.log(err);
     res.status(500).send(err);
   }
});

module.exports = router;
