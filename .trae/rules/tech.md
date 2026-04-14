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
