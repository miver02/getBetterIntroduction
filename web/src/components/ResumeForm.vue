<!-- src/components/ResumeForm.vue -->
<template>
  <el-form class="job-form" @submit.prevent="handleSubmit" label-position="top">
    <el-form-item label="职位名称" required>
      <el-input
        v-model="formData.job"
        placeholder="例如：嵌入式应用开发工程师"
        clearable
      />
    </el-form-item>

    <el-form-item label="筛选条件" required>
      <el-input
        v-model="formData.select"
        placeholder="例如：1，十年经验；2，独立开发;"
        clearable
        type="textarea"
        :rows="3"
      />
    </el-form-item>

    <el-form-item label="上传简历文件" required>
      <el-upload
        ref="uploadRef"
        class="upload-wrapper"
        :auto-upload="false"
        multiple
        :on-change="handleFileChange"
        accept=".pdf"
      >
        <template #trigger>
          <el-button type="primary" class="">选择文件</el-button>
        </template>
        <el-button 
          type="success" 
          class="clear-btn"
          @click="clearFiles"
        >
          清空文件
        </el-button>
        <template #tip>
          <div class="el-upload__tip">
            可选择多个PDF文件同时上传
          </div>
        </template>
      </el-upload>
    </el-form-item>

    <el-button 
      type="primary" 
      native-type="submit" 
      :loading="loading"
      style="width: 100%; margin-top: 1rem;"
    >
      {{ loading ? '正在处理...' : '开始筛选' }}
    </el-button>
  </el-form>
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
const uploadRef = ref(null)

// 获取父组件方法
const parent = inject('parent')

// 文件选择处理
const handleFileChange = (file, fileList) => {
  files.value = fileList.map(f => f.raw)
}

// 清空文件
const clearFiles = () => {
  uploadRef.value.clearFiles()
  files.value = []
}

// 表单提交处理
const handleSubmit = async () => {
  if (!formData.value.job || !formData.value.select) {
    ElMessage.warning('请填写职位名称和筛选条件')
    return
  }

  if (files.value.length === 0) {
    ElMessage.warning('请至少上传一个简历文件')
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
      // 清空已上传的文件
      clearFiles()
    } else {
      throw new Error('无效的数据格式')
    }
  } catch (error) {
    console.error('Error:', error)
    ElMessage.error(`错误: ${error.message}`)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.job-form {
  width: 100%;
}

/* 控制上传区域按钮与列表布局，按钮可换行并随容器移动 */
.upload-wrapper {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 10px;
  justify-content: left;
}

/* 保证 tip 和文件列表占满整行，显示在按钮下方 */
.upload-wrapper .el-upload__tip {
  order: 2;
  width: 100%;
  margin-top: 2px;
  color: ragb(0,0,0,.45);
  text-align: left;
  margin-left: 8px;
}

.upload-wrapper .el-upload__list {
  order: 3;
  width: 100%;
  margin-top: 2px;
  text-align: left;
}

/* 如果需要更精确地控制文件项的对齐方式，可以添加以下样式 */
.upload-wrapper ::v-deep .el-upload-list {
  text-align: left;
}

.upload-wrapper ::v-deep .el-upload-list__item {
  justify-content: flex-start; /* 使文件项内容靠左对齐 */
}

/* 文件名过长处理：单行省略，防止溢出布局 */
.upload-wrapper ::v-deep .el-upload-list__item-name {
  display: flex;
  max-width: calc(100% - 20px); /* 保留图标/操作空间，按需调整 */
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  vertical-align: middle;
}

/* 在非常窄的屏幕上允许换行以便查看完整名称（可选） */
@media (max-width: 420px) {
  .upload-wrapper ::v-deep .el-upload-list__item-name {
    white-space: normal;
    word-break: break-word;
    max-width: 100%;
  }
}
</style>