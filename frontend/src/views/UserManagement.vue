<template>
  <div class="page-container">
    <!-- 背景动画 -->
    <div class="bg-animation">
      <div class="particle"></div>
      <div class="particle"></div>
      <div class="particle"></div>
      <div class="particle"></div>
      <div class="particle"></div>
    </div>

    <!-- 头部区域 -->
    <div class="page-header">
      <h1 class="page-title">用户管理</h1>
      <p class="page-subtitle">User Management</p>
      <el-button @click="$router.push('/')" class="back-btn">
        <el-icon><ArrowLeft /></el-icon>
        返回主页
      </el-button>
    </div>

    <!-- 主要内容区域 -->
    <div class="glass-card main-content">
      <!-- 操作栏 -->
      <div class="toolbar">
        <el-button type="primary" @click="showAddDialog">
          <el-icon><Plus /></el-icon>
          添加用户
        </el-button>
        <el-button @click="loadUsers">
          <el-icon><Refresh /></el-icon>
          刷新
        </el-button>
      </div>

      <!-- 用户表格 -->
      <el-table 
        :data="users" 
        style="width: 100%" 
        v-loading="loading"
        empty-text="暂无用户数据"
      >
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="姓名" width="120" />
        <el-table-column prop="identity" label="身份" width="100">
          <template #default="scope">
            <el-tag :type="scope.row.identity === 'teacher' ? 'success' : 'primary'">
              {{ scope.row.identity === 'teacher' ? '老师' : '学生' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="grade" label="年级" width="100" />
        <el-table-column prop="class_" label="班级" width="100" />
        <el-table-column prop="office" label="办公室" width="120" />
        <el-table-column label="借用钥匙" width="200">
          <template #default="scope">
            <div v-if="scope.row.keys && scope.row.keys.length > 0">
              <el-tag 
                v-for="key in scope.row.keys" 
                :key="key.id"
                size="small"
                style="margin-right: 5px;"
              >
                {{ key.room }}号房间
              </el-tag>
            </div>
            <span v-else style="color: #999;">无</span>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200">
          <template #default="scope">
            <el-button size="small" @click="editUser(scope.row)">编辑</el-button>
            <el-button 
              size="small" 
              type="danger" 
              @click="deleteUser(scope.row)"
            >
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <!-- 添加/编辑用户对话框 -->
    <el-dialog
      :title="dialogTitle"
      v-model="dialogVisible"
      width="500px"
    >
      <el-form
        ref="userFormRef"
        :model="userForm"
        :rules="userRules"
        label-width="80px"
      >
        <el-form-item label="姓名" prop="name">
          <el-input v-model="userForm.name" placeholder="请输入姓名" />
        </el-form-item>
        
        <el-form-item label="身份" prop="identity">
          <el-radio-group v-model="userForm.identity">
            <el-radio label="student">学生</el-radio>
            <el-radio label="teacher">老师</el-radio>
          </el-radio-group>
        </el-form-item>
        
        <el-form-item label="年级" prop="grade" v-if="userForm.identity === 'student'">
          <el-input v-model="userForm.grade" placeholder="请输入年级" />
        </el-form-item>
        
        <el-form-item label="班级" prop="class_" v-if="userForm.identity === 'student'">
          <el-input v-model="userForm.class_" placeholder="请输入班级" />
        </el-form-item>
        
        <el-form-item label="办公室" prop="office" v-if="userForm.identity === 'teacher'">
          <el-input v-model="userForm.office" placeholder="请输入办公室" />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="saveUser" :loading="saving">
            确定
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { ArrowLeft, Plus, Refresh } from '@element-plus/icons-vue'
import { userAPI } from '../api'

export default {
  name: 'UserManagement',
  components: {
    ArrowLeft,
    Plus,
    Refresh
  },
  setup() {
    const users = ref([])
    const loading = ref(false)
    const dialogVisible = ref(false)
    const dialogTitle = ref('添加用户')
    const userFormRef = ref()
    const saving = ref(false)
    const editingUserId = ref(null)

    const userForm = reactive({
      name: '',
      identity: 'student',
      grade: '',
      class_: '',
      office: ''
    })

    const userRules = {
      name: [
        { required: true, message: '请输入姓名', trigger: 'blur' }
      ],
      identity: [
        { required: true, message: '请选择身份', trigger: 'change' }
      ]
    }

    const loadUsers = async () => {
      loading.value = true
      try {
        const data = await userAPI.getUsers()
        users.value = data
      } catch (error) {
        console.error('加载用户列表失败:', error)
        ElMessage.error('加载用户列表失败')
      } finally {
        loading.value = false
      }
    }

    const showAddDialog = () => {
      dialogTitle.value = '添加用户'
      editingUserId.value = null
      resetForm()
      dialogVisible.value = true
    }

    const editUser = (user) => {
      dialogTitle.value = '编辑用户'
      editingUserId.value = user.id
      Object.assign(userForm, {
        name: user.name,
        identity: user.identity,
        grade: user.grade || '',
        class_: user.class_ || '',
        office: user.office || ''
      })
      dialogVisible.value = true
    }

    const saveUser = async () => {
      if (!userFormRef.value) return

      try {
        await userFormRef.value.validate()
        saving.value = true

        const userData = {
          name: userForm.name,
          identity: userForm.identity,
          grade: userForm.identity === 'student' ? userForm.grade : null,
          class_: userForm.identity === 'student' ? userForm.class_ : null,
          office: userForm.identity === 'teacher' ? userForm.office : null
        }

        if (editingUserId.value) {
          await userAPI.updateUser(editingUserId.value, userData)
          ElMessage.success('用户更新成功')
        } else {
          await userAPI.createUser(userData)
          ElMessage.success('用户添加成功')
        }

        dialogVisible.value = false
        loadUsers()
      } catch (error) {
        console.error('保存用户失败:', error)
        ElMessage.error('保存用户失败')
      } finally {
        saving.value = false
      }
    }

    const deleteUser = async (user) => {
      try {
        await ElMessageBox.confirm(
          `确定要删除用户 "${user.name}" 吗？`,
          '确认删除',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }
        )

        await userAPI.deleteUser(user.id)
        ElMessage.success('用户删除成功')
        loadUsers()
      } catch (error) {
        if (error !== 'cancel') {
          console.error('删除用户失败:', error)
          ElMessage.error('删除用户失败')
        }
      }
    }

    const resetForm = () => {
      Object.assign(userForm, {
        name: '',
        identity: 'student',
        grade: '',
        class_: '',
        office: ''
      })
      if (userFormRef.value) {
        userFormRef.value.resetFields()
      }
    }

    onMounted(() => {
      loadUsers()
    })

    return {
      users,
      loading,
      dialogVisible,
      dialogTitle,
      userFormRef,
      userForm,
      userRules,
      saving,
      loadUsers,
      showAddDialog,
      editUser,
      saveUser,
      deleteUser
    }
  }
}
</script>

<style scoped>
.main-content {
  padding: 30px;
}

.back-btn {
  position: absolute;
  top: 20px;
  left: 20px;
}

.toolbar {
  margin-bottom: 20px;
  display: flex;
  gap: 10px;
}

@media (max-width: 768px) {
  .main-content {
    padding: 15px;
  }
  
  .toolbar {
    flex-direction: column;
  }
}
</style>