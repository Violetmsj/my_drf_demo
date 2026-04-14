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
