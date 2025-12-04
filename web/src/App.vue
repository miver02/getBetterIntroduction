<!-- src/App.vue -->
<template>
  <div id="app">
    <header>
      <div class="header-container">
        <div class="logo">智能简历筛选系统</div>
      </div>
    </header>

    <main class="main-container">
      <!-- 左侧面板修改为表单 -->
      <aside class="left-panel">
        <h2 class="panel-title">筛选条件</h2>
        <ResumeForm />
      </aside>

      <!-- 右侧内容区 -->
      <section class="right-panel">
        <div class="search-bar">
          <input
            type="text"
            v-model="searchTerm"
            class="search-input"
            placeholder="搜索候选人姓名、技能或经历..."
          />
          <button @click="handleSearch" class="search-button">搜索</button>
        </div>

        <!-- 结果标题 -->
        <div class="result-header" v-if="jobTitle" style="margin-bottom: 1rem">
          <h2 style="font-size: 1.2rem; color: #333">
            搜索结果：<span>{{ jobTitle }}</span>
            <span style="font-size: 0.9rem; color: #666; margin-left: 10px">
              共 {{ resumeData.length }} 名候选人
            </span>
          </h2>
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
  // 搜索逻辑已经在计算属性中处理
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

.logo {
  font-size: 1.5rem;
  font-weight: bold;
  color: #2d5bff;
  text-align: center;
}

/* 主内容区域 */
.main-container {
  display: flex;
  max-width: 1400px;
  margin: 2rem auto;
  min-height: calc(100vh - 150px);
}

/* 左侧面板 */
.left-panel {
  flex: 1;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 0 15px rgba(0, 0, 0, 0.05);
  padding: 1.5rem;
  margin-right: 1.5rem;
  max-width: 300px;
  height: fit-content;
}

.panel-title {
  font-size: 1.2rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
  color: #333;
  display: flex;
  align-items: center;
}

.panel-title::before {
  content: '';
  display: inline-block;
  width: 4px;
  height: 20px;
  background-color: #2d5bff;
  margin-right: 10px;
  border-radius: 2px;
}

/* 右侧内容区 */
.right-panel {
  flex: 3;
  display: flex;
  flex-direction: column;
}

.search-bar {
  display: flex;
  margin-bottom: 1.5rem;
}

.search-input {
  flex: 1;
  padding: 12px 15px;
  border: 1px solid #e0e0e0;
  border-radius: 8px 0 0 8px;
  font-size: 1rem;
  outline: none;
  transition: border 0.3s;
}

.search-input:focus {
  border-color: #2d5bff;
}

.search-button {
  background-color: #2d5bff;
  color: white;
  border: none;
  padding: 0 20px;
  border-radius: 0 8px 8px 0;
  cursor: pointer;
  font-weight: 500;
  transition: background-color 0.3s;
}

.search-button:hover {
  background-color: #1a46e0;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .main-container {
    flex-direction: column;
  }

  .left-panel {
    max-width: 100%;
    margin-right: 0;
    margin-bottom: 1.5rem;
  }
}
</style>
