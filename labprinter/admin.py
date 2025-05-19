from django.contrib import admin

from labprinter.models import Printer


class PrinterAdmin(admin.ModelAdmin):
    model = Printer
    list_display = ["name", "description"]


admin.site.register(Printer, PrinterAdmin)
