var express = require('express');
var router = express.Router();
var bodyParser = require('body-parser')
var fetch = require('node-fetch')


var app = express()
var jsonParser = bodyParser.json()
const https = require('https');


const httpsAgent = new https.Agent({
  rejectUnauthorized: false,
});

router.post('/', jsonParser, function(req, res, next) {

   const input = req.body;
   console.log(input);
   
   try {
      fetch( 'http://localhost:3011/graphdb', {
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
