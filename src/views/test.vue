<template>
    <div class="summary-wrap">
      <div class="ms-summary">
        <div class="ms-title">会议摘要文本</div>
        <el-form :model="param" :rules="rules" ref="summary" label-width="130px" class="ms-content">
                  <!-- 添加一个按钮来启动/停止录音 -->
          <el-row>
            <!-- 开始录音按钮 -->
            <el-col :span="12">
              <div class="summary-btn" style="margin-top: 20px;">
                <el-button type="primary" v-if="!isRecording" @click="startRecording">Start Recording</el-button>
                <el-button type="danger" v-else @click="stopRecording">Stop Recording</el-button>
              </div>
            </el-col>
            <!-- 上传音频文件的组件 -->
            <el-col :span="12">
                <el-form-item label="Upload Audio File" style="margin-bottom: 0;">
                  <el-upload
                    class="upload-demo"
                    :show-file-list="false"
                    action="http://127.0.0.1:5000/upload"
                    :on-success="handleFileUpload"
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
  
  // export default {
  //   data() {
  //     return {
  //       param: {
  //         input_text: '',
  //         num_words: 50,
  //         num_beams: 4,
  //         model: 'bart',
  //         username: localStorage.getItem('ms_username')
  //       },
  //       rules: {
  //         input_text: [
  //           { required: true, message: 'Please enter input text', trigger: 'blur' }
  //         ]
  //       },
  //       summaryContent: ''
  //     };
  //   },
  //   methods: {
  //     async generateSummary() {
  //       try {
  //         const response = await axios.post('http://127.0.0.1:5000/predict', this.param);
  //         if (response.status === 200) {
  //           this.summaryContent = response.data.response.summary;
  //           ElMessage.success('Summary generated successfully');
  //         } else {
  //           ElMessage.error('Failed to generate summary');
  //         }
  //       } catch (error) {
  //         console.error('Error generating summary:', error);
  //         ElMessage.error('Failed to generate summary');
  //       }
  //     }
  //   }
  // };
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
        isRecording: false,
        websocket: null // 将 websocket 声明为组件的数据属性
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
  
      // async handleFileUpload(file) {
      //   try {
      //     const formData = new FormData();
      //     formData.append('audio', file.raw);
      //     const response = await axios.post('http://127.0.0.1:5000/upload', formData, {
      //       headers: {
      //         'Content-Type': 'multipart/form-data'
      //       }
      //     });
      //     if (response.status === 200) {
      //       this.param.input_text += response.data.transcript;
      //       ElMessage.success('Audio file uploaded successfully');
      //     } else {
      //       ElMessage.error('Failed to upload audio file');
      //     }
      //   } catch (error) {
      //     console.error('Error uploading audio file:', error);
      //     ElMessage.error('Failed to upload audio file');
      //   }
      // }
    async handleUploadSuccess(response, file, fileList) {
    if (response.status === 200) {
      // 处理上传成功后的逻辑
      if (response.data && response.data.text) {
        // 获取上传文件的转录文本并添加到 input_text 中
        this.param.input_text += response.data.text;
        ElMessage.success('Audio file uploaded successfully');
      } else {
        ElMessage.error('Transcript not found in response');
      }
    } else {
      ElMessage.error('Failed to upload audio file');
    }
  },
  
    }
  
    }
  
  </script>
  
  
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
  <template>
    <div class="summary-wrap">
      <div class="ms-summary">
        <div class="ms-title">会议摘要文本</div>
        <el-form :model="param" :rules="rules" ref="summaryForm" label-width="130px" class="ms-content">
          <el-row>
            <el-col :span="12">
              <el-form-item label="Upload Audio File">
                <el-upload
                  class="upload-demo"
                  action="http://127.0.0.1:5000/upload"
                  :on-success="handleUploadSuccess"
                  :show-file-list="false"
                  :before-upload="beforeUpload">
                  <el-button slot="trigger" type="success" icon="el-icon-upload">Click to Upload</el-button>
                </el-upload>
              </el-form-item>
            </el-col>
          </el-row>
          <el-form-item label="Input Text" prop="input_text">
            <el-input v-model="param.input_text" type="textarea" :rows="13" placeholder="Please enter input text"></el-input>
          </el-form-item>
          <el-row>
            <el-col :span="8">
              <el-form-item label="Number of Words in Summary">
                <el-slider v-model="param.num_words" :min="50" :max="200" :step="10"></el-slider>
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item label="Number of Beams">
                <el-slider v-model="param.num_beams" :min="1" :max="20" :step="1"></el-slider>
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item label="Model">
                <el-select v-model="param.model" placeholder="Please select model">
                  <el-option label="BART" value="bart"></el-option>
                  <el-option label="T5" value="t5"></el-option>
                </el-select>
              </el-form-item>
            </el-col>
          </el-row>
          <div class="summary-btn">
            <el-button type="primary" @click="generateSummary">Generate Summary</el-button>
          </div>
        </el-form>
        <el-form-item label="Summary result">
          <el-input v-model="summaryContent" type="textarea" :rows="7" readonly placeholder="Summary result..."></el-input>
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
          num_words: 100,
          num_beams: 5,
          model: 'bart',
          username: localStorage.getItem('ms_username')
        },
        rules: {
          input_text: [{ required: true, message: 'Please enter input text', trigger: 'blur' }]
        },
        summaryContent: '',
        isRecording: false
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
          ElMessage.error('Error during summary generation');
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

    }
  };
  </script>
  
  <style scoped>
  .summary-wrap {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    background-color: #f5f5f5;
  }
  .ms-summary {
    border-radius: 10px;
    background: #fff;
    padding: 20px;
    width: 100%; 
    max-width: 1200px;
  }
  .ms-title {
    text-align: center;
    font-size: 24px;
    color: #333;
    font-weight: bold;
  }
  </style>
  