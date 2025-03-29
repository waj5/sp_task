<!-- views/AddTask/AddTask.vue -->
<script setup>
import { useAddTask } from './useAddTask'
import './AddTask.css'

const emit = defineEmits(['task-added'])
const {
  dialogVisible,
  taskFormRef,
  formData,
  formRules,
  isSubmitting,
  showDialog,
  handleSubmit,
  handleDialogClose
} = useAddTask(emit)

defineExpose({ showDialog })
</script>

<template>
  <el-dialog
    v-model="dialogVisible"
    title="添加任务"
    width="40%"
    @closed="handleDialogClose"
  >
    <el-form :model="formData" :rules="formRules" ref="taskFormRef">
      <el-form-item label="任务标题" prop="title">
        <el-input v-model="formData.title" />
      </el-form-item>
      <el-form-item label="任务内容" prop="content">
        <el-input
          v-model="formData.content"
          type="textarea"
          rows="4" />
      </el-form-item>
      <el-form-item label="负责人" prop="designeeName">
        <el-input v-model="formData.designeeName" />
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="dialogVisible = false">取消</el-button>
      <el-button
        type="primary"
        @click="handleSubmit"
        :loading="isSubmitting">
        确认添加
      </el-button>
    </template>
  </el-dialog>
</template>
