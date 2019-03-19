const aliyunIot = require('aliyun-iot-device-sdk');
var bucket = require('./getBucket');

// 设置时间延时为1天
// var delay = 24*60*60*1000
var delay = 1 * 60 * 1000;

var shell_res = 0; 
var bucketNum = 0;

// 创建设备实例
const device = aliyunIot.device({
    // 激活凭证 这里替换成你自己上一步申请到的激活凭证
    productKey: 'xxxxxx',
    deviceName: 'xxxxxx',
    deviceSecret: 'xxxxxx',
});

device.on('connect', () => {
    console.log('connect successfully');
    beginRun();
});

function beginRun() {
    setInterval(function() {
        shell_res = bucket.getBucket();
        if (shell_res.status == 0) {
            bucketNum = shell_res.stdout[0] - 48;
        }
        console.log(bucketNum);

        device.postProps({
            "bucketNum": bucketNum
        });
    }, delay);
}

