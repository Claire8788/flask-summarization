<template>
    <div>
      <el-button type="button" @click="startRecordAudio">开始录音</el-button>
      <h3>录音时长：{{ recorder.duration.toFixed(4) }}</h3>
      <br />
      <el-button type="button" @click="stopRecordAudio">停止录音</el-button>
      <el-button type="button" @click="playRecordAudio">播放录音</el-button>
      <el-button type="button" @click="getPCBRecordAudioData"
        >获取PCB录音数据</el-button
      >
      <el-button type="button" @click="downloadPCBRecordAudioData"
        >下载PCB录音文件</el-button
      >
      <el-button type="button" @click="getWAVRecordAudioData"
        >获取WAV录音数据</el-button
      >
      <el-button type="button" @click="downloadWAVRecordAudioData"
        >下载WAV录音文件</el-button
      >
      <el-button type="button" @click="uploadWAVData">上传WAV录音数据</el-button>
      <br />
    </div>
  </template>
   
  <script>
  import Recorder from "js-audio-recorder";
  import { uploadWavData } from "@/api/system/audioRecorder";
  export default {
    name: "audioRecorder",
    data() {
      return {
        recorder: new Recorder({
          sampleBits: 16, // 采样位数，支持 8 或 16，默认是16
          sampleRate: 16000, // 采样率，支持 11025、16000、22050、24000、44100、48000，根据浏览器默认值，我的chrome是48000
          numChannels: 1, // 声道，支持 1 或 2， 默认是1
          // compiling: false,(0.x版本中生效,1.x增加中)  // 是否边录边转换，默认是false
        }),
      };
    },
    mounted() {},
    methods: {
      //开始录音
      startRecordAudio() {
        Recorder.getPermission().then(
          () => {
            console.log("开始录音");
            this.recorder.start(); // 开始录音
          },
          (error) => {
            this.$message({
              message: "请先允许该网页使用麦克风",
              type: "info",
            });
            console.log(`${error.name} : ${error.message}`);
          }
        );
      },
      //停止录音
      stopRecordAudio() {
        console.log("停止录音");
        this.recorder.stop();
      },
      //播放录音
      playRecordAudio() {
        console.log("播放录音");
        this.recorder.play();
      },
      //获取PCB录音数据
      getPCBRecordAudioData() {
        var pcmBlob = this.recorder.getPCMBlob();
        console.log(pcmBlob);
      },
      //获取WAV录音数据
      getWAVRecordAudioData() {
        var wavBlob = this.recorder.getWAVBlob();
        console.log(wavBlob);
      },
      //下载PCB录音文件
      downloadPCBRecordAudioData() {
        this.recorder.downloadPCM("badao");
      },
      //下载WAV录音文件
      downloadWAVRecordAudioData() {
        this.recorder.downloadWAV("badao");
      },
      //上传wav录音数据
      uploadWAVData() {
        var wavBlob = this.recorder.getWAVBlob();
        // 创建一个formData对象
      var formData = new FormData()
        // 此处获取到blob对象后需要设置fileName满足当前项目上传需求，其它项目可直接传把blob作为file塞入formData
        const newbolb = new Blob([wavBlob], { type: 'audio/wav' })
        //获取当时时间戳作为文件名
        const fileOfBlob = new File([newbolb], new Date().getTime() + '.wav')
        formData.append('file', fileOfBlob)
        uploadWavData(formData).then((response) => {
          console.log(response);
        });
      },
    },
    watch: {},
  };
  </script>
   
  <style scoped lang="scss">
  </style>