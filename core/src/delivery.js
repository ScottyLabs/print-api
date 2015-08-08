/* @file delivery.js
 * @brief Single REST endpoint listening for files to be uploaded, which are
 * then passed to the converter engine.
 */
'use strict';

// Requires.
var config = require('config');

// Express setup.
var express = require('express');
var app = express();

// Turn on CORS for this endpoint.
app.use(function (req, res, next) {
  res.header('Access-Control-Allow-Origin', '*');
  res.header('Access-Control-Allow-Headers',
             'Origin, X-Requested-With, Content-Type, Accept');
  next();
});
//
// Logging setup.
var fs = require('fs');
var morgan = require('morgan');
var rotator = require('file-stream-rotator');

// Two sets of logging
// One is to STDOUT, which is the colored pretty-print.
var stdoutLogger = morgan('dev');

// The other is to a file and uses the Apache .log format
var logDir = config.get('log-dir');
if (!fs.existsSync(logDir)) {
  fs.mkdirSync(logDir);
}

var fileStream = rotator.getStream({
  filename: logDir + '/delivery-%DATE%.log',
  frequency: 'daily',
  verbose: false,
  date_format: 'YYYY-MM-DD',
});

var fileLogger = morgan('combined', {
  stream: fileStream,
});

app.use(stdoutLogger);
app.use(fileLogger);

// Multer setup.
var multer = require('multer');

var uploadDir = config.get('upload-dir');

if (!fs.existsSync(uploadDir)) {
  fs.mkdirSync(uploadDir);
}

var storage = multer.diskStorage({
  destination: function (req, file, next) {
    next(null, uploadDir);
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

// Use multer middleware.
app.post('/upload/:andrewID', upload.array('toPrint'), function (req, res) {
  res.status(200);
  res.end('OK.');
});

/* @function start
 * @brief Starts the delivery node.
 */
function start() {
  app.listen(config.get('delivery.port'));
}

module.exports = {
  start: start,
};
