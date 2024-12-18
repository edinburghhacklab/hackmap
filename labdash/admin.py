from django.contrib import admin

from labdash.models import Button, ButtonGroup, Action


# Register your models here.
class ActionsInline(admin.TabularInline):
    model = Action


class ButtonAdmin(admin.ModelAdmin):
    model = Button
    list_display = ["name", "get_group_name"]
    list_filter = ("group__name",)
    inlines = [ActionsInline]

    def get_group_name(self, obj):
        return obj.group.name


class ButtonGroupAdmin(admin.ModelAdmin):
    model = ButtonGroup
    list_display = ["name", "priority", "color"]


admin.site.register(Button, ButtonAdmin)
admin.site.register(ButtonGroup, ButtonGroupAdmin)
