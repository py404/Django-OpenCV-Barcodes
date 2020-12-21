from django.shortcuts import render


# Create your views here.
def detect(request):
    return render(request, 'detect_barcodes/detect.html')
