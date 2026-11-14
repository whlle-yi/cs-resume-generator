<script setup lang="ts">
import { Plus } from '@element-plus/icons-vue'

import { useResumeStore } from '@/stores/resume'
import { DEGREE_OPTIONS } from '@/types/resume'
import ItemCard from './ItemCard.vue'
import TagInput from './TagInput.vue'
import DateRange from './DateRange.vue'

/** 教育背景。 */
const store = useResumeStore()
const key = 'education' as const
</script>

<template>
  <div>
    <ItemCard
      v-for="(edu, index) in store.data.education"
      :key="index"
      :title="edu.school || `教育经历 ${index + 1}`"
      @move-up="store.moveListItem(key, index, -1)"
      @move-down="store.moveListItem(key, index, 1)"
      @remove="store.removeListItem(key, index)"
    >
      <el-form label-position="top">
        <div class="grid-2">
          <el-form-item label="学校" required>
            <el-input v-model="edu.school" placeholder="如：华中科技大学" />
          </el-form-item>
          <el-form-item label="学院">
            <el-input v-model="edu.college" placeholder="如：计算机科学与技术学院" />
          </el-form-item>
          <el-form-item label="专业" required>
            <el-input v-model="edu.major" placeholder="如：计算机科学与技术" />
          </el-form-item>
          <el-form-item label="学历" required>
            <el-select v-model="edu.degree" style="width: 100%">
              <el-option v-for="d in DEGREE_OPTIONS" :key="d" :label="d" :value="d" />
            </el-select>
          </el-form-item>
          <el-form-item label="起止时间" required>
            <DateRange v-model:start="edu.start_date" v-model:end="edu.end_date" />
          </el-form-item>
          <el-form-item label="GPA / 排名">
            <el-input v-model="edu.gpa_rank" placeholder="如：GPA 3.8/4.0（专业前 5%）" />
          </el-form-item>
        </div>
        <el-form-item label="主修课程">
          <TagInput v-model="edu.courses" placeholder="输入课程名后回车，如：数据结构" />
        </el-form-item>
      </el-form>
    </ItemCard>
    <el-button plain class="add-btn" :icon="Plus" @click="store.addListItem(key)">
      添加教育经历
    </el-button>
  </div>
</template>
