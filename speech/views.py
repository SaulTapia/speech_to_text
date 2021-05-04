from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
from django.http import FileResponse, HttpResponse
from django.views.static import serve
import os

import speech_recognition as sr

# Create your views here.

def download(request, filename):
    filepath = os.path.join(settings.MEDIA_ROOT, filename)
    #return serve(request, os.path.basename(filepath), os.path.dirname(filepath))
    response = FileResponse(open(filepath, 'rb'))
    return response

def index(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)

        r = sr.Recognizer()

        with sr.AudioFile(os.path.join(settings.MEDIA_ROOT, filename)) as source:
            audio = r.listen(source)

            try:
                text = r.recognize_google(audio, language='es-ES')
                print(text)
                response = HttpResponse(text, content_type='application/text charset=utf-8')
                response['Content-Disposition'] = 'attachment; filename="transcripcion.txt"'
                return response

            except Exception as e:
                print('Failed, exception: ')
                print(e)
                return(render(request, 'speech/index.html'))

        return(download(request, filename))
        
    return render(request, 'speech/index.html')