// declare necessary dependencies
var express = require('express');
var http = require('http');

var app = express();
var server = http.createServer(app);

// serve static public files
app.use('/visualization', express.static('visualization'));
app.use('/parsed_dates', express.static('parsed_dates'));
app.use('/new_parsed_dates', express.static('new_parsed_dates'));
app.use('/aggregate_data', express.static('aggregate_data'));

server.listen(3000, function () {
  console.log('server running on port 3000');
});
