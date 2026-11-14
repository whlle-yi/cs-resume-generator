<script setup lang="ts">
import { Document, Download, RefreshLeft, Upload } from '@element-plus/icons-vue'
import { ElMessageBox } from 'element-plus'
import type { UploadFile } from 'element-plus'

import { useResumeStore } from '@/stores/resume'

/** 预览工具栏：模板切换、示例/清空、JSON 导入导出、PDF 导出。 */
const store = useResumeStore()

function onFileChange(file: UploadFile): void {
  if (file.raw) void store.importJson(file.raw)
}

function confirmReset(): void {
  ElMessageBox.confirm('清空后草稿会被覆盖，不可恢复，确定继续？', '清空简历', {
    type: 'warning',
    confirmButtonText: '清空',
    cancelButtonText: '取消',
  })
    .then(() => store.resetToEmpty())
    .catch(() => undefined)
}
</script>

<template>
  <div class="toolbar">
    <div class="toolbar__left">
      <span class="toolbar__label">模板</span>
      <el-radio-group v-model="store.template">
        <el-radio-button v-for="t in store.templates" :key="t.id" :value="t.id">
          {{ t.name }}
        </el-radio-button>
      </el-radio-group>
    </div>
    <div class="toolbar__right">
      <el-button :icon="RefreshLeft" @click="confirmReset">清空</el-button>
      <el-button :icon="Document" @click="store.loadSample()">填充示例</el-button>
      <el-upload
        :auto-upload="false"
        :show-file-list="false"
        :on-change="onFileChange"
        accept=".json,application/json"
      >
        <el-button :icon="Upload">导入 JSON</el-button>
      </el-upload>
      <el-button :icon="Download" @click="store.exportJson()">导出 JSON</el-button>
      <el-button
        type="primary"
        :icon="Download"
        :loading="store.exporting"
        @click="store.exportPdf()"
      >
        导出 PDF
      </el-button>
    </div>
  </div>
</template>

<style scoped>
.toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
  padding: 10px 16px;
  background: #fff;
  border-bottom: 1px solid var(--el-border-color-light);
  flex-wrap: wrap;
}
.toolbar__left {
  display: flex;
  align-items: center;
  gap: 8px;
}
.toolbar__label {
  font-size: 13px;
  color: var(--el-text-color-secondary);
}
.toolbar__right {
  display: flex;
  align-items: center;
  gap: 0;
}
.toolbar__right :deep(.el-upload) {
  margin: 0 12px 0 12px;
}
</style>
