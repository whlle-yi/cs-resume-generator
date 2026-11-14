# 架构设计

## 总体分层

系统为前后端分离的 Monorepo，两层各自自包含、可独立运行：

```
┌─────────────────────────────┐        ┌──────────────────────────────────┐
│ frontend (Vue3 + TS)        │  HTTP  │ backend (FastAPI)                │
│                             │ ─────► │                                  │
│  views/HomeView             │  JSON  │  api/v1 (路由/端点)               │
│    ├─ components/forms      │        │    └─► services (业务逻辑)        │
│    ├─ components/preview    │        │          ├─ RenderService        │
│    ├─ stores/resume         │        │          └─ PdfService           │
│    └─ api (axios 封装)       │        │  schemas (Pydantic 数据契约)      │
│                             │        │  templates (Jinja2 + 打印 CSS)   │
└─────────────────────────────┘        └──────────────────────────────────┘
```

请求流（预览 / 导出）：

```
表单输入 ──► Pinia store（watch 深度监听）
              ├─ 800ms 防抖 ──► localStorage 草稿
              └─ 500ms 防抖 ──► POST /api/v1/resume/preview ──► Jinja2 渲染
                                                                  │
              「导出 PDF」点击 ──► POST /api/v1/resume/export/pdf ──► Playwright Chromium
                                                                     └─► A4 PDF 字节流
```

## 关键设计决策

### 1. 数据契约唯一（Pydantic 是唯一数据源）

`backend/app/schemas/resume.py` 定义简历全部结构（Basics / Education / SkillGroup / ProjectExperience …）与校验规则（手机号正则、邮箱、URL、YYYY-MM 月份格式、起止时间顺序、要点非空）。前端 `frontend/src/types/resume.ts` 是它的 TypeScript 镜像。改字段先改 Pydantic，再同步 TS 类型。

`schema_version` 置于数据根节点，用于后续结构演进时的迁移判断。

### 2. 内容与版式分离

简历数据不携带任何排版信息；模板选择（`classic` / `modern`）是渲染请求的独立字段，草稿中单独保存。新增一套模板只需：

1. 在 `app/templates/` 添加 `<id>.html.j2` 与 `styles/<id>.css`；
2. 在 `app/services/render_service.py` 的 `AVAILABLE_TEMPLATES` 登记。

零 Python 业务代码改动。

### 3. 自包含 HTML 渲染产物

Jinja2 渲染时把公共样式 + 模板私有样式合并后**内联**进 `<style>`，产物不引用任何外部资源：

- 预览 iframe 用 `srcdoc` 即可展示（`sandbox=""` 阻断脚本，防注入）；
- PDF 导出无需等待网络资源，离线环境也能出图。

### 4. PDF 引擎常驻复用

`PdfService` 在首次导出时惰性启动无头 Chromium（约 1–2s），此后浏览器实例常驻，单次导出约 400ms；应用关闭时由 FastAPI lifespan 统一释放。引擎调用收敛在单一类中，未来可替换为 WeasyPrint 等实现而不影响上层。

### 5. 预览即最终产物

预览与 PDF 使用**同一次渲染**的同一份 HTML，唯一的差异是 Chromium 打印时应用 `@page` 规则（A4、页边距）。因此预览可信，不存在「预览正常、PDF 走样」的问题。

## 打印排版要点（templates/styles/base.css）

- `@page { size: A4; margin: 12mm 11mm }` + `page.pdf(prefer_css_page_size=True)`
- `.entry { break-inside: avoid }`：条目不跨页断裂；`h2 { break-after: avoid }`：标题不与内容分离
- 字体栈 `"Times New Roman", "SimSun", ...`：西文/数字走 Times，中文回退宋体
- 屏幕媒体下 `.page` 模拟 A4 纸张（阴影居中），打印媒体下交还 `@page` 控制

## 错误处理约定

- 业务异常继承 `core/errors.py::AppError`（code + message + details），由 `main.py` 全局处理器转为统一 JSON：`{"code", "message", "details"}`
- 请求体校验失败统一 422 `VALIDATION_ERROR`，details 中为逐字段错误（loc/msg/type），前端拦截器取首条拼接可读信息
