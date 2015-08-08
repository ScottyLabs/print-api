/* @file delivery.js
 * @brief Single REST endpoint listening for files to be uploaded, which are
 * then passed to the converter engine.
 */
'use strict';

// Requires.
var express = require('express');
var multer = require('multer');
var config = require('config');

var storage = multer.diskStorage({
  destination: function (req, file, next) {
    next(null, config.get('delivery.upload-destination'));
  },
  filename: function (req, file, next) {
    var filename = req.params.andrewID + '-';
    filename += file.originalname + '-';
    filename += Date.now() % 10000;
    next(null, filename);
  },
});

var upload = multer({
  storage: storage,
  limits: {
    fileSize: config.get('delivery.upload-max-filesize'), // 100 MB
  },
});

var app = express();

// Turn on CORS for this endpoint.
app.use(function (req, res, next) {
  res.header('Access-Control-Allow-Origin', '*');
  res.header('Access-Control-Allow-Headers',
             'Origin, X-Requested-With, Content-Type, Accept');
  next();
});

app.post('/upload/:andrewID', upload.array('toPrint'), function (req, res) {
  res.status(200);
  res.end('OK.');
});

app.get('/', function (req, res) {
  res.sendFile('test.html', { root: __dirname });
});

/* @function start
 * @brief Starts the delivery node.
 */
function start() {
  app.listen(8080);
}

module.exports = {
  start: start,
};
