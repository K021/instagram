from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from member.forms import SignupForm
from member.models import User, Relation


# class RelationInline()


class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ('추가 정보', {'fields': ('user_type', 'nickname', 'img_profile', 'introduction', 'liked_posts',)}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('추가 정보', {'fields': ('nickname', 'img_profile', 'user_type')}),
    )
    add_form = SignupForm


admin.site.register(User, UserAdmin)
admin.site.register(Relation)
