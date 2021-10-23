from tortoise import fields, models, Tortoise
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise import models, fields


class Verification(models.Model):
    """ Модель для подтверждения регистрации пользователя
    """
    link = fields.UUIDField(pk=True)
    user = fields.ForeignKeyField('models.User', related_name='verification')
