<script setup lang="ts">
import { onMounted, watch } from 'vue'

import { useResumeStore } from '@/stores/resume'

import AwardForm from '@/components/forms/AwardForm.vue'
import BasicInfoForm from '@/components/forms/BasicInfoForm.vue'
import CampusForm from '@/components/forms/CampusForm.vue'
import EducationForm from '@/components/forms/EducationForm.vue'
import InternshipForm from '@/components/forms/InternshipForm.vue'
import ProjectForm from '@/components/forms/ProjectForm.vue'
import SectionCard from '@/components/forms/SectionCard.vue'
import SelfEvalForm from '@/components/forms/SelfEvalForm.vue'
import SkillForm from '@/components/forms/SkillForm.vue'
import PreviewPane from '@/components/preview/PreviewPane.vue'
import Toolbar from '@/components/preview/Toolbar.vue'

/** 主视图：左侧表单 + 右侧实时预览。 */
const store = useResumeStore()

onMounted(() => {
  void store.init()
})

// 内容或模板变化 → 防抖刷新预览（store 内部再做过 500ms 防抖）
watch(() => [store.data, store.template], () => store.refreshPreview(), { deep: true })
</script>

<template>
  <el-container class="layout">
    <el-header class="app-header" height="52px">
      <span class="app-header__title">CS 简历生成器</span>
      <span class="app-header__sub">
        填写信息 → 实时预览 → 导出 PDF · 数据仅保存在本机浏览器
      </span>
    </el-header>
    <el-container class="layout__body">
      <el-aside class="form-aside" width="46%">
        <el-scrollbar>
          <div class="form-col">
            <SectionCard title="基本信息">
              <BasicInfoForm />
            </SectionCard>
            <SectionCard title="教育背景" :count="store.data.education.length">
              <EducationForm />
            </SectionCard>
            <SectionCard title="专业技能" :count="store.data.skills.length">
              <SkillForm />
            </SectionCard>
            <SectionCard title="实习经历" :count="store.data.internships.length">
              <InternshipForm />
            </SectionCard>
            <SectionCard title="项目经历" :count="store.data.projects.length">
              <ProjectForm />
            </SectionCard>
            <SectionCard title="校园经历（可选）" :count="store.data.campus.length">
              <CampusForm />
            </SectionCard>
            <SectionCard title="获奖情况" :count="store.data.awards.length">
              <AwardForm />
            </SectionCard>
            <SectionCard title="自我评价（可选）" :count="store.data.self_evaluation.length">
              <SelfEvalForm />
            </SectionCard>
          </div>
        </el-scrollbar>
      </el-aside>
      <el-main class="preview-main">
        <Toolbar />
        <PreviewPane />
      </el-main>
    </el-container>
  </el-container>
</template>
