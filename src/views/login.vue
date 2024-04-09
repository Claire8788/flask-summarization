<template>
    <div class="login-wrap">
        <div class="ms-login">
            <div class="ms-title">会议摘要系统</div>
            <el-form :model="param" :rules="rules" ref="login" label-width="0px" class="ms-content">
                <el-form-item prop="username">
                    <el-input v-model="param.username" placeholder="username">
                        <template #prepend>
                            <el-button :icon="User"></el-button>
                        </template>
                    </el-input>
                </el-form-item>
                <el-form-item prop="password">
                    <el-input
                        type="password"
                        placeholder="password"
                        v-model="param.password"
                        @keyup.enter="submitForm(login)"
                    >
                        <template #prepend>
                            <el-button :icon="Lock"></el-button>
                        </template>
                    </el-input>
                </el-form-item>
                <div class="login-btn">
                    <el-button type="primary" @click="submitForm(login)">登录</el-button>
                </div>
                <div class="register-btn">
                    <el-button type="primary" @click="goToRegister">注册</el-button>
                </div>
                <el-checkbox class="login-tips" v-model="checked" label="记住密码" size="large" />
                <!-- <p class="login-tips">Tips : 用户名和密码随便填。</p> -->
            </el-form>
        </div>
    </div>
</template>

<script setup lang="ts">
// 引入 Vue 相关依赖和组件
import { ref, reactive } from 'vue';
import axios from 'axios'; // 引入 Axios 用于发送 HTTP 请求
import { fetchData } from '../api/index';
import { useTagsStore } from '../store/tags';
import { usePermissStore } from '../store/permiss';
import { useRouter } from 'vue-router';
import { ElMessage } from 'element-plus';
import type { FormInstance, FormRules } from 'element-plus';
import { Lock, User } from '@element-plus/icons-vue';
// 定义登录信息接口
interface LoginInfo {
    username: string;
    password: string;
}
// 从本地存储获取登录参数
const lgStr = localStorage.getItem('login-param');
const defParam = lgStr ? JSON.parse(lgStr) : null;
const checked = ref(lgStr ? true : false);
// 创建路由实例
const router = useRouter();

// 定义响应式登录参数
const param = reactive<LoginInfo>({
    username: defParam ? defParam.username : '',
    password: defParam ? defParam.password : '',
});
// 定义登录表单验证规则
const rules: FormRules = {
    username: [
        {
            required: true,
            message: '请输入用户名',
            trigger: 'blur',
        },
    ],
    password: [{ required: true, message: '请输入密码', trigger: 'blur' }],
};


// const permiss = usePermissStore();
// const login = ref<FormInstance>();
// const submitForm = (formEl: FormInstance | undefined) => {
//     if (!formEl) return;
//     formEl.validate((valid: boolean) => {
//         if (valid) {
//             ElMessage.success('登录成功');
//             localStorage.setItem('ms_username', param.username);
//             const keys = permiss.defaultList[param.username == 'admin' ? 'admin' : 'user'];
//             permiss.handleSet(keys);
//             localStorage.setItem('ms_keys', JSON.stringify(keys));
//             router.push('/table');
//             if (checked.value) {
//                 localStorage.setItem('login-param', JSON.stringify(param));
//             } else {
//                 localStorage.removeItem('login-param');
//             }
//         } else {
//             ElMessage.error('登录失败');
//             return false;
//         }
//     });
// };

const permiss = usePermissStore();
const login = ref<FormInstance>();
const submitForm = async (formEl: FormInstance | undefined) => {
    if (!formEl) return;

    // 验证表单
    const valid = await formEl.validate();
    if (!valid) return;

    // 发送登录请求给后端
    try {
        const response = await axios.post('http://127.0.0.1:5000/login', {
            username: param.username,
            password: param.password,
        });

        // 处理后端返回的响应
        if (response.status === 200) {
            // 登录成功，显示成功信息并跳转到 '/table' 页面
            ElMessage.success('登录成功');
            localStorage.setItem('ms_username', param.username);
            const keys = permiss.defaultList[param.username == 'admin' ? 'admin' : 'user'];
            //判断是否为管理员 进入不同页面
            permiss.handleSet(keys);
            localStorage.setItem('ms_keys', JSON.stringify(keys));
            router.push('/table');
        } else {
            // 登录失败，显示错误信息
            ElMessage.error('登录失败，请检查用户名和密码');
        }
    } catch (error) {
        // 发生错误，显示错误信息
        console.error('登录失败：', error);
        ElMessage.error('登录失败，请稍后重试');
    }
};

// const goToRegister = () => {
//     router.push('/register'); // 假设注册页面路径为 '/register'
// };
const goToRegister = () => {
    console.log('点击注册按钮'); // 添加日志输出
    router.push('/register'); // 假设注册页面路径为 '/register'
};

// 清空标签存储
const tags = useTagsStore();
tags.clearTags();
</script>


<style scoped>
.login-wrap {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    height: 100%;
    background-image: url(../assets/img/login-bg.jpg);
    background-size: 100%;
}
.ms-title {
    line-height: 50px;
    text-align: center;
    font-size: 20px;
    color: #333;
    font-weight: bold;
    padding-top: 10px;
}
.ms-login {
    width: 350px;
    border-radius: 5px;
    background: #fff;
}
.ms-content {
    padding: 10px 30px 30px;
}
.login-btn {
    text-align: center;
}
.login-btn button {
    width: 100%;
    height: 36px;
    margin-bottom: 10px;
}
.register-btn button {
    width: 100%;
    height: 36px;
    margin-bottom: 10px;
}
.login-tips {
    font-size: 12px;
    line-height: 30px;
    color: #333;
}
</style>
