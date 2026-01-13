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
      <div class="logo-container">
        <div class="space-station">
          <div class="station-core"></div>
          <div class="station-ring ring-1"></div>
          <div class="station-ring ring-2"></div>
          <div class="station-ring ring-3"></div>
        </div>
        <div class="logo-icon">
          <div class="key-icon">🔑</div>
          <div class="pulse-ring"></div>
        </div>
      </div>
      <h1 class="page-title">济外国际智能钥匙柜管理系统</h1>
      <p class="page-subtitle">Jiwai International Smart Key Cabinet System</p>
    </div>

    <!-- 主要内容区域 -->
    <div class="glass-card main-content">
      <div class="welcome-section">
        <h2>欢迎使用智能钥匙柜系统</h2>
        <p class="bilingual-subtitle">Welcome to Smart Key Cabinet System</p>
        <p>请选择您需要的操作</p>
        <p class="bilingual-subtitle">Please select your operation</p>
      </div>

      <!-- 操作按钮区域 -->
      <div class="action-buttons">
        <el-row :gutter="30" justify="center">
          <el-col :xs="24" :sm="12" :md="8" :lg="6">
            <div class="action-card" @click="$router.push('/borrow')">
              <div class="card-icon">📤</div>
              <h3>借钥匙</h3>
              <p class="bilingual-subtitle">Borrow Key</p>
              <div class="card-glow"></div>
            </div>
          </el-col>
          
          <el-col :xs="24" :sm="12" :md="8" :lg="6">
            <div class="action-card" @click="$router.push('/return')">
              <div class="card-icon">📥</div>
              <h3>还钥匙</h3>
              <p class="bilingual-subtitle">Return Key</p>
              <div class="card-glow"></div>
            </div>
          </el-col>
          
          <el-col :xs="24" :sm="12" :md="8" :lg="6">
            <div class="action-card" @click="$router.push('/users')">
              <div class="card-icon">👥</div>
              <h3>用户管理</h3>
              <p class="bilingual-subtitle">User Management</p>
              <div class="card-glow"></div>
            </div>
          </el-col>
          
          <el-col :xs="24" :sm="12" :md="8" :lg="6">
            <div class="action-card" @click="$router.push('/keys')">
              <div class="card-icon">🗝️</div>
              <h3>钥匙管理</h3>
              <p class="bilingual-subtitle">Key Management</p>
              <div class="card-glow"></div>
            </div>
          </el-col>
        </el-row>
      </div>

      <!-- 系统状态显示 -->
      <div class="status-panel">
        <h3>系统状态</h3>
        <p class="bilingual-subtitle">System Status</p>
        <el-row :gutter="20">
          <el-col :xs="24" :sm="8">
            <div class="status-item">
              <div class="status-icon">🔓</div>
              <div class="status-info">
                <span class="status-label">可用钥匙</span>
                <span class="bilingual-subtitle">Available Keys</span>
                <span class="status-value">{{ availableKeys }}</span>
              </div>
            </div>
          </el-col>
          
          <el-col :xs="24" :sm="8">
            <div class="status-item">
              <div class="status-icon">🔒</div>
              <div class="status-info">
                <span class="status-label">已借出</span>
                <span class="bilingual-subtitle">Borrowed</span>
                <span class="status-value">{{ borrowedKeys }}</span>
              </div>
            </div>
          </el-col>
          
          <el-col :xs="24" :sm="8">
            <div class="status-item">
              <div class="status-icon">⚡</div>
              <div class="status-info">
                <span class="status-label">系统状态</span>
                <span class="bilingual-subtitle">System Status</span>
                <span class="status-value online">在线</span>
                <span class="bilingual-subtitle">Online</span>
              </div>
            </div>
          </el-col>
        </el-row>
      </div>
    </div>

    <!-- 底部信息 -->
    <div class="footer">
      <p>&copy; 2025 智能钥匙柜管理系统 | 计算机原理课程作业</p>
      <div class="tech-info">
        <span>Powered by Vue 3 & Element Plus</span>
        <span class="separator">|</span>
        <span>Version 1.0.0</span>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { keyAPI, userAPI } from '../api'

export default {
  name: 'Home',
  setup() {
    const availableKeys = ref(0)
    const borrowedKeys = ref(0)

    const loadSystemStatus = async () => {
      try {
        const [keys, users] = await Promise.all([
          keyAPI.getKeys(),
          userAPI.getUsers()
        ])
        
        availableKeys.value = keys.length
        
        // 计算已借出的钥匙数量
        let borrowed = 0
        users.forEach(user => {
          if (user.keys && user.keys.length > 0) {
            borrowed += user.keys.length
          }
        })
        borrowedKeys.value = borrowed
        
      } catch (error) {
        console.error('加载系统状态失败:', error)
      }
    }

    onMounted(() => {
      loadSystemStatus()
      
      // 每5秒更新一次状态
      setInterval(loadSystemStatus, 5000)
    })

    return {
      availableKeys,
      borrowedKeys
    }
  }
}
</script>

<style scoped>
.main-content {
  padding: 40px;
  margin-bottom: 40px;
}

.logo-container {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 30px;
  margin-bottom: 20px;
}

.space-station {
  position: relative;
  width: 120px;
  height: 120px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.station-core {
  width: 40px;
  height: 40px;
  background: linear-gradient(45deg, #00ffff, #0080ff);
  border-radius: 50%;
  position: relative;
  z-index: 3;
  animation: corePulse 2s ease-in-out infinite;
  box-shadow: 
    0 0 20px rgba(0, 255, 255, 0.6),
    inset 0 0 10px rgba(255, 255, 255, 0.3);
}

.station-ring {
  position: absolute;
  border: 2px solid;
  border-radius: 50%;
  animation: ringRotate 10s linear infinite;
}

.ring-1 {
  width: 80px;
  height: 80px;
  border-color: #00ffff;
  animation-duration: 8s;
  box-shadow: 0 0 15px rgba(0, 255, 255, 0.4);
}

.ring-2 {
  width: 100px;
  height: 100px;
  border-color: #0080ff;
  animation-duration: 12s;
  animation-direction: reverse;
  box-shadow: 0 0 15px rgba(0, 128, 255, 0.4);
}

.ring-3 {
  width: 120px;
  height: 120px;
  border-color: #8000ff;
  animation-duration: 15s;
  box-shadow: 0 0 15px rgba(128, 0, 255, 0.4);
}

@keyframes corePulse {
  0%, 100% { 
    transform: scale(1);
    box-shadow: 
      0 0 20px rgba(0, 255, 255, 0.6),
      inset 0 0 10px rgba(255, 255, 255, 0.3);
  }
  50% { 
    transform: scale(1.1);
    box-shadow: 
      0 0 30px rgba(0, 255, 255, 0.8),
      inset 0 0 15px rgba(255, 255, 255, 0.5);
  }
}

@keyframes ringRotate {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.logo-icon {
  position: relative;
  width: 80px;
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
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

.welcome-section {
  text-align: center;
  margin-bottom: 40px;
}

.welcome-section h2 {
  font-size: 2rem;
  margin-bottom: 10px;
  color: #ffffff;
}

.welcome-section p {
  color: #aaa;
  font-size: 1.1rem;
}

.bilingual-subtitle {
  color: #aaa;
  font-size: 0.9rem;
  margin: 5px 0;
  font-style: italic;
}

.action-buttons {
  margin-bottom: 40px;
}

.action-card {
  background: linear-gradient(135deg, rgba(0, 255, 255, 0.1), rgba(0, 128, 255, 0.1));
  border: 1px solid rgba(0, 255, 255, 0.3);
  border-radius: 15px;
  padding: 30px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
  margin-bottom: 20px;
}

.action-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 35px rgba(0, 255, 255, 0.4);
  border-color: #00ffff;
}

.card-icon {
  font-size: 3rem;
  margin-bottom: 15px;
  display: block;
}

.action-card h3 {
  font-size: 1.5rem;
  margin-bottom: 5px;
  color: #ffffff;
}

.card-glow {
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: left 0.5s ease;
}

.action-card:hover .card-glow {
  left: 100%;
}

.status-panel {
  background: rgba(0, 0, 0, 0.3);
  border-radius: 15px;
  padding: 25px;
  border: 1px solid rgba(0, 255, 255, 0.2);
}

.status-panel h3 {
  margin-bottom: 20px;
  color: #00ffff;
  font-size: 1.3rem;
  text-align: center;
}

.status-item {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 15px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 10px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  margin-bottom: 15px;
}

.status-icon {
  font-size: 2rem;
}

.status-info {
  display: flex;
  flex-direction: column;
}

.status-label {
  color: #aaa;
  font-size: 0.9rem;
}

.status-value {
  color: #00ffff;
  font-size: 1.5rem;
  font-weight: bold;
}

.status-value.online {
  color: #00ff00;
}

.footer {
  text-align: center;
  padding: 30px 0;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  color: #666;
}

.tech-info {
  margin-top: 10px;
  font-size: 0.9rem;
}

.separator {
  margin: 0 10px;
}

@media (max-width: 768px) {
  .logo-container {
    flex-direction: column;
    gap: 20px;
  }
  
  .main-content {
    padding: 20px;
  }
}
</style>