<!-- src/components/ResumeForm.vue -->
<template>
  <form class="job-form" @submit.prevent="handleSubmit">
    <div class="form-group">
      <label class="form-label" for="job">职位名称</label>
      <input
        type="text"
        id="job"
        v-model="formData.job"
        class="form-control"
        placeholder="例如：嵌入式应用开发工程师"
        required
      />
    </div>

    <div class="form-group">
      <label class="form-label" for="select">筛选条件</label>
      <input
        type="text"
        id="select"
        v-model="formData.select"
        class="form-control"
        placeholder="例如：1，十年经验；2，独立开发;"
        required
      />
    </div>

    <div class="form-group">
      <label class="form-label" for="files">上传简历文件</label>
      <input
        type="file"
        id="files"
        @change="handleFileChange"
        class="form-control"
        multiple
        accept=".pdf"
        style="padding: 8px"
      />
      <small style="color: #888; font-size: 0.8rem"
        >可选择多个PDF文件同时上传</small
      >
    </div>

    <button type="submit" class="submit-btn" :disabled="loading">
      {{ loading ? '正在处理...' : '开始筛选' }}
    </button>
  </form>
</template>

<script setup>
import { ref, inject } from 'vue'

const emit = defineEmits(['upload-success'])

// 表单数据
const formData = ref({
  job: '',
  select: '',
})

const files = ref([])
const loading = ref(false)

// 获取父组件方法
const parent = inject('parent')

// 文件选择处理
const handleFileChange = event => {
  files.value = Array.from(event.target.files)
}

// 表单提交处理
const handleSubmit = async () => {
  if (!formData.value.job || !formData.value.select) {
    alert('请填写职位名称和筛选条件')
    return
  }

  loading.value = true

  try {
    const formDataObj = new FormData()
    formDataObj.append('job', formData.value.job)
    formDataObj.append('select', formData.value.select)

    files.value.forEach(file => {
      formDataObj.append('files', file)
    })

    const response = await fetch('/api/models/get_rank', {
      method: 'POST',
      body: formDataObj,
    })

    if (!response.ok) {
      throw new Error('网络请求失败')
    }

    const data = await response.json()

    if (data && data.data && Array.isArray(data.data)) {
      // 添加保护性检查
      if (parent && typeof parent.updateResumeData === 'function') {
        parent.updateResumeData(data.data, formData.value.job)
      } else {
        console.warn('Parent component did not provide updateResumeData method')
      }
      emit('upload-success', data.data)
    } else {
      throw new Error('无效的数据格式')
    }
  } catch (error) {
    console.error('Error:', error)
    alert(`错误: ${error.message}`)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
/* 表单样式 */
.job-form {
  width: 100%;
}

.form-group {
  margin-bottom: 1.2rem;
}

.form-label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #555;
}

.form-control {
  width: 100%;
  padding: 10px;
  border: 1px solid #e0e0e0;
  border-radius: 6px;
  font-size: 0.9rem;
  transition: border-color 0.3s;
}

.form-control:focus {
  border-color: #2d5bff;
  outline: none;
}

.submit-btn {
  width: 100%;
  background-color: #2d5bff;
  color: white;
  border: none;
  padding: 12px;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
  margin-top: 1rem;
  transition: background-color 0.3s;
}

.submit-btn:hover:not(:disabled) {
  background-color: #1a46e0;
}

.submit-btn:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}
</style>
