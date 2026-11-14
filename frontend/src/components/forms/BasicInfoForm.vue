<script setup lang="ts">
import { useResumeStore } from '@/stores/resume'

/** 基本信息：联系方式与求职意向。 */
const store = useResumeStore()
</script>

<template>
  <el-form label-position="top" class="basic-info">
    <div class="grid-2">
      <el-form-item label="姓名" required>
        <el-input v-model="store.data.basics.name" placeholder="姓名" />
      </el-form-item>
      <el-form-item label="求职意向" required>
        <el-input v-model="store.data.basics.objective" placeholder="如：后端开发工程师" />
      </el-form-item>
      <el-form-item label="手机号" required>
        <el-input v-model="store.data.basics.phone" placeholder="13800138000" />
      </el-form-item>
      <el-form-item label="邮箱" required>
        <el-input v-model="store.data.basics.email" placeholder="name@example.com" />
      </el-form-item>
      <el-form-item label="所在城市">
        <el-input v-model="store.data.basics.city" placeholder="如：北京" />
      </el-form-item>
      <el-form-item label="GitHub 主页">
        <el-input v-model="store.data.basics.github" placeholder="https://github.com/username" />
      </el-form-item>
      <el-form-item label="个人博客">
        <el-input v-model="store.data.basics.blog" placeholder="https://blog.example.com" />
      </el-form-item>
      <el-form-item label="证件照链接（可选）">
        <el-input v-model="store.data.basics.photo_url" placeholder="https://..." />
      </el-form-item>
    </div>
  </el-form>
</template>
