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
        <div class="logo-icon">
          <div class="key-icon">🔑</div>
          <div class="pulse-ring"></div>
        </div>
      </div>
      <h1 class="page-title">济外国际智能钥匙柜</h1>
      <p class="page-subtitle">Smart Key Cabinet System</p>
    </div>

    <!-- 主要内容区域 -->
    <div class="main-content">
      <!-- 操作按钮区域 -->
      <div class="action-grid">
        <div class="action-card primary" @click="$router.push('/borrow')">
          <div class="card-icon">📤</div>
          <h3>借钥匙</h3>
          <p>Borrow Key</p>
        </div>
        
        <div class="action-card primary" @click="$router.push('/return')">
          <div class="card-icon">📥</div>
          <h3>还钥匙</h3>
          <p>Return Key</p>
        </div>
        
        <div class="action-card secondary" @click="$router.push('/users')">
          <div class="card-icon">👥</div>
          <h3>用户管理</h3>
          <p>User Management</p>
        </div>
        
        <div class="action-card secondary" @click="$router.push('/keys')">
          <div class="card-icon">🗝️</div>
          <h3>钥匙管理</h3>
          <p>Key Management</p>
        </div>
      </div>
    </div>

    <!-- 底部状态栏 -->
    <div class="status-bar">
      <div class="status-item">
        <span class="status-icon">🔓</span>
        <span class="status-text">可用: {{ availableKeys }}</span>
      </div>
      <div class="status-item">
        <span class="status-icon">🔒</span>
        <span class="status-text">已借: {{ borrowedKeys }}</span>
      </div>
      <div class="status-item">
        <span class="status-icon online">⚡</span>
        <span class="status-text">在线</span>
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
.page-container {
  height: 100vh;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.page-header {
  flex-shrink: 0;
  padding: 20px;
  text-align: center;
}

.logo-container {
  display: flex;
  justify-content: center;
  margin-bottom: 15px;
}

.logo-icon {
  position: relative;
  width: 60px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.key-icon {
  font-size: 30px;
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

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 0 20px;
  overflow: hidden;
}

.action-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
  max-width: 400px;
  margin: 0 auto;
}

.action-card {
  background: linear-gradient(135deg, rgba(0, 255, 255, 0.1), rgba(0, 128, 255, 0.1));
  border: 1px solid rgba(0, 255, 255, 0.3);
  border-radius: 15px;
  padding: 25px 15px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
  aspect-ratio: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.action-card.primary {
  background: linear-gradient(135deg, rgba(0, 255, 255, 0.15), rgba(0, 128, 255, 0.15));
  border-color: #00ffff;
}

.action-card.secondary {
  background: linear-gradient(135deg, rgba(128, 0, 255, 0.1), rgba(0, 128, 255, 0.1));
  border-color: rgba(128, 0, 255, 0.5);
}

.action-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 25px rgba(0, 255, 255, 0.4);
}

.action-card.primary:hover {
  box-shadow: 0 10px 25px rgba(0, 255, 255, 0.6);
}

.action-card.secondary:hover {
  box-shadow: 0 10px 25px rgba(128, 0, 255, 0.4);
}

.card-icon {
  font-size: 2.5rem;
  margin-bottom: 10px;
  display: block;
}

.action-card h3 {
  font-size: 1.2rem;
  margin-bottom: 5px;
  color: #ffffff;
}

.action-card p {
  color: #aaa;
  font-size: 0.8rem;
  margin: 0;
}

.status-bar {
  flex-shrink: 0;
  display: flex;
  justify-content: space-around;
  padding: 15px 20px;
  background: rgba(0, 0, 0, 0.3);
  border-top: 1px solid rgba(0, 255, 255, 0.2);
}

.status-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 5px;
}

.status-icon {
  font-size: 1.5rem;
}

.status-icon.online {
  color: #00ff00;
}

.status-text {
  color: #aaa;
  font-size: 0.8rem;
  text-align: center;
}

@media (max-width: 480px) {
  .action-grid {
    max-width: 300px;
    gap: 12px;
  }
  
  .action-card {
    padding: 20px 10px;
  }
  
  .card-icon {
    font-size: 2rem;
  }
  
  .action-card h3 {
    font-size: 1rem;
  }
  
  .action-card p {
    font-size: 0.7rem;
  }
}
</style>