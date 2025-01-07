import json
from django.contrib import admin
from django.db import models
from django.utils import timezone


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Telecaller(BaseModel):
    ROLE_CHOICES = [
        ('support', 'Support'),
        ('sales', 'Sales'),
    ]
    name = models.CharField(max_length=250)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    max_leads = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class LeadSourceConfig(BaseModel):
    name = models.CharField(max_length=250)
    telecallers = models.ManyToManyField(Telecaller)
    filter_logic = models.TextField()

    @admin.display(description='Telecallers')
    def telecallers_list(self):
        return ', '.join([telecaller.name for telecaller in self.telecallers.all()])

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):

        super().save(*args, **kwargs)

    def assing_leads(self, list):
        print(list)
# Create your models here.

class SalesLead(BaseModel):
    telecaller = models.ForeignKey(Telecaller, on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    source = models.ForeignKey(LeadSourceConfig, on_delete=models.CASCADE, default=1)

    @admin.display(description='telecaller_role')
    def telecaller_role(self):
        return self.telecaller.role

    def __str__(self):
        return f"Lead: {self.user.username} assigned to {self.telecaller.name}"


from django.db import models

class Config(models.Model):
    key = models.CharField(max_length=100, unique=True)
    KEY_TYPE_CHOICES = [
        ('string', 'String'),
        ('int_array', 'Array of Integers'),
        ('json', 'JSON'),
    ]
    type = models.CharField(max_length=20, choices=KEY_TYPE_CHOICES)
    value = models.JSONField()

    @classmethod
    def get(cls, key):
        try:
            config = cls.objects.get(key=key)
            return config.value
        except cls.DoesNotExist:
            raise ValueError(f"Config with key '{key}' does not exist.")

    @classmethod
    def set(cls, key, value):
        config = cls.objects.get(key=key)
        config_type = config.type
        if config_type == 'json':
            new_value = json.loads(value)
        elif config_type == 'int_array' and isinstance(value, list):
            new_value = [int(v) for v in value]
        elif config_type == "int_array" and isinstance(value, int):
            new_value = [int(v) for v in config.value]
            new_value.append(value)
        elif config_type == 'string':
            new_value = str(value)
        config.value = new_value
        config.save()
        return config