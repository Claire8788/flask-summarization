<template>
  <div class="summary-wrap">
    <div class="ms-summary">
      <div class="ms-title">会议摘要文本</div>
      <el-form :model="param" :rules="rules" ref="summary" label-width="120px" class="ms-content">
        <el-form-item label="Input Text" prop="input_text">
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
        input_text: [
          { required: true, message: 'Please enter input text', trigger: 'blur' }
        ]
      },
      summaryContent: ''
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
    }
  }
};
</script>

<!-- <style scoped>
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
  width: 800px;
  border-radius: 5px;
  background: #fff;
  margin-bottom: 20px;
  padding: 20px;
}
.ms-content {
  padding: 10px;
}
.summary-btn {
  text-align: center;
}
.summary-result {
  width: 800px;
}
.summary-result h3 {
  margin-bottom: 10px;
  text-align: center;
}

</style> -->
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
