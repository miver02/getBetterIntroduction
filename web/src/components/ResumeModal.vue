<template>
  <el-dialog
    :model-value="visible"
    :title="`${resume?.name || 'None'}的简历详情`"
    width="80%"
    max-width="900px"
    @close="$emit('close')"
    top="5vh"
  >
    <div v-if="resume" class="modal-body">
      <!-- 基本信息部分 -->
      <el-card class="section-card" shadow="hover">
        <template #header>
          <div class="section-header">
            <el-icon><User /></el-icon>
            <span>基本信息</span>
          </div>
        </template>
        <el-descriptions :column="2" border size="small">
          <el-descriptions-item label="姓名">{{ resume.name || '未知' }}</el-descriptions-item>
          <el-descriptions-item label="性别">{{ resume.gender || '未知' }}</el-descriptions-item>
          <el-descriptions-item label="年龄">{{ resume.age || '未知' }}</el-descriptions-item>
          <el-descriptions-item label="工龄">{{ resume.work_years || '0' }}年</el-descriptions-item>
          <el-descriptions-item label="邮箱">{{ resume.email || '未知' }}</el-descriptions-item>
          <el-descriptions-item label="现居住地址">{{ resume.address || '未知' }}</el-descriptions-item>
        </el-descriptions>
      </el-card>

      <!-- 技术技能经历部分 -->
      <el-card class="section-card" shadow="hover">
        <template #header>
          <div class="section-header">
            <el-icon><Star /></el-icon>
            <span>技能</span>
          </div>
        </template>
        <el-space wrap>
          <el-tag 
            v-for="(skill, index) in (Array.isArray(resume.skills) ? resume.skills : [resume.skills])" 
            :key="index" 
            type="primary" 
            effect="dark"
          >
            {{ skill }}
          </el-tag>
        </el-space>
      </el-card>

      <!-- 工作经历部分 -->
      <el-card class="section-card" shadow="hover">
        <template #header>
          <div class="section-header">
            <el-icon><OfficeBuilding /></el-icon>
            <span>工作经历</span>
          </div>
        </template>
        <el-timeline>
          <el-timeline-item
            v-for="(experience, index) in (Array.isArray(resume.work_experience) ? resume.work_experience : [resume.work_experience])"
            :key="index"
            placement="top"
          >
            <el-card shadow="never" size="small">
              <p>{{ experience }}</p>
            </el-card>
          </el-timeline-item>
        </el-timeline>
      </el-card>

      <!-- 项目经历部分 -->
      <el-card class="section-card" shadow="hover">
        <template #header>
          <div class="section-header">
            <el-icon><Collection /></el-icon>
            <span>项目经历</span>
          </div>
        </template>
        <el-timeline>
          <el-timeline-item
            v-for="(project, index) in (Array.isArray(resume.project_experience) ? resume.project_experience : [resume.project_experience])"
            :key="index"
            placement="top"
          >
            <el-card shadow="never" size="small">
              <p>{{ project }}</p>
            </el-card>
          </el-timeline-item>
        </el-timeline>
      </el-card>

      <!-- 其他信息 -->
      <el-card class="section-card" shadow="hover" v-if="Object.keys(otherInfo).length > 0">
        <template #header>
          <div class="section-header">
            <el-icon><InfoFilled /></el-icon>
            <span>其他信息</span>
          </div>
        </template>
        <el-descriptions :column="1" border size="small">
          <el-descriptions-item 
            v-for="(value, key) in otherInfo" 
            :key="key" 
            :label="getFieldDisplayName(key)"
          >
            {{ value }}
          </el-descriptions-item>
        </el-descriptions>
      </el-card>
    </div>

    <template #footer>
      <span class="dialog-footer">
        <el-button @click="$emit('close')">关闭</el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script setup>
import { computed } from 'vue'
import { 
  User, 
  Star, 
  OfficeBuilding, 
  Collection, 
  InfoFilled 
} from '@element-plus/icons-vue'

const props = defineProps({
  resume: {
    type: Object,
    default: null,
  },
  visible: {
    type: Boolean,
    default: false,
  },
})

defineEmits(['close'])

// 字段映射
const fieldMapping = {
  education: '学历',
  university: '大学',
  degree_time: '毕业时间',
  competitions: '竞赛经历',
  self_introduction: '自我介绍',
}

// 获取其他信息（排除已显示的字段）
const otherInfo = computed(() => {
  if (!props.resume) return {}

  const excludedFields = [
    "education",
    "university",
    "degree_time",
    "competitions",
    "self_introduction",
  ]
  const result = {}

  for (const key in props.resume) {
    if (excludedFields.includes(key) && props.resume[key]) {
      result[key] = props.resume[key]
    }
  }

  return result
})

const getFieldDisplayName = key => {
  return fieldMapping[key] || key
}
</script>

<style scoped>
.section-card {
  margin-bottom: 20px;
}

.section-header {
  display: flex;
  align-items: center;
  font-size: 1.1rem;
  font-weight: 500;
  color: #409eff;
}

.section-header .el-icon {
  margin-right: 8px;
}

:deep(.el-card__header) {
  padding: 15px 20px;
  background-color: #f5f7fa;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
}
</style>