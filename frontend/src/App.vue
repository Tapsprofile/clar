<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'

type Garment = {
  id: string
  name: string
  imageUrl: string
  wooProductId?: string | null
}

type TryOnResponse = {
  jobId: string
  resultUrl: string
}

const API_BASE = (import.meta.env.VITE_API_BASE_URL as string | undefined) ?? ''

function apiUrl(path: string) {
  if (!API_BASE) return path
  return `${API_BASE.replace(/\/$/, '')}${path.startsWith('/') ? path : `/${path}`}`
}

const garments = ref<Garment[]>([])
const selectedGarmentId = ref<string>('')

const personFile = ref<File | null>(null)
const dressFile = ref<File | null>(null)

const personPreviewUrl = ref<string>('')
const dressPreviewUrl = ref<string>('')

const isLoading = ref(false)
const errorMessage = ref<string>('')
const result = ref<TryOnResponse | null>(null)

const selectedGarment = computed(() => garments.value.find((g) => g.id === selectedGarmentId.value))

async function loadGarments() {
  try {
    const resp = await fetch(apiUrl('/api/garments'))
    if (!resp.ok) throw new Error(`Failed to load garments (${resp.status})`)
    garments.value = (await resp.json()) as Garment[]
    const first = garments.value[0]
    if (first) selectedGarmentId.value = first.id
  } catch (e) {
    // Garment list is optional; the tool still works with direct dress upload.
    garments.value = []
  }
}

function onPickPerson(e: Event) {
  const input = e.target as HTMLInputElement
  const file = input.files?.[0] ?? null
  personFile.value = file
  personPreviewUrl.value = file ? URL.createObjectURL(file) : ''
  result.value = null
}

function onPickDress(e: Event) {
  const input = e.target as HTMLInputElement
  const file = input.files?.[0] ?? null
  dressFile.value = file
  dressPreviewUrl.value = file ? URL.createObjectURL(file) : ''
  result.value = null
}

async function generateTryOn() {
  errorMessage.value = ''
  result.value = null

  if (!personFile.value) {
    errorMessage.value = 'Please upload a person photo.'
    return
  }

  // If a dress file is not provided, we fall back to selected garment image URL.
  // The backend MVP expects a dress upload; if you want URL support, we can add it next.
  if (!dressFile.value) {
    errorMessage.value = 'Please upload a dress image (this MVP currently requires a dress file).'
    return
  }

  isLoading.value = true
  try {
    const form = new FormData()
    form.append('personImage', personFile.value)
    form.append('dressImage', dressFile.value)

    const resp = await fetch(apiUrl('/api/tryon'), { method: 'POST', body: form })
    const body = await resp.json().catch(() => ({}))
    if (!resp.ok) {
      throw new Error((body as any)?.error ?? (body as any)?.detail ?? `Request failed (${resp.status})`)
    }
    result.value = body as TryOnResponse
  } catch (e: any) {
    errorMessage.value = e?.message ?? 'Try-on failed.'
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  loadGarments()
})
</script>

<template>
  <div class="page">
    <header class="topbar">
      <div class="brand">
        <div class="brand__title">Virtual Dress Try‑On</div>
        <div class="brand__subtitle">Upload your photo + a dress image to preview the look.</div>
      </div>

      <div class="env">
        <span class="env__label">API</span>
        <code class="env__value">{{ API_BASE || 'same-origin (/api/*)' }}</code>
      </div>
    </header>

    <main class="grid">
      <section class="card">
        <h2 class="card__title">1) Choose a dress</h2>

        <div v-if="garments.length" class="row">
          <label class="field">
            <span class="field__label">From list (optional)</span>
            <select v-model="selectedGarmentId" class="input">
              <option v-for="g in garments" :key="g.id" :value="g.id">
                {{ g.name }}
              </option>
            </select>
          </label>
          <div class="preview">
            <img v-if="selectedGarment?.imageUrl" class="preview__img" :src="selectedGarment.imageUrl" alt="Selected dress" />
            <div v-else class="preview__placeholder">No preview</div>
          </div>
        </div>

        <div class="row">
          <label class="field">
            <span class="field__label">Upload dress image (required for MVP)</span>
            <input class="input" type="file" accept="image/*" @change="onPickDress" />
          </label>

          <div class="preview">
            <img v-if="dressPreviewUrl" class="preview__img" :src="dressPreviewUrl" alt="Dress preview" />
            <div v-else class="preview__placeholder">Dress preview</div>
          </div>
        </div>
      </section>

      <section class="card">
        <h2 class="card__title">2) Upload your photo</h2>

        <div class="row">
          <label class="field">
            <span class="field__label">Person image</span>
            <input class="input" type="file" accept="image/*" @change="onPickPerson" />
          </label>

          <div class="preview">
            <img v-if="personPreviewUrl" class="preview__img" :src="personPreviewUrl" alt="Person preview" />
            <div v-else class="preview__placeholder">Person preview</div>
          </div>
        </div>
      </section>

      <section class="card card--full">
        <h2 class="card__title">3) Generate try‑on</h2>

        <div class="actions">
          <button class="btn" type="button" :disabled="isLoading" @click="generateTryOn">
            {{ isLoading ? 'Generating…' : 'Generate Preview' }}
          </button>

          <div v-if="errorMessage" class="alert alert--error">{{ errorMessage }}</div>
        </div>

        <div v-if="result" class="result">
          <div class="result__meta">
            <div><strong>Job</strong>: <code>{{ result.jobId }}</code></div>
            <div><strong>Result URL</strong>: <a :href="result.resultUrl" target="_blank" rel="noreferrer">{{ result.resultUrl }}</a></div>
          </div>
          <img class="result__img" :src="result.resultUrl" alt="Try-on result" />
        </div>

        <div v-else class="hint">
          The backend will return a URL to the rendered image. If you haven’t started the backend yet, set
          <code>VITE_API_BASE_URL</code> in <code>frontend/.env</code>.
        </div>
      </section>
    </main>
  </div>
</template>
