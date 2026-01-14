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
        <div class="key-icon">📤</div>
        <div class="pulse-ring"></div>
        <div class="glow-effect"></div>
      </div>
      <h1 class="page-title">借钥匙</h1>
      <p class="page-subtitle">Borrow Key</p>
    </div>

    <!-- 主要内容区域 -->
    <div class="main-content">
      <el-form
        ref="borrowFormRef"
        :model="borrowForm"
        :rules="borrowRules"
        class="borrow-form glass-form"
      >
        <!-- 个人信息 -->
        <div class="form-row">
          <el-form-item prop="name" class="form-item">
            <div class="input-wrapper">
              <span class="input-icon">👤</span>
              <el-input
                v-model="borrowForm.name"
                placeholder="姓名 Name"
                size="large"
              />
            </div>
          </el-form-item>
          
          <el-form-item prop="studentId" class="form-item">
            <div class="input-wrapper">
              <span class="input-icon">🏷️</span>
              <el-input
                v-model="borrowForm.studentId"
                :placeholder="borrowForm.identity === 'teacher' ? '工号 ID' : '学号 Student ID'"
                size="large"
              />
            </div>
          </el-form-item>
        </div>

        <!-- 身份和班级 -->
        <div class="form-row">
          <el-form-item prop="identity" class="form-item">
            <div class="identity-card-group">
              <div 
                class="identity-card"
                :class="{ active: borrowForm.identity === 'student' }"
                @click="borrowForm.identity = 'student'"
              >
                <div class="identity-icon">👤</div>
                <div class="identity-text">
                  <div class="identity-title">学生</div>
                  <div class="identity-subtitle">Student</div>
                </div>
              </div>
              <div 
                class="identity-card"
                :class="{ active: borrowForm.identity === 'teacher' }"
                @click="borrowForm.identity = 'teacher'"
              >
                <div class="identity-icon">👨‍🏫</div>
                <div class="identity-text">
                  <div class="identity-title">老师</div>
                  <div class="identity-subtitle">Teacher</div>
                </div>
              </div>
            </div>
          </el-form-item>
          
          <el-form-item prop="classOrOffice" class="form-item" v-if="borrowForm.identity === 'teacher'">
            <div class="input-wrapper">
              <span class="input-icon">🏫</span>
              <el-input
                v-model="borrowForm.classOrOffice"
                placeholder="班级/办公室 Class/Office"
                size="large"
              />
            </div>
          </el-form-item>
        </div>

        <!-- 钥匙选择和借用理由 -->
        <div class="form-row">
          <el-form-item prop="keyId" class="form-item">
            <div class="input-wrapper">
              <span class="input-icon">🔑</span>
              <el-select
                v-model="borrowForm.keyId"
                placeholder="选择钥匙 Select Key"
                size="large"
                style="width: 100%"
                popper-class="borrow-select-dropdown"
                @change="onKeySelect"
              >
                <el-option
                  v-for="key in availableKeys"
                  :key="key.id"
                  :label="key.is_borrowed ? `${key.room}号房间 - 已借出 (${key.borrower_name || 'Unknown'})` : `${key.room}号房间 Room ${key.room}`"
                  :value="key.id"
                  :disabled="key.is_borrowed"
                  :class="key.is_borrowed ? 'option-borrowed' : 'option-available'"
                />
              </el-select>
            </div>
          </el-form-item>
        </div>

        <!-- 借用理由 -->
        <div class="form-row">
          <el-form-item prop="reason" class="form-item full-width">
            <div class="input-wrapper">
              <span class="input-icon">📝</span>
              <el-input
                v-model="borrowForm.reason"
                type="textarea"
                placeholder="请输入借用理由 Please enter the reason for borrowing"
                :rows="3"
                size="large"
                maxlength="200"
                show-word-limit
              />
            </div>
          </el-form-item>
        </div>
      </el-form>
    </div>

    <!-- 底部按钮 -->
    <div class="bottom-actions">
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
        <span>{{ submitting ? '提交中...' : '提交申请' }}</span>
      </el-button>
    </div>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { ArrowLeft, RefreshLeft, Check } from '@element-plus/icons-vue'
import { userAPI, keyAPI } from '../api'

export default {
  name: 'BorrowKey',
  components: {
    ArrowLeft,
    RefreshLeft,
    Check
  },
  setup() {
    const borrowFormRef = ref()
    const submitting = ref(false)
    const availableKeys = ref([])
    const selectedRoom = ref('')

    const borrowForm = reactive({
      name: '',
      identity: 'student',
      studentId: '',
      grade: '',
      classOrOffice: '',
      keyId: null,
      reason: ''
    })

    const borrowRules = {
      name: [
        { required: true, message: '请输入姓名', trigger: 'blur' }
      ],
      identity: [
        { required: true, message: '请选择身份类型', trigger: 'change' }
      ],
      studentId: [
        { required: true, message: '请输入学号/工号', trigger: 'blur' },
        {
          validator: (rule, value, callback) => {
            if (borrowForm.identity === 'student' && value && !/^\d{6}$/.test(value)) {
              callback(new Error('学生学号必须是6位数字'))
            } else {
              callback()
            }
          },
          trigger: 'blur'
        }
      ],
      keyId: [
        { required: true, message: '请选择要借用的钥匙', trigger: 'change' }
      ],
      reason: [
        { required: true, message: '请输入借用理由', trigger: 'blur' }
      ]
    }

    const loadAvailableKeys = async () => {
      try {
        const keys = await keyAPI.getKeys()
        // 这里可以添加逻辑来过滤已被借用的钥匙
        availableKeys.value = keys
      } catch (error) {
        console.error('加载钥匙列表失败:', error)
        ElMessage.error('加载钥匙列表失败')
      }
    }

    const onKeySelect = () => {
      const selectedKey = availableKeys.value.find(key => key.id === borrowForm.keyId)
      if (selectedKey) {
        selectedRoom.value = selectedKey.room
      }
    }

    const submitForm = async () => {
      if (!borrowFormRef.value) return

      try {
        await borrowFormRef.value.validate()
        submitting.value = true

        // 首先创建或查找用户
        const userData = {
          name: borrowForm.name,
          identity: borrowForm.identity,
          student_id: borrowForm.studentId,
          grade: borrowForm.grade || null,
          class_: borrowForm.classOrOffice || null,
          office: borrowForm.identity === 'teacher' ? borrowForm.classOrOffice : null
        }

        // 创建用户
        const user = await userAPI.createUser(userData)
        
        // 借钥匙
        await userAPI.borrowKey(user.id, borrowForm.keyId, borrowForm.reason)

        ElMessage.success('钥匙借用申请提交成功！')
        
        // 显示成功动画
        showSuccessAnimation()
        
        // 重置表单
        setTimeout(() => {
          resetForm()
        }, 2000)

      } catch (error) {
        console.error('提交失败:', error)
        if (error.response?.data?.error) {
          ElMessage.error(error.response.data.error)
        } else {
          ElMessage.error('提交失败，请重试')
        }
      } finally {
        submitting.value = false
      }
    }

    const resetForm = () => {
      if (borrowFormRef.value) {
        borrowFormRef.value.resetFields()
      }
      selectedRoom.value = ''
      Object.assign(borrowForm, {
        name: '',
        identity: 'student',
        studentId: '',
        grade: '',
        classOrOffice: '',
        keyId: null,
        reason: ''
      })
    }

    const showSuccessAnimation = () => {
      // 创建成功动画效果
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
          <div style="font-size: 4rem; margin-bottom: 20px;">✅</div>
          <h2 style="color: #00ffff; margin-bottom: 10px;">借用成功！</h2>
          <p>钥匙借用申请已成功提交</p>
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

    onMounted(() => {
      loadAvailableKeys()
    })

    return {
      borrowFormRef,
      borrowForm,
      borrowRules,
      submitting,
      availableKeys,
      selectedRoom,
      submitForm,
      resetForm,
      onKeySelect
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
  50% { transform: translateY(-5px) rotate(5deg); }
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
  justify-content: center;
  padding: 0 20px;
  overflow: hidden;
}

.borrow-form {
  max-width: 450px;
  margin: 0 auto;
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

.identity-card-group {
  display: flex;
  gap: 12px;
  width: 100%;
}

.identity-card {
  flex: 1;
  background: linear-gradient(145deg, rgba(255, 255, 255, 0.08), rgba(0, 0, 0, 0.3));
  border-radius: 16px;
  padding: 12px 14px;
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
  border: 2px solid transparent;
  box-shadow: 0 6px 18px rgba(0, 0, 0, 0.35);
  transition: all 0.25s ease;
}

.identity-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 25px rgba(0, 255, 255, 0.25);
}

.identity-card.active {
  border-color: rgba(0, 255, 255, 0.8);
  box-shadow:
    0 0 18px rgba(0, 255, 255, 0.35),
    0 6px 20px rgba(0, 0, 0, 0.6);
  background: radial-gradient(circle at top left, rgba(0, 255, 255, 0.35), rgba(0, 0, 0, 0.7));
}

.identity-icon {
  font-size: 20px;
  filter: drop-shadow(0 0 6px rgba(0, 255, 255, 0.7));
}

.identity-text {
  display: flex;
  flex-direction: column;
}

.identity-title {
  font-size: 15px;
  font-weight: 600;
  color: #ffffff;
}

.identity-subtitle {
  font-size: 11px;
  color: #66ccff;
  opacity: 0.9;
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
  z-index: 1;
  filter: drop-shadow(0 0 5px rgba(0, 255, 255, 0.5));
  pointer-events: none;
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
  height: 60px;
  padding-left: 50px !important;
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
  padding-left: 0 !important;
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

:deep(.el-select) {
  width: 100%;
}

:deep(.el-select .el-input) {
  height: 60px;
}

:deep(.el-select__wrapper) {
  border-radius: 12px !important;
  background: transparent !important;
  box-shadow: none !important;
  min-height: 60px !important;
}

:deep(.el-select .el-input__wrapper) {
  padding-left: 50px !important;
  padding-right: 35px !important;
  background: rgba(255, 255, 255, 0.05) !important;
  border: 2px solid rgba(255, 255, 255, 0.2) !important;
  border-radius: 12px !important;
  height: 60px !important;
  transition: all 0.3s ease !important;
  box-shadow: inset 0 2px 10px rgba(0, 0, 0, 0.2) !important;
}

:deep(.el-select__selected-item) {
  color: #00ffff !important;
  font-weight: 500 !important;
  font-size: 16px !important;
}

:deep(.el-select__selected-item.el-select__placeholder) {
  color: #666 !important;
}

:deep(.el-select .el-input__wrapper:hover) {
  border-color: rgba(0, 255, 255, 0.5) !important;
  background: rgba(255, 255, 255, 0.08) !important;
}

:deep(.el-select .el-input__wrapper.is-focus) {
  border-color: #00ffff !important;
  box-shadow: 
    0 0 20px rgba(0, 255, 255, 0.3),
    inset 0 2px 10px rgba(0, 0, 0, 0.2) !important;
  background: rgba(255, 255, 255, 0.1) !important;
}

:deep(.el-select .el-input__inner) {
  padding-left: 0 !important;
  padding-right: 0 !important;
  color: #ffffff !important;
  font-size: 16px !important;
  font-weight: 500 !important;
  height: 56px !important;
  line-height: 56px !important;
  background: transparent !important;
}

:deep(.el-select__placeholder) {
  color: #666 !important;
  font-weight: 400 !important;
}

:deep(.el-select .el-select__caret),
:deep(.el-select .el-select__icon) {
  color: #00ffff !important;
  font-size: 14px !important;
}

/* 让下拉箭头更像普通输入框的装饰 */
:deep(.el-select .el-select__caret.is-reverse),
:deep(.el-select .el-select__icon.is-reverse) {
  transform: rotateZ(180deg) !important;
}

:deep(.el-select-dropdown) {
  background: rgba(10, 14, 39, 0.98) !important;
  backdrop-filter: blur(20px) !important;
  border: 2px solid rgba(0, 255, 255, 0.3) !important;
  border-radius: 12px !important;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5) !important;
  margin-top: 5px !important;
}

:deep(.el-select-dropdown__item) {
  color: #ffffff !important;
  transition: all 0.2s ease !important;
  background: transparent !important;
  padding: 12px 20px !important;
  font-size: 15px !important;
}

:deep(.el-select-dropdown__item:hover) {
  background: rgba(0, 255, 255, 0.15) !important;
  color: #00ffff !important;
}

:deep(.el-select-dropdown__item.selected) {
  background: rgba(0, 255, 255, 0.25) !important;
  color: #00ffff !important;
  font-weight: 600 !important;
}

:deep(.el-select-dropdown__item.is-hovering) {
  background: rgba(0, 255, 255, 0.15) !important;
  color: #00ffff !important;
}

:deep(.el-select-dropdown__item.option-available) {
  color: #00ffff !important;
}

:deep(.el-select-dropdown__item.option-borrowed) {
  color: #888888 !important;
}

:deep(.el-textarea__inner) {
  background: rgba(255, 255, 255, 0.05) !important;
  border: 2px solid rgba(255, 255, 255, 0.2) !important;
  border-radius: 12px !important;
  color: #ffffff !important;
  font-size: 15px !important;
  font-weight: 500 !important;
  padding: 15px 50px 15px 50px !important;
  transition: all 0.3s ease !important;
  box-shadow: inset 0 2px 10px rgba(0, 0, 0, 0.2) !important;
  resize: vertical !important;
  min-height: 80px !important;
}

:deep(.el-textarea__inner:hover) {
  border-color: rgba(0, 255, 255, 0.5) !important;
  background: rgba(255, 255, 255, 0.08) !important;
}

:deep(.el-textarea__inner:focus) {
  border-color: #00ffff !important;
  box-shadow: 
    0 0 20px rgba(0, 255, 255, 0.3),
    inset 0 2px 10px rgba(0, 0, 0, 0.2) !important;
  background: rgba(255, 255, 255, 0.1) !important;
}

:deep(.el-textarea__inner::placeholder) {
  color: #666 !important;
  font-weight: 400 !important;
}

:deep(.el-input__count) {
  background: rgba(0, 0, 0, 0.3) !important;
  color: #00ffff !important;
  border-radius: 8px !important;
  padding: 2px 8px !important;
  font-size: 12px !important;
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
}
</style>

<style>
/* 全局样式覆盖 - 用于 Element Plus 下拉菜单 */
.borrow-select-dropdown.el-select-dropdown {
  background: rgba(10, 14, 39, 0.98) !important;
  backdrop-filter: blur(20px) !important;
  border: 2px solid rgba(0, 255, 255, 0.3) !important;
  border-radius: 12px !important;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5) !important;
}

.borrow-select-dropdown .el-select-dropdown__item {
  transition: all 0.2s ease !important;
  background: transparent !important;
  padding: 12px 20px !important;
  font-size: 15px !important;
}

.borrow-select-dropdown .el-select-dropdown__item:hover,
.borrow-select-dropdown .el-select-dropdown__item.is-hovering {
  background: rgba(0, 255, 255, 0.15) !important;
}

.borrow-select-dropdown .el-select-dropdown__item.selected {
  background: rgba(0, 255, 255, 0.25) !important;
  font-weight: 600 !important;
}

/* 可用钥匙 - 亮青色 */
.borrow-select-dropdown .el-select-dropdown__item.option-available {
  color: #00ffff !important;
}

.borrow-select-dropdown .el-select-dropdown__item.option-available.selected {
  color: #00ffff !important;
}

/* 已借出钥匙 - 灰色 */
.borrow-select-dropdown .el-select-dropdown__item.option-borrowed {
  color: #666666 !important;
}

.borrow-select-dropdown .el-select-dropdown__item.option-borrowed.is-disabled {
  color: #666666 !important;
}
</style>
