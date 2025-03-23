from fastapi import APIRouter, Depends, HTTPException, status
from backend.utils import get_current_user
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from backend.database import query_tasks_by_user_or_designee, get_designees_by_task, update_task, delete_task, query_tasks_fuzzy,get_user_id_by_name

router = APIRouter(prefix="/auth", tags=["tasks"])

class TaskCreate(BaseModel):
    title: str  # 任务标题
    content: str  # 任务内容
    designee_name: str  # 被指派者的姓名
    complete_time: Optional[datetime] = None  # 完成时间（可选）

class TaskUpdate(BaseModel):
    title: Optional[str] = None  # 任务标题（可选）
    content: Optional[str] = None  # 任务内容（可选）
    status: Optional[str] = None
    designee_name: Optional[str] = None
    complete_time: Optional[datetime] = None  # 完成时间（可选）



@router.get("/tasks")
async def get_tasks(current_user_id: str = Depends(get_current_user)):
    tasks = await query_tasks_by_user_or_designee(current_user_id, current_user_id)
    return {
        "tasks": [
            {
                "id": task.id,
                "title": task.title,
                "content": task.content,
                "status": task.status,
                "create_time": task.create_time.isoformat(),
                "complete_time": task.update_time.isoformat() if task.update_time else None,
                "creator_name": (await task.creator).name,  # 获取创建人姓名
                "designee_name": (await task.designee).name  # 获取负责人姓名
            }
            for task in tasks
        ]
    }

@router.post("/tasks", status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: TaskCreate,  # 任务创建请求体
    current_user_id: str = Depends(get_current_user)  # 当前用户 ID
):
    # 创建任务
    tasks = await get_designees_by_task(task_data, current_user_id)
    print("任务内容：", tasks)
    # 返回成功响应
    # return {
    #     "tasks": [{
    #         "id": task.id,
    #         "title": task.title,
    #         "content": task.content,
    #         "creator_name": task.creator.name,  # 确保关联查询了creator
    #         "designee_name": task.designee.name,  # 确保关联查询了designee
    #         "create_time": task.create_time.isoformat(),
    #         "complete_time": task.complete_time.isoformat() if task.complete_time else None
    #     } for task in tasks]
    # }


@router.patch("/tasks/{task_id}", status_code=200)
async def update_task_by_id(
        task_id: str,
        task_update: TaskUpdate,
        current_user_id: str = Depends(get_current_user)
):
    update_data = task_update.model_dump(exclude_unset=True)

    try:
        # 改为调用数据库层方法
        if 'designee_name' in update_data:
            update_data['designee_id'] = await get_user_id_by_name(update_data['designee_name'])
            del update_data['designee_name']

        updated_task = await update_task(task_id, update_data, current_user_id)

        return {
            "id": updated_task.id,
            "title": updated_task.title,
            "status": updated_task.status,
            "creator_name": (await updated_task.creator).name,
            "designee_name": (await updated_task.designee).name
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(500, detail=str(e))


@router.delete("/tasks/{task_id}", status_code=status.HTTP_200_OK)
async def delete_task_by_id(
    task_id: str,
    current_user_id: str = Depends(get_current_user)
):
    try:
        await delete_task(task_id, current_user_id)  # 调用数据层方法
        return {"detail": "任务已成功删除"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(500, detail=str(e))

# 新增：模糊查询任务
@router.get("/tasks/fuzzy")
async def fuzzy_search_tasks(
    query_str: str,
    current_user_id: str = Depends(get_current_user)
):
    try:
        tasks = await query_tasks_fuzzy(query_str)
        return {"tasks": tasks}
    except HTTPException as e:
        # 捕获并重新抛出已知的HTTP异常
        raise e
    except Exception as e:
        # 处理其他意外错误
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"模糊查询任务时发生错误：{str(e)}"
        )