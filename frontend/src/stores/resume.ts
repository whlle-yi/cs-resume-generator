import { computed, ref, watch } from 'vue'
import { defineStore } from 'pinia'
import { ElMessage } from 'element-plus'

import { exportPdf as exportPdfApi, fetchSample, fetchTemplates, renderPreview } from '@/api/resume'
import type { Education, RenderRequest, ResumeData, TemplateInfo } from '@/types/resume'
import { emptyResume } from '@/types/resume'

const STORAGE_KEY = 'cs-resume-generator/draft-v1'
const PREVIEW_DEBOUNCE_MS = 500
const AUTOSAVE_DEBOUNCE_MS = 800

/** 列表字段 key 与对应空白条目工厂（用于「添加」操作）。 */
type ListKey = 'education' | 'skills' | 'projects' | 'internships' | 'campus' | 'awards'

const blankFactories: Record<ListKey, () => unknown> = {
  education: (): Education => ({
    school: '',
    college: null,
    major: '',
    degree: '本科',
    start_date: '2022-09',
    end_date: '2026-06',
    gpa_rank: null,
    courses: [],
  }),
  skills: () => ({ category: '', items: [{ name: '', level: null }] }),
  projects: () => ({
    name: '',
    role: null,
    start_date: '2024-01',
    end_date: '2024-06',
    tech_stack: [],
    highlights: [''],
    link: null,
  }),
  internships: () => ({
    company: '',
    position: '',
    start_date: '2024-07',
    end_date: '2024-10',
    highlights: [''],
  }),
  campus: () => ({
    organization: '',
    role: null,
    start_date: '2023-09',
    end_date: '2024-06',
    highlights: [],
  }),
  awards: () => ({ name: '', level: null, date: '2024-12' }),
}

const FALLBACK_TEMPLATES: TemplateInfo[] = [
  { id: 'classic', name: '经典单栏', description: '传统单栏版式，信息密度高' },
  { id: 'modern', name: '简约双栏', description: '左侧信息栏 + 右侧主栏' },
]

export const useResumeStore = defineStore('resume', () => {
  const data = ref<ResumeData>(emptyResume())
  const template = ref('classic')
  const templates = ref<TemplateInfo[]>(FALLBACK_TEMPLATES)

  const previewHtml = ref('')
  const previewError = ref('')
  const previewLoading = ref(false)
  const exporting = ref(false)
  const initialized = ref(false)
  const loadedFromDraft = ref(false)

  /** 基本信息（渲染的最小前提）是否已填写。 */
  const isRenderable = computed(
    () =>
      !!(
        data.value.basics.name &&
        data.value.basics.objective &&
        data.value.basics.phone &&
        data.value.basics.email
      ),
  )

  // ---------- 初始化 / 草稿 ----------

  let saveTimer: ReturnType<typeof setTimeout> | null = null

  function scheduleAutosave(): void {
    if (saveTimer) clearTimeout(saveTimer)
    saveTimer = setTimeout(() => {
      try {
        localStorage.setItem(STORAGE_KEY, JSON.stringify({ data: data.value, template: template.value }))
      } catch {
        // 存储不可用（隐私模式等）时静默忽略
      }
    }, AUTOSAVE_DEBOUNCE_MS)
  }

  /** 首次挂载时调用：恢复草稿或加载示例，并建立自动保存。 */
  async function init(): Promise<void> {
    if (initialized.value) return
    initialized.value = true

    fetchTemplates()
      .then((list) => (templates.value = list))
      .catch(() => undefined)

    const raw = localStorage.getItem(STORAGE_KEY)
    if (raw) {
      try {
        const draft = JSON.parse(raw) as { data: ResumeData; template: string }
        if (draft?.data?.basics) {
          data.value = draft.data
          template.value = draft.template ?? 'classic'
          loadedFromDraft.value = true
        }
      } catch {
        // 草稿损坏则退回示例数据
      }
    }
    if (!loadedFromDraft.value) {
      await loadSample()
    }

    watch([data, template], scheduleAutosave, { deep: true })
    await refreshPreview()
  }

  async function loadSample(): Promise<void> {
    try {
      data.value = await fetchSample()
      loadedFromDraft.value = false
      ElMessage.success('已载入示例简历，可直接修改')
    } catch (error) {
      ElMessage.error((error as Error).message)
    }
  }

  function resetToEmpty(): void {
    data.value = emptyResume()
    ElMessage.success('已清空，开始填写你的简历吧')
  }

  // ---------- 列表通用操作 ----------

  function listRef(key: ListKey): unknown[] {
    return data.value[key] as unknown as unknown[]
  }

  function addListItem(key: ListKey): void {
    listRef(key).push(blankFactories[key]())
  }

  function removeListItem(key: ListKey, index: number): void {
    listRef(key).splice(index, 1)
  }

  function moveListItem(key: ListKey, index: number, direction: -1 | 1): void {
    const list = listRef(key)
    const target = index + direction
    if (target < 0 || target >= list.length) return
    ;[list[index], list[target]] = [list[target], list[index]]
  }

  // ---------- 导入 / 导出 ----------

  async function importJson(file: File): Promise<void> {
    try {
      const parsed = JSON.parse(await file.text()) as ResumeData
      if (!parsed?.basics?.name) {
        throw new Error('不是本工具导出的简历 JSON（缺少 basics.name）')
      }
      data.value = parsed
      ElMessage.success('导入成功')
    } catch (error) {
      ElMessage.error(`导入失败：${(error as Error).message}`)
    }
  }

  function exportJson(): void {
    const blob = new Blob([JSON.stringify(data.value, null, 2)], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = `${data.value.basics.name || '简历'}.json`
    link.click()
    URL.revokeObjectURL(url)
  }

  // ---------- 预览 / 导出 PDF ----------

  let previewTimer: ReturnType<typeof setTimeout> | null = null

  function refreshPreview(): void {
    if (!isRenderable.value) {
      previewHtml.value = ''
      previewError.value = '请先完善「基本信息」（姓名、求职意向、手机号、邮箱）'
      previewLoading.value = false
      return
    }
    previewLoading.value = true
    if (previewTimer) clearTimeout(previewTimer)
    previewTimer = setTimeout(async () => {
      try {
        const request: RenderRequest = { data: data.value, template: template.value }
        previewHtml.value = await renderPreview(request)
        previewError.value = ''
      } catch (error) {
        previewError.value = (error as Error).message
      } finally {
        previewLoading.value = false
      }
    }, PREVIEW_DEBOUNCE_MS)
  }

  async function exportPdf(): Promise<void> {
    if (!isRenderable.value) {
      ElMessage.warning('请先完善「基本信息」再导出 PDF')
      return
    }
    exporting.value = true
    try {
      const blob = await exportPdfApi({ data: data.value, template: template.value })
      const url = URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.download = `${data.value.basics.name || '简历'}_简历.pdf`
      link.click()
      URL.revokeObjectURL(url)
      ElMessage.success('PDF 已导出')
    } catch (error) {
      ElMessage.error((error as Error).message)
    } finally {
      exporting.value = false
    }
  }

  return {
    data,
    template,
    templates,
    previewHtml,
    previewError,
    previewLoading,
    exporting,
    initialized,
    loadedFromDraft,
    isRenderable,
    init,
    loadSample,
    resetToEmpty,
    addListItem,
    removeListItem,
    moveListItem,
    importJson,
    exportJson,
    exportPdf,
    refreshPreview,
  }
})
