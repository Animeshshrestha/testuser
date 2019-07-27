from django.contrib import admin
from .models import UserInfo, UserProfile, Education, WorkExperience, Skills, Training, SocialAccount

admin.site.register(UserInfo)
admin.site.register(UserProfile)
admin.site.register(Education)
admin.site.register(WorkExperience)
admin.site.register(Skills)
admin.site.register(Training)
admin.site.register(SocialAccount)