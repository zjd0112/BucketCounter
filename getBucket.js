module.exports = {
    getBucket:function() {
        var execSync = require('child_process').execSync; 
        var cmdStr = "raspistill -t 2000 -o temp/image.jpg"
        var spawnSync = require('child_process').spawnSync;
        var bucketNum = 0;

        // 拍照
        execSync(cmdStr);

        // 调用Python脚本识别
        bucketNum = spawnSync('python3', ['getBucketNum.py']);
        return bucketNum;
    }
}

