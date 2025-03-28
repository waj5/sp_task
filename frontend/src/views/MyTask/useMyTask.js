import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { fetchTasks, updateTaskStatus, deleteTask } from '@/api/auth'

export function useMyTask() {
  const router = useRouter()
  const tasks = ref([])
  const activeTaskId = ref(null)
  const deleting = ref(false)

  const loadTasks = async () => {
    try {
      const response = await fetchTasks()
      tasks.value = response || []
    } catch (error) {
      ElMessage.error("加载任务失败")
    }
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

  return {
    tasks,
    activeTaskId,
    deleting,
    loadTasks,
    markTaskComplete,
    deleteTaskHandler ,
    goBack
  }
}
