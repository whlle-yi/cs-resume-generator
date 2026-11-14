<script setup lang="ts">
/** 列表条目卡片：标题 + 上移/下移/删除操作。 */
defineProps<{ title: string }>()

defineEmits<{
  'move-up': []
  'move-down': []
  remove: []
}>()
</script>

<template>
  <el-card shadow="never" class="item-card">
    <template #header>
      <div class="item-card__head">
        <span class="item-card__title">{{ title }}</span>
        <span class="item-card__ops">
          <slot name="ops" />
          <el-button link size="small" @click="$emit('move-up')">上移</el-button>
          <el-button link size="small" @click="$emit('move-down')">下移</el-button>
          <el-button link size="small" type="danger" @click="$emit('remove')">删除</el-button>
        </span>
      </div>
    </template>
    <slot />
  </el-card>
</template>

<style scoped>
.item-card {
  --el-card-padding: 12px;
  margin-bottom: 10px;
}
.item-card__head {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.item-card__title {
  font-weight: 600;
  font-size: 13px;
}
.item-card__ops :deep(.el-button + .el-button) {
  margin-left: 8px;
}
</style>
