<script setup lang="ts">
import { Plus } from '@element-plus/icons-vue'

import { useResumeStore } from '@/stores/resume'
import ItemCard from './ItemCard.vue'
import DateRange from './DateRange.vue'
import BulletEditor from './BulletEditor.vue'

/** 实习经历。 */
const store = useResumeStore()
const key = 'internships' as const
</script>

<template>
  <div>
    <ItemCard
      v-for="(item, index) in store.data.internships"
      :key="index"
      :title="item.company || `实习 ${index + 1}`"
      @move-up="store.moveListItem(key, index, -1)"
      @move-down="store.moveListItem(key, index, 1)"
      @remove="store.removeListItem(key, index)"
    >
      <el-form label-position="top">
        <div class="grid-2">
          <el-form-item label="公司名称" required>
            <el-input v-model="item.company" placeholder="如：小米科技" />
          </el-form-item>
          <el-form-item label="实习岗位" required>
            <el-input v-model="item.position" placeholder="如：后端开发实习生" />
          </el-form-item>
          <el-form-item label="起止时间" required>
            <DateRange v-model:start="item.start_date" v-model:end="item.end_date" />
          </el-form-item>
        </div>
        <el-form-item label="工作内容（建议按 STAR 法则，突出量化结果）" required>
          <BulletEditor
            v-model="item.highlights"
            placeholder="如：负责 xx 模块开发，通过 xx 优化将 P99 延迟降低 xx%"
          />
        </el-form-item>
      </el-form>
    </ItemCard>
    <el-button plain class="add-btn" :icon="Plus" @click="store.addListItem(key)">
      添加实习经历
    </el-button>
  </div>
</template>
