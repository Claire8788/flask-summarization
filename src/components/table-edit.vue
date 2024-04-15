<template>
  <el-form ref="formRef" :model="form" :rules="rules">
    <el-form-item label="ID" prop="id">
      <!-- <el-input v-model="form.id"></el-input> -->
	  <el-input v-model="form.id" :disabled="true"></el-input>
    </el-form-item>
    <el-form-item label="文本" prop="text">
      <!-- <el-input v-model="form.text" autosize style="max-height: 200px; overflow-y: auto;"></el-input> -->
	  <el-input v-model="form.text" type="textarea" style="height: 300px; max-height: 300px; overflow-y: scroll;" :rows="13" wrap="wrap"></el-input>
    </el-form-item>
    <el-form-item label="摘要" prop="summary">
      <!-- <el-input v-model="form.summary" autosize style="max-height: 200px; overflow-y: auto;"></el-input> -->
	  <el-input v-model="form.summary" type="textarea" style="height: 200px; max-height: 200px; overflow-y: scroll;" :rows="8" wrap="wrap"></el-input>
    </el-form-item>
    <el-form-item label="模型" prop="model">
      <!-- <el-input v-model="form.model"></el-input> -->
	  <el-input v-model="form.model" :disabled="true"></el-input>
    </el-form-item>
    <el-form-item label="时间" prop="created_at">
      <!-- <el-input v-model="form.created_at"></el-input> -->
	  <el-input v-model="form.created_at" :disabled="true"></el-input>
    </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="saveEdit(formRef)">保存</el-button>
    </el-form-item>
  </el-form>
</template>


<script setup lang="ts">
import { ElMessage, FormInstance, FormRules } from 'element-plus';
import { defineProps, ref } from 'vue';

const props = defineProps({
	data: {
		type: Object,
		required: true
	},
	edit: {
		type: Boolean,
		required: false
	},
	update: {
		type: Function,
		required: true
	}
});

const form = ref(props.edit ? { ...props.data } : { id: '', text: '', summary: '', model: '', created_at: '', date: new Date() });

const rules: FormRules = {
	name: [{ required: true, message: '用户名', trigger: 'blur' }]
};
const formRef = ref<FormInstance>();
const saveEdit = async (formEl: FormInstance | undefined) => {
    if (!formEl) return;

    // 验证表单
    const valid = await formEl.validate();
    if (!valid) return;

    try {
        // 发送更新请求到后端
        const response = await fetch('http://127.0.0.1:5000/api/updateData', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(form.value)
        });

        if (response.ok) {
            // 更新成功，调用传入的 update 函数
            props.update(form.value);
            ElMessage.success('保存成功！');
        } else {
            // 更新失败，显示错误消息
            const data = await response.json();
            ElMessage.error(data.message || '保存失败！');
        }
    } catch (error) {
        console.error('Failed to save edit:', error);
        ElMessage.error('保存失败，请稍后重试！');
    }
};
// const formRef = ref<FormInstance>();
// const saveEdit = (formEl: FormInstance | undefined) => {
// 	if (!formEl) return;
// 	formEl.validate(valid => {
// 		if (!valid) return false;
// 		props.update(form.value);
// 		ElMessage.success('保存成功！');
// 	});
// };

// const fetchEditData = async (id) => {
//     try {
//         const res = await fetch(`/api/editData?id=${id}`);
//         if (res.ok) {
//             const data = await res.json();
//             form.value = data.data;
//         } else {
//             console.error('Failed to fetch edit data:', res.statusText);
//         }
//     } catch (error) {
//         console.error('Failed to fetch edit data:', error);
//     }
// };

</script>



<style>
.avatar-uploader .el-upload {
	border: 1px dashed var(--el-border-color);
	border-radius: 6px;
	cursor: pointer;
	position: relative;
	overflow: hidden;
	transition: var(--el-transition-duration-fast);
}

.avatar-uploader .el-upload:hover {
	border-color: var(--el-color-primary);
}

.el-icon.avatar-uploader-icon {
	font-size: 28px;
	color: #8c939d;
	width: 178px;
	height: 178px;
	text-align: center;
}
</style>
