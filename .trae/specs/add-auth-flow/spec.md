# 登录注册功能 Spec

## Why
当前项目已经有课程相关 API，但默认要求认证，缺少一套完整、可独立理解的用户注册、登录、退出登录闭环，导致前后端联调和 DRF 认证机制的学习都不完整。
这次需求不仅要补齐功能，还要把后端设计这类需求时的思考路径显式写出来，帮助前端背景的开发者建立“先边界、再状态、后接口”的后端思维。

## What Changes
- 新增注册接口，允许游客创建账号，并返回最小必要的用户信息
- 新增登录接口，校验用户名和密码，登录成功后返回 Token 与当前用户信息
- 新增退出登录接口，要求携带已登录 Token，请求成功后使当前 Token 失效
- 新增“当前登录用户”接口，用于前端刷新后恢复登录态并判断首页展示内容
- 新增前端登录页、注册页、首页以及基础路由守卫
- 首页在已登录状态下显示“登录成功”和退出登录按钮，未登录用户跳转到登录页
- 为认证流程补充基础接口校验与最小必要测试

## Impact
- Affected specs: 用户认证、前端路由访问控制、首页登录态展示
- Affected code: `backend/mydrfdemo/settings.py`、`backend/mydrfdemo/urls.py`、`backend/course/serializers.py`、`backend/course/views.py`、`backend/course/urls.py`、`backend/course/tests.py`、`frontend/src/App.vue`、`frontend/src/main.js`、`frontend/package.json`

## 设计思考
### 一个有经验的后端会先考虑什么
- 认证方案先定边界：当前项目已经启用 `TokenAuthentication`、`SessionAuthentication`、`BasicAuthentication`，但前后端分离场景最适合优先走 Token，因为前端最容易保存、透传和调试
- 先区分“公开接口”和“受保护接口”：注册、登录必须允许匿名访问；退出登录、获取当前用户信息必须要求已登录，否则默认全局 `IsAuthenticated` 会把入口也拦掉
- 明确“登录态存在哪里”：本方案以服务端签发 Token、前端持有 Token 为主，后端不负责页面跳转，只负责认证结果与状态校验
- 先想清楚注销语义：退出登录不是“前端把本地 Token 删掉”这么简单，后端也需要让当前 Token 失效，否则旧 Token 仍可继续访问受保护接口
- 输入校验和错误响应要稳定：用户名是否唯一、密码是否为空、登录失败提示什么、状态码怎么返回，都会直接影响前端接入成本
- 给前端一个稳定的“身份确认点”：刷新页面后，前端不能只依赖本地缓存判断是否登录，最好调用“当前用户”接口做一次后端确认
- 保持最小闭环：这一版只做注册、登录、退出、获取当前用户和首页展示，不提前扩展邮箱验证、短信验证码、找回密码、刷新 Token 等复杂能力

### 本次设计取舍
- 采用 Django 内置 `User` 模型，不引入自定义用户表，降低学习成本和迁移复杂度
- 采用 DRF Token 作为本次主认证方式，复用项目现有依赖，不额外引入 JWT
- 登录成功直接返回 Token，便于前端后续通过 `Authorization: Token <token>` 访问受保护接口
- 退出登录通过失效当前 Token 实现；如需再次登录，可重新签发新的 Token
- 前端只做最小页面与路由骨架，重点把接口职责、认证边界和状态恢复流程讲清楚

## ADDED Requirements
### Requirement: 用户注册
系统 SHALL 提供匿名可访问的注册接口，允许用户使用用户名和密码创建账号，并返回注册成功后的基础用户信息。

#### Scenario: 注册成功
- **WHEN** 游客提交唯一用户名和合法密码
- **THEN** 系统创建用户账号并返回 `201 Created`
- **THEN** 响应体包含基础用户信息，且不返回明文密码

#### Scenario: 用户名重复
- **WHEN** 游客使用已存在的用户名提交注册
- **THEN** 系统返回 `400 Bad Request`
- **THEN** 响应体包含可供前端展示的字段级错误信息

### Requirement: 用户登录
系统 SHALL 提供匿名可访问的登录接口，校验用户名和密码，成功后返回可用于后续认证的 Token 和当前用户信息。

#### Scenario: 登录成功
- **WHEN** 用户提交正确的用户名和密码
- **THEN** 系统返回 `200 OK`
- **THEN** 响应体包含 Token 与当前用户基础信息

#### Scenario: 登录失败
- **WHEN** 用户提交错误的用户名或密码
- **THEN** 系统返回 `400 Bad Request` 或 `401 Unauthorized`
- **THEN** 响应体包含统一且可理解的错误提示

### Requirement: 用户退出登录
系统 SHALL 提供仅登录用户可访问的退出登录接口，使当前 Token 失效。

#### Scenario: 退出成功
- **WHEN** 已登录用户携带有效 Token 调用退出登录接口
- **THEN** 系统返回 `200 OK` 或 `204 No Content`
- **THEN** 当前 Token 失效，后续再使用该 Token 访问受保护接口会被拒绝

### Requirement: 获取当前登录用户
系统 SHALL 提供仅登录用户可访问的当前用户信息接口，用于前端恢复登录态和展示首页内容。

#### Scenario: 获取当前用户成功
- **WHEN** 已登录用户携带有效 Token 请求当前用户接口
- **THEN** 系统返回 `200 OK`
- **THEN** 响应体包含当前用户的基础信息

#### Scenario: 未登录访问当前用户
- **WHEN** 未登录用户或携带无效 Token 请求当前用户接口
- **THEN** 系统返回 `401 Unauthorized`

### Requirement: 前端登录态路由
系统 SHALL 提供最小前端页面与路由流程，支持注册、登录、首页展示与退出登录。

#### Scenario: 未登录访问首页
- **WHEN** 用户直接访问首页
- **THEN** 前端检测不到有效登录态并跳转到登录页

#### Scenario: 登录后进入首页
- **WHEN** 用户登录成功
- **THEN** 前端保存 Token 并跳转到首页
- **THEN** 首页显示“登录成功”和退出登录按钮

#### Scenario: 退出后回到登录页
- **WHEN** 用户在首页点击退出登录
- **THEN** 前端调用退出接口并清理本地登录态
- **THEN** 页面跳转回登录页
