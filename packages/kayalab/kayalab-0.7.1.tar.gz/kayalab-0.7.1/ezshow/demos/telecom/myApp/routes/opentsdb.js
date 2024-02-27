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

   try {
      fetch( config.mapr.opentsdb + '/api/query/exp', {
         method: 'POST',
         headers: {
            'Content-Type': 'application/json'
         },
         body: JSON.stringify(req.body) 
      })
     .then(data => {
          return data.json()
      })
      .then(data => {
          res.json(data);
       });
 
   } catch (err) {
     console.log(err);
     res.status(500).send(err);
   }
});



module.exports = router;
