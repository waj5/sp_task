<template>
  <el-dialog
    v-model="dialogVisible"
    title="创建新任务"
    width="30%"
    @closed="handleDialogClose"
  >
    <el-form
      ref="taskFormRef"
      :model="formData"
      :rules="formRules"
      label-width="100px"
      status-icon
    >
      <el-form-item label="任务标题:" prop="title">
        <el-input
          v-model.trim="formData.title"
          placeholder="请输入任务标题"
          clearable
        />
      </el-form-item>

      <el-form-item label="任务内容:" prop="content">
        <el-input
          v-model.trim="formData.content"
          type="textarea"
          :rows="4"
          placeholder="请输入详细任务描述"
          resize="none"
        />
      </el-form-item>

      <el-form-item label="负责人ID:" prop="designeeId">
        <el-input-number
          v-model="formData.designeeId"
          :min="1"
          controls-position="right"
          placeholder="请输入负责人ID"
        />
      </el-form-item>
    </el-form>

    <template #footer>
      <span class="dialog-footer">
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button
          type="primary"
          :loading="isSubmitting"
          @click="handleSubmit"
        >
          确认创建
        </el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, reactive } from 'vue';
import { addTask } from '@/api/auth';
import { ElMessage } from 'element-plus';

const emit = defineEmits(['task-added']);

// 对话框显示状态
const dialogVisible = ref(false);

// 表单相关
const taskFormRef = ref(null);
const isSubmitting = ref(false);
const formData = reactive({
  title: '',
  content: '',
  designeeId: null
});

// 验证规则
const formRules = {
  title: [
    { required: true, message: '请输入任务标题', trigger: 'blur' },
    { max: 50, message: '标题长度不能超过50个字符', trigger: 'blur' }
  ],
  content: [
    { required: true, message: '请输入任务内容', trigger: 'blur' },
    { max: 500, message: '内容长度不能超过500个字符', trigger: 'blur' }
  ],
  designeeId: [
    { required: true, message: '请选择负责人', trigger: 'blur' },
    { type: 'number', message: '必须为有效数字', trigger: 'blur' }
  ]
};

// 暴露给父组件的方法
const showDialog = () => {
  dialogVisible.value = true;
};

// 提交处理
const handleSubmit = async () => {
  try {
    isSubmitting.value = true;

    // 表单验证
    await taskFormRef.value.validate();

    // 提交数据
    await addTask({
      title: formData.title,
      content: formData.content,
      designee_id: formData.designeeId
    });

    ElMessage.success('任务创建成功');
    dialogVisible.value = false;
    emit('task-added');  // 通知父组件刷新
  } catch (error) {
    console.error('任务创建失败:', error);
    const errorMessage = error.response?.data?.message || '创建任务失败，请稍后重试';
    ElMessage.error(errorMessage);
  } finally {
    isSubmitting.value = false;
  }
};

// 关闭对话框处理
const handleDialogClose = () => {
  taskFormRef.value?.resetFields();
};

// 暴露方法给父组件
defineExpose({
  showDialog
});
</script>

<style scoped>
.el-input-number {
  width: 100%;
}

:deep(.el-dialog__body) {
  padding: 20px 30px;
}
</style>
