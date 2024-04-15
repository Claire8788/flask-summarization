<template>
    <div>
        <div class="container">
            <!-- 搜索框 -->
            <div class="search-box">
                <el-input v-model="query.username" placeholder="用户名" class="search-input mr10" clearable></el-input>
                <el-button type="primary" :icon="Search" @click="handleSearch">搜索</el-button>
            </div>
            
            <!-- 管理员列表 -->
            <el-table :data="adminList" border class="table" ref="adminTable" header-cell-class-name="table-header">
                <el-table-column prop="id" label="ID" width="55" align="center"></el-table-column>
                <el-table-column prop="username" label="用户名" align="center"></el-table-column>
                <!-- <el-table-column prop="password" label="密码" align="center"></el-table-column> -->
                <el-table-column prop="password" label="密码" align="center">
                    <template #default="{ row }">
                        <div>
                            <span v-if="!row.showPassword">{{ hidePassword(row.password) }}</span>
                            
                            <span v-else >{{ row.password }}</span>
                            <span>&nbsp;</span>
                            <span>&nbsp;</span><span>&nbsp;</span>
                            <el-button size="mini" @click="togglePasswordVisibility(row)">{{ row.showPassword ? '隐藏密码' : '显示密码' }}</el-button>
                        </div>
                    </template>
                </el-table-column>
                <el-table-column prop="email" label="邮箱" align="center"></el-table-column>
                <el-table-column prop="created_at" label="创建时间" align="center"></el-table-column>
                <el-table-column prop="status" label="状态" align="center">
                    <template #default="{ row }">
                    <el-tag v-if="row.status === 1" type="success">正常</el-tag>
                    <el-tag v-else type="danger">已删除</el-tag>
                    </template>
                </el-table-column>
                <el-table-column label="操作" width="200" align="center">
                    
                <!-- <template #default="scope">
                    <el-button type="primary" size="small" @click="handleEdit(scope.row)">编辑</el-button>
                    <el-button type="danger" size="small" @click="handleDelete(scope.row.id)">删除</el-button>
                </template> -->
                <template #default="scope">
                    <el-button
                    type="primary"
                    size="small"
                    :icon="Edit"
                    @click="handleEdit(scope.$index, scope.row)"
                    v-permiss="15"
                    >
                    编辑
                    </el-button>
                    <!-- <el-button
                    type="danger"
                    size="small"
                    :icon="Delete"
                    @click="handleDelete(scope.$index)"
                    v-permiss="16"
                    > -->
                    <el-button
                    type="danger"
                    size="small"
                    :icon="Delete"
                    @click="handleDelete(scope.row.id)"
                    v-permiss="16"
                    >
                    删除
                    </el-button>
                </template>
                </el-table-column>
            </el-table>
            <div class="pagination">
		        <p>查询到: {{ adminList.length }}条数据</p>
        <!-- <el-pagination
          background
          layout="total, prev, pager, next"
          :current-page="query.pageIndex"
          :page-size="query.pageSize"
          :total="pageTotal"
          @current-change="handlePageChange"
        ></el-pagination> -->
            </div>
            <!-- </div> -->
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
        </div>
    </div> 
    
</template>
  
  <script setup lang="ts">
//   <script setup lang="ts" name="basetable">
  import { ref, reactive, onMounted ,computed} from 'vue';
  import { ElMessage, ElMessageBox } from 'element-plus';
  import { Delete, Edit, Search, CirclePlusFilled, View } from '@element-plus/icons-vue';
  import { queryUser } from '../api/index'; // 导入发送请求的函数
  import { deleteAdmin } from '../api/index'; // 导入发送请求的函数
  import TableEdit from '../components/admin_edit.vue';

  
  
  
  interface AdminItem {
      id: number;
      username: string;
      password: string;
      email: string;
      created_at: string; // 注意：这里可能需要根据后端返回的日期格式进行调整
  }
  
  const query = reactive({
      // address: '',
      username: ''
    //   created_at: '',
      // pageIndex: 1,
      // pageSize: 10
    // username: localStorage.getItem('ms_username')
  });
  // const tableData = ref<TableItem[]>([]);
  const adminList = ref<AdminItem[]>([]);
//   const pageTotal = ref(0)
  
  // 添加一个函数来发送请求以获取表格数据
  const getData = async () => {
      try {
          const res = await queryUser(query); // 调用发送请求的函数
          adminList.value = res.data.users;
          
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
        const res = await queryUser(query); // 传递查询条件给后端
          adminList.value = res.data.users;
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
  
  const handleDelete = async (id) => {
    try {
      await deleteAdmin({ id }); // 发送请求删除对应 ID 的数据
      const index = adminList.value.findIndex(item => item.id === id); // 找到要删除的行在表格数据中的索引
      if (index !== -1) {
        adminList.value.splice(index, 1); // 删除表格中对应的行
      }
      ElMessage.success('删除成功');
    } catch (error) {
      console.error('删除数据失败：', error);
      ElMessage.error('删除数据失败，请稍后重试');
    }
  };
  
  
  const visible = ref(false);
  let idx: number = -1;
  const idEdit = ref(false);
  const rowData = ref({});
  const handleEdit = (index: number, row: AdminItem) => {
      idx = index;
      rowData.value = row;
      idEdit.value = true;
      visible.value = true;
  };
  const updateData = (row: AdminItem) => {
      idEdit.value ? (adminList.value[idx] = row) : adminList.value.unshift(row);
      console.log(adminList.value);
      closeDialog();
  };
  
  const closeDialog = () => {
      visible.value = false;
      idEdit.value = false;
  };
  
  const visible1 = ref(false);
  const handleView = (row: AdminItem) => {
      rowData.value = row;
      visible1.value = true;
  };
  
  

// 切换密码显示状态的方法
const togglePasswordVisibility = (row) => {
  row.showPassword = !row.showPassword;
};

// 加密密码的方法（示例中使用了简单的方法，实际项目中应该使用更安全的加密方式）
const hidePassword = (password) => {
  // 在这里编写加密密码的逻辑，这里简单地用*替代密码
  return '*'.repeat(password.length);
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
  