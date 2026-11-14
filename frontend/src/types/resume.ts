/** 简历数据类型：与后端 app/schemas/resume.py 的 Pydantic 模型保持镜像。 */

export type Degree = '专科' | '本科' | '硕士' | '博士'
export type Proficiency = '了解' | '掌握' | '熟练' | '精通'

export interface Basics {
  name: string
  objective: string
  phone: string
  email: string
  city: string | null
  github: string | null
  blog: string | null
  photo_url: string | null
}

export interface Education {
  school: string
  college: string | null
  major: string
  degree: Degree
  start_date: string
  end_date: string
  gpa_rank: string | null
  courses: string[]
}

export interface SkillItem {
  name: string
  level: Proficiency | null
}

export interface SkillGroup {
  category: string
  items: SkillItem[]
}

export interface ProjectExperience {
  name: string
  role: string | null
  start_date: string
  end_date: string
  tech_stack: string[]
  highlights: string[]
  link: string | null
}

export interface InternshipExperience {
  company: string
  position: string
  start_date: string
  end_date: string
  highlights: string[]
}

export interface CampusExperience {
  organization: string
  role: string | null
  start_date: string
  end_date: string
  highlights: string[]
}

export interface Award {
  name: string
  level: string | null
  date: string
}

export interface ResumeData {
  schema_version: number
  basics: Basics
  education: Education[]
  skills: SkillGroup[]
  projects: ProjectExperience[]
  internships: InternshipExperience[]
  campus: CampusExperience[]
  awards: Award[]
  self_evaluation: string[]
}

export interface TemplateInfo {
  id: string
  name: string
  description: string
}

export interface RenderRequest {
  data: ResumeData
  template: string
}

/** 完全空白的简历数据。 */
export function emptyResume(): ResumeData {
  return {
    schema_version: 1,
    basics: {
      name: '',
      objective: '',
      phone: '',
      email: '',
      city: null,
      github: null,
      blog: null,
      photo_url: null,
    },
    education: [],
    skills: [],
    projects: [],
    internships: [],
    campus: [],
    awards: [],
    self_evaluation: [],
  }
}

export const DEGREE_OPTIONS: Degree[] = ['专科', '本科', '硕士', '博士']
export const PROFICIENCY_OPTIONS: Proficiency[] = ['了解', '掌握', '熟练', '精通']
