import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 10000
})

// 请求拦截器
api.interceptors.request.use(
  config => {
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  response => {
    return response.data
  },
  error => {
    console.error('API Error:', error)
    return Promise.reject(error)
  }
)

// 用户相关API
export const userAPI = {
  // 获取所有用户
  getUsers: () => api.get('/user/'),
  
  // 获取单个用户
  getUser: (id) => api.get(`/user/${id}`),
  
  // 创建用户
  createUser: (userData) => api.post('/user/', userData),
  
  // 更新用户
  updateUser: (id, userData) => api.put(`/user/${id}`, userData),
  
  // 删除用户
  deleteUser: (id) => api.delete(`/user/${id}`),
  
  // 借钥匙
  borrowKey: (userId, keyId) => api.post(`/user/${userId}/borrow`, { key_id: keyId }),
  
  // 还钥匙
  returnKey: (userId, keyId) => api.post(`/user/${userId}/return`, { key_id: keyId })
}

// 钥匙相关API
export const keyAPI = {
  // 获取所有钥匙
  getKeys: () => api.get('/key/'),
  
  // 获取单个钥匙
  getKey: (id) => api.get(`/key/${id}`),
  
  // 创建钥匙
  createKey: (keyData) => api.post('/key/', keyData),
  
  // 更新钥匙
  updateKey: (id, keyData) => api.put(`/key/${id}`, keyData),
  
  // 删除钥匙
  deleteKey: (id) => api.delete(`/key/${id}`)
}

export default api