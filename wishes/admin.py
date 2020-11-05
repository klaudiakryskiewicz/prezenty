from django.contrib import admin

from wishes.models import Family, Member


@admin.register(Family)
class FamilyAdmin(admin.ModelAdmin):
    pass

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    pass

