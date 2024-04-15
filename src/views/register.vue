<template>
    <div class="register-wrap">
      <div class="ms-register">
        <div class="ms-title">注册新账号</div>
        <el-form :model="param" :rules="rules" ref="register" label-width="0px" class="ms-content">
          <el-form-item prop="username">
            <el-input v-model="param.username" placeholder="Username">
              <template #prepend>
                <el-button :icon="User"></el-button>
              </template>
            </el-input>
          </el-form-item>
          <el-form-item prop="email">
            <el-input v-model="param.email" placeholder="Email">
              <template #prepend>
                <el-button :icon="User"></el-button>
              </template>
            </el-input>
          </el-form-item>
          <el-form-item prop="password">
            <el-input
              type="password"
              placeholder="Password"
              v-model="param.password"
              @keyup.enter="submitForm(register)"
            >
              <template #prepend>
                <el-button :icon="User"></el-button>
              </template>
            </el-input>
          </el-form-item>
          <!-- <el-form-item prop="confirmPassword">
            <el-input
              type="password"
              placeholder="Confirm Password"
              v-model="param.confirmPassword"
              @keyup.enter="submitForm(register)"
            >
              <template #prepend>
                <el-button :icon="Lock"></el-button>
              </template>
            </el-input>
          </el-form-item> -->
          <div class="register-btn">
            <el-button type="primary" @click="submitForm(register)">注册</el-button>
          </div>
        </el-form>
      </div>
    </div>
</template>

<script setup lang="ts" name="register">
import { ref, reactive, defineProps, onMounted } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';
import { ElMessage } from 'element-plus';
import type { FormInstance, FormRules } from 'element-plus';
import { Lock, User} from '@element-plus/icons-vue';

interface RegisterInfo {
  username: string;
  email: string;
  password: string;
  confirmPassword: string;
}

const router = useRouter();
const props = defineProps<RegisterInfo>();
const param = reactive<RegisterInfo>({
  username: props.username || '',
  email: props.email || '',
  password: props.password || '',
  confirmPassword: props.confirmPassword || '',
});

const rules: FormRules = {
    username: [
        {
            required: true,
            message: '请输入用户名',
            trigger: 'blur',
        },
    ],
    email: [
        {
            required: true,
            message: '请输入邮箱',
            trigger: 'blur',
        },
        // {
        //     type: 'email',
        //     message: '请输入有效的邮箱地址',
        //     trigger: ['blur', 'change'],
        // },
    ],
    password: [
        { required: true, message: '请输入密码', trigger: 'blur' },
        // { min: 6, max: 20, message: '密码长度为6-20位', trigger: 'blur' },
    ],
};

const register = ref<FormInstance>();

const submitForm = async (formEl: FormInstance | undefined) => {
  if (!formEl) return;

  const valid = await formEl.validate();
  if (!valid) return;

//   try {
//     const response = await axios.post('http://127.0.0.1:5000/register', {
//       username: param.username,
//       email: param.email,
//       password: param.password,
//     });

//     if (response.status === 200) {
//       ElMessage.success('注册成功');
//       router.push('/login');
//     } else {
//       ElMessage.error('注册失败，请稍后重试');
//     }
//   } catch (error) {
//     console.error('注册失败：', error);
//     ElMessage.error('注册失败，请稍后重试');
//   }
// };
  try {
    const response = await axios.post('http://127.0.0.1:5000/register', {
      username: param.username,
      email: param.email,
      password: param.password,
    });

    if (response.status === 200) {
      ElMessage.success('注册成功');
      router.push('/login');
    } else {
      ElMessage.error(response.data.message);
    }
  } 
//   catch (error) {
//     console.error('注册失败：', error);
//     ElMessage.error('注册失败，请稍后重试');
    
//   }
    catch (error) {
    console.error('注册失败：', error);
    if (error.response && error.response.data && error.response.data.message) {
        ElMessage.error(error.response.data.message);
    } else {
        ElMessage.error('注册失败，请稍后重试');
    }
    }

};
</script>

<style scoped>
.register-wrap {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
  background-image: url(../assets/img/register_bg.jpg);
  background-size: 100%;
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
.ms-register {
  width: 350px;
  border-radius: 5px;
  background: #fff;
}
.ms-content {
  padding: 10px 30px 30px;
}
.register-btn {
  text-align: center;
}
.register-btn button {
  width: 100%;
  height: 36px;
  margin-bottom: 10px;
}
</style>
