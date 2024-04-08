<template>
  <div>
    <div class="container">
      <div class="search-box">
        <el-input v-model="query.created_at" placeholder="时间" class="search-input mr10" clearable></el-input>
        <el-button type="primary" :icon="Search" @click="handleSearch">搜索</el-button>
        <!-- <el-button type="warning" :icon="CirclePlusFilled" @click="visible = true">新增</el-button> -->
      </div>
      <el-table :data="tableData" border class="table" ref="multipleTable" header-cell-class-name="table-header">
        <el-table-column prop="id" label="ID" width="55" align="center"></el-table-column>
        <el-table-column prop="text" label="文本" align="center">
          <template #default="scope">
            <div>
              <span v-if="scope.row.text.length <= maxLength || !isCollapsed(scope.row.id)">
                {{ scope.row.text }}
              </span>
              <span v-else>
                {{ scope.row.text.slice(0, maxLength) }}...
                <el-link @click="toggleCollapse(scope.row.id)" style="margin-left: 5px;">展开</el-link>
              </span>
            </div>
          </template>
        </el-table-column>
		<el-table-column prop="summary" label="摘要" align="center">
          <template #default="scope">
            <div>
              <span v-if="scope.row.summary.length <= maxLength || !isCollapsed(scope.row.id)">
                {{ scope.row.summary }}
              </span>
              <span v-else>
                {{ scope.row.summary.slice(0, maxLength) }}...
                <el-link @click="toggleCollapse(scope.row.summary)" style="margin-left: 5px;">展开</el-link>
              </span>
            </div>
          </template>
        </el-table-column>
        <!-- <el-table-column label="摘要" align="center">
          <template #default="scope">{{ scope.row.summary }}</template>
        </el-table-column> -->
        <el-table-column prop="model" label="模型" align="center"></el-table-column>
        <el-table-column prop="created_at" label="时间" align="center"></el-table-column>
        <el-table-column label="操作" width="280" align="center">
          <template #default="scope">
            <el-button type="warning" size="small" :icon="View" @click="handleView(scope.row)">
              查看
            </el-button>
            <el-button
              type="primary"
              size="small"
              :icon="Edit"
              @click="handleEdit(scope.$index, scope.row)"
              v-permiss="15"
            >
              编辑
            </el-button>
            <el-button
              type="danger"
              size="small"
              :icon="Delete"
              @click="handleDelete(scope.$index)"
              v-permiss="16"
            >
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      <div class="pagination">
		<p>查询到: {{ tableData.length }}条数据</p>
        <!-- <el-pagination
          background
          layout="total, prev, pager, next"
          :current-page="query.pageIndex"
          :page-size="query.pageSize"
          :total="pageTotal"
          @current-change="handlePageChange"
        ></el-pagination> -->
      </div>
    </div>
    <el-dialog
      :title="idEdit ? '编辑文本' : '新增文本'"
      v-model="visible"
      width="500px"
      destroy-on-close
      :close-on-click-modal="false"
      @close="closeDialog"
    >
      <TableEdit :data="rowData" :edit="idEdit" :update="updateData" />
    </el-dialog>
    <el-dialog title="查看文本详情" v-model="visible1" width="700px" destroy-on-close>
      <TableDetail :data="rowData" />
    </el-dialog>
  </div>
</template>

<!-- <script setup lang="ts"> -->
<script setup lang="ts" name="basetable">

import { ref, reactive, onMounted ,computed} from 'vue';
import { ElMessage, ElMessageBox } from 'element-plus';
import { Delete, Edit, Search, CirclePlusFilled, View } from '@element-plus/icons-vue';
import { fetchData } from '../api/index'; // 导入发送请求的函数
import TableEdit from '../components/table-edit.vue';
import TableDetail from '../components/table-detail.vue';



interface TableItem {
	id: number;
	text: string;
	summary: string;
	model: string;
	created_at: string; // 注意：这里可能需要根据后端返回的日期格式进行调整
}

const query = reactive({
	// address: '',
	// name: '',
	created_at: '',
	// pageIndex: 1,
	// pageSize: 10
});
// const tableData = ref<TableItem[]>([]);
const tableData = ref<TableItem[]>([]);
const pageTotal = ref(0);

// 添加一个函数来发送请求以获取表格数据
const getData = async () => {
	try {
		const res = await fetchData(query); // 调用发送请求的函数
		tableData.value = res.data.list;
		// pageTotal.value = res.data.pageTotal || 50;
	} catch (error) {
		console.error('获取表格数据失败：', error);
		ElMessage.error('获取表格数据失败，请稍后重试');
	}
};

onMounted(() => {
	getData(); // 页面加载时获取表格数据
});



// 在查询操作中调用后端接口，并将查询条件传递给后端
const handleSearch = async () => {
    try {
        const res = await fetchData(query); // 传递查询条件给后端
        tableData.value = res.data.list;
        // pageTotal.value = res.data.pageTotal || 50;
    } catch (error) {
        console.error('获取表格数据失败：', error);
        ElMessage.error('获取表格数据失败，请稍后重试');
    }
};

// // 分页导航
// const handlePageChange = (val: number) => {
// 	query.pageIndex = val;
// 	getData();
// };

// 删除操作
const handleDelete = (index: number) => {
	// 二次确认删除
	ElMessageBox.confirm('确定要删除吗？', '提示', {
		type: 'warning'
	})
		.then(() => {
			ElMessage.success('删除成功');
			tableData.value.splice(index, 1);
		})
		.catch(() => {});
};

const visible = ref(false);
let idx: number = -1;
const idEdit = ref(false);
const rowData = ref({});
const handleEdit = (index: number, row: TableItem) => {
	idx = index;
	rowData.value = row;
	idEdit.value = true;
	visible.value = true;
};
const updateData = (row: TableItem) => {
	idEdit.value ? (tableData.value[idx] = row) : tableData.value.unshift(row);
	console.log(tableData.value);
	closeDialog();
};

const closeDialog = () => {
	visible.value = false;
	idEdit.value = false;
};

const visible1 = ref(false);
const handleView = (row: TableItem) => {
	rowData.value = row;
	visible1.value = true;
};


  // 添加展开和收起功能
const maxLength = 100; // 文本最大长度

const collapsedMap = new Map<number, boolean>(); // 存储展开和收起状态

const isCollapsed = (id: number) => {
  return !collapsedMap.has(id) || collapsedMap.get(id)!;
};

const toggleCollapse = (id: number) => {
  const collapsed = !isCollapsed(id);
  collapsedMap.set(id, collapsed);
};

</script>

<style scoped>
.search-box {
	margin-bottom: 20px;
}

.search-input {
	width: 200px;
}

.mr10 {
	margin-right: 10px;
}
.table-td-thumb {
	display: block;
	margin: auto;
	width: 40px;
	height: 40px;
}
</style>
