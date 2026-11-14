<script setup lang="ts">
import { Delete, Plus } from '@element-plus/icons-vue'

/** 要点编辑器：多条目文本，用于项目/实习/自我评价的 bullet 描述。 */
const model = defineModel<string[]>({ required: true })

withDefaults(
  defineProps<{
    placeholder?: string
    rows?: number
    addLabel?: string
  }>(),
  {
    placeholder: '一句话一个要点，建议按「背景-行动-结果」撰写，尽量带数据',
    rows: 2,
    addLabel: '添加要点',
  },
)

function add(): void {
  model.value.push('')
}

function remove(index: number): void {
  model.value.splice(index, 1)
}
</script>

<template>
  <div class="bullet-editor">
    <div v-for="(_, index) in model" :key="index" class="bullet-editor__row">
      <span class="bullet-editor__dot">{{ index + 1 }}.</span>
      <el-input
        v-model="model[index]"
        type="textarea"
        :rows="rows"
        :placeholder="placeholder"
        :autosize="{ minRows: rows, maxRows: 6 }"
      />
      <el-button
        link
        type="danger"
        :icon="Delete"
        :disabled="model.length <= 1"
        @click="remove(index)"
      />
    </div>
    <el-button link type="primary" :icon="Plus" @click="add">{{ addLabel }}</el-button>
  </div>
</template>

<style scoped>
.bullet-editor__row {
  display: flex;
  align-items: flex-start;
  gap: 6px;
  margin-bottom: 8px;
}
.bullet-editor__dot {
  line-height: 28px;
  color: var(--el-text-color-secondary);
  font-size: 12px;
  min-width: 18px;
}
</style>
