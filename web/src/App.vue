<!-- src/App.vue -->
<template>
  <div id="app">
    <header>
      <div class="header-container">
        <div class="logo">
          <el-text tag="b" size="large" type="primary">智能简历筛选系统</el-text>
        </div>
      </div>
    </header>

    <main class="main-container">
      <!-- 左侧面板修改为表单 -->
      <aside class="left-panel">
        <el-text tag="b" size="large">筛选条件</el-text>
        <ResumeForm />
      </aside>

      <!-- 右侧内容区 -->
      <section class="right-panel">
        <div class="search-bar">
          <el-input
            v-model="searchTerm"
            placeholder="搜索候选人姓名、技能或经历..."
            style="flex: 1"
          >
            <template #append>
              <el-button @click="handleSearch">
                <el-icon><Search /></el-icon>
                搜索
              </el-button>
            </template>
          </el-input>
        </div>

        <!-- 结果标题 -->
        <div class="result-header" v-if="jobTitle" style="margin-bottom: 1rem">
          <el-text tag="b" size="large">
            搜索结果：
            <el-tag type="primary">{{ jobTitle }}</el-tag>
            <el-text size="small" type="info" style="margin-left: 10px">
              共 {{ filteredResumes.length }} 名候选人
            </el-text>
          </el-text>
        </div>

        <!-- 结果列表 -->
        <ResumeList
          :resumes="filteredResumes"
          @view-detail="showResumeDetail"
        />

        <!-- 简历详情模态框 -->
        <ResumeModal
          :resume="selectedResume"
          :visible="isModalVisible"
          @close="isModalVisible = false"
        />
      </section>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, provide } from 'vue'
import { Search } from '@element-plus/icons-vue'
import ResumeForm from './components/ResumeForm.vue'
import ResumeList from './components/ResumeList.vue'
import ResumeModal from './components/ResumeModal.vue'

// 响应式数据
const resumeData = ref([])
const searchTerm = ref('')
const jobTitle = ref('')
const selectedResume = ref(null)
const isModalVisible = ref(false)

// 计算属性：过滤后的简历数据
const filteredResumes = computed(() => {
  if (!searchTerm.value) return resumeData.value

  const term = searchTerm.value.toLowerCase()
  return resumeData.value.filter(resume => {
    return (
      resume.name?.toLowerCase().includes(term) ||
      resume.skills?.toLowerCase().includes(term) ||
      resume.work_experience?.toLowerCase().includes(term)
    )
  })
})

// 搜索处理函数
const handleSearch = () => {
  // 触发重新计算 filteredResumes
  filteredResumes.value;
}

// 显示简历详情
const showResumeDetail = resume => {
  selectedResume.value = resume
  isModalVisible.value = true
}

// 提供给子组件的方法：更新简历数据
const updateResumeData = (data, title) => {
  resumeData.value = data
  jobTitle.value = title
}

// 将方法暴露给子组件使用
provide('parent', {
  updateResumeData,
})
</script>

<style>
/* 全局样式 - 从原index.html迁移 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif;
}

body {
  background-color: #f5f7fa;
  color: #333;
  line-height: 1.6;
}

/* 头部区域 */
header {
  background-color: #fff;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  padding: 1rem 2rem;
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-container {
  display: flex;
  justify-content: center;
  align-items: center;
  max-width: 1400px;
  margin: 0 auto;
}

/* 主内容区域 */
.main-container {
  display: flex;
  max-width: 1400px;
  margin: 2rem auto;
  min-height: calc(100vh - 150px);
  gap: 2rem;
}

/* 左侧面板 */
.left-panel {
  flex: 1;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 0 15px rgba(0, 0, 0, 0.05);
  padding: 1.5rem;
  margin-right: 1.5rem;
  max-width: 33%;
  height: fit-content;
  min-width: 240px;
}

/* 右侧内容区 */
.right-panel {
  flex: 3;
  display: flex;
  flex-direction: column;
  max-width: 67%;
  min-width: 480px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .main-container {
    flex-direction: column;
    gap: 1rem;
  }

  .left-panel {
    max-width: 100%;
    margin-right: 0;
    margin-bottom: 1.5rem;
  }

  .right-panel {
    max-width: 100%;
  }
}
</style>