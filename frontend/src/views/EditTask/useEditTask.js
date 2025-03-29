import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { updateTaskDetail } from '@/api/auth'

export function useEditTask(emit) {
  const dialogVisible = ref(false)
  const form = ref({
    title: '',
    content: '',
    designee_name: '',
    status: '未完成'
  })
  const currentTaskId = ref(null)

  const openDialog = (task) => {
    currentTaskId.value = task.id
    form.value = {
      title: task.title,
      content: task.content,
      designee_name: task.designee_name,
      status: task.status
    }
    dialogVisible.value = true
  }

  const submitEdit = async () => {
    try {
      if (!form.value.designee_name.trim()) {
        ElMessage.warning('负责人不能为空')
        return
      }
      await updateTaskDetail(currentTaskId.value, form.value)
      ElMessage.success('任务修改成功')
      dialogVisible.value = false
      emit('task-updated')
    } catch (error) {
      console.error('完整错误信息:', error)
      ElMessage.error(error.message || '修改失败')
    }
  }

  return {
    dialogVisible,
    form,
    openDialog,
    submitEdit
  }
}
