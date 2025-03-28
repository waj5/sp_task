<script setup>
import { ref } from 'vue';
import { updateTaskDetail } from '@/api/auth.js';
import { ElMessage } from 'element-plus';

// 定义 emit
const emit = defineEmits(['task-updated']);

const dialogVisible = ref(false);
const form = ref({
  title: '',
  content: '',
  designee_name: '',
  status: '未完成'
});
const currentTaskId = ref(null);

const openDialog = (task) => {
  currentTaskId.value = task.id;
  form.value = {
    title: task.title,
    content: task.content,
    designee_name: task.designee_name,
    status: task.status
  };
  dialogVisible.value = true;
};

const submitEdit = async () => {
  try {
    if (!form.value.designee_name.trim()) {
      ElMessage.warning('负责人不能为空');
      return;
    }
    await updateTaskDetail(currentTaskId.value, form.value);
    ElMessage.success('任务修改成功');
    emit('task-updated'); // 触发事件
    dialogVisible.value = false;
  } catch (error) {
    console.error('完整错误信息:', error);
    ElMessage.error(error.message || '修改失败');
  }
};

defineExpose({ openDialog }); // 暴露 openDialog 方法
</script>

<template>
  <el-dialog
    v-model="dialogVisible"
    title="编辑任务"
    width="40%">
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
