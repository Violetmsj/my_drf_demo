<script setup>
import { onMounted, reactive, ref } from 'vue'
import { RouterLink, useRoute, useRouter } from 'vue-router'

import { loginUser } from '../services/auth'

const router = useRouter()
const route = useRoute()

const form = reactive({
  username: '',
  password: '',
})

const errorMessage = ref('')
const successMessage = ref('')
const isSubmitting = ref(false)

onMounted(() => {
  if (typeof route.query.username === 'string') {
    form.username = route.query.username
  }

  if (route.query.registered === '1') {
    successMessage.value = '注册成功，请使用刚才的账号登录。'
  }
})

async function handleSubmit() {
  errorMessage.value = ''
  successMessage.value = ''
  isSubmitting.value = true

  try {
    await loginUser(form)
    const redirect = typeof route.query.redirect === 'string' ? route.query.redirect : '/'
    await router.replace(redirect)
  } catch (error) {
    errorMessage.value = error.message
  } finally {
    isSubmitting.value = false
  }
}
</script>

<template>
  <main class="page-shell">
    <section class="auth-card">
      <div class="auth-header">
        <p class="eyebrow">DRF Demo</p>
        <h1>登录</h1>
        <p class="page-desc">输入用户名和密码，获取 Token 后进入首页。</p>
      </div>

      <form class="auth-form" @submit.prevent="handleSubmit">
        <label class="field">
          <span>用户名</span>
          <input
            v-model.trim="form.username"
            type="text"
            autocomplete="username"
            placeholder="请输入用户名"
            required
          />
        </label>

        <label class="field">
          <span>密码</span>
          <input
            v-model="form.password"
            type="password"
            autocomplete="current-password"
            placeholder="请输入密码"
            required
          />
        </label>

        <p v-if="successMessage" class="message message-success">{{ successMessage }}</p>
        <p v-if="errorMessage" class="message message-error">{{ errorMessage }}</p>

        <button class="button button-primary" type="submit" :disabled="isSubmitting">
          {{ isSubmitting ? '登录中...' : '登录' }}
        </button>
      </form>

      <p class="auth-footer">
        还没有账号？
        <RouterLink to="/register">去注册</RouterLink>
      </p>
    </section>
  </main>
</template>
