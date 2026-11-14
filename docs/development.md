# 本地开发指南

## 目录约定

- 后端 Python 虚拟环境：`backend/.venv`（不入库）
- 前端依赖：`frontend/node_modules`（不入库）
- 本地生成产物：`output/`（不入库）

## 日常开发流程

```bash
# 终端 1：后端（自动重载）
cd backend
.venv\Scripts\activate
uvicorn app.main:app --reload --port 8000

# 终端 2：前端（Vite 热更新，/api 代理到 8000）
cd frontend
npm run dev
```

访问 <http://localhost:5173>。

## 常用任务

| 任务 | 命令 |
|---|---|
| 后端测试 | `cd backend && pytest -v` |
| 仅跑非 PDF 测试 | `pytest -m "not pdf"` |
| 静态检查 | `cd backend && ruff check .` |
| 前端类型检查 + 构建 | `cd frontend && npm run build` |
| 生成本地样例 PDF | 见下文脚本 |

## 生成样例 PDF（验证模板改动）

```bash
cd backend
.venv\Scripts\python -c "import asyncio; from app.services.sample_service import load_sample_resume; from app.services.render_service import RenderService; from app.services.pdf_service import PdfService; exec(open('../scripts/gen_samples.py', encoding='utf-8').read())"
```

或直接用简化脚本 `scripts/gen_samples.py`（见仓库 scripts/ 目录）。

## 配置项

| 环境变量 | 默认值 | 说明 |
|---|---|---|
| `RESUME_DEBUG` | `false` | 调试模式 |
| `RESUME_LOG_LEVEL` | `INFO` | 日志级别 |
| `RESUME_CORS_ORIGINS` | `["http://localhost:5173", ...]` | 允许的跨域来源（JSON 数组） |
| `RESUME_PDF_TIMEOUT_MS` | `30000` | PDF 导出超时 |
| `RESUME_FRONTEND_DIST_DIR` | 自动探测 `frontend/dist` | 生产模式前端产物目录 |

## 发布检查清单

1. `ruff check .` 与 `pytest` 全过
2. `npm run build` 无类型错误
3. 两种模板各导出一份 PDF 目检（字体、分页、链接）
4. JSON 导出 → 清空 → 导入，数据无损
5. 更新 `schema_version`（若数据结构有变更）并在 README 标注
