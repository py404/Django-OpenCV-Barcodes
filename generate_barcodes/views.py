import barcode
import qrcode
from barcode.writer import ImageWriter
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.encoding import smart_str


def generate_file(barcode_file):
    # output = HttpResponse(content_type="image/jpeg")
    output = HttpResponse(content_type="application/force-download")
    barcode_file.save(output, "JPEG")
    output['Content-Disposition'] = 'attachment; filename=%s' % smart_str('barcode.jpg')
    output['X-Sendfile'] = smart_str('barcode.jpg')
    return output


# Create your views here.
def generate(request):
    context = {
        'barcode_types': [b for b in barcode.PROVIDED_BARCODES if str(b).startswith('code')] + ['qrcode']
    }

    if request.method == 'POST':
        b_type = request.POST['typeOfBarcode']
        b_data = request.POST['barcodeData']

        if b_type == 'qrcode':
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=1,
            )
            qr.add_data(b_data)
            qr.make(fit=True)
            qr_file = qr.make_image(fill_color="black", back_color="white") # render qr image
            return generate_file(qr_file) # generate the file

        else:        
            bar = barcode.get_barcode(name=b_type, code=b_data, writer=ImageWriter())
            barcode_file = bar.render() # creates a PIL class image object
            return generate_file(barcode_file) # generate the file
    else:
        return render(request, 'generate_barcodes/generate.html', context=context)
