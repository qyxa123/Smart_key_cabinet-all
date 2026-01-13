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
      <h1 class="page-title">借钥匙</h1>
      <p class="page-subtitle">Borrow Key</p>
      <el-button @click="$router.push('/')" class="back-btn">
        <el-icon><ArrowLeft /></el-icon>
        返回主页
      </el-button>
    </div>

    <!-- 主要内容区域 -->
    <div class="glass-card main-content">
      <div class="form-header">
        <h2>钥匙借用申请</h2>
        <p class="bilingual-subtitle">Key Borrowing Application</p>
        <p>请填写以下信息完成钥匙借用</p>
        <p class="bilingual-subtitle">Please fill in the following information to complete key borrowing</p>
      </div>

      <el-form
        ref="borrowFormRef"
        :model="borrowForm"
        :rules="borrowRules"
        label-width="120px"
        class="borrow-form"
      >
        <!-- 个人信息部分 -->
        <div class="form-section">
          <h3>个人信息</h3>
          <p class="bilingual-subtitle">Personal Information</p>
          
          <el-form-item label="身份类型" prop="identity" required>
            <el-radio-group v-model="borrowForm.identity">
              <el-radio label="teacher">老师 (Teacher)</el-radio>
              <el-radio label="student">学生 (Student)</el-radio>
            </el-radio-group>
          </el-form-item>
          
          <el-row :gutter="20">
            <el-col :span="12">
              <el-form-item label="姓名" prop="name" required>
                <el-input
                  v-model="borrowForm.name"
                  placeholder="请输入您的姓名"
                />
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item 
                :label="borrowForm.identity === 'teacher' ? '工号' : '学号'" 
                prop="studentId" 
                required
              >
                <el-input
                  v-model="borrowForm.studentId"
                  :placeholder="borrowForm.identity === 'teacher' ? '请输入工号' : '请输入6位学号'"
                />
              </el-form-item>
            </el-col>
          </el-row>
          
          <el-row :gutter="20">
            <el-col :span="12">
              <el-form-item label="年级" prop="grade">
                <el-input
                  v-model="borrowForm.grade"
                  placeholder="请输入年级（学生填写）"
                />
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="班级/办公室" prop="classOrOffice">
                <el-input
                  v-model="borrowForm.classOrOffice"
                  placeholder="请输入班级或办公室"
                />
              </el-form-item>
            </el-col>
          </el-row>
        </div>

        <!-- 钥匙信息部分 -->
        <div class="form-section">
          <h3>钥匙信息</h3>
          <p class="bilingual-subtitle">Key Information</p>
          
          <el-row :gutter="20">
            <el-col :span="12">
              <el-form-item label="选择钥匙" prop="keyId" required>
                <el-select
                  v-model="borrowForm.keyId"
                  placeholder="请选择要借用的钥匙"
                  style="width: 100%"
                  @change="onKeySelect"
                >
                  <el-option
                    v-for="key in availableKeys"
                    :key="key.id"
                    :label="`${key.room}号房间`"
                    :value="key.id"
                  />
                </el-select>
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="房间号">
                <el-input
                  v-model="selectedRoom"
                  placeholder="选择钥匙后自动填充"
                  readonly
                />
              </el-form-item>
            </el-col>
          </el-row>
        </div>

        <!-- 提交按钮 -->
        <div class="form-actions">
          <el-button @click="resetForm">重置表单</el-button>
          <el-button type="primary" @click="submitForm" :loading="submitting">
            提交申请
          </el-button>
        </div>
      </el-form>
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