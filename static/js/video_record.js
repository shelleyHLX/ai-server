/* 音频 */
var recorder;
var audio = document.querySelector('audio');

function startRecording() {
    HZRecorder.get(function (rec) {
        recorder = rec;
        recorder.start();
    });
}


function obtainRecord() {
    var record = recorder.getBlob();
    debugger;
};

function stopRecord() {
    recorder.stop();
};

function playRecord() {
    recorder.play(audio);
};

/* 视频 */
function scamera() {
    var videoElement = document.getElementById('video1');
    var canvasObj = document.getElementById('canvas1');
    var context1 = canvasObj.getContext('2d');
    context1.fillStyle = "#ffffff";
    context1.fillRect(0, 0, 320, 240);
    context1.drawImage(videoElement, 0, 0, 320, 240);
};

function playVideo() {
    var videoElement1 = document.getElementById('video1');
    var videoElement2 = document.getElementById('video2');
    videoElement2.setAttribute("src", videoElement1);
};
