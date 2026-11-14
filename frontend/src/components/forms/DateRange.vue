<script setup lang="ts">
import { computed } from 'vue'

/** 起止年月选择器：结束时间支持「至今」。YYYY-MM 字符串，与后端契约一致。 */
const start = defineModel<string>('start', { required: true })
const end = defineModel<string>('end', { required: true })

const isNow = computed({
  get: () => end.value === '至今',
  set: (value: boolean) => {
    end.value = value ? '至今' : ''
  },
})
</script>

<template>
  <div class="date-range">
    <el-date-picker
      v-model="start"
      type="month"
      value-format="YYYY-MM"
      placeholder="开始年月"
      style="width: 132px"
    />
    <span class="date-range__sep">至</span>
    <el-date-picker
      v-if="!isNow"
      v-model="end"
      type="month"
      value-format="YYYY-MM"
      placeholder="结束年月"
      style="width: 132px"
    />
    <span v-else class="date-range__now">至今</span>
    <el-checkbox v-model="isNow" label="至今" />
  </div>
</template>

<style scoped>
.date-range {
  display: flex;
  align-items: center;
  gap: 6px;
}
.date-range__sep {
  color: var(--el-text-color-secondary);
}
.date-range__now {
  width: 132px;
  color: var(--el-text-color-regular);
}
</style>
