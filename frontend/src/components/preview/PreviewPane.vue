<script setup lang="ts">
import { Loading } from '@element-plus/icons-vue'

import { useResumeStore } from '@/stores/resume'

/** 预览面板：iframe 沙箱渲染后端返回的自包含 HTML。 */
const store = useResumeStore()
</script>

<template>
  <div class="preview-pane">
    <iframe
      v-if="store.previewHtml"
      class="preview-pane__frame"
      title="简历预览"
      sandbox=""
      :srcdoc="store.previewHtml"
    />
    <div v-else class="preview-pane__state">
      <el-empty :description="store.previewError || '完善基本信息后即可实时预览'" />
    </div>
    <transition name="fade">
      <div v-if="store.previewLoading && store.previewHtml" class="preview-pane__loading">
        <el-icon class="is-loading" :size="22"><Loading /></el-icon>
      </div>
    </transition>
  </div>
</template>

<style scoped>
.preview-pane {
  position: relative;
  flex: 1;
  overflow: auto;
  padding: 16px;
}
.preview-pane__frame {
  width: 100%;
  height: 100%;
  border: none;
}
.preview-pane__state {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
}
.preview-pane__loading {
  position: absolute;
  top: 24px;
  right: 24px;
  color: var(--el-color-primary);
  background: rgba(255, 255, 255, 0.85);
  border-radius: 50%;
  padding: 6px;
  box-shadow: 0 1px 6px rgba(0, 0, 0, 0.15);
}
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
