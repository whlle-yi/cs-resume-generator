import axios from 'axios'

/** axios 实例：开发模式经 Vite 代理转发到 FastAPI，生产模式同源部署。 */
export const api = axios.create({
  baseURL: '/api/v1',
  timeout: 60_000,
})

api.interceptors.response.use(
  (resp) => resp.data,
  (error) => {
    const body = error.response?.data
    let message = body?.message ?? error.message ?? '请求失败'
    // 把后端校验错误的首条字段信息透出，方便定位是哪一项没填对
    const detail = body?.details?.[0]
    if (body?.code === 'VALIDATION_ERROR' && detail) {
      const field = (detail.loc ?? []).slice(1).join('.')
      message = `${message}${field ? `（字段：${field}）` : ''}：${detail.msg}`
    }
    return Promise.reject(new Error(message))
  },
)
