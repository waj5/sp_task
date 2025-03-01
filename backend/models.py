import bcrypt
import uuid
from tortoise import fields, Model

class Master(Model):
    id = fields.UUIDField(pk=True, default=uuid.uuid4)
    name = fields.CharField(max_length=100)
    password = fields.CharField(max_length=128)  # 增加长度以适应 bcrypt 哈希值
    sex = fields.CharField(max_length=10)
    age = fields.IntField()
    email = fields.CharField(max_length=100)
    administered = fields.ManyToManyField("models.Administered", related_name="administered")  # 如果 Master 和 Administered 定义在同一文件，可改为直接使用类名

    class Meta:
        table = 'master'

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
    sex = fields.CharField(max_length=10)
    age = fields.IntField()
    email = fields.CharField(max_length=100)
    master = fields.ManyToManyField("models.Master", related_name="master")  # 直接使用类名

    class Meta:
        table = 'administered'

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
    create_user = fields.ForeignKeyField("models.Master", related_name="task")  # 直接使用类名
    designee = fields.ForeignKeyField("models.Administered", related_name="designee_task")  # 直接使用类名
    content = fields.TextField()

    class Meta:
        table = 'task'
