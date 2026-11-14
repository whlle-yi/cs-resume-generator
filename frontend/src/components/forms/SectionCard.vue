<script setup lang="ts">
import { ref } from 'vue'

/** 表单分区卡片：可折叠，标题右侧显示条目数。 */
const props = defineProps<{
  title: string
  count?: number
}>()

const expanded = ref(true)
</script>

<template>
  <el-collapse v-model="expanded" class="section-card">
    <el-collapse-item :name="props.title">
      <template #title>
        <span class="section-card__title">{{ props.title }}</span>
        <el-tag v-if="props.count" size="small" type="info" effect="plain" round>
          {{ props.count }}
        </el-tag>
      </template>
      <slot />
    </el-collapse-item>
  </el-collapse>
</template>

<style scoped>
.section-card {
  --el-collapse-header-height: 44px;
  border: none;
}
.section-card :deep(.el-collapse-item__header) {
  font-size: 15px;
  font-weight: 600;
  color: var(--el-text-color-primary);
}
.section-card__title {
  margin-right: 8px;
}
.section-card :deep(.el-collapse-item__content) {
  padding-bottom: 16px;
}
</style>
