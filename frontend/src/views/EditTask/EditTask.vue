<!-- views/EditTask/EditTask.vue -->
<script setup>
import { useEditTask } from './useEditTask'
import './EditTask.css'

const emit = defineEmits(['task-updated'])
const {
  dialogVisible,
  form,
  openDialog,
  submitEdit
} = useEditTask(emit)

defineExpose({ openDialog })
</script>

<template>
  <el-dialog
    v-model="dialogVisible"
    title="编辑任务"
    width="40%"
  >
    <el-form :model="form" label-width="80px">
      <el-form-item label="任务标题">
        <el-input v-model="form.title" />
      </el-form-item>
      <el-form-item label="任务内容">
        <el-input
          v-model="form.content"
          type="textarea"
          rows="4" />
      </el-form-item>
      <el-form-item label="负责人">
        <el-input v-model="form.designee_name" />
      </el-form-item>
      <el-form-item label="任务状态">
        <el-select v-model="form.status">
          <el-option
            v-for="status in ['未完成', '进行中', '已完成']"
            :key="status"
            :label="status"
            :value="status"
          />
        </el-select>
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="dialogVisible = false">取消</el-button>
      <el-button type="primary" @click="submitEdit">确认修改</el-button>
    </template>
  </el-dialog>
</template>
