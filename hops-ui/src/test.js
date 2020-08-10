var http = require('http');

var data = {
  items: [{
    HostID: '1',
    hostName: 'game1',
    os: 'CentOS7.5',
    status: '运行中',
    configuration: '4核8G 500G',
    innerIP: '10.0.0.18',
    outerIP: '134.11.23.145',
    product: '封神纪元',
    cloud:'腾讯云',
    region:'广州四区',
    createTime:'2020-2-24'
  }]}
var str = JSON.stringify(data)

http.createServer(function (request, response) {

    // 发送 HTTP 头部 
    // HTTP 状态值: 200 : OK
    // 内容类型: text/plain
    response.writeHead(200, {'Content-Type': 'text/plain; charset=utf-8'});

    // 发送响应数据 "Hello World"
    response.end(str);
}).listen(8888);

// 终端打印如下信息
console.log('Server running at http://127.0.0.1:8888/');