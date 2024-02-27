var fs = require('fs');
var express = require('express');
var router = express.Router();
var bodyParser = require('body-parser')

var app = express()
var jsonParser = bodyParser.json()

const config = require('../config');

router.post('/', jsonParser, function(req, res, next) {
  try {
      let input = req.body
      let sourceData = {};
      fs.readFile( config.params.markers, (err, data) => {
         if (err) throw err;
         sourceData = JSON.parse(data);

         var marker = {}
         marker.file = input.photo;
         marker.farmer = input.farmer;
         marker.upload = new Date().toLocaleDateString('en-US')
         marker.longitude = input.longitude;
         marker.latitude = input.latitude;

        sourceData.DocumentStream.push(marker);

        fs.writeFileSync( config.params.markers, JSON.stringify(sourceData));

        res.json({
          status: true,
          message: 'File is registered'
        });
    });
  } catch (err) {
     console.log(err);
     res.status(500).send(err);
  }
});

module.exports = router;
