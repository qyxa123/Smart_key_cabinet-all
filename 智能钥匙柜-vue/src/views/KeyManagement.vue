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
      <h1 class="page-title">钥匙管理</h1>
      <p class="page-subtitle">Key Management</p>
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
          添加钥匙
        </el-button>
        <el-button @click="loadKeys">
          <el-icon><Refresh /></el-icon>
          刷新
        </el-button>
      </div>

      <!-- 钥匙表格 -->
      <el-table 
        :data="keys" 
        style="width: 100%" 
        v-loading="loading"
        empty-text="暂无钥匙数据"
      >
        <el-table-column prop="id" label="钥匙ID" width="100" />
        <el-table-column prop="room" label="房间号" width="150" />
        <el-table-column label="使用状态" width="150">
          <template #default="scope">
            <el-tag :type="isKeyBorrowed(scope.row) ? 'danger' : 'success'">
              {{ isKeyBorrowed(scope.row) ? '已借出' : '可用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="借用者" width="200">
          <template #default="scope">
            <div v-if="scope.row.users && scope.row.users.length > 0">
              <el-tag 
                v-for="user in scope.row.users" 
                :key="user.id"
                size="small"
                type="info"
                style="margin-right: 5px;"
              >
                {{ user.name }} ({{ user.identity === 'teacher' ? '老师' : '学生' }})
              </el-tag>
            </div>
            <span v-else style="color: #999;">无</span>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200">
          <template #default="scope">
            <el-button size="small" @click="editKey(scope.row)">编辑</el-button>
            <el-button 
              size="small" 
              type="danger" 
              @click="deleteKey(scope.row)"
              :disabled="isKeyBorrowed(scope.row)"
            >
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <!-- 添加/编辑钥匙对话框 -->
    <el-dialog
      :title="dialogTitle"
      v-model="dialogVisible"
      width="400px"
    >
      <el-form
        ref="keyFormRef"
        :model="keyForm"
        :rules="keyRules"
        label-width="80px"
      >
        <el-form-item label="房间号" prop="room">
          <el-input 
            v-model="keyForm.room" 
            placeholder="请输入房间号，如：101、205"
            maxlength="10"
          />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="saveKey" :loading="saving">
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
import { keyAPI } from '../api'

export default {
  name: 'KeyManagement',
  components: {
    ArrowLeft,
    Plus,
    Refresh
  },
  setup() {
    const keys = ref([])
    const loading = ref(false)
    const dialogVisible = ref(false)
    const dialogTitle = ref('添加钥匙')
    const keyFormRef = ref()
    const saving = ref(false)
    const editingKeyId = ref(null)

    const keyForm = reactive({
      room: ''
    })

    const keyRules = {
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
        const data = await keyAPI.getKeys()
        keys.value = data
      } catch (error) {
        console.error('加载钥匙列表失败:', error)
        ElMessage.error('加载钥匙列表失败')
      } finally {
        loading.value = false
      }
    }

    const isKeyBorrowed = (key) => {
      return key.users && key.users.length > 0
    }

    const showAddDialog = () => {
      dialogTitle.value = '添加钥匙'
      editingKeyId.value = null
      resetForm()
      dialogVisible.value = true
    }

    const editKey = (key) => {
      dialogTitle.value = '编辑钥匙'
      editingKeyId.value = key.id
      keyForm.room = key.room
      dialogVisible.value = true
    }

    const saveKey = async () => {
      if (!keyFormRef.value) return

      try {
        await keyFormRef.value.validate()
        saving.value = true

        const keyData = {
          room: keyForm.room
        }

        if (editingKeyId.value) {
          await keyAPI.updateKey(editingKeyId.value, keyData)
          ElMessage.success('钥匙更新成功')
        } else {
          await keyAPI.createKey(keyData)
          ElMessage.success('钥匙添加成功')
        }

        dialogVisible.value = false
        loadKeys()
      } catch (error) {
        console.error('保存钥匙失败:', error)
        if (error.response?.status === 400) {
          ElMessage.error('该房间号的钥匙已存在')
        } else {
          ElMessage.error('保存钥匙失败')
        }
      } finally {
        saving.value = false
      }
    }

    const deleteKey = async (key) => {
      if (isKeyBorrowed(key)) {
        ElMessage.warning('该钥匙正在被借用，无法删除')
        return
      }

      try {
        await ElMessageBox.confirm(
          `确定要删除 "${key.room}" 号房间的钥匙吗？`,
          '确认删除',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }
        )

        await keyAPI.deleteKey(key.id)
        ElMessage.success('钥匙删除成功')
        loadKeys()
      } catch (error) {
        if (error !== 'cancel') {
          console.error('删除钥匙失败:', error)
          ElMessage.error('删除钥匙失败')
        }
      }
    }

    const resetForm = () => {
      keyForm.room = ''
      if (keyFormRef.value) {
        keyFormRef.value.resetFields()
      }
    }

    onMounted(() => {
      loadKeys()
    })

    return {
      keys,
      loading,
      dialogVisible,
      dialogTitle,
      keyFormRef,
      keyForm,
      keyRules,
      saving,
      loadKeys,
      isKeyBorrowed,
      showAddDialog,
      editKey,
      saveKey,
      deleteKey
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