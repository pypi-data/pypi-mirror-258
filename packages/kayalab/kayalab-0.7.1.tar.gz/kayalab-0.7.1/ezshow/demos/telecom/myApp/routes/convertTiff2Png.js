var express = require('express');
var fileUpload = require('express-fileupload');
var sharp = require('sharp');

var router = express.Router();
var app = express()

app.use(fileUpload({
    createParentPath: true
}));


var pngLocation = '/Users/fberque/Documents/myprojects/ukcloud/myApp/public/data/sawie/convert/';

/* Upload and convert  file */
router.post('/', function(req, res, next) {
  try {
   if(req.files) {
      let capture = req.files.capture
      //'/bd-fs-mnt/TenantShare/repo/data/sawie/mobile_uploads/'

      const filename = capture.name.substr(0, capture.name.lastIndexOf('.'));
      const destinationTIFF_File = '/Users/fberque/Documents/myprojects/ukcloud/myApp/public/data/sawie/upload/' + capture.name;

      capture.mv(destinationTIFF_File, function(err) {

        sharp(destinationTIFF_File)
           .toFile( pngLocation + filename + '.png', function(err) { 

	       if (err) return res.status(500).send(err);
     
	       res.json({
               	 status: true,
                 message: 'File is uploaded and converted',
                 name: capture.name,
                 mimetype: capture.mimetype,
                 size: capture.size
               });
           });

        });
     }
  } catch (err) {
     res.status(500).send(err);
  }
});

module.exports = router;
