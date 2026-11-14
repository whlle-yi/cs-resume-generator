<script setup lang="ts">
import { Plus } from '@element-plus/icons-vue'

import { useResumeStore } from '@/stores/resume'
import ItemCard from './ItemCard.vue'
import TagInput from './TagInput.vue'
import DateRange from './DateRange.vue'
import BulletEditor from './BulletEditor.vue'

/** 项目经历：要点建议按 STAR 法则撰写。 */
const store = useResumeStore()
const key = 'projects' as const
</script>

<template>
  <div>
    <ItemCard
      v-for="(proj, index) in store.data.projects"
      :key="index"
      :title="proj.name || `项目 ${index + 1}`"
      @move-up="store.moveListItem(key, index, -1)"
      @move-down="store.moveListItem(key, index, 1)"
      @remove="store.removeListItem(key, index)"
    >
      <el-form label-position="top">
        <div class="grid-2">
          <el-form-item label="项目名称" required>
            <el-input v-model="proj.name" placeholder="如：分布式键值存储系统" />
          </el-form-item>
          <el-form-item label="担任角色">
            <el-input v-model="proj.role" placeholder="如：核心开发 / 组长" />
          </el-form-item>
          <el-form-item label="起止时间" required>
            <DateRange v-model:start="proj.start_date" v-model:end="proj.end_date" />
          </el-form-item>
          <el-form-item label="项目链接">
            <el-input v-model="proj.link" placeholder="https://github.com/..." />
          </el-form-item>
        </div>
        <el-form-item label="技术栈">
          <TagInput v-model="proj.tech_stack" placeholder="输入技术后回车，如：Go" />
        </el-form-item>
        <el-form-item label="要点描述（建议按 STAR 法则，突出量化结果）" required>
          <BulletEditor
            v-model="proj.highlights"
            placeholder="如：设计 xx 方案解决 xx 问题，性能提升 xx%"
          />
        </el-form-item>
      </el-form>
    </ItemCard>
    <el-button plain class="add-btn" :icon="Plus" @click="store.addListItem(key)">
      添加项目经历
    </el-button>
  </div>
</template>
