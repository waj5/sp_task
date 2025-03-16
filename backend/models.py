import bcrypt
import uuid
from tortoise import fields, Model

class User(Model):
    id = fields.UUIDField(pk=True, default=uuid.uuid4, db_type="char(36)")  # 新增db_type
    name = fields.CharField(max_length=100)
    password = fields.CharField(max_length=128)
    email = fields.CharField(max_length=100)
    is_admin = fields.BooleanField(default=False)
    role = fields.CharField(max_length=20, default='administered')  # 新增角色字段

    # 公共密码验证方法
    def set_password(self, raw_password: str):
        if len(raw_password) < 8:
            raise ValueError("密码至少需要8个字符")
        self.password = bcrypt.hashpw(raw_password.encode(), bcrypt.gensalt()).decode()

    def check_password(self, raw_password: str) -> bool:
        return bcrypt.checkpw(raw_password.encode(), self.password.encode())

    class Meta:
        table = 'users'
        database = "default"

class Master(Model):
    id = fields.UUIDField(pk=True, default=uuid.uuid4, db_type="char(36)")  # 添加显式主键
    user = fields.OneToOneField(
        'models.User',
        related_name='master',
        db_constraint=False,
        db_type="char(36)"
    )
    administered = fields.ManyToManyField(
        "models.Administered",
        related_name="masters",
        through="masters_administered",
        forward_key={"db_column": "master_id", "db_type": "char(36)"},
        backward_key={"db_column": "administered_id", "db_type": "char(36)"}
    )
    class Meta:
        table ='master'
        database = "default"

class Administered(Model):
    id = fields.UUIDField(pk=True, default=uuid.uuid4, db_type="char(36)")  # 显式定义主键
    user = fields.OneToOneField('models.User', related_name='administered', db_type="char(36)")
    master = fields.ForeignKeyField(
        'models.Master',
        related_name='administereds',
        null=True,
        db_type="char(36)"
    )
    class Meta:
        table = 'administered'
        database = "default"

class MastersAdministered(Model):
    master = fields.ForeignKeyField(
        "models.Master",
        db_column="master_id",
        db_type="char(36)"  # 新增
    )
    administered = fields.ForeignKeyField(
        "models.Administered",
        db_column="administered_id",
        db_type="char(36)"  # 新增
    )
    class Meta:
        table = "masters_administered"
        indexes = [
            ("master_id", "administered_id")  # 明确指定联合索引字段
        ]

class Task(Model):
    id = fields.UUIDField(pk=True, default=uuid.uuid4, db_type="char(36)")
    title = fields.CharField(max_length=100)
    content = fields.TextField()
    status = fields.CharField(max_length=20, default="未完成")
    create_time = fields.DatetimeField(auto_now_add=True)
    complete_time = fields.DatetimeField(null=True)

    # 统一关联用户表
    creator = fields.ForeignKeyField(
        "models.User",
        related_name="created_tasks"
    )
    designee = fields.ForeignKeyField(
        "models.User",  # 直接关联到User表
        related_name="assigned_tasks"
    )

    async def get_details(self):
        await self.fetch_related('creator', 'designee')
        return self
    class Meta:
        table = 'task'
        database = "default"



