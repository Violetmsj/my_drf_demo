# CLAUDE.md

本文件为 Claude Code（claude.ai/code）在此仓库中工作时提供指导。

## 项目概述

一个用于学习 Django REST Framework 的演示项目 — 展示了课程 CRUD API 的多种视图实现方式（FBV / CBV / Generic CBV / ViewSet），支持 Token / Session / BasicAuth 三种认证方式。使用者是一名前端工程师，正在学习 Django/DRF 后端概念。

## 常用命令

### 后端（在 `backend/` 目录下执行）

```bash
uv sync                           # 安装依赖
python manage.py runserver        # 启动开发服务器，端口 :8000
python manage.py makemigrations   # 生成迁移文件
python manage.py migrate          # 执行数据库迁移
python manage.py createsuperuser  # 创建管理员用户
ruff check .                      # 代码检查
ruff format .                     # 代码格式化
```

### 前端（在 `frontend/` 目录下执行）

```bash
pnpm install   # 安装依赖
pnpm dev       # 启动 Vite 开发服务器，端口 :5173，代理 /api → :8000
pnpm build     # 生产构建
```

## 架构

### 后端 App

- **`mydrfdemo/`** — Django 项目配置。`settings.py` 中配置了 DRF 默认项：`PageNumberPagination`（page_size=50）、默认权限 `IsAuthenticated`、三种认证类（Basic、Session、Token）、`drf_spectacular` 用于生成 OpenAPI 文档。时区：`Asia/Shanghai`，`USE_TZ = False`。
- **`course/`** — 主要演示 App。`Course` 模型包含字段：name、introduction、teacher（外键关联 User）、price、时间戳。`views.py` 中包含四种不同抽象层次的视图实现，全部挂载在 `/course/` 路径下。
- **`accounts/`** — 用户认证 App。提供注册、登录（返回 Token）、登出（删除 token）、获取当前用户等接口，挂载在 `/accounts/auth/` 下。`signals.py` 通过 `post_save` 信号在用户注册时自动创建 DRF Token。

### URL 结构

| 前缀 | 说明 |
|---|---|
| `/admin/` | Django 管理后台 |
| `/api-auth/` | DRF 可浏览的登录/登出页面 |
| `/api/schema/`、`/api/docs/` | OpenAPI schema + Swagger 文档界面 |
| `/accounts/auth/` | 注册、登录、登出、当前用户 |
| `/course/fbv/` | 函数式视图（FBV） |
| `/course/cbv/` | 类视图（APIView） |
| `/course/gcbv/` | 通用类视图（ListCreateAPIView 等） |
| `/course/viewsets/` | ViewSet + Router |

### 前端

Vue 3 + Vue Router + Vite。认证状态存储在 `localStorage` 中，键名为 `drf-demo-token`，由 `src/services/auth.js` 统一管理（响应式状态、token 持久化、带去重的会话恢复）。路由守卫会将未认证用户重定向到 `/login`，将已认证用户从游客页面重定向出去。Vite 将 `/api/*` 代理到 `http://127.0.0.1:8000`，并去掉 `/api` 前缀。

### 关键约定

- 新的 Django App 直接放在 `backend/` 目录下，并在 `INSTALLED_APPS` 中注册其 `AppConfig`
- 每个 App 在自身的 `urls.py` 中定义路由，然后通过 `mydrfdemo/urls.py` 的 `include()` 挂载
- 新增接口优先使用 ViewSet + Router；FBV/CBV/GCBV 的实现仅用于学习对比
- 自定义权限类放在 `<app>/permissions.py` 中
- 序列化器中外键的展示字段使用 `ReadOnlyField(source='...')`
- 前端使用 `<script setup>` 组合式 API；API 请求统一通过 `/api/` 发起（由 Vite 代理转发）
- 仓库根目录的 `pyrightconfig.json` 为 `backend/` 目录配置了 Pyright，类型检查模式为 `basic`
