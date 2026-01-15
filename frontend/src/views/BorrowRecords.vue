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
        <div class="key-icon">📋</div>
        <div class="pulse-ring"></div>
        <div class="glow-effect"></div>
      </div>
      <h1 class="page-title">借用记录</h1>
      <p class="page-subtitle">Borrow Records</p>
    </div>

    <!-- 筛选器 -->
    <div class="filter-section">
      <el-radio-group v-model="filterType" @change="loadRecords" class="filter-tabs">
        <el-radio-button label="all">全部记录</el-radio-button>
        <el-radio-button label="active">未归还</el-radio-button>
        <el-radio-button label="returned">已归还</el-radio-button>
      </el-radio-group>
    </div>

    <!-- 主要内容区域 -->
    <div class="main-content">
      <div class="records-container" v-loading="loading">
        <div v-if="records.length === 0" class="empty-state">
          <div class="empty-icon">📝</div>
          <p>暂无借用记录</p>
        </div>
        
        <div v-else class="records-list">
          <div 
            v-for="record in paginatedRecords" 
            :key="record.id" 
            class="record-card"
            :class="{ 'active': record.status === 'borrowed' }"
          >
            <div class="record-header">
              <div class="user-info">
                <span class="user-name">{{ record.user.name }}</span>
                <span class="user-id">{{ record.user.identity === 'student' ? '学号' : '工号' }}: {{ getStudentId(record.user) }}</span>
              </div>
              <div class="status-badge" :class="record.status">
                {{ record.status === 'borrowed' ? '未归还' : '已归还' }}
              </div>
            </div>
            
            <div class="record-body">
              <div class="key-info">
                <span class="key-room">🔑 {{ record.key.room }}号房间</span>
              </div>
              
              <div class="reason-section">
                <span class="reason-label">借用理由：</span>
                <p class="reason-text">{{ record.reason }}</p>
              </div>
              
              <div class="time-info">
                <div class="time-item">
                  <span class="time-label">借用时间：</span>
                  <span class="time-value">{{ formatDateTime(record.borrow_time) }}</span>
                </div>
                <div v-if="record.return_time" class="time-item">
                  <span class="time-label">归还时间：</span>
                  <span class="time-value">{{ formatDateTime(record.return_time) }}</span>
                </div>
                <div v-if="record.status === 'borrowed'" class="time-item">
                  <span class="time-label">借用时长：</span>
                  <span class="time-value duration">{{ getBorrowDuration(record.borrow_time) }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="pagination-container" v-if="records.length > 0">
        <el-pagination
          layout="prev, pager, next"
          background
          :current-page="currentPage"
          :page-size="pageSize"
          :total="records.length"
          @current-change="handlePageChange"
        />
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { ArrowLeft } from '@element-plus/icons-vue'
import { userAPI } from '../api'

export default {
  name: 'BorrowRecords',
  components: {
    ArrowLeft
  },
  setup() {
    const loading = ref(false)
    const records = ref([])
    const filterType = ref('all')
    const currentPage = ref(1)
    const pageSize = ref(8)

    const loadRecords = async () => {
      loading.value = true
      try {
        let data
        switch (filterType.value) {
          case 'active':
            data = await userAPI.getActiveBorrowRecords()
            break
          case 'returned':
            data = await userAPI.getAllBorrowRecords()
            data = data.filter(record => record.status === 'returned')
            break
          default:
            data = await userAPI.getAllBorrowRecords()
        }
        records.value = data
        currentPage.value = 1
      } catch (error) {
        console.error('加载借用记录失败:', error)
        ElMessage.error('加载借用记录失败')
      } finally {
        loading.value = false
      }
    }

    const formatDateTime = (dateTimeStr) => {
      if (!dateTimeStr) return ''
      const date = new Date(dateTimeStr)
      return date.toLocaleString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
      })
    }

    const getBorrowDuration = (borrowTimeStr) => {
      const borrowTime = new Date(borrowTimeStr)
      const now = new Date()
      const diffMs = now - borrowTime
      const diffHours = Math.floor(diffMs / (1000 * 60 * 60))
      const diffDays = Math.floor(diffHours / 24)
      
      if (diffDays > 0) {
        return `${diffDays}天${diffHours % 24}小时`
      } else {
        return `${diffHours}小时`
      }
    }

    const getStudentId = (user) => {
      // 根据用户数据结构返回正确的ID字段
      return user.student_id || `ID-${user.id}`
    }

    const paginatedRecords = computed(() => {
      const start = (currentPage.value - 1) * pageSize.value
      return records.value.slice(start, start + pageSize.value)
    })

    const handlePageChange = (page) => {
      currentPage.value = page
    }

    onMounted(() => {
      loadRecords()
    })

    return {
      loading,
      records,
      filterType,
      currentPage,
      pageSize,
      paginatedRecords,
      loadRecords,
      formatDateTime,
      getBorrowDuration,
      getStudentId,
      handlePageChange
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

.page-title {
  color: #ffffff;
  font-size: 28px;
  font-weight: 700;
  margin: 0;
  text-shadow: 0 0 20px rgba(0, 255, 255, 0.5);
}

.page-subtitle {
  color: #00ffff;
  font-size: 14px;
  margin: 5px 0 0 0;
  opacity: 0.8;
}

.filter-section {
  flex-shrink: 0;
  padding: 0 20px 20px;
  display: flex;
  justify-content: center;
}

.filter-tabs {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  padding: 4px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(0, 255, 255, 0.2);
}

.main-content {
  flex: 1;
  padding: 0 20px 20px;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.records-container {
  flex: 1;
  overflow-y: auto;
  min-height: 0; /* 关键：防止 flex 子项溢出 */
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #666;
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 20px;
  opacity: 0.5;
}

.records-list {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
  padding-bottom: 10px;
}

.pagination-container {
  flex-shrink: 0;
  padding: 10px 20px 20px;
  display: flex;
  justify-content: center;
}

/* 增强分页按钮样式 */
:deep(.el-pagination.is-background .el-pager li:not(.is-disabled)) {
  background-color: rgba(255, 255, 255, 0.1);
  color: #fff;
  border: 1px solid rgba(0, 255, 255, 0.3);
  font-size: 16px;
  min-width: 40px;
  height: 40px;
  line-height: 40px;
  border-radius: 8px;
  margin: 0 5px;
}

:deep(.el-pagination.is-background .el-pager li:not(.is-disabled).is-active) {
  background-color: #00ffff;
  color: #000;
  font-weight: bold;
  border-color: #00ffff;
  box-shadow: 0 0 10px rgba(0, 255, 255, 0.5);
}

:deep(.el-pagination.is-background .btn-prev),
:deep(.el-pagination.is-background .btn-next) {
  background-color: rgba(255, 255, 255, 0.1);
  color: #fff;
  border: 1px solid rgba(0, 255, 255, 0.3);
  min-width: 40px;
  height: 40px;
  border-radius: 8px;
}

:deep(.el-pagination.is-background .btn-prev:disabled),
:deep(.el-pagination.is-background .btn-next:disabled) {
  background-color: rgba(255, 255, 255, 0.05);
  color: #666;
  border-color: rgba(255, 255, 255, 0.1);
}

.record-card {
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(10px);
  border-radius: 12px;
  padding: 15px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: all 0.3s ease;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.record-body {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.record-card.active {
  border-color: rgba(255, 165, 0, 0.5);
  box-shadow: 0 0 20px rgba(255, 165, 0, 0.2);
}

.record-card:hover {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(0, 255, 255, 0.3);
  transform: translateY(-2px);
}

.record-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.user-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.user-name {
  color: #ffffff;
  font-size: 18px;
  font-weight: 600;
}

.user-id {
  color: #999;
  font-size: 14px;
}

.status-badge {
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
}

.status-badge.borrowed {
  background: linear-gradient(135deg, rgba(255, 165, 0, 0.2), rgba(255, 140, 0, 0.2));
  color: #ffa500;
  border: 1px solid rgba(255, 165, 0, 0.5);
}

.status-badge.returned {
  background: linear-gradient(135deg, rgba(0, 255, 0, 0.2), rgba(0, 200, 0, 0.2));
  color: #00ff00;
  border: 1px solid rgba(0, 255, 0, 0.5);
}



.key-info {
  color: #00ffff;
  font-weight: 500;
}

.reason-section {
  background: rgba(0, 0, 0, 0.2);
  padding: 8px 12px;
  border-radius: 6px;
  border-left: 3px solid #00ffff;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.reason-label {
  color: #00ffff;
  font-size: 14px;
  font-weight: 500;
}

.reason-text {
  color: #ffffff;
  margin: 5px 0 0 0;
  line-height: 1.3;
  font-size: 13px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.time-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
  margin-top: auto;
}

.time-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 12px;
}

.time-label {
  color: #999;
  font-size: 14px;
}

.time-value {
  color: #ffffff;
  font-size: 14px;
}

.time-value.duration {
  color: #ffa500;
  font-weight: 600;
}

/* Element Plus 样式覆盖 */
:deep(.el-radio-button__inner) {
  background: transparent;
  border: none;
  color: #999;
  padding: 8px 16px;
  border-radius: 8px;
  transition: all 0.3s ease;
}

:deep(.el-radio-button__original-radio:checked + .el-radio-button__inner) {
  background: linear-gradient(135deg, #00ffff, #0080ff);
  color: #000;
  font-weight: 600;
  box-shadow: 0 0 15px rgba(0, 255, 255, 0.3);
}

:deep(.el-radio-button:first-child .el-radio-button__inner) {
  border-radius: 8px;
}

:deep(.el-radio-button:last-child .el-radio-button__inner) {
  border-radius: 8px;
}

@media (max-width: 480px) {
  .record-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }
  
  .time-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 2px;
  }
  
  .filter-tabs {
    width: 100%;
  }
  
  :deep(.el-radio-button__inner) {
    padding: 6px 12px;
    font-size: 14px;
  }
}
</style>
