var express = require('express');
var fileUpload = require('express-fileupload');
var router = express.Router();

var app = express()

app.use(fileUpload({
    createParentPath: true
}));


/* Upload file */
router.post('/', function(req, res, next) {
  try {
   if(req.files) {
      let capture = req.files.capture
      capture.mv('/Users/fberque/Documents/myprojects/ukcloud/myApp/public/data/sawie/upload/' + capture.name);
      res.json({
        status: true,
        message: 'File is uploaded',
        name: capture.name,
        mimetype: capture.mimetype,
        size: capture.size
      });
    }
  } catch (err) {
     res.status(500).send(err);
  }
});

module.exports = router;
