from django.contrib import admin
from .models import Story
from .models import Author

class StoryAdmin(admin.ModelAdmin):
    list_display = ('id','headline','author','category','region')

admin.site.register(Author)
admin.site.register(Story,StoryAdmin)
