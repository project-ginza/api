from django.contrib import admin
from user.models import User, UserProfile, Address

# Register your models here.
admin.site.register(User)
admin.site.register(UserProfile)
admin.site.register(Address)
