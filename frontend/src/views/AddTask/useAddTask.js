import { reactive, ref } from 'vue'
import { ElMessage } from 'element-plus'
import { addTask } from '@/api/auth'

export function useAddTask(emit) {
  const dialogVisible = ref(false)
  const taskFormRef = ref(null)
  const isSubmitting = ref(false)

  const formData = reactive({
    title: '',
    content: '',
    designeeName: ''
  })

  const formRules = reactive({
    title: [
      { required: true, message: '请输入任务标题', trigger: 'blur' },
      { max: 50, message: '标题长度不能超过50个字符', trigger: 'blur' }
    ],
    content: [
      { required: true, message: '请输入任务内容', trigger: 'blur' },
      { max: 500, message: '内容长度不能超过500个字符', trigger: 'blur' }
    ],
    designeeName: [
      { required: true, message: '请输入负责人姓名', trigger: 'blur' }
    ]
  })

  const showDialog = () => {
    dialogVisible.value = true
  }

  const handleSubmit = async () => {
    try {
      isSubmitting.value = true
      await taskFormRef.value.validate()
      await addTask({
        title: formData.title,
        content: formData.content,
        designee_name: formData.designeeName
      })
      ElMessage.success('任务创建成功')
      dialogVisible.value = false
      resetForm()
      emit('task-added')
    } catch (error) {
      console.error('任务创建失败:', error)
      const errorMessage = error.response?.data?.message || '创建任务失败，请稍后重试'
      ElMessage.error(errorMessage)
    } finally {
      isSubmitting.value = false
    }
  }

  const resetForm = () => {
    if (taskFormRef.value) {
      taskFormRef.value.resetFields()
    }
  }

  const handleDialogClose = () => {
    resetForm()
  }

  return {
    dialogVisible,
    taskFormRef,
    formData,
    formRules,
    isSubmitting,
    showDialog,
    handleSubmit,
    handleDialogClose
  }
}
