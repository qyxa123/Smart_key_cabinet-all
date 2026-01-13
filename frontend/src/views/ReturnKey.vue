
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
        <div class="key-icon">📥</div>
        <div class="pulse-ring"></div>
        <div class="glow-effect"></div>
      </div>
      <h1 class="page-title">还钥匙</h1>
      <p class="page-subtitle">Return Key</p>
    </div>

    <!-- 主要内容区域 -->
    <div class="main-content">
      <el-form
        ref="returnFormRef"
        :model="returnForm"
        :rules="returnRules"
        class="return-form glass-form"
      >
        <!-- 身份验证 -->
        <div class="form-row">
          <el-form-item prop="name" class="form-item">
            <div class="input-wrapper">
              <span class="input-icon">👤</span>
              <el-input
                v-model="returnForm.name"
                placeholder="姓名 Name"
                size="large"
                @blur="searchUser"
              />
            </div>
          </el-form-item>
          
          <el-form-item prop="studentId" class="form-item">
            <div class="input-wrapper">
              <span class="input-icon">🎫</span>
              <el-input
                v-model="returnForm.studentId"
                placeholder="学号/工号 ID"
                size="large"
                @blur="searchUser"
              />
            </div>
          </el-form-item>
        </div>

        <!-- 借用记录 -->
        <div class="borrowed-keys" v-if="borrowedKeys.length > 0">
          <p class="section-title">
            <span class="title-icon">📋</span>
            您的借用记录
          </p>
          <div class="key-list">
            <div 
              v-for="key in borrowedKeys" 
              :key="key.id"
              class="key-item"
              :class="{ active: returnForm.keyId === key.id.toString() }"
              @click="selectKeyToReturn(key)"
            >
              <div class="key-info">
                <span class="room-number">{{ key.room }}号房间</span>
                <span class="key-id">ID: {{ key.id }}</span>
              </div>
              <div class="select-icon">
                {{ returnForm.keyId === key.id.toString() ? '✓' : '→' }}
              </div>
              <div class="item-glow"></div>
            </div>
          </div>
        </div>

        <!-- 钥匙状态 -->
        <div class="form-row" v-if="returnForm.keyId">
          <el-form-item prop="keyCondition" class="form-item full-width">
            <div class="input-wrapper">
              <span class="input-icon">🔍</span>
              <el-select
                v-model="returnForm.keyCondition"
                placeholder="钥匙状态 Key Condition"
                size="large"
                style="width: 100%"
              >
                <el-option label="完好无损 Excellent" value="excellent" />
                <el-option label="轻微磨损 Good" value="good" />
                <el-option label="有损坏 Damaged" value="damaged" />
              </el-select>
            </div>
          </el-form-item>
        </div>

        <!-- 满意度评价 -->
        <div class="rating-section" v-if="returnForm.keyId">
          <p class="section-title">
            <span class="title-icon">⭐</span>
            服务评价
          </p>
          <el-form-item prop="satisfaction" class="rating-item">
            <el-rate
              v-model="returnForm.satisfaction"
              :colors="['#ff6b6b', '#ffa500', '#00ffff']"
              size="large"
              show-text
              :texts="['很差', '较差', '一般', '满意', '很好']"
            />
          </el-form-item>
        </div>
      </el-form>
    </div>

    <!-- 底部按钮 -->
    <div class="bottom-actions" v-if="returnForm.keyId">
      <el-button @click="resetForm" size="large" class="action-btn secondary">
        <el-icon><RefreshLeft /></el-icon>
        <span>重置</span>
      </el-button>
      <el-button 
        type="primary" 
        @click="submitForm" 
        :loading="submitting"
        size="large"
        class="action-btn primary"
      >
        <el-icon v-if="!submitting"><Check /></el-icon>
        <span>{{ submitting ? '归还中...' : '确认归还' }}</span>
      </el-button>
    </div>
  </div>
</template>

<script>
import { ref, reactive, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { ArrowLeft, RefreshLeft, Check } from '@element-plus/icons-vue'
import { userAPI } from '../api'

export default {
  name: 'ReturnKey',
  components: {
    ArrowLeft,
    RefreshLeft,
    Check
  },export default {
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
  background: linear-gradient(135deg, rgba(0, 255, 255, 0.2), rgba(0, 128, 255, 0.2));
  border: 2px solid rgba(0, 255, 255, 0.5);
  color: #00ffff;
  transition: all 0.3s ease;
}

.back-btn:hover {
  background: linear-gradient(135deg, rgba(0, 255, 255, 0.3), rgba(0, 128, 255, 0.3));
  border-color: #00ffff;
  transform: translateX(-3px);
  box-shadow: 0 0 20px rgba(0, 255, 255, 0.5);
}

.logo-icon {
  margin: 10px auto 15px;
  width: 70px;
  height: 70px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, rgba(0, 255, 255, 0.15), rgba(0, 128, 255, 0.15));
  border-radius: 50%;
  border: 2px solid rgba(0, 255, 255, 0.5);
  position: relative;
  box-shadow: 
    0 0 30px rgba(0, 255, 255, 0.3),
    inset 0 0 20px rgba(0, 255, 255, 0.1);
}

.key-icon {
  font-size: 32px;
  z-index: 2;
  filter: drop-shadow(0 0 10px rgba(0, 255, 255, 0.8));
  animation: iconBounce 2s ease-in-out infinite;
}

@keyframes iconBounce {
  0%, 100% { transform: translateY(0px) rotate(0deg); }
  50% { transform: translateY(-5px) rotate(-5deg); }
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
    transform: scale(0.9);
    opacity: 1;
  }
  100% {
    transform: scale(1.3);
    opacity: 0;
  }
}

.glow-effect {
  position: absolute;
  width: 100%;
  height: 100%;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(0, 255, 255, 0.4) 0%, transparent 70%);
  animation: glowPulse 2s ease-in-out infinite;
}

@keyframes glowPulse {
  0%, 100% { transform: scale(1); opacity: 0.5; }
  50% { transform: scale(1.1); opacity: 0.8; }
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 0 20px;
  overflow-y: auto;
}

.return-form {
  max-width: 450px;
  margin: 0 auto;
  flex: 1;
  width: 100%;
}

.glass-form {
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  padding: 25px;
  border: 1px solid rgba(0, 255, 255, 0.2);
  box-shadow: 
    0 8px 32px rgba(0, 0, 0, 0.3),
    inset 0 0 20px rgba(0, 255, 255, 0.05);
}

.form-row {
  display: flex;
  gap: 15px;
  margin-bottom: 20px;
}

.form-item {
  flex: 1;
  margin-bottom: 0;
}

.form-item.full-width {
  flex: none;
  width: 100%;
}

.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.input-icon {
  position: absolute;
  left: 15px;
  font-size: 18px;
  z-index: 10;
  filter: drop-shadow(0 0 5px rgba(0, 255, 255, 0.5));
}

.section-title {
  color: #00ffff;
  font-size: 15px;
  margin-bottom: 15px;
  text-align: center;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  text-shadow: 0 0 10px rgba(0, 255, 255, 0.5);
}

.title-icon {
  font-size: 18px;
  filter: drop-shadow(0 0 8px rgba(0, 255, 255, 0.8));
}

.borrowed-keys {
  margin-bottom: 20px;
}

.key-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.key-item {
  position: relative;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
  background: rgba(255, 255, 255, 0.05);
  border: 2px solid rgba(255, 255, 255, 0.2);
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  overflow: hidden;
}

.key-item:hover {
  background: rgba(0, 255, 255, 0.1);
  border-color: rgba(0, 255, 255, 0.5);
  transform: translateX(5px);
}

.key-item.active {
  background: linear-gradient(135deg, rgba(0, 255, 255, 0.2), rgba(0, 128, 255, 0.2));
  border-color: #00ffff;
  box-shadow: 
    0 0 20px rgba(0, 255, 255, 0.4),
    inset 0 0 20px rgba(0, 255, 255, 0.1);
}

.item-glow {
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: left 0.5s ease;
}

.key-item:hover .item-glow {
  left: 100%;
}

.key-info {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.room-number {
  color: #ffffff;
  font-weight: 600;
  font-size: 16px;
  text-shadow: 0 0 5px rgba(0, 255, 255, 0.3);
}

.key-id {
  color: #aaa;
  font-size: 12px;
}

.select-icon {
  color: #00ffff;
  font-size: 20px;
  font-weight: bold;
  text-shadow: 0 0 10px rgba(0, 255, 255, 0.8);
}

.rating-section {
  margin-bottom: 20px;
}

.rating-item {
  margin-bottom: 0;
}

.rating-item :deep(.el-rate) {
  justify-content: center;
}

.rating-item :deep(.el-rate__icon) {
  font-size: 32px;
  margin: 0 5px;
}

.rating-item :deep(.el-rate__text) {
  color: #00ffff;
  font-size: 15px;
  font-weight: 600;
  text-shadow: 0 0 10px rgba(0, 255, 255, 0.5);
}

.bottom-actions {
  flex-shrink: 0;
  display: flex;
  gap: 15px;
  padding: 20px;
  background: linear-gradient(180deg, transparent, rgba(0, 0, 0, 0.5));
  border-top: 1px solid rgba(0, 255, 255, 0.3);
  backdrop-filter: blur(10px);
}

.action-btn {
  flex: 1;
  height: 55px;
  font-size: 16px;
  font-weight: 600;
  border-radius: 15px;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.action-btn.secondary {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.05));
  border: 2px solid rgba(255, 255, 255, 0.3);
  color: #ffffff;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}

.action-btn.secondary:hover {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.2), rgba(255, 255, 255, 0.1));
  border-color: rgba(255, 255, 255, 0.5);
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(255, 255, 255, 0.2);
}

.action-btn.primary {
  background: linear-gradient(135deg, #00ffff, #0080ff);
  border: 2px solid #00ffff;
  color: #000;
  font-weight: 700;
  box-shadow: 
    0 4px 15px rgba(0, 255, 255, 0.3),
    inset 0 0 20px rgba(255, 255, 255, 0.2);
}

.action-btn.primary:hover {
  background: linear-gradient(135deg, #0080ff, #00ffff);
  transform: translateY(-3px);
  box-shadow: 
    0 8px 30px rgba(0, 255, 255, 0.5),
    inset 0 0 30px rgba(255, 255, 255, 0.3);
}

/* Element Plus 组件样式覆盖 */
:deep(.el-input__wrapper) {
  background: rgba(255, 255, 255, 0.05);
  border: 2px solid rgba(255, 255, 255, 0.2);
  border-radius: 12px;
  height: 50px;
  padding-left: 45px;
  transition: all 0.3s ease;
  box-shadow: inset 0 2px 10px rgba(0, 0, 0, 0.2);
}

:deep(.el-input__wrapper:hover) {
  border-color: rgba(0, 255, 255, 0.5);
  background: rgba(255, 255, 255, 0.08);
}

:deep(.el-input__wrapper.is-focus) {
  border-color: #00ffff;
  box-shadow: 
    0 0 20px rgba(0, 255, 255, 0.3),
    inset 0 2px 10px rgba(0, 0, 0, 0.2);
  background: rgba(255, 255, 255, 0.1);
}

:deep(.el-input__inner) {
  color: #ffffff;
  font-size: 15px;
  font-weight: 500;
}

:deep(.el-input__inner::placeholder) {
  color: #666;
  font-weight: 400;
}

:deep(.el-select .el-input__wrapper) {
  padding-left: 45px;
}

:deep(.el-select-dropdown) {
  background: rgba(26, 26, 46, 0.95);
  backdrop-filter: blur(10px);
  border: 2px solid rgba(0, 255, 255, 0.3);
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5);
}

:deep(.el-select-dropdown__item) {
  color: #ffffff;
  transition: all 0.2s ease;
}

:deep(.el-select-dropdown__item:hover) {
  background: rgba(0, 255, 255, 0.15);
  color: #00ffff;
}

:deep(.el-select-dropdown__item.selected) {
  background: rgba(0, 255, 255, 0.25);
  color: #00ffff;
  font-weight: 600;
}

@media (max-width: 480px) {
  .form-row {
    flex-direction: column;
    gap: 15px;
  }
  
  .glass-form {
    padding: 20px;
  }
  
  .bottom-actions {
    flex-direction: column;
  }
  
  .action-btn {
    height: 50px;
  }
  
  .rating-item :deep(.el-rate__icon) {
    font-size: 28px;
    margin: 0 3px;
  }
}
</style>