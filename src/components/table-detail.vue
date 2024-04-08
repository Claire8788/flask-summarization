<template>
	<el-descriptions title="" :column="2" border>
		<!-- <el-descriptions-item>
			<template #label> 用户ID </template>
			{{ data.id }}
		</el-descriptions-item>
		<el-descriptions-item>
			<template #label> 用户名 </template>
			{{ data.name }}
		</el-descriptions-item> -->
		<el-descriptions-item :span="2">
			<template #label> ID </template>
			{{ data.id }}
		</el-descriptions-item>
		<!-- <el-descriptions-item>
			<template #label> 账户状态 </template>
			{{ data.state ? '正常' : '异常' }}
		</el-descriptions-item> -->
		<el-descriptions-item :span="2">
			<template #label> 文本 </template>
			{{ data.text }}
		</el-descriptions-item>
		<el-descriptions-item :span="2">
		<template #label> 摘要 </template>
			{{ data.summary }}
		</el-descriptions-item>
		<el-descriptions-item>
			<template #label> 模型 </template>
			{{ data.model }}
		</el-descriptions-item>
		<el-descriptions-item>
			<template #label> 时间 </template>
			{{ data.created_at }}
		</el-descriptions-item>
		<!-- <el-descriptions-item>
			<template #label> 头像 </template>
			<img :src="data.thumb" style="width: 120px" alt="" />
		</el-descriptions-item> -->
	</el-descriptions>
</template>

<script lang="ts" setup>
const props = defineProps({
	data: {
		type: Object,
		required: true
	}
});
</script>
