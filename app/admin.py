from django.contrib import admin
from .models import Language, Agent, Voice


admin.site.register(Agent)
admin.site.register(Voice)
admin.site.register(Language)
