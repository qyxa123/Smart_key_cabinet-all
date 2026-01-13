
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
      <div class="logo-icon">
        <div class="key-icon">🔑</div>
        <div class="pulse-ring"></div>
      </div>
      <h1 class="page-title">还钥匙</h1>
      <p class="page-subtitle">Return Key</p>
      <el-button @click="$router.push('/')" class="back-btn">
        <el-icon><ArrowLeft /></el-icon>
        返回主页
      </el-button>
    </div>

    <!-- 主要内容区域 -->
    <div class="glass-card main-content">
      <div class="form-header">
        <h2>钥匙归还申请</h2>
        <p class="bilingual-subtitle">Key Return Application</p>
        <p>请填写以下信息完成钥匙归还</p>
        <p class="bilingual-subtitle">Please fill in the following information to complete key return</p>
      </div>

      <el-form
        ref="returnFormRef"
        :model="returnForm"
        :rules="returnRules"
        label-width="120px"
        class="return-form"
      >
        <!-- 身份验证部分 -->
        <div class="form-section">
          <h3>身份验证</h3>
          <p class="bilingual-subtitle">Identity Verification</p>
          
          <el-row :gutter="20">
            <el-col :span="12">
              <el-form-item label="姓名" prop="name" required>
                <el-input
                  v-model="returnForm.name"
                  placeholder="请输入您的姓名"
                  @blur="searchUser"
                />
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="学号/工号" prop="studentId" required>
                <el-input
                  v-model="returnForm.studentId"
                  placeholder="请输入学号或工号"
                  @blur="searchUser"
                />
              </el-form-item>
            </el-col>
          </el-row>
        </div>

        <!-- 借用记录 -->
        <div class="form-section" v-if="borrowedKeys.length > 0">
          <h3>您的借用记录</h3>
          <p class="bilingual-subtitle">Your Borrowed Keys</p>
          
          <el-table :data="borrowedKeys" style="width: 100%">
            <el-table-column prop="id" label="钥匙ID" width="80" />
            <el-table-column prop="room" label="房间号" width="120" />
            <el-table-column label="操作" width="120">
              <template #default="scope">
                <el-button 
                  type="primary" 
                  size="small"
                  @click="selectKeyToReturn(scope.row)"
                >
                  选择归还
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </div>

        <!-- 钥匙信息部分 -->
        <div class="form-section">
          <h3>归还钥匙信息</h3>
          <p class="bilingual-subtitle">Return Key Information</p>
          
          <el-row :gutter="20">
            <el-col :span="12">
              <el-form-item label="钥匙ID" prop="keyId" required>
                <el-input
                  v-model="returnForm.keyId"
                  placeholder="请输入要归还的钥匙ID"
                  readonly
                />
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="房间号">
                <el-input
                  v-model="returnForm.roomNumber"
                  placeholder="选择钥匙后自动填充"
                  readonly
                />
              </el-form-item>
            </el-col>
          </el-row>
        </div>

        <!-- 使用情况反馈 -->
        <div class="form-section">
          <h3>使用情况反馈</h3>
          <p class="bilingual-subtitle">Usage Feedback</p>
          
          <el-form-item label="钥匙状态" prop="keyCondition" required>
            <el-radio-group v-model="returnForm.keyCondition">
              <el-radio label="excellent">完好无损 (Excellent)</el-radio>
              <el-radio label="good">轻微磨损 (Good)</el-radio>
              <el-radio label="damaged">有损坏 (Damaged)</el-radio>
            </el-radio-group>
          </el-form-item>
          
          <el-form-item label="使用备注">
            <el-input
              v-model="returnForm.usageNotes"
              type="textarea"
              :rows="3"
              placeholder="请描述钥匙的使用情况或任何需要说明的事项"
            />
          </el-form-item>
        </div>

        <!-- 服务评价 -->
        <div class="form-section">
          <h3>服务评价</h3>
          <p class="bilingual-subtitle">Service Rating</p>
          
          <el-form-item label="满意度" prop="satisfaction" required>
            <el-rate
              v-model="returnForm.satisfaction"
              :colors="['#ff6b6b', '#ffa500', '#00ffff']"
              show-text
              :texts="['非常不满意', '不满意', '一般', '满意', '非常满意']"
            />
          </el-form-item>
          
          <el-form-item label="改进建议">
            <el-input
              v-model="returnForm.suggestions"
              type="textarea"
              :rows="3"
              placeholder="请提供您的宝贵建议，帮助我们改进服务"
            />
          </el-form-item>
        </div>

        <!-- 提交按钮 -->
        <div class="form-actions">
          <el-button @click="resetForm">重置表单</el-button>
          <el-button type="primary" @click="submitForm" :loading="submitting">
            确认归还
          </el-button>
        </div>
      </el-form>
    </div>
  </div>
</template>

<script>
import { ref, reactive, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { ArrowLeft } from '@element-plus/icons-vue'
import { userAPI } from '../api'

export default {
  name: 'ReturnKey',
  components: {
    ArrowLeft
  },
  setup() {
    const returnFormRef = ref()
    const submitting = ref(false)
    const borrowedKeys = ref([])
    const currentUser = ref(null)

    const returnForm = reactive({
      name: '',
      studentId: '',
      keyId: '',
      roomNumber: '',
      keyCondition: 'excellent',
      usageNotes: '',
      satisfaction: 5,
      suggestions: ''
    })

    const returnRules = {
      name: [
        { required: true, message: '请输入姓名', trigger: 'blur' }
      ],
      studentId: [
        { required: true, message: '请输入学号/工号', trigger: 'blur' }
      ],
      keyId: [
        { required: true, message: '请选择要归还的钥匙', trigger: 'change' }
      ],
      keyCondition: [
        { required: true, message: '请选择钥匙状态', trigger: 'change' }
      ],
      satisfaction: [
        { required: true, message: '请进行服务评价', trigger: 'change' }
      ]
    }

    const searchUser = async () => {
      if (!returnForm.name || !returnForm.studentId) return

      try {
        const users = await userAPI.getUsers()
        const user = users.find(u => 
          u.name === returnForm.name && 
          (u.id.toString() === returnForm.studentId || u.name === returnForm.name)
        )

        if (user && user.keys && user.keys.length > 0) {
          currentUser.value = user
          borrowedKeys.value = user.keys
          ElMessage.success(`找到用户 ${user.name}，共借用 ${user.keys.length} 把钥匙`)
        } else if (user) {
          ElMessage.warning('该用户当前没有借用钥匙')
          borrowedKeys.value = []
        } else {
          ElMessage.error('未找到匹配的用户信息')
          borrowedKeys.value = []
        }
      } catch (error) {
        console.error('搜索用户失败:', error)
        ElMessage.error('搜索用户失败')
      }
    }

    const selectKeyToReturn = (key) => {
      returnForm.keyId = key.id.toString()
      returnForm.roomNumber = key.room
      ElMessage.success(`已选择归还 ${key.room} 号房间的钥匙`)
    }

    const submitForm = async () => {
      if (!returnFormRef.value) return

      try {
        await returnFormRef.value.validate()
        
        if (!currentUser.value) {
          ElMessage.error('请先验证身份信息')
          return
        }

        submitting.value = true

        // 归还钥匙
        await userAPI.returnKey(currentUser.value.id, parseInt(returnForm.keyId))

        ElMessage.success('钥匙归还成功！')
        
        // 显示成功动画
        showSuccessAnimation()
        
        // 重置表单
        setTimeout(() => {
          resetForm()
        }, 2000)

      } catch (error) {
        console.error('归还失败:', error)
        if (error.response?.data?.error) {
          ElMessage.error(error.response.data.error)
        } else {
          ElMessage.error('归还失败，请重试')
        }
      } finally {
        submitting.value = false
      }
    }

    const resetForm = () => {
      if (returnFormRef.value) {
        returnFormRef.value.resetFields()
      }
      borrowedKeys.value = []
      currentUser.value = null
      Object.assign(returnForm, {
        name: '',
        studentId: '',
        keyId: '',
        roomNumber: '',
        keyCondition: 'excellent',
        usageNotes: '',
        satisfaction: 5,
        suggestions: ''
      })
    }

    const showSuccessAnimation = () => {
      const overlay = document.createElement('div')
      overlay.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(135deg, rgba(0, 0, 0, 0.9), rgba(26, 26, 46, 0.95));
        z-index: 10000;
        display: flex;
        align-items: center;
        justify-content: center;
        animation: fadeIn 0.5s ease-out;
      `
      
      overlay.innerHTML = `
        <div style="text-align: center; color: #ffffff;">
          <div style="font-size: 4rem; margin-bottom: 20px;">🎉</div>
          <h2 style="color: #00ffff; margin-bottom: 10px;">归还成功！</h2>
          <p>感谢您使用智能钥匙柜系统</p>
        </div>
      `
      
      document.body.appendChild(overlay)
      
      setTimeout(() => {
        overlay.style.animation = 'fadeOut 0.5s ease-out'
        setTimeout(() => {
          document.body.removeChild(overlay)
        }, 500)
      }, 2000)
    }

    return {
      returnFormRef,
      returnForm,
      returnRules,
      submitting,
      borrowedKeys,
      currentUser,
      searchUser,
      selectKeyToReturn,
      submitForm,
      resetForm
    }
  }
}
</script>

<style scoped>
.main-content {
  padding: 40px;
  max-width: 800px;
  margin: 0 auto;
}

.back-btn {
  position: absolute;
  top: 20px;
  left: 20px;
}

.form-header {
  text-align: center;
  margin-bottom: 40px;
}

.form-header h2 {
  font-size: 2rem;
  margin-bottom: 10px;
  color: #ffffff;
}

.form-section {
  margin-bottom: 40px;
  padding: 25px;
  background: rgba(0, 0, 0, 0.2);
  border-radius: 15px;
  border: 1px solid rgba(0, 255, 255, 0.1);
}

.form-section h3 {
  color: #00ffff;
  margin-bottom: 20px;
  font-size: 1.3rem;
  border-bottom: 1px solid rgba(0, 255, 255, 0.3);
  padding-bottom: 10px;
}

.form-actions {
  display: flex;
  gap: 20px;
  justify-content: center;
  margin-top: 40px;
}

.logo-icon {
  position: relative;
  width: 80px;
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 20px;
}

.key-icon {
  font-size: 40px;
  z-index: 2;
  position: relative;
}

.pulse-ring {
  position: absolute;
  width: 100%;
  height: 100%;
  border: 2px solid #00ffff;
  border-radius: 50%;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% {
    transform: scale(0.8);
    opacity: 1;
  }
  100% {
    transform: scale(1.2);
    opacity: 0;
  }
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes fadeOut {
  from { opacity: 1; }
  to { opacity: 0; }
}

@media (max-width: 768px) {
  .main-content {
    padding: 20px;
  }
  
  .form-section {
    padding: 15px;
  }
  
  .form-actions {
    flex-direction: column;
  }
}
</style>