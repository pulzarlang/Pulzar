var fs = require('fs');
const http = require('http');
const hostname = '127.0.0.1';
const port = 3000;
var output = "";
fs.readFile('web.txt', 'utf8', function(err, data) {
    if (err) throw err;
    output = data;
});
const server = http.createServer((req, res) => {
  console.log(req);
  res.statusCode = 200;
  res.setHeader('Content-Type', 'text/html');
  res.write(output);
  res.end();
});

server.listen(port, hostname, () => {
  console.log(`Server running at http://${hostname}:${port}/`);
});