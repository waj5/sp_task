import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { fetchTasks, updateTaskStatus, deleteTask, addTask, updateTaskDetail } from '@/api/auth'

export function useMyTask() {
  const router = useRouter()
  const tasks = ref([])
  const activeTaskId = ref(null)
  const deleting = ref(false)
  const addTaskRef = ref(null)
  const dialogVisible = ref(false)
  const selectedTask = ref(null)
  const createDialogVisible = ref(false)
  const isEditing = ref(false)
  const editingTask = ref(null)
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

  // 检查是否有删除权限
  const canDeleteTask = (task) => {
    // 获取当前用户信息
    const userInfo = JSON.parse(localStorage.getItem('userInfo') || '{}')
    // 只有任务创建者或管理员可以删除任务
    return userInfo.role === 'admin' || task.creator_id === userInfo.id
  }

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
    isEditing.value = false
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
      const taskData = {
        title: newTask.value.title,
        content: newTask.value.content,
        designee_name: newTask.value.designee_name
      }
      await addTask(taskData)
      ElMessage.success('任务创建成功')
      createDialogVisible.value = false
      await loadTasks()
      // 重置表单
      newTask.value = {
        title: '',
        content: '',
        designee_name: ''
      }
    } catch (error) {
      console.error('创建任务失败:', error)
      if (error.response) {
        ElMessage.error(`创建失败: ${error.response.data.detail || '未知错误'}`)
      } else {
        ElMessage.error("创建失败，请重试")
      }
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
      // 关闭对话框
      dialogVisible.value = false
      // 刷新任务列表
      await loadTasks()
    } catch (error) {
      console.error('完整错误对象:', error)
      // 直接显示错误消息
      ElMessage.error(error.message || '删除失败')
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
    if (editTaskRef.value) {
      editTaskRef.value.openDialog(task)
    } else {
      console.error('EditTask component reference is not available')
    }
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

  const startEdit = () => {
    isEditing.value = true
    editingTask.value = { ...selectedTask.value }
  }

  const cancelEdit = () => {
    isEditing.value = false
    editingTask.value = null
  }

  const saveTask = async () => {
    try {
      // 如果状态变为已完成，添加完成时间
      if (editingTask.value.status === '已完成' && selectedTask.value.status !== '已完成') {
        editingTask.value.complete_time = new Date().toISOString()
      }
      // 如果状态从已完成变为进行中，清除完成时间
      if (editingTask.value.status === '进行中' && selectedTask.value.status === '已完成') {
        editingTask.value.complete_time = null
      }
      
      // 确保发送所有必要的字段
      const taskData = {
        title: editingTask.value.title,
        content: editingTask.value.content,
        designee_name: editingTask.value.designee_name,
        status: editingTask.value.status,
        complete_time: editingTask.value.complete_time
      }
      
      console.log('更新任务数据:', taskData) // 添加日志
      const response = await updateTaskDetail(editingTask.value.id, taskData)
      console.log('更新响应:', response) // 添加日志
      
      // 确保使用后端返回的状态
      if (response.status) {
        editingTask.value.status = response.status
      }
      
      ElMessage.success("任务更新成功")
      isEditing.value = false
      await loadTasks()
      // 更新当前选中的任务
      selectedTask.value = editingTask.value
    } catch (error) {
      console.error("更新任务错误:", error)
      ElMessage.error(error.message || "更新失败")
    }
  }

  return {
    tasks,
    activeTaskId,
    deleting,
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
    showCreateTaskDialog,
    isEditing,
    editingTask,
    startEdit,
    cancelEdit,
    saveTask,
    canDeleteTask
  }
}
