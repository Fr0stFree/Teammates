from django.contrib import admin

from rooms.models import Room, Message, Topic


admin.site.register(Topic)
admin.site.register(Room)
admin.site.register(Message)
