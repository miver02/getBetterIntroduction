<template>
  <div class="resume-list">
    <el-empty
      v-if="resumes.length === 0"
      description="未找到符合条件的简历，请调整搜索关键词"
      :image-size="200"
    />

    <el-table
      v-else
      :data="resumes"
      style="width: 100%"
      stripe
      border
    >
      <el-table-column
        prop="rank"
        label="排名"
        width="80"
        align="center"
      >
        <template #default="scope">
          {{ scope.$index + 1 }}
        </template>
      </el-table-column>
      
      <el-table-column
        prop="name"
        label="姓名"
        width="120"
      >
        <template #default="scope">
          {{ scope.row.name || 'None' }}
        </template>
      </el-table-column>
      
      <el-table-column
        prop="age"
        label="年龄"
        width="80"
      >
        <template #default="scope">
          {{ scope.row.age || 'None' }}
        </template>
      </el-table-column>
      
      <el-table-column
        prop="major"
        label="专业"
        width="150"
      >
        <template #default="scope">
          {{ scope.row.major || 'None' }}
        </template>
      </el-table-column>
      
      <el-table-column
        prop="phone"
        label="手机号"
        width="150"
      >
        <template #default="scope">
          {{ scope.row.phone || 'None' }}
        </template>
      </el-table-column>
      
      <el-table-column
        prop="match"
        label="契合度"
        width="150"
        align="center"
      >
        <template #default="scope">
          <div class="rating">
            <span
              v-for="star in 5"
              :key="star"
              class="star"
              :style="{
                color: star <= getStarCount(scope.$index) ? '#ffce54' : '#ddd',
              }"
            >
              {{ star <= getStarCount(scope.$index) ? '★' : '☆' }}
            </span>
          </div>
        </template>
      </el-table-column>
      
      <el-table-column
        label="详情"
        width="120"
        align="center"
      >
        <template #default="scope">
          <el-button
            type="primary"
            link
            @click="$emit('view-detail', scope.row)"
          >
            查看详情
          </el-button>
        </template>
      </el-table-column>
    </el-table>
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
  const total = props.resumes.length
  if (total === 0) return 0
  return 5 - Math.floor((index / total) * 5)
}
</script>

<style scoped>
.rating {
  display: flex;
  justify-content: center;
  gap: 2px;
}
</style>