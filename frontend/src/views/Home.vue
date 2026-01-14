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
        </div>
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
          <div class="card-bg-effect"></div>
          <div class="card-content">
            <div class="card-icon">📤</div>
            <h3>借钥匙</h3>
            <p>Borrow Key</p>
          </div>
          <div class="card-glow"></div>
        </div>
        
        <div class="action-card primary" @click="$router.push('/return')">
          <div class="card-bg-effect"></div>
          <div class="card-content">
            <div class="card-icon">📥</div>
            <h3>还钥匙</h3>
            <p>Return Key</p>
          </div>
          <div class="card-glow"></div>
        </div>
        
        <div class="action-card secondary" @click="$router.push('/records')">
          <div class="card-bg-effect"></div>
          <div class="card-content">
            <div class="card-icon">📋</div>
            <h3>借用记录</h3>
            <p>Borrow Records</p>
          </div>
          <div class="card-glow"></div>
        </div>
        
        <div class="action-card secondary" @click="$router.push('/keys')">
          <div class="card-bg-effect"></div>
          <div class="card-content">
            <div class="card-icon">🗝️</div>
            <h3>钥匙管理</h3>
            <p>Key Management</p>
          </div>
          <div class="card-glow"></div>
        </div>
      </div>
    </div>

    <!-- 底部状态栏 -->
    <div class="status-bar">
      <div class="status-item">
        <div class="status-icon-wrapper">
          <span class="status-icon">🔓</span>
          <div class="icon-glow"></div>
        </div>
        <div class="status-info">
          <span class="status-label">可用钥匙</span>
          <span class="status-value">{{ availableKeys }}</span>
        </div>
      </div>
      <div class="status-item">
        <div class="status-icon-wrapper">
          <span class="status-icon">🔒</span>
          <div class="icon-glow"></div>
        </div>
        <div class="status-info">
          <span class="status-label">已借出</span>
          <span class="status-value">{{ borrowedKeys }}</span>
        </div>
      </div>
      <div class="status-item">
        <div class="status-icon-wrapper online">
          <span class="status-icon">⚡</span>
          <div class="icon-glow online"></div>
        </div>
        <div class="status-info">
          <span class="status-label">系统状态</span>
          <span class="status-value online">在线</span>
        </div>
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
  align-items: center;
  justify-content: center;
  gap: 20px;
  margin-bottom: 15px;
}

.space-station {
  position: relative;
  width: 80px;
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.station-core {
  width: 30px;
  height: 30px;
  background: linear-gradient(45deg, #00ffff, #0080ff);
  border-radius: 50%;
  position: relative;
  z-index: 3;
  animation: corePulse 2s ease-in-out infinite;
  box-shadow: 
    0 0 20px rgba(0, 255, 255, 0.8),
    inset 0 0 10px rgba(255, 255, 255, 0.5);
}

.station-ring {
  position: absolute;
  border: 2px solid;
  border-radius: 50%;
  animation: ringRotate 10s linear infinite;
}

.ring-1 {
  width: 60px;
  height: 60px;
  border-color: #00ffff;
  animation-duration: 8s;
  box-shadow: 0 0 15px rgba(0, 255, 255, 0.6);
}

.ring-2 {
  width: 80px;
  height: 80px;
  border-color: #0080ff;
  animation-duration: 12s;
  animation-direction: reverse;
  box-shadow: 0 0 15px rgba(0, 128, 255, 0.6);
}

@keyframes corePulse {
  0%, 100% { 
    transform: scale(1);
    box-shadow: 
      0 0 20px rgba(0, 255, 255, 0.8),
      inset 0 0 10px rgba(255, 255, 255, 0.5);
  }
  50% { 
    transform: scale(1.15);
    box-shadow: 
      0 0 35px rgba(0, 255, 255, 1),
      inset 0 0 15px rgba(255, 255, 255, 0.8);
  }
}

@keyframes ringRotate {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
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
  font-size: 32px;
  z-index: 2;
  position: relative;
  filter: drop-shadow(0 0 10px rgba(0, 255, 255, 0.8));
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
    transform: scale(1.4);
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
  grid-template-rows: 1fr 1fr auto;
  gap: 15px;
  max-width: 450px;
  margin: 0 auto;
}

.action-grid .action-card:nth-child(5) {
  grid-column: 1 / -1;
  max-width: 200px;
  margin: 0 auto;
}

.action-card {
  position: relative;
  border-radius: 20px;
  padding: 30px 20px;
  text-align: center;
  cursor: pointer;
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  overflow: hidden;
  aspect-ratio: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  border: 2px solid;
}

.action-card.primary {
  background: linear-gradient(135deg, rgba(0, 255, 255, 0.15), rgba(0, 128, 255, 0.15));
  border-color: rgba(0, 255, 255, 0.5);
  box-shadow: 
    0 8px 32px rgba(0, 255, 255, 0.2),
    inset 0 0 20px rgba(0, 255, 255, 0.1);
}

.action-card.secondary {
  background: linear-gradient(135deg, rgba(128, 0, 255, 0.15), rgba(0, 128, 255, 0.15));
  border-color: rgba(128, 0, 255, 0.5);
  box-shadow: 
    0 8px 32px rgba(128, 0, 255, 0.2),
    inset 0 0 20px rgba(128, 0, 255, 0.1);
}

.card-bg-effect {
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(0, 255, 255, 0.1) 0%, transparent 70%);
  animation: bgRotate 8s linear infinite;
  pointer-events: none;
}

@keyframes bgRotate {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.card-content {
  position: relative;
  z-index: 2;
}

.action-card:hover {
  transform: translateY(-8px) scale(1.02);
}

.action-card.primary:hover {
  box-shadow: 
    0 15px 45px rgba(0, 255, 255, 0.4),
    inset 0 0 30px rgba(0, 255, 255, 0.2);
  border-color: #00ffff;
}

.action-card.secondary:hover {
  box-shadow: 
    0 15px 45px rgba(128, 0, 255, 0.4),
    inset 0 0 30px rgba(128, 0, 255, 0.2);
  border-color: #8000ff;
}

.card-icon {
  font-size: 3rem;
  margin-bottom: 12px;
  display: block;
  filter: drop-shadow(0 0 10px rgba(0, 255, 255, 0.6));
  animation: iconFloat 3s ease-in-out infinite;
}

@keyframes iconFloat {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-5px); }
}

.action-card h3 {
  font-size: 1.3rem;
  margin-bottom: 5px;
  color: #ffffff;
  font-weight: 600;
  text-shadow: 0 0 10px rgba(0, 255, 255, 0.5);
}

.action-card p {
  color: #aaa;
  font-size: 0.85rem;
  margin: 0;
  font-style: italic;
}

.card-glow {
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
  transition: left 0.6s ease;
  pointer-events: none;
}

.action-card:hover .card-glow {
  left: 100%;
}

.status-bar {
  flex-shrink: 0;
  display: flex;
  justify-content: space-around;
  padding: 20px;
  background: linear-gradient(180deg, transparent, rgba(0, 0, 0, 0.5));
  border-top: 1px solid rgba(0, 255, 255, 0.3);
  backdrop-filter: blur(10px);
}

.status-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.status-icon-wrapper {
  position: relative;
  width: 45px;
  height: 45px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0, 255, 255, 0.1);
  border-radius: 50%;
  border: 2px solid rgba(0, 255, 255, 0.3);
}

.status-icon-wrapper.online {
  background: rgba(0, 255, 0, 0.1);
  border-color: rgba(0, 255, 0, 0.5);
}

.status-icon {
  font-size: 1.5rem;
  z-index: 2;
}

.icon-glow {
  position: absolute;
  width: 100%;
  height: 100%;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(0, 255, 255, 0.4) 0%, transparent 70%);
  animation: glowPulse 2s ease-in-out infinite;
}

.icon-glow.online {
  background: radial-gradient(circle, rgba(0, 255, 0, 0.4) 0%, transparent 70%);
}

@keyframes glowPulse {
  0%, 100% { transform: scale(1); opacity: 0.5; }
  50% { transform: scale(1.2); opacity: 0.8; }
}

.status-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2px;
}

.status-label {
  color: #888;
  font-size: 0.75rem;
  text-align: center;
}

.status-value {
  color: #00ffff;
  font-size: 1.1rem;
  font-weight: 700;
  text-shadow: 0 0 10px rgba(0, 255, 255, 0.8);
}

.status-value.online {
  color: #00ff00;
  text-shadow: 0 0 10px rgba(0, 255, 0, 0.8);
}

@media (max-width: 480px) {
  .action-grid {
    max-width: 350px;
    gap: 12px;
  }
  
  .action-card {
    padding: 25px 15px;
  }
  
  .card-icon {
    font-size: 2.5rem;
  }
  
  .action-card h3 {
    font-size: 1.1rem;
  }
  
  .action-card p {
    font-size: 0.75rem;
  }
  
  .logo-container {
    gap: 15px;
  }
  
  .space-station {
    width: 60px;
    height: 60px;
  }
  
  .station-core {
    width: 24px;
    height: 24px;
  }
  
  .ring-1 {
    width: 45px;
    height: 45px;
  }
  
  .ring-2 {
    width: 60px;
    height: 60px;
  }
}
</style>
