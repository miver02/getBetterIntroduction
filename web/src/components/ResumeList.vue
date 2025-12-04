<!-- src/components/ResumeList.vue -->
<template>
  <div class="resume-list">
    <p
      v-if="resumes.length === 0"
      style="text-align: center; color: #666; padding: 2rem"
    >
      请在左侧输入职位名称并上传简历文件开始筛选
    </p>

    <table
      v-else
      style="width: 100%; border-collapse: collapse; margin-bottom: 2rem"
    >
      <thead>
        <tr style="background-color: #f5f7fa; text-align: left">
          <th style="padding: 12px 15px; border-bottom: 1px solid #e0e0e0">
            排名
          </th>
          <th style="padding: 12px 15px; border-bottom: 1px solid #e0e0e0">
            姓名
          </th>
          <th style="padding: 12px 15px; border-bottom: 1px solid #e0e0e0">
            年龄
          </th>
          <th style="padding: 12px 15px; border-bottom: 1px solid #e0e0e0">
            工龄
          </th>
          <th
            style="
              padding: 12px 15px;
              border-bottom: 1px solid #e0e0e0;
              text-align: center;
            "
          >
            契合度
          </th>
          <th
            style="
              padding: 12px 15px;
              border-bottom: 1px solid #e0e0e0;
              text-align: center;
            "
          >
            详情
          </th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="(resume, index) in resumes" :key="index">
          <td style="padding: 12px 15px; border-bottom: 1px solid #f0f0f0">
            {{ index + 1 }}
          </td>
          <td style="padding: 12px 15px; border-bottom: 1px solid #f0f0f0">
            {{ resume.name || 'None' }}
          </td>
          <td style="padding: 12px 15px; border-bottom: 1px solid #f0f0f0">
            {{ resume.age || 'None' }}
          </td>
          <td style="padding: 12px 15px; border-bottom: 1px solid #f0f0f0">
            {{ resume.work_years || 'None' }}
          </td>
          <td
            style="
              padding: 12px 15px;
              border-bottom: 1px solid #f0f0f0;
              text-align: center;
            "
          >
            <div class="rating">
              <span
                v-for="star in getStars(index)"
                :key="star"
                class="star"
                :style="{
                  color: star <= getStarCount(index) ? '#ffce54' : '#ddd',
                }"
              >
                {{ star <= getStarCount(index) ? '★' : '☆' }}
              </span>
            </div>
          </td>
          <td
            style="
              padding: 12px 15px;
              border-bottom: 1px solid #f0f0f0;
              text-align: center;
            "
          >
            <button class="view-button" @click="$emit('view-detail', resume)">
              查看详情
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
const props = defineProps({
  resumes: {
    type: Array,
    default: () => [],
  },
})

defineEmits(['view-detail'])

const getStarCount = index => {
  // 假设有5个等级，根据排名计算星级
  const total = props.resumes.length
  if (total === 0) return 0
  return 5 - Math.floor((index / total) * 5)
}

const getStars = index => {
  return Array.from({ length: 5 }, (_, i) => i + 1)
}
</script>

<style scoped>
.view-button {
  background-color: transparent;
  color: #2d5bff;
  border: 1px solid #2d5bff;
  padding: 5px 10px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.8rem;
  transition: all 0.3s;
}

.view-button:hover {
  background-color: #2d5bff;
  color: white;
}
</style>
