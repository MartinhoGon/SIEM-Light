from django.contrib import admin
from api.models import *
# Register your models here.

admin.site.register(feed.Feed)
admin.site.register(category.Category)
admin.site.register(value.Value)


