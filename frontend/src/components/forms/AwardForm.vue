<script setup lang="ts">
import { Plus } from '@element-plus/icons-vue'

import { useResumeStore } from '@/stores/resume'
import ItemCard from './ItemCard.vue'

/** 获奖情况。 */
const store = useResumeStore()
const key = 'awards' as const
</script>

<template>
  <div>
    <ItemCard
      v-for="(award, index) in store.data.awards"
      :key="index"
      :title="award.name || `奖项 ${index + 1}`"
      @move-up="store.moveListItem(key, index, -1)"
      @move-down="store.moveListItem(key, index, 1)"
      @remove="store.removeListItem(key, index)"
    >
      <el-form label-position="top">
        <div class="grid-2">
          <el-form-item label="奖项名称" required>
            <el-input v-model="award.name" placeholder="如：蓝桥杯软件类 C/C++ 组" />
          </el-form-item>
          <el-form-item label="奖项级别">
            <el-input v-model="award.level" placeholder="如：省级一等奖" />
          </el-form-item>
          <el-form-item label="获奖时间" required>
            <el-date-picker
              v-model="award.date"
              type="month"
              value-format="YYYY-MM"
              placeholder="选择年月"
              style="width: 100%"
            />
          </el-form-item>
        </div>
      </el-form>
    </ItemCard>
    <el-button plain class="add-btn" :icon="Plus" @click="store.addListItem(key)">
      添加获奖
    </el-button>
  </div>
</template>
