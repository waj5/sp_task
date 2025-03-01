
from fastapi import Depends, APIRouter
from backend.utils import get_current_user
from backend.database import query_tasks_by_user_or_designee

router = APIRouter(prefix="/auth", tags=["Authentication"])
@router.get("/tasks")
async def get_tasks(current_user_id: str = Depends(get_current_user)):
    # 假设 designee_id 也是当前用户
    tasks = await query_tasks_by_user_or_designee(current_user_id, current_user_id)
    return {"tasks": tasks}