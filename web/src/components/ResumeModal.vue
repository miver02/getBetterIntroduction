<!-- src/components/ResumeModal.vue -->
<template>
  <div 
    v-if="visible" 
    class="resume-modal" 
    @click.self="$emit('close')"
  >
    <div class="modal-content">
      <button class="close-button" @click="$emit('close')">×</button>
      <h2 class="modal-title">{{ resume?.name || 'None' }}的简历详情</h2>
      
      <div v-if="resume" class="modal-body">
        <!-- 基本信息部分 -->
        <div class="section">
          <h3 class="section-title">基本信息</h3>
          <table class="info-table">
            <tbody>
                <tr>
                <td class="label">Name</td>
                <td>{{ resume.name || 'None' }}</td>
                <td class="label">Gender</td>
                <td>{{ resume.gender || 'None' }}</td>
                </tr>
                <tr>
                <td class="label">Age</td>
                <td>{{ resume.age || 'None' }}</td>
                <td class="label">WorkYears</td>
                <td>{{ resume.work_years || 'None' }}</td>
                </tr>
            </tbody>
          </table>
        </div>
        
        <!-- 工作经历部分 -->
        <div class="section">
          <h3 class="section-title">WorkExperience</h3>
          <div class="content-block">{{ resume.work_experience || 'No WorkExperience' }}</div>
        </div>
        
        <!-- 项目经历部分 -->
        <div class="section">
          <h3 class="section-title">ProjectExperience</h3>
          <div class="content-block">{{ resume.project_experience || 'No ProjectExperience' }}</div>
        </div>
        
        <!-- 其他信息 -->
        <div class="section">
          <h3 class="section-title">Other</h3>
          <table class="info-table">
            <tr v-for="(value, key) in otherInfo" :key="key">
              <td class="label">{{ getFieldDisplayName(key) }}</td>
              <td>{{ value }}</td>
            </tr>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  resume: {
    type: Object,
    default: null
  },
  visible: {
    type: Boolean,
    default: false
  }
})

defineEmits(['close'])

// 字段映射
const fieldMapping = {
  'name': 'Name',
  'gender': 'Gender',
  'age': 'Age',
  'work_years': 'WorkYears',
  'work_experience': 'WorkExperience',
  'project_experience': 'ProjectExperience',
  'education': 'Education',
  'skills': 'Skills',
  'certifications': 'Certifications',
  'languages': 'Languages',
  'email': 'Email',
  'phone': 'Phone'
}

// 获取其他信息（排除已显示的字段）
const otherInfo = computed(() => {
  if (!props.resume) return {}
  
  const excludedFields = ['name', 'gender', 'age', 'work_years', 'work_experience', 'project_experience']
  const result = {}
  
  for (const key in props.resume) {
    if (!excludedFields.includes(key)) {
      result[key] = props.resume[key]
    }
  }
  
  return result
})

const getFieldDisplayName = (key) => {
  return fieldMapping[key] || key
}
</script>

<style scoped>
.resume-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 1000;
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  position: relative;
  width: 80%;
  max-width: 800px;
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  max-height: 80vh;
  overflow-y: auto;
}

.close-button {
  position: absolute;
  right: 15px;
  top: 15px;
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
}

.modal-title {
  margin-bottom: 15px;
  padding-bottom: 15px;
  border-bottom: 1px solid #eee;
}

.section {
  margin-bottom: 20px;
}

.section-title {
  font-size: 1.1rem;
  margin-bottom: 10px;
}

.info-table {
  width: 100%;
  border-collapse: collapse;
}

.info-table td {
  padding: 8px;
  border-bottom: 1px solid #eee;
}

.info-table .label {
  width: 100px;
  font-weight: 500;
}

.content-block {
  padding: 10px;
  background-color: #f9f9f9;
  border-radius: 4px;
}
</style>