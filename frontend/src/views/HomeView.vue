<script setup>
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'

import { authState, logoutUser } from '../services/auth'

const router = useRouter()

const isSubmitting = ref(false)
const errorMessage = ref('')
const username = computed(() => authState.user?.username || '')

async function handleLogout() {
  errorMessage.value = ''
  isSubmitting.value = true

  try {
    await logoutUser()
    await router.replace({
      name: 'login',
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
    <section class="home-card">
      <p class="eyebrow">DRF Demo</p>
      <h1>登录成功</h1>
      <p class="page-desc">当前用户：{{ username || '正在加载用户信息...' }}</p>

      <div class="home-actions">
        <button class="button button-primary" type="button" :disabled="isSubmitting" @click="handleLogout">
          {{ isSubmitting ? '退出中...' : '退出登录' }}
        </button>
      </div>

      <p v-if="errorMessage" class="message message-error">{{ errorMessage }}</p>
    </section>
  </main>
</template>
