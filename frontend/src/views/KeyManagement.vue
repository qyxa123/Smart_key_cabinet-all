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
        <div class="key-icon">🗝️</div>
      </div>
      <h1 class="page-title">钥匙管理</h1>
      <p class="page-subtitle">Key Management</p>
    </div>

    <!-- 主要内容区域 -->
    <div class="main-content">
      <!-- 钥匙列表 -->
      <div class="key-list" v-loading="loading">
        <div 
          v-for="key in keys" 
          :key="key.id"
          class="key-card"
          :class="{ borrowed: isKeyBorrowed(key) }"
          @click="showKeyDetail(key)"
        >
          <div class="key-info">
            <div class="room-number">{{ key.room }}号房间</div>
            <div class="key-details">
              <span class="key-id">ID: {{ key.id }}</span>
              <el-tag 
                :type="isKeyBorrowed(key) ? 'danger' : 'success'"
                size="small"
              >
                {{ isKeyBorrowed(key) ? '已借出' : '可用' }}
              </el-tag>
            </div>
            <div class="borrower-info" v-if="getKeyBorrower(key)">
              <span class="borrower-name">借用人: {{ getKeyBorrower(key).name }}</span>
            </div>
          </div>
          <div class="key-actions">
            <el-icon class="action-icon"><ArrowRight /></el-icon>
          </div>
        </div>
        
        <div v-if="keys.length === 0 && !loading" class="empty-state">
          <div class="empty-icon">🗝️</div>
          <p>暂无钥匙数据</p>
          <p class="empty-subtitle">No keys found</p>
        </div>
      </div>
    </div>

    <!-- 底部按钮 -->
    <div class="bottom-actions">
      <el-button @click="loadKeys" size="large" class="action-btn secondary">
        <el-icon><Refresh /></el-icon>
        刷新 Refresh
      </el-button>
      <el-button type="primary" @click="showAddDialog" size="large" class="action-btn primary">
        <el-icon><Plus /></el-icon>
        添加钥匙 Add Key
      </el-button>
    </div>

    <!-- 钥匙详情对话框 -->
    <el-dialog
      v-model="detailDialogVisible"
      :title="selectedKey?.room + '号房间钥匙'"
      width="90%"
      :before-close="handleDetailClose"
    >
      <div v-if="selectedKey" class="key-detail">
        <div class="detail-section">
          <h4>钥匙信息</h4>
          <p><strong>钥匙ID:</strong> {{ selectedKey.id }}</p>
          <p><strong>房间号:</strong> {{ selectedKey.room }}</p>
          <p><strong>状态:</strong> 
            <el-tag :type="isKeyBorrowed(selectedKey) ? 'danger' : 'success'">
              {{ isKeyBorrowed(selectedKey) ? '已借出' : '可用' }}
            </el-tag>
          </p>
        </div>
        
        <div class="detail-section" v-if="getKeyBorrower(selectedKey)">
          <h4>借用信息</h4>
          <p><strong>借用人:</strong> {{ getKeyBorrower(selectedKey).name }}</p>
          <p><strong>身份:</strong> {{ getKeyBorrower(selectedKey).identity === 'teacher' ? '老师' : '学生' }}</p>
          <p v-if="getKeyBorrower(selectedKey).grade"><strong>年级:</strong> {{ getKeyBorrower(selectedKey).grade }}</p>
          <p v-if="getKeyBorrower(selectedKey).class_"><strong>班级:</strong> {{ getKeyBorrower(selectedKey).class_ }}</p>
        </div>
      </div>
      
      <template #footer>
        <el-button @click="detailDialogVisible = false">关闭</el-button>
        <el-button type="danger" @click="confirmDeleteKey">删除钥匙</el-button>
      </template>
    </el-dialog>

    <!-- 添加钥匙对话框 -->
    <el-dialog
      v-model="addDialogVisible"
      title="添加新钥匙"
      width="90%"
      :before-close="handleAddClose"
    >
      <el-form
        ref="addFormRef"
        :model="addForm"
        :rules="addRules"
        label-width="80px"
      >
        <el-form-item label="房间号" prop="room">
          <el-input v-model="addForm.room" placeholder="请输入房间号" />
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
import { keyAPI, userAPI } from '../api'

export default {
  name: 'KeyManagement',
  components: {
    ArrowLeft,
    Plus,
    Refresh,
    ArrowRight
  },
  setup() {
    const keys = ref([])
    const users = ref([])
    const loading = ref(false)
    const detailDialogVisible = ref(false)
    const addDialogVisible = ref(false)
    const selectedKey = ref(null)
    const addFormRef = ref()
    const submitting = ref(false)

    const addForm = reactive({
      room: ''
    })

    const addRules = {
      room: [
        { required: true, message: '请输入房间号', trigger: 'blur' },
        { 
          pattern: /^\d{3}$/, 
          message: '房间号必须是3位数字，如：101、205', 
          trigger: 'blur' 
        }
      ]
    }

    const loadKeys = async () => {
      loading.value = true
      try {
        const [keysData, usersData] = await Promise.all([
          keyAPI.getKeys(),
          userAPI.getUsers()
        ])
        keys.value = keysData
        users.value = usersData
      } catch (error) {
        console.error('加载数据失败:', error)
        ElMessage.error('加载数据失败')
      } finally {
        loading.value = false
      }
    }

    const isKeyBorrowed = (key) => {
      return users.value.some(user => 
        user.keys && user.keys.some(userKey => userKey.id === key.id)
      )
    }

    const getKeyBorrower = (key) => {
      return users.value.find(user => 
        user.keys && user.keys.some(userKey => userKey.id === key.id)
      )
    }

    const showKeyDetail = (key) => {
      selectedKey.value = key
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

        const keyData = {
          room: addForm.room
        }

        await keyAPI.createKey(keyData)
        ElMessage.success('钥匙添加成功')
        addDialogVisible.value = false
        loadKeys()
      } catch (error) {
        console.error('添加钥匙失败:', error)
        if (error.response?.status === 400) {
          ElMessage.error('该房间号的钥匙已存在')
        } else {
          ElMessage.error('添加钥匙失败')
        }
      } finally {
        submitting.value = false
      }
    }

    const confirmDeleteKey = async () => {
      if (!selectedKey.value) return

      if (isKeyBorrowed(selectedKey.value)) {
        ElMessage.warning('该钥匙正在被借用，无法删除')
        return
      }

      try {
        await ElMessageBox.confirm(
          `确定要删除 "${selectedKey.value.room}" 号房间的钥匙吗？`,
          '确认删除',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }
        )

        await keyAPI.deleteKey(selectedKey.value.id)
        ElMessage.success('钥匙删除成功')
        detailDialogVisible.value = false
        loadKeys()
      } catch (error) {
        if (error !== 'cancel') {
          console.error('删除钥匙失败:', error)
          ElMessage.error('删除钥匙失败')
        }
      }
    }

    const resetAddForm = () => {
      addForm.room = ''
      if (addFormRef.value) {
        addFormRef.value.resetFields()
      }
    }

    const handleDetailClose = () => {
      detailDialogVisible.value = false
      selectedKey.value = null
    }

    const handleAddClose = () => {
      addDialogVisible.value = false
      resetAddForm()
    }

    onMounted(() => {
      loadKeys()
    })

    return {
      keys,
      users,
      loading,
      detailDialogVisible,
      addDialogVisible,
      selectedKey,
      addFormRef,
      addForm,
      addRules,
      submitting,
      loadKeys,
      isKeyBorrowed,
      getKeyBorrower,
      showKeyDetail,
      showAddDialog,
      submitAddForm,
      confirmDeleteKey,
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

.key-list {
  max-width: 400px;
  margin: 0 auto;
}

.key-card {
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

.key-card:hover {
  background: rgba(0, 255, 255, 0.1);
  border-color: #00ffff;
  transform: translateY(-2px);
}

.key-card.borrowed {
  background: rgba(255, 0, 0, 0.1);
  border-color: rgba(255, 0, 0, 0.3);
}

.key-card.borrowed:hover {
  background: rgba(255, 0, 0, 0.2);
  border-color: #ff6b6b;
}

.key-info {
  flex: 1;
}

.room-number {
  color: #ffffff;
  font-weight: 600;
  font-size: 16px;
  margin-bottom: 5px;
}

.key-details {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 5px;
}

.key-id {
  color: #aaa;
  font-size: 12px;
}

.borrower-info {
  color: #ff6b6b;
  font-size: 12px;
}

.borrower-name {
  font-weight: 500;
}

.key-actions {
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

.key-detail {
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

@media (max-width: 480px) {
  .bottom-actions {
    flex-direction: column;
  }
  
  .action-btn {
    height: 45px;
  }
}
</style>