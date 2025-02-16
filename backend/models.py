from tortoise import fields, Model

# 角色基类
class Role(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    created_at = fields.DatetimeField(auto_now_add=True)
    role_type = fields.CharField(max_length=20)

    class Meta:
        table = "role"

# 主角色
class MainRole(Role):
    class Meta:
        table = "main_role"

# 次角色
class SecondaryRole(Role):
    description = fields.TextField()

    class Meta:
        table = "secondary_role"

# 中间表处理 MainRole 和 SecondaryRole 的多对多关系
class MainRoleSecondaryRole(Model):
    id = fields.IntField(pk=True)
    main_role = fields.ForeignKeyField('models.MainRole', related_name='main_role_secondary_roles')
    secondary_role = fields.ForeignKeyField('models.SecondaryRole', related_name='secondary_role_main_roles')

    class Meta:
        table = "main_role_secondary_role"

# 任务表
class Task(Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=255)
    content = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)
    main_role = fields.ForeignKeyField("models.MainRole", related_name="tasks", null=True)
    secondary_role = fields.ForeignKeyField("models.SecondaryRole", related_name="tasks", null=True)

    class Meta:
        table = "task"
