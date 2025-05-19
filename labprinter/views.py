from django.shortcuts import render
from labprinter.models import Printer
from django.views.generic.list import ListView


class Printers(ListView):
    model = Printer
    context_object_name = "printers"
    queryset = Printer.objects.all().order_by("shortname")
