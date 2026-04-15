<script setup>
import { reactive, ref } from 'vue'
import { RouterLink, useRouter } from 'vue-router'

import { registerUser } from '../services/auth'

const router = useRouter()

const form = reactive({
  username: '',
  password: '',
})

const errorMessage = ref('')
const isSubmitting = ref(false)

async function handleSubmit() {
  errorMessage.value = ''
  isSubmitting.value = true

  try {
    const payload = await registerUser(form)
    await router.replace({
      name: 'login',
      query: {
        registered: '1',
        username: payload.username,
      },
    })
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
        <h1>注册</h1>
        <p class="page-desc">创建新账号后，再使用同一组凭证登录。</p>
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
            autocomplete="new-password"
            placeholder="请输入密码"
            required
          />
        </label>

        <p v-if="errorMessage" class="message message-error">{{ errorMessage }}</p>

        <button class="button button-primary" type="submit" :disabled="isSubmitting">
          {{ isSubmitting ? '注册中...' : '注册' }}
        </button>
      </form>

      <p class="auth-footer">
        已有账号？
        <RouterLink to="/login">去登录</RouterLink>
      </p>
    </section>
  </main>
</template>
