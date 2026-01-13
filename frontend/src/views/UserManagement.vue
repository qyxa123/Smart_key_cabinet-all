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
      <el-button @click="$router.push('/')" class="back-btn" circle>
        <el-icon><ArrowLeft /></el-icon>
      </el-button>
      <div class="logo-icon">
        <div class="key-icon">👥</div>
      </div>
      <h1 class="page-title">用户管理</h1>
      <p class="page-subtitle">User Management</p>
    </div>

    <!-- 主要内容区域 -->
    <div class="main-content">
      <!-- 用户列表 -->
      <div class="user-list" v-loading="loading">
        <div 
          v-for="user in users" 
          :key="user.id"
          class="user-card"
          @click="showUserDetail(user)"
        >
          <div class="user-info">
            <div class="user-name">{{ user.name }}</div>
            <div class="user-details">
              <span class="user-id">ID: {{ user.id }}</span>
              <el-tag 
                :type="user.identity === 'teacher' ? 'success' : 'primary'"
                size="small"
              >
                {{ user.identity === 'teacher' ? '老师' : '学生' }}
              </el-tag>
            </div>
            <div class="user-keys" v-if="user.keys && user.keys.length > 0">
              <span class="keys-count">借用钥匙: {{ user.keys.length }}把</span>
            </div>
          </div>
          <div class="user-actions">
            <el-icon class="action-icon"><ArrowRight /></el-icon>
          </div>
        </div>
        
        <div v-if="users.length === 0 && !loading" class="empty-state">
          <div class="empty-icon">👤</div>
          <p>暂无用户数据</p>
          <p class="empty-subtitle">No users found</p>
        </div>
      </div>
    </div>

    <!-- 底部按钮 -->
    <div class="bottom-actions">
      <el-button @click="loadUsers" size="large" class="action-btn secondary">
        <el-icon><Refresh /></el-icon>
        刷新 Refresh
      </el-button>
      <el-button type="primary" @click="showAddDialog" size="large" class="action-btn primary">
        <el-icon><Plus /></el-icon>
        添加用户 Add User
      </el-button>
    </div>

    <!-- 用户详情对话框 -->
    <el-dialog
      v-model="detailDialogVisible"
      :title="selectedUser?.name + ' 的详细信息'"
      width="90%"
      :before-close="handleDetailClose"
    >
      <div v-if="selectedUser" class="user-detail">
        <div class="detail-section">
          <h4>基本信息</h4>
          <p><strong>姓名:</strong> {{ selectedUser.name }}</p>
          <p><strong>ID:</strong> {{ selectedUser.id }}</p>
          <p><strong>身份:</strong> {{ selectedUser.identity === 'teacher' ? '老师' : '学生' }}</p>
          <p v-if="selectedUser.grade"><strong>年级:</strong> {{ selectedUser.grade }}</p>
          <p v-if="selectedUser.class_"><strong>班级:</strong> {{ selectedUser.class_ }}</p>
          <p v-if="selectedUser.office"><strong>办公室:</strong> {{ selectedUser.office }}</p>
        </div>
        
        <div class="detail-section" v-if="selectedUser.keys && selectedUser.keys.length > 0">
          <h4>借用的钥匙</h4>
          <div class="borrowed-keys-list">
            <div v-for="key in selectedUser.keys" :key="key.id" class="borrowed-key-item">
              <span>{{ key.room }}号房间</span>
              <span class="key-id">ID: {{ key.id }}</span>
            </div>
          </div>
        </div>
      </div>
      
      <template #footer>
        <el-button @click="detailDialogVisible = false">关闭</el-button>
        <el-button type="danger" @click="confirmDeleteUser">删除用户</el-button>
      </template>
    </el-dialog>

    <!-- 添加用户对话框 -->
    <el-dialog
      v-model="addDialogVisible"
      title="添加新用户"
      width="90%"
      :before-close="handleAddClose"
    >
      <el-form
        ref="addFormRef"
        :model="addForm"
        :rules="addRules"
        label-width="80px"
      >
        <el-form-item label="姓名" prop="name">
          <el-input v-model="addForm.name" placeholder="请输入姓名" />
        </el-form-item>
        
        <el-form-item label="身份" prop="identity">
          <el-radio-group v-model="addForm.identity">
            <el-radio label="student">学生</el-radio>
            <el-radio label="teacher">老师</el-radio>
          </el-radio-group>
        </el-form-item>
        
        <el-form-item label="年级" prop="grade" v-if="addForm.identity === 'student'">
          <el-input v-model="addForm.grade" placeholder="请输入年级" />
        </el-form-item>
        
        <el-form-item label="班级" prop="class_" v-if="addForm.identity === 'student'">
          <el-input v-model="addForm.class_" placeholder="请输入班级" />
        </el-form-item>
        
        <el-form-item label="办公室" prop="office" v-if="addForm.identity === 'teacher'">
          <el-input v-model="addForm.office" placeholder="请输入办公室" />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <el-button @click="addDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitAddForm" :loading="submitting">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>
<script>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { ArrowLeft, Plus, Refresh, ArrowRight } from '@element-plus/icons-vue'
import { userAPI } from '../api'

export default {
  name: 'UserManagement',
  components: {
    ArrowLeft,
    Plus,
    Refresh,
    ArrowRight
  },
  setup() {
    const users = ref([])
    const loading = ref(false)
    const detailDialogVisible = ref(false)
    const addDialogVisible = ref(false)
    const selectedUser = ref(null)
    const addFormRef = ref()
    const submitting = ref(false)

    const addForm = reactive({
      name: '',
      identity: 'student',
      grade: '',
      class_: '',
      office: ''
    })

    const addRules = {
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

    const showUserDetail = (user) => {
      selectedUser.value = user
      detailDialogVisible.value = true
    }

    const showAddDialog = () => {
      resetAddForm()
      addDialogVisible.value = true
    }

    const submitAddForm = async () => {
      if (!addFormRef.value) return

      try {
        await addFormRef.value.validate()
        submitting.value = true

        const userData = {
          name: addForm.name,
          identity: addForm.identity,
          grade: addForm.identity === 'student' ? addForm.grade : null,
          class_: addForm.identity === 'student' ? addForm.class_ : null,
          office: addForm.identity === 'teacher' ? addForm.office : null
        }

        await userAPI.createUser(userData)
        ElMessage.success('用户添加成功')
        addDialogVisible.value = false
        loadUsers()
      } catch (error) {
        console.error('添加用户失败:', error)
        ElMessage.error('添加用户失败')
      } finally {
        submitting.value = false
      }
    }

    const confirmDeleteUser = async () => {
      if (!selectedUser.value) return

      try {
        await ElMessageBox.confirm(
          `确定要删除用户 "${selectedUser.value.name}" 吗？`,
          '确认删除',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }
        )

        await userAPI.deleteUser(selectedUser.value.id)
        ElMessage.success('用户删除成功')
        detailDialogVisible.value = false
        loadUsers()
      } catch (error) {
        if (error !== 'cancel') {
          console.error('删除用户失败:', error)
          ElMessage.error('删除用户失败')
        }
      }
    }

    const resetAddForm = () => {
      Object.assign(addForm, {
        name: '',
        identity: 'student',
        grade: '',
        class_: '',
        office: ''
      })
      if (addFormRef.value) {
        addFormRef.value.resetFields()
      }
    }

    const handleDetailClose = () => {
      detailDialogVisible.value = false
      selectedUser.value = null
    }

    const handleAddClose = () => {
      addDialogVisible.value = false
      resetAddForm()
    }

    onMounted(() => {
      loadUsers()
    })

    return {
      users,
      loading,
      detailDialogVisible,
      addDialogVisible,
      selectedUser,
      addFormRef,
      addForm,
      addRules,
      submitting,
      loadUsers,
      showUserDetail,
      showAddDialog,
      submitAddForm,
      confirmDeleteUser,
      handleDetailClose,
      handleAddClose
    }
  }
}
</script>

<style scoped>
.page-container {
  height: 100vh;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.page-header {
  flex-shrink: 0;
  padding: 15px 20px;
  text-align: center;
  position: relative;
}

.back-btn {
  position: absolute;
  top: 15px;
  left: 20px;
  background: rgba(0, 255, 255, 0.1);
  border: 1px solid rgba(0, 255, 255, 0.3);
  color: #00ffff;
}

.back-btn:hover {
  background: rgba(0, 255, 255, 0.2);
  border-color: #00ffff;
}

.logo-icon {
  margin: 10px auto 15px;
  width: 50px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, rgba(0, 255, 255, 0.1), rgba(0, 128, 255, 0.1));
  border-radius: 50%;
  border: 1px solid rgba(0, 255, 255, 0.3);
}

.key-icon {
  font-size: 24px;
}

.main-content {
  flex: 1;
  padding: 0 20px;
  overflow-y: auto;
}

.user-list {
  max-width: 400px;
  margin: 0 auto;
}

.user-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
  margin-bottom: 10px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.user-card:hover {
  background: rgba(0, 255, 255, 0.1);
  border-color: #00ffff;
  transform: translateY(-2px);
}

.user-info {
  flex: 1;
}

.user-name {
  color: #ffffff;
  font-weight: 600;
  font-size: 16px;
  margin-bottom: 5px;
}

.user-details {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 5px;
}

.user-id {
  color: #aaa;
  font-size: 12px;
}

.user-keys {
  color: #00ffff;
  font-size: 12px;
}

.keys-count {
  font-weight: 500;
}

.user-actions {
  display: flex;
  align-items: center;
}

.action-icon {
  color: #00ffff;
  font-size: 18px;
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: #666;
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 20px;
}

.empty-subtitle {
  font-size: 14px;
  color: #888;
  margin-top: 5px;
}

.bottom-actions {
  flex-shrink: 0;
  display: flex;
  gap: 15px;
  padding: 20px;
  background: rgba(0, 0, 0, 0.3);
  border-top: 1px solid rgba(0, 255, 255, 0.2);
}

.action-btn {
  flex: 1;
  height: 50px;
  font-size: 16px;
  font-weight: 600;
}

.action-btn.secondary {
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.3);
  color: #ffffff;
}

.action-btn.secondary:hover {
  background: rgba(255, 255, 255, 0.2);
  border-color: rgba(255, 255, 255, 0.5);
}

.action-btn.primary {
  background: linear-gradient(45deg, #00ffff, #0080ff);
  border: 1px solid #00ffff;
  color: #000;
}

.action-btn.primary:hover {
  background: linear-gradient(45deg, #0080ff, #00ffff);
  transform: translateY(-2px);
  box-shadow: 0 10px 25px rgba(0, 255, 255, 0.4);
}

.user-detail {
  color: #ffffff;
}

.detail-section {
  margin-bottom: 20px;
  padding: 15px;
  background: rgba(0, 0, 0, 0.2);
  border-radius: 8px;
  border: 1px solid rgba(0, 255, 255, 0.1);
}

.detail-section h4 {
  color: #00ffff;
  margin-bottom: 10px;
  font-size: 16px;
}

.detail-section p {
  margin-bottom: 8px;
  font-size: 14px;
}

.borrowed-keys-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.borrowed-key-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 12px;
  background: rgba(0, 255, 255, 0.1);
  border-radius: 6px;
  border: 1px solid rgba(0, 255, 255, 0.2);
}

.borrowed-key-item .key-id {
  color: #aaa;
  font-size: 12px;
}

@media (max-width: 480px) {
  .bottom-actions {
    flex-direction: column;
  }
  
  .action-btn {
    height: 45px;
  }
}
</style>