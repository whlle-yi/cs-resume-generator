<script setup lang="ts">
import { Plus } from '@element-plus/icons-vue'

import { useResumeStore } from '@/stores/resume'
import ItemCard from './ItemCard.vue'
import DateRange from './DateRange.vue'
import BulletEditor from './BulletEditor.vue'

/** 校园经历 / 学生工作（可选）。 */
const store = useResumeStore()
const key = 'campus' as const
</script>

<template>
  <div>
    <ItemCard
      v-for="(item, index) in store.data.campus"
      :key="index"
      :title="item.organization || `校园经历 ${index + 1}`"
      @move-up="store.moveListItem(key, index, -1)"
      @move-down="store.moveListItem(key, index, 1)"
      @remove="store.removeListItem(key, index)"
    >
      <el-form label-position="top">
        <div class="grid-2">
          <el-form-item label="组织 / 社团" required>
            <el-input v-model="item.organization" placeholder="如：校计算机协会" />
          </el-form-item>
          <el-form-item label="担任职务">
            <el-input v-model="item.role" placeholder="如：技术部部长" />
          </el-form-item>
          <el-form-item label="起止时间" required>
            <DateRange v-model:start="item.start_date" v-model:end="item.end_date" />
          </el-form-item>
        </div>
        <el-form-item label="经历要点">
          <BulletEditor v-model="item.highlights" placeholder="如：组织 xx 活动，覆盖 xx 人" />
        </el-form-item>
      </el-form>
    </ItemCard>
    <el-button plain class="add-btn" :icon="Plus" @click="store.addListItem(key)">
      添加校园经历
    </el-button>
  </div>
</template>
