from django.shortcuts import render

# Create your views here.
from django.views.generic.list import ListView

from demo2_app.models import Foobar


class FoobarView(ListView):
    model = Foobar
