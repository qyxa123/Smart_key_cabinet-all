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
        class="borrow-form"
      >
        <!-- 个人信息 -->
        <div class="form-row">
          <el-form-item prop="name" class="form-item">
            <el-input
              v-model="borrowForm.name"
              placeholder="姓名 Name"
              size="large"
            />
          </el-form-item>
          
          <el-form-item prop="studentId" class="form-item">
            <el-input
              v-model="borrowForm.studentId"
              :placeholder="borrowForm.identity === 'teacher' ? '工号 ID' : '学号 Student ID'"
              size="large"
            />
          </el-form-item>
        </div>

        <!-- 身份和班级 -->
        <div class="form-row">
          <el-form-item prop="identity" class="form-item">
            <el-select
              v-model="borrowForm.identity"
              placeholder="身份类型"
              size="large"
              style="width: 100%"
            >
              <el-option label="学生 Student" value="student" />
              <el-option label="老师 Teacher" value="teacher" />
            </el-select>
          </el-form-item>
          
          <el-form-item prop="classOrOffice" class="form-item">
            <el-input
              v-model="borrowForm.classOrOffice"
              placeholder="班级/办公室 Class/Office"
              size="large"
            />
          </el-form-item>
        </div>

        <!-- 钥匙选择 -->
        <div class="form-row">
          <el-form-item prop="keyId" class="form-item full-width">
            <el-select
              v-model="borrowForm.keyId"
              placeholder="选择钥匙 Select Key"
              size="large"
              style="width: 100%"
              @change="onKeySelect"
            >
              <el-option
                v-for="key in availableKeys"
                :key="key.id"
                :label="`${key.room}号房间 Room ${key.room}`"
                :value="key.id"
              />
            </el-select>
          </el-form-item>
        </div>
      </el-form>
    </div>

    <!-- 底部按钮 -->
    <div class="bottom-actions">
      <el-button @click="resetForm" size="large" class="action-btn secondary">
        重置 Reset
      </el-button>
      <el-button 
        type="primary" 
        @click="submitForm" 
        :loading="submitting"
        size="large"
        class="action-btn primary"
      >
        {{ submitting ? '提交中...' : '提交申请 Submit' }}
      </el-button>
    </div>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { ArrowLeft } from '@element-plus/icons-vue'
import { userAPI, keyAPI } from '../api'

export default {
  name: 'BorrowKey',
  components: {
    ArrowLeft
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
      keyId: null
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
          grade: borrowForm.grade || null,
          class_: borrowForm.classOrOffice || null,
          office: borrowForm.identity === 'teacher' ? borrowForm.classOrOffice : null
        }

        // 创建用户
        const user = await userAPI.createUser(userData)
        
        // 借钥匙
        await userAPI.borrowKey(user.id, borrowForm.keyId)

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
        keyId: null
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
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 0 20px;
  overflow: hidden;
}

.borrow-form {
  max-width: 400px;
  margin: 0 auto;
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

/* Element Plus 组件样式覆盖 */
:deep(.el-input__wrapper) {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 8px;
  height: 50px;
}

:deep(.el-input__wrapper:hover) {
  border-color: #00ffff;
}

:deep(.el-input__wrapper.is-focus) {
  border-color: #00ffff;
  box-shadow: 0 0 10px rgba(0, 255, 255, 0.3);
}

:deep(.el-input__inner) {
  color: #ffffff;
  font-size: 16px;
}

:deep(.el-input__inner::placeholder) {
  color: #666;
}

:deep(.el-select .el-input__wrapper) {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

:deep(.el-select-dropdown) {
  background: rgba(26, 26, 46, 0.95);
  border: 1px solid rgba(0, 255, 255, 0.3);
}

:deep(.el-select-dropdown__item) {
  color: #ffffff;
}

:deep(.el-select-dropdown__item:hover) {
  background: rgba(0, 255, 255, 0.1);
}

:deep(.el-select-dropdown__item.selected) {
  background: rgba(0, 255, 255, 0.2);
  color: #00ffff;
}

@media (max-width: 480px) {
  .form-row {
    flex-direction: column;
    gap: 15px;
  }
  
  .bottom-actions {
    flex-direction: column;
  }
  
  .action-btn {
    height: 45px;
  }
}
</style>