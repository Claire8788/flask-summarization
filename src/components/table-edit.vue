<template>
  <el-form ref="formRef" :model="form" :rules="rules">
    <el-form-item label="ID" prop="id">
      <el-input v-model="form.id"></el-input>
    </el-form-item>
    <el-form-item label="文本" prop="text">
      <el-input v-model="form.text" autosize style="max-height: 200px; overflow-y: auto;"></el-input>
    </el-form-item>
    <el-form-item label="摘要" prop="summary">
      <el-input v-model="form.summary" autosize style="max-height: 200px; overflow-y: auto;"></el-input>
    </el-form-item>
    <el-form-item label="模型" prop="model">
      <el-input v-model="form.model"></el-input>
    </el-form-item>
    <el-form-item label="时间" prop="created_at">
      <el-input v-model="form.created_at"></el-input>
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
const saveEdit = (formEl: FormInstance | undefined) => {
	if (!formEl) return;
	formEl.validate(valid => {
		if (!valid) return false;
		props.update(form.value);
		ElMessage.success('保存成功！');
	});
};
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
