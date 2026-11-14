<script setup lang="ts">
import { Delete, Plus } from '@element-plus/icons-vue'

import { useResumeStore } from '@/stores/resume'
import { PROFICIENCY_OPTIONS } from '@/types/resume'
import ItemCard from './ItemCard.vue'

/** 专业技能：分组条目。 */
const store = useResumeStore()
const key = 'skills' as const

function addItem(groupIndex: number): void {
  store.data.skills[groupIndex]?.items.push({ name: '', level: null })
}

function removeItem(groupIndex: number, itemIndex: number): void {
  store.data.skills[groupIndex]?.items.splice(itemIndex, 1)
}
</script>

<template>
  <div>
    <ItemCard
      v-for="(group, index) in store.data.skills"
      :key="index"
      :title="group.category || `技能分组 ${index + 1}`"
      @move-up="store.moveListItem(key, index, -1)"
      @move-down="store.moveListItem(key, index, 1)"
      @remove="store.removeListItem(key, index)"
    >
      <el-form label-position="top">
        <el-form-item label="分组名称" required>
          <el-input v-model="group.category" placeholder="如：编程语言 / 框架与中间件 / 工具与平台" />
        </el-form-item>
        <el-form-item label="技能条目" required>
          <div class="skill-items">
            <div v-for="(item, itemIndex) in group.items" :key="itemIndex" class="skill-item">
              <el-input v-model="item.name" placeholder="如：Python" />
              <el-select v-model="item.level" placeholder="熟练度" clearable style="width: 120px">
                <el-option v-for="p in PROFICIENCY_OPTIONS" :key="p" :label="p" :value="p" />
              </el-select>
              <el-button
                link
                type="danger"
                :icon="Delete"
                :disabled="group.items.length <= 1"
                @click="removeItem(index, itemIndex)"
              />
            </div>
            <el-button link type="primary" :icon="Plus" @click="addItem(index)">添加技能</el-button>
          </div>
        </el-form-item>
      </el-form>
    </ItemCard>
    <el-button plain class="add-btn" :icon="Plus" @click="store.addListItem(key)">
      添加技能分组
    </el-button>
  </div>
</template>

<style scoped>
.skill-items {
  width: 100%;
}
.skill-item {
  display: flex;
  gap: 8px;
  align-items: center;
  margin-bottom: 8px;
}
</style>
