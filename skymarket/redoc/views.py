from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


def redoc(request):
    return render(request, 'Redoc.html')


@method_decorator(csrf_exempt, name='dispatch')
def redoc_json(request):
    return render(request, 'redoc-2.json')
