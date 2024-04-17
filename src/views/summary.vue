<template>
  <div class="summary-wrap">
    <div class="ms-summary">
      <div class="ms-title">会议摘要文本</div>
      <el-form :model="param" :rules="rules" ref="summary" label-width="130px" class="ms-content">
                <!-- 添加一个按钮来启动/停止录音 -->
        <el-row>
          <!-- 开始录音按钮 -->
          <!-- <el-col :span="12">
            <div class="summary-btn" style="margin-top: 20px;">
               <el-button type="primary" @click="startRecording" :disabled="isRecording">Start Recording</el-button>
              <el-button type="danger" @click="stopRecording" :disabled="!isRecording">Stop Recording</el-button>

              <audio v-if="audioUrl" controls :src="audioUrl"></audio>
              
            </div>
          </el-col> -->
          <!-- 上传音频文件的组件 -->
          <el-col :span="12">
              <el-form-item label="Upload Audio File" style="margin-bottom: 0;">
                <el-upload
                  class="upload-demo"
                  action="http://127.0.0.1:5000/upload"
                  :show-file-list="false"
                  :on-success="handleUploadSuccess"
                  :before-upload="beforeUpload"
                >
                <el-button type="success" icon="el-icon-upload">Click to Upload</el-button>
              </el-upload>
            </el-form-item>
          </el-col>
          
        </el-row>


        <el-form-item label="Input Text" prop="input_text" style="margin-top: 20px;">
          <el-input v-model="param.input_text" type="textarea" :rows="13" placeholder="Please enter input text"></el-input>
        </el-form-item>

        <el-row style="margin-top: 80px;">
          <el-col :span="8">
            <el-form-item label="Number of Words in Summary" prop="num_words">
              <el-slider v-model="param.num_words" :min="50" :max="200" :step="10"></el-slider>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="Number of Beams" prop="num_beams" style="margin-left: 10px;">
              <el-slider v-model="param.num_beams" :min="1" :max="20" :step="1"></el-slider>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="Model" prop="model">
              <el-select v-model="param.model" placeholder="Please select model">
                <el-option label="BART" value="bart"></el-option>
                <el-option label="T5" value="t5"></el-option>
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <div class="summary-btn" style="margin-top: 80px;">
          <el-button type="primary" @click="generateSummary">Generate Summary</el-button>
        </div>
      </el-form>

      <el-form-item label="Summary result" >
        <el-input v-model="summaryContent" type="textarea" :rows="7" :readonly="true" placeholder="Summary result..."></el-input>
      </el-form-item>

    </div>

  </div>
</template>


<script>
import axios from 'axios';
import { ElMessage } from 'element-plus';

export default {
  data() {
    return {
      param: {
        input_text: '',
        num_words: 50,
        num_beams: 4,
        model: 'bart',
        username: localStorage.getItem('ms_username')
      },
      rules: {
        input_text: [{ required: true, message: 'Please enter input text', trigger: 'blur' }]
      },
      summaryContent: '',
      isRecording: false,
      isMicrophoneAllowed: false,
      mediaRecorder: null,
      audioChunks: [],
      audioData: null,
      audioUrl: null, // 添加一个新的数据项来存储音频文件的 URL
    };
  },
  methods: {
    async generateSummary() {
      try {
        const response = await axios.post('http://127.0.0.1:5000/predict', this.param);
        if (response.status === 200) {
          this.summaryContent = response.data.response.summary;
          ElMessage.success('Summary generated successfully');
        } else {
          ElMessage.error('Failed to generate summary');
        }
      } catch (error) {
        console.error('Error generating summary:', error);
        ElMessage.error('Failed to generate summary');
      }
    },
    handleUploadSuccess(response, file) {
      if (response.text) {
        this.param.input_text += ' ' + response.text;
        ElMessage.success('Audio file uploaded and transcribed successfully');
      } else {
        ElMessage.error('Transcript not found in response');
      }
    },
    beforeUpload(file) {
      const isAudio = file.type === 'audio/mpeg' || file.type === 'audio/wav';
      if (!isAudio) {
        ElMessage.error('You can only upload audio files!');
        return false;
      }
      return true;
    },
    async startRecording() {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        this.isMicrophoneAllowed = true;
        this.mediaRecorder = new MediaRecorder(stream);
        this.audioChunks = [];

        this.mediaRecorder.addEventListener('dataavailable', event => {
          this.audioChunks.push(event.data);
        });

        this.mediaRecorder.addEventListener('stop', () => {
          const audioBlob = new Blob(this.audioChunks, { type: 'audio/wav' });
          this.audioData = audioBlob;
          this.isRecording = false;
          this.uploadAudio();
        });

        this.mediaRecorder.start();
        this.isRecording = true;
      } catch (error) {
        console.error('Error accessing microphone:', error);
        ElMessage.error('Failed to access microphone');
      }
    },
    // stopRecording() {
    //   if (this.mediaRecorder && this.isRecording) {
    //     this.mediaRecorder.stop();
    //   }
    // },
//     stopRecording() {
//   if (this.mediaRecorder && this.isRecording) {
//     this.mediaRecorder.stop();
//     this.isRecording = false;
//   }
// },
stopRecording() {
      if (this.mediaRecorder) {
        this.mediaRecorder.stop();
        this.mediaRecorder.onstop = async () => {
          // 将 Blob 对象转换成 URL，并赋值给 audioUrl
          this.audioUrl = URL.createObjectURL(new Blob(this.audioChunks));
          this.isRecording = false;
          // 如果需要上传到服务器，请继续执行上传逻辑
        };
      }
    },
    // async uploadAudio() {
    //   try {
    //     const formData = new FormData();
    //     formData.append('audio', this.audioData);
    //     const response = await axios.post('http://127.0.0.1:5000/upload', formData, {
    //       headers: {
    //         'Content-Type': 'multipart/form-data'
    //       }
    //     });
    //     if (response.status === 200) {
    //       this.param.input_text += response.data.text;
    //       ElMessage.success('Audio file uploaded and transcribed successfully');
    //     } else {
    //       ElMessage.error('Failed to upload audio file');
    //     }
    //   } catch (error) {
    //     console.error('Error uploading audio file:', error);
    //     ElMessage.error('Failed to upload audio file');
    //   }
    // }
    async uploadAudio() {
  try {
    const formData = new FormData();
    formData.append('audio', this.audioData);
    const response = await axios.post('http://127.0.0.1:5000/upload_1', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
    if (response.status === 200) {
      this.param.input_text += response.data.text;
      ElMessage.success('Audio file uploaded and transcribed successfully');
    } else {
      ElMessage.error('Failed to upload audio file');
    }
  } catch (error) {
    console.error('Error uploading audio file:', error); // 添加这行代码来打印错误信息
    ElMessage.error('Failed to upload audio file');
  }
}
  }
};
</script>
<!-- <script >
import axios from 'axios';
import { ElMessage } from 'element-plus';

export default {
  data() {
    return {
      param: {
        input_text: '',
        num_words: 50,
        num_beams: 4,
        model: 'bart',
        username: localStorage.getItem('ms_username')

      },
      rules: {
        input_text: [
          { required: true, message: 'Please enter input text', trigger: 'blur' }
        ]
      },
      summaryContent: '',
      // isRecording: false,
      // websocket: null // 将 websocket 声明为组件的数据属性
        // 语音转文字功能（实时）
        isRecording: false,
        mediaRecorder: null,
        audioChunks: [],
        audioData: null, // 用于存储录音数据
        // websocket: null,

    };
  },
  methods: {
    async generateSummary() {
      try {
        const response = await axios.post('http://127.0.0.1:5000/predict', this.param);
        if (response.status === 200) {
          this.summaryContent = response.data.response.summary;
          ElMessage.success('Summary generated successfully');
        } else {
          ElMessage.error('Failed to generate summary');
        }
      } catch (error) {
        console.error('Error generating summary:', error);
        ElMessage.error('Failed to generate summary');
      }
    },

    handleUploadSuccess(response, file) {
      if (response.text) {
        this.param.input_text += ' ' + response.text;
        ElMessage.success('Audio file uploaded and transcribed successfully');
      } else {
        ElMessage.error('Transcript not found in response');
      }
    },
      beforeUpload(file) {
        const isAudio = file.type === 'audio/mpeg' || file.type === 'audio/wav';
        if (!isAudio) {
          ElMessage.error('You can only upload audio files!');
          return false;
        }
        return true;
      },



    startRecording() {
      // 在开始录音时，设置录音状态为 true
      this.isRecording = true;
      // 在这里开始录音，具体实现根据你的录音库或服务来
      // 假设录音库提供了一个 startRecording 方法，并在录音结束后返回录音数据
      startRecording().then(data => {
        // 将录音数据存储到 audioData 中
        this.audioData = data;
        // 录音结束后，设置录音状态为 false
        this.isRecording = false;
      }).catch(error => {
        console.error('Error starting recording:', error);
        // 出错时，也要设置录音状态为 false
        this.isRecording = false;
      });
    },
    stopRecording() {
      // 在停止录音时，设置录音状态为 false
      this.isRecording = false;
      // 在这里停止录音，具体实现根据你的录音库或服务来
      // 假设录音库提供了一个 stopRecording 方法，并返回录音数据
      stopRecording().then(data => {
        // 将录音数据存储到 audioData 中
        this.audioData = data;
        // 录音结束后，调用上传录音文件的方法
        this.uploadAudio();
      }).catch(error => {
        console.error('Error stopping recording:', error);
        // 出错时，也要设置录音状态为 false
        this.isRecording = false;
      });
    },
    async uploadAudio() {
    try {
      // 创建一个 FormData 对象
      const formData = new FormData();
      // 将录音数据添加到 FormData 中，键名为 'audio'
      formData.append('audio', this.audioData);
      // 发送 POST 请求到后端，上传录音文件
      const response = await axios.post('http://127.0.0.1:5000/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      // 处理上传成功后的响应
      if (response.status === 200) {
        // 将上传文件的转录文本添加到输入框中
        this.param.input_text += response.data.text;
        ElMessage.success('Audio file uploaded and transcribed successfully');
      } else {
        ElMessage.error('Failed to upload audio file');
      }
    } catch (error) {
      console.error('Error uploading audio file:', error);
      ElMessage.error('Failed to upload audio file');
    }
  }
      // startRecording() {
      // if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
      //   navigator.mediaDevices.getUserMedia({ audio: true })
      //     .then(stream => {
      //       this.mediaRecorder = new MediaRecorder(stream);
      //       this.mediaRecorder.start();
      //       this.isRecording = true;

      //       this.audioChunks = [];
      //       // this.mediaRecorder.ondataavailable = event => {
      //       //   if (this.isRecording) {
      //       //     this.websocket.send(event.data);
      //       //   }
      //       // };
      //       this.mediaRecorder.ondataavailable = event => {
      //       if (this.isRecording) {
      //         // 此处创建一个 FileReader 来读取 Blob 数据
      //         let reader = new FileReader();
      //         reader.onload = () => {
      //           // 读取完毕后，发送 ArrayBuffer 数据
      //           this.websocket.send(JSON.stringify({ event: 'audio_data', data: reader.result }));
      //         };
      //         reader.readAsArrayBuffer(event.data);
      //       }
      //     };

      //       this.mediaRecorder.onstart = () => {
      //         this.openWebSocket();
      //       };
      //     })
      //     .catch(error => {
      //       console.error('Error accessing the microphone', error);
      //     });
      // }
      // },
    // stopRecording() {
    //   if (this.mediaRecorder) {
    //     this.mediaRecorder.stop();
    //     this.isRecording = false;
    //     if (this.websocket) {
    //       this.websocket.close();
    //     }
    //   }
    // },
    // openWebSocket() {
    //   // this.websocket = new WebSocket('ws://127.0.0.1:5000/audio_data');
    //   // this.websocket = new WebSocket('ws://127.0.0.1:5000/socket.io/?EIO=3&transport=websocket');
    //   this.websocket = new WebSocket('ws://127.0.0.1:5000/socket.io/?EIO=3&transport=websocket');
    //   this.websocket.binaryType = 'arraybuffer';  // 确保以二进制形式发送数据

    //   this.websocket.onopen = () => {
    //     console.log('WebSocket Connected');
    //   };
    //   this.websocket.onmessage = (event) => {
    //     console.log('Received:', event.data);
    //   };
    //   this.websocket.onerror = (error) => {
    //     console.error('WebSocket Error:', error);
    //   };
    //   this.websocket.onclose = () => {
    //     console.log('WebSocket Disconnected');
    //   };
    // },
  },
  // beforeDestroy() {
  //   if (this.mediaRecorder && this.isRecording) {
  //     this.mediaRecorder.stop();
  //   }
  //   if (this.websocket) {
  //     this.websocket.close();
  //   }
  // }

  }

  

</script> -->


<style scoped>
.summary-wrap {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
  background-color: #f5f5f5;
}
.ms-title {
  line-height: 50px;
  text-align: center;
  font-size: 20px;
  color: #333;
  font-weight: bold;
  padding-top: 10px;
}
.ms-summary {

  border-radius: 10px;
  background: #fff;
  margin-bottom: 10px;
  padding: 10px;
  width: 100%; 
  max-width: 1500px; 
}
.ms-content {
  padding: 20px;
}
.summary-btn {
  text-align: center;
}
/* .summary-result {
  width: 85%; 
  max-width: 1500px; 
  margin: 0 auto;
} */
/* .summary-result h3 {
  margin-bottom: 10px;
  text-align: center;
} */
</style>