from django.shortcuts import render


# Create your views here.
def main_view(request):
    context = dict()
    return render(request, 'main.html', context)
