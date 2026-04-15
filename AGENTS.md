# 产品概述

这是一个课程管理系统的演示项目（DRF Demo），用于展示 Django REST Framework 的各种视图模式和 API 设计方式。
这是我用来学习 django 和 drf 的一个项目，我本身是一名前端开发工程师，我缺乏后端的思维，所以本项目主要是为了学习和理解 django 和 drf 的工作原理，前端方面只要能实现功能就行。
## 核心功能

- 课程（Course）的增删改查 API
- 多种视图实现方式的对比演示（FBV / CBV / Generic CBV / ViewSet）
- 基于 Token、Session、BasicAuth 的多种认证方式
- 自定义权限控制（仅课程创建者可编辑）
- Vue 3 前端页面通过代理调用后端 API

## 目标用户

学习 Django REST Framework 的开发者，用于理解不同视图层次的实现差异。
# 项目结构

```
├── backend/                        # Django 后端
│   ├── mydrfdemo/                  # Django 项目配置
│   │   ├── settings.py             # 全局配置（DRF、数据库、认证等）
│   │   └── urls.py                 # 根路由（挂载 api-auth、admin）
│   ├── course/                     # 课程 App
│   │   ├── models.py               # Course 模型
│   │   ├── serializers.py          # CourseSerializer、UserSerializer
│   │   ├── views.py                # 四种视图实现（FBV/CBV/Generic/ViewSet）
│   │   ├── urls.py                 # 课程相关路由
│   │   ├── permissions.py          # 自定义权限 IsOwnerOrReadOnly
│   │   ├── admin.py
│   │   └── migrations/
│   ├── manage.py
│   └── pyproject.toml
│
└── frontend/                       # Vue 3 前端
    ├── src/
    │   ├── App.vue                 # 根组件
    │   ├── components/             # 通用组件
    │   ├── main.js                 # 应用入口
    │   └── style.css
    ├── public/
    ├── vite.config.js              # Vite 配置（含 /api 代理）
    └── package.json
```

## 后端架构约定

- 新 Django App 放在 `backend/` 根目录下，并在 `settings.py` 的 `INSTALLED_APPS` 中注册
- 每个 App 的路由在自身 `urls.py` 中定义，再通过 `mydrfdemo/urls.py` 的 `include()` 挂载
- 视图优先使用 `ViewSet` + `Router`，其次是 `Generic CBV`；FBV 和 CBV 仅用于演示对比
- 自定义权限类放在 App 内的 `permissions.py`
- 序列化器中外键字段使用 `ReadOnlyField(source='...')` 展示关联对象的可读字段

## 前端架构约定

- 使用 `<script setup>` 语法（Composition API）
- 组件放在 `src/components/`
- API 请求路径以 `/api/` 开头，由 Vite 代理转发到后端

## 路由结构（后端）

| 前缀 | 说明 |
|------|------|
| `/admin/` | Django 管理后台 |
| `/api-auth/` | DRF 内置登录/登出 |
| `/fbv/` | Function Based View 示例 |
| `/cbv/` | Class Based View 示例 |
| `/gcbv/` | Generic CBV 示例 |
| `/viewsets/` | ViewSet + Router 示例 |
# 技术栈

## 后端

- Python >= 3.14
- Django 6.0.3
- Django REST Framework 3.17.1
- 数据库：SQLite（开发环境）
- 包管理：uv（使用 `uv.lock` 锁定依赖）
- 代码检查：ruff

## 前端

- Vue 3（Composition API / `<script setup>`）
- Vite 8
- pnpm 包管理

## 认证方式

- TokenAuthentication（推荐）
- SessionAuthentication
- BasicAuthentication

## DRF 全局配置（settings.py）

- 分页：`PageNumberPagination`，每页 50 条
- 默认权限：`IsAuthenticated`
- 时间格式：`%Y-%m-%d %H:%M:%S`
- 语言：`zh-hans`，时区：`Asia/Shanghai`

## 常用命令

### 后端（在 `backend/` 目录下执行）

```bash
# 安装依赖
uv sync

# 数据库迁移
python manage.py makemigrations
python manage.py migrate

# 启动开发服务器（端口 8000）
python manage.py runserver

# 创建超级用户
python manage.py createsuperuser

# 代码检查
ruff check .
ruff format .
```

### 前端（在 `frontend/` 目录下执行）

```bash
# 安装依赖
pnpm install

# 启动开发服务器（端口 5173，自动代理 /api 到 8000）
pnpm dev

# 构建生产包
pnpm build
```

## 前后端联调

Vite 配置了代理：前端请求 `/api/*` 会自动转发到 `http://127.0.0.1:8000`，无需手动处理跨域。
