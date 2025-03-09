import bcrypt
import uuid
from tortoise import fields, Model

class Master(Model):
    id = fields.UUIDField(pk=True, default=uuid.uuid4)
    name = fields.CharField(max_length=100)
    password = fields.CharField(max_length=128)  # 增加长度以适应 bcrypt 哈希值
    sex = fields.CharField(max_length=10, null=True, default="未知")  # 允许为空，设置默认值为“未知”
    age = fields.IntField(null=True, default=0)  # 允许为空，设置默认值为0
    email = fields.CharField(max_length=100)
    is_admin = fields.BooleanField(default=True)  # 新增字段判断是否是管理者
    administered = fields.ManyToManyField("models.Administered", related_name="masters")  # 修改 related_name

    class Meta:
        table = 'master'
        database = "default"

    def set_password(self, raw_password: str) -> None:
        """使用 bcrypt 哈希密码"""
        self.password = bcrypt.hashpw(raw_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, raw_password: str) -> bool:
        """验证密码"""
        return bcrypt.checkpw(raw_password.encode('utf-8'), self.password.encode('utf-8'))

class Administered(Model):
    id = fields.UUIDField(pk=True, default=uuid.uuid4)
    name = fields.CharField(max_length=100)
    password = fields.CharField(max_length=128)  # 增加长度以适应 bcrypt 哈希值
    sex = fields.CharField(max_length=10, null=True, default="未知")  # 允许为空，设置默认值为“未知”
    age = fields.IntField(null=True, default=0)  # 允许为空，设置默认值为0
    email = fields.CharField(max_length=100)
    is_admin = fields.BooleanField(default=False)  # 新增字段判断是否是管理者
    master = fields.ForeignKeyField("models.Master", related_name="administereds", null=True)  # 新增外键关联到 Master

    class Meta:
        table = 'administered'
        database = "default"

    def set_password(self, raw_password: str) -> None:
        """使用 bcrypt 哈希密码"""
        self.password = bcrypt.hashpw(raw_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, raw_password: str) -> bool:
        """验证密码"""
        return bcrypt.checkpw(raw_password.encode('utf-8'), self.password.encode('utf-8'))

class Task(Model):
    id = fields.UUIDField(pk=True, default=uuid.uuid4)
    title = fields.CharField(max_length=100)
    create_time = fields.DatetimeField(auto_now_add=True)
    complete_time = fields.DatetimeField(null=True, blank=True)  # 作为可选字段处理
    content = fields.TextField()
    status = fields.CharField(max_length=50, default="未完成")  # 设置默认值为“未完成”
    create_user = fields.ForeignKeyField("models.Master", related_name="tasks")  # 直接使用类名
    designee = fields.ForeignKeyField("models.Administered", related_name="designee_tasks")  # 直接使用类名

    class Meta:
        table = 'task'
        database = "default"
