from django.contrib import admin
from leads.models import Lead, User, Agent
# Register your models here.


admin.site.register(Lead)
admin.site.register(User)
admin.site.register(Agent)
