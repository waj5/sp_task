import { updateTaskDetail } from '@/api/auth.js';
import { ElMessage } from 'element-plus';

export default {
  name: 'EditTask',
  data() {
    return {
      dialogVisible: false,
      form: {
        title: '',
        content: '',
        designee_name: '',
        status: '未完成'
      },
      currentTaskId: null
    };
  },
  methods: {
    openDialog(task) {
      this.currentTaskId = task.id;
      this.form = {
        title: task.title,
        content: task.content,
        designee_name: task.designee_name,
        status: task.status
      };
      this.dialogVisible = true;
    },
    async submitEdit() {
      try {
        // 添加空值检查
        if (!this.form.designee_name.trim()) {
          ElMessage.warning('负责人不能为空');
          return;
        }

        await updateTaskDetail(this.currentTaskId, this.form);
        ElMessage.success('任务修改成功');
        this.$emit('task-updated');
        this.dialogVisible = false;
      } catch (error) {
        console.error('完整错误信息:', error);
        ElMessage.error(error.message || '修改失败');
      }
    }
  }
};
