import { reactive } from 'vue'

const TOKEN_KEY = 'drf-demo-token'
const AUTH_API_BASE = '/api/accounts/auth'

export const authState = reactive({
  token: readStoredToken(),
  user: null,
})

let restorePromise = null

function readStoredToken() {
  return window.localStorage.getItem(TOKEN_KEY) || ''
}

function writeStoredToken(token) {
  window.localStorage.setItem(TOKEN_KEY, token)
  authState.token = token
}

export function clearAuthState() {
  window.localStorage.removeItem(TOKEN_KEY)
  authState.token = ''
  authState.user = null
}

function extractErrorMessage(payload) {
  if (!payload) {
    return '请求失败，请稍后重试'
  }

  if (typeof payload === 'string') {
    return payload
  }

  if (typeof payload.detail === 'string') {
    return payload.detail
  }

  if (Array.isArray(payload.non_field_errors) && payload.non_field_errors.length > 0) {
    return payload.non_field_errors[0]
  }

  const firstField = Object.keys(payload)[0]
  if (!firstField) {
    return '请求失败，请稍后重试'
  }

  const firstValue = payload[firstField]
  if (Array.isArray(firstValue) && firstValue.length > 0) {
    return firstValue[0]
  }

  if (typeof firstValue === 'string') {
    return firstValue
  }

  return '请求失败，请稍后重试'
}

async function requestAuth(path, { method = 'GET', body, token = authState.token } = {}) {
  const headers = {
    Accept: 'application/json',
  }

  if (body) {
    headers['Content-Type'] = 'application/json'
  }

  if (token) {
    headers.Authorization = `Token ${token}`
  }

  const response = await fetch(`${AUTH_API_BASE}${path}`, {
    method,
    headers,
    body: body ? JSON.stringify(body) : undefined,
  })

  const text = await response.text()
  let payload = null
  if (text) {
    try {
      payload = JSON.parse(text)
    } catch {
      payload = text
    }
  }

  if (!response.ok) {
    const error = new Error(extractErrorMessage(payload))
    error.status = response.status
    error.payload = payload
    throw error
  }

  return payload
}

export async function registerUser(formData) {
  return requestAuth('/register/', {
    method: 'POST',
    body: formData,
    token: '',
  })
}

export async function loginUser(formData) {
  const payload = await requestAuth('/login/', {
    method: 'POST',
    body: formData,
    token: '',
  })

  writeStoredToken(payload.token)
  authState.user = payload.user
  return payload
}

export async function fetchCurrentUser() {
  const payload = await requestAuth('/me/')
  authState.user = payload
  return payload
}

export async function restoreSession(force = false) {
  if (!authState.token) {
    authState.user = null
    return null
  }

  if (authState.user && !force) {
    return authState.user
  }

  if (restorePromise && !force) {
    return restorePromise
  }

  restorePromise = (async () => {
    try {
      return await fetchCurrentUser()
    } catch (error) {
      clearAuthState()
      throw error
    } finally {
      restorePromise = null
    }
  })()

  return restorePromise
}

export async function logoutUser() {
  try {
    if (authState.token) {
      await requestAuth('/logout/', {
        method: 'POST',
      })
    }
  } finally {
    clearAuthState()
  }
}
