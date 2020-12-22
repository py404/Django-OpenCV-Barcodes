from django.shortcuts import render


# Create your views here.
def generate(request):
    return render(request, 'generate_barcodes/generate.html')
