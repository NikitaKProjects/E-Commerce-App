from io import BytesIO
from django.template.loader import get_template
import xhtml2pdf.pisa as pisa
from django.conf import settings
import uuid

def save_pdf(params:dict):
    template = get_template("pdfs/invoice.html")
    html = template.render(params)
    response = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode('UTF-8')),response)
    file_name = uuid.uuid4()

    try:
        with open(str(settings.BASE_DIR)+f"/public/static/pdfs/{file_name}.pdf","wb+") as output:
            pdf = pisa.pisaDocument(BytesIO(html.encode('UTF-8')), output)

    except Exception as e:
        print(e)

    if pdf.err:
        return '',False
    
    return file_name,True