import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { fetchTasks, updateTaskStatus, deleteTask } from '@/api/auth'

export function useMyTask() {
  const router = useRouter()
  const tasks = ref([])
  const activeTaskId = ref(null)
  const deleting = ref(false)
  const editTaskRef = ref(null)
  const addTaskRef = ref(null)
  const dialogVisible = ref(false)
  const selectedTask = ref(null)
  const createDialogVisible = ref(false)
  const newTask = ref({
    title: '',
    content: '',
    designee_name: ''
  })

  // 背景图片样式
  const myTaskStyle = computed(() => {
    const bgImage = `url('${import.meta.env.VITE_HOME_BG_IMAGE}')`
    console.log('Background image URL:', bgImage)
    return {
      '--home-bg-image': bgImage
    }
  })

  const loadTasks = async () => {
    try {
      const response = await fetchTasks()
      tasks.value = response || []
    } catch (error) {
      ElMessage.error("加载任务失败")
    }
  }

  const showTaskDetails = (task) => {
    selectedTask.value = task
    dialogVisible.value = true
  }

  const completeTask = async (task) => {
    try {
      await updateTaskStatus(task.id)
      ElMessage.success("任务已完成")
      dialogVisible.value = false
      await loadTasks()
    } catch (error) {
      ElMessage.error("操作失败")
    }
  }

  const createTask = async () => {
    if (!newTask.value.title || !newTask.value.content || !newTask.value.designee_name) {
      ElMessage.warning("请填写完整信息")
      return
    }
    try {
      // 这里需要调用创建任务的API
      ElMessage.success("创建成功")
      createDialogVisible.value = false
      await loadTasks()
      // 重置表单
      newTask.value = {
        title: '',
        content: '',
        designee_name: ''
      }
    } catch (error) {
      ElMessage.error("创建失败")
    }
  }

  const showCreateTaskDialog = () => {
    createDialogVisible.value = true
  }

  const markTaskComplete = async (task) => {
    try {
      await updateTaskStatus(task.id)
      ElMessage.success("任务已标记完成")
      await loadTasks()
    } catch (error) {
      ElMessage.error(error.message || "操作失败")
      console.error("标记完成错误:", error)
    }
  }

  const deleteTaskHandler = async (task) => {
    try {
      const confirm = await ElMessageBox.confirm('确认删除？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      })

      if (confirm !== 'confirm') return

      await deleteTask(task.id)
      ElMessage.success("删除成功")
      await loadTasks()
    } catch (error) {
      console.error('完整错误对象:', error)
      if (error.code === 'ECONNABORTED') {
        ElMessage.error('请求超时，请检查网络')
      } else if (error.response) {
        ElMessage.error(`后端错误: ${error.response.data.detail}`)
      } else if (error.request) {
        console.log('请求已发出但无响应:', error.request)
        ElMessage.error('服务器无响应')
      } else {
        ElMessage.error('请求配置错误')
      }
    }
  }

  const goBack = () => {
    router.push({ name: "Home" })
  }

  const handleMenuSelect = (index) => {
    if (index === '1') {
      addTaskRef.value.showDialog()
    }
  }

  const openEditDialog = (task) => {
    editTaskRef.value.openDialog(task)
  }

  const goToHome = () => {
    router.push('/')
  }

  const logout = () => {
    // 清除用户信息
    localStorage.removeItem('token')
    localStorage.removeItem('userInfo')
    // 跳转到登录页
    router.push('/login')
  }

  return {
    tasks,
    activeTaskId,
    deleting,
    editTaskRef,
    addTaskRef,
    myTaskStyle,
    loadTasks,
    markTaskComplete,
    deleteTaskHandler,
    goBack,
    handleMenuSelect,
    openEditDialog,
    goToHome,
    logout,
    dialogVisible,
    selectedTask,
    createDialogVisible,
    newTask,
    showTaskDetails,
    createTask,
    completeTask,
    showCreateTaskDialog
  }
}
