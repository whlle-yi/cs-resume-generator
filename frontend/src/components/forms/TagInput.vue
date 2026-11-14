<script setup lang="ts">
/** 标签输入：回车或失焦创建，用于课程、技术栈等多值字段。 */
const model = defineModel<string[]>({ required: true })

withDefaults(defineProps<{ placeholder?: string }>(), {
  placeholder: '输入后回车添加',
})
</script>

<template>
  <el-select
    v-model="model"
    multiple
    filterable
    allow-create
    default-first-option
    :reserve-keyword="false"
    :placeholder="placeholder"
    style="width: 100%"
  >
    <el-option v-for="tag in model" :key="tag" :label="tag" :value="tag" />
  </el-select>
</template>
