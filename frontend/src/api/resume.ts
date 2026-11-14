import { api } from './client'
import type { RenderRequest, ResumeData, TemplateInfo } from '@/types/resume'

/** 可用模板列表。 */
export async function fetchTemplates(): Promise<TemplateInfo[]> {
  const data = await api.get<unknown, { templates: TemplateInfo[] }>('/meta/templates')
  return data.templates
}

/** 后端内置示例简历。 */
export async function fetchSample(): Promise<ResumeData> {
  return api.get<unknown, ResumeData>('/resume/sample')
}

/** 渲染 HTML 预览。 */
export async function renderPreview(req: RenderRequest): Promise<string> {
  const data = await api.post<unknown, { html: string }>('/resume/preview', req)
  return data.html
}

/** 导出 PDF（Blob）。 */
export async function exportPdf(req: RenderRequest): Promise<Blob> {
  return api.post('/resume/export/pdf', req, { responseType: 'blob' })
}
