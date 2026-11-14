<script setup lang="ts">
import { useResumeStore } from '@/stores/resume'
import BulletEditor from './BulletEditor.vue'

/** 自我评价（可选）。 */
const store = useResumeStore()
</script>

<template>
  <el-form label-position="top">
    <el-form-item>
      <BulletEditor
        v-model="store.data.self_evaluation"
        add-label="添加评价"
        placeholder="一句话一个优点，结合事实，如：具备完整项目经验，重视代码质量"
      />
    </el-form-item>
  </el-form>
</template>
