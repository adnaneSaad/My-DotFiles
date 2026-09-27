import os, markdown, time
from gtts import gTTS
from langdetect import detect
from strip_markdown import strip_markdown
from xhtml2pdf import pisa

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.template.loader import render_to_string

from .models import StudentData
from OrientationApp import logic

def Signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('Orientation')
    else:
        form = UserCreationForm()
    return render(request, 'Signup.html', {'form': form})

def Login(request):
    request.session['didit'] = True
    if request.method == 'POST':
        form = AuthenticationForm(request, data = request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('Orientation')
    else:
        form = AuthenticationForm()
    return render(request, 'Login.html', {'form': form})

def Logout(request):
    if request.method == 'POST':
        logout(request)
        return redirect('Login')

def View(request):
    if request.user.is_authenticated and request.session.get('didit') == True:

        context['done']= False

        studentdata, created = StudentData.objects.get_or_create(user = request.user)

        if request.method == 'POST':

            def get_mark(field_name):
                v = request.POST.get(field_name, '')
                try:
                    if v != '':
                        return float(v)
                    else:
                        return 0.0

                except ValueError:
                    return 0.0
            if 'Calculate' in request.POST or 'download_pdf' in request.POST:
                marks = {
                    "Physics": get_mark('Physics'),
                    "HistGeo": get_mark('HistGeo'),
                    "ICT": get_mark('ICT'),
                    "EduIslamic": get_mark('EduIslamic'),
                    "English": get_mark('English'),
                    "Arabic": get_mark('Arabic'),
                    "French": get_mark('French'),
                    "Maths": get_mark('Maths'),
                    "SVT": get_mark('SVT'),
                }

                results = logic.start(marks)
                studentdata.Marks = marks
                studentdata.Results = results
                studentdata.save()
            Marks = studentdata.Marks
            Results = studentdata.Results
            print(context)
            if 'Calculate' in request.POST:
                context['done'] = True

                context.update(Results)
                print(context)
            if 'download_pdf' in request.POST:
                context['done'] = True

                context = {'Marks': Marks, 'Results': Results}
                PlainHTML = render_to_string('HTMLtoPDF.html', context)

                response = HttpResponse(content_type='application/pdf')

                response[
                    'Content-Disposition'] = 'attachment; filename="Orientation Report.pdf"'

                status = pisa.CreatePDF(PlainHTML, dest=response)
                if status.err:
                    return HttpResponse('Error generating PDF', status=500)
                return response

        if 'AccountActivity' in request.POST:
            context['btn'] = True
        elif 'Close' in request.POST:
            context['btn'] = False
        # AI part

        if 'AI_HTML_WeakPoints' in request.POST:
            AI_AiToUser_RawAnswer = logic.AI(Marks, Results, Mode="AI_AiToUser_WeakPoints")
            AI_AiToUser_Answer = markdown.markdown(AI_AiToUser_RawAnswer, extensions=['extra', 'nl2br']) if AI_AiToUser_RawAnswer else "No Response From AI"
            if AI_AiToUser_RawAnswer:
                AI_AiToUser_RawAnswerStripped = AI_AiToUser_RawAnswer.strip()
                TTS_Text = strip_markdown(AI_AiToUser_RawAnswerStripped)

                if not request.session.session_key:
                    request.session.create()

                audio_Dir = os.path.join(settings.MEDIA_ROOT, 'audio1')
                os.makedirs(audio_Dir, exist_ok=True)

                audio_Filename = f"weakpoints_{request.user.id}_{request.session.session_key}.mp3"
                audio_File = os.path.join(audio_Dir, audio_Filename)

                try:
                    lang = detect(TTS_Text)
                except Exception:
                    lang = "en"

                tts = gTTS(text=TTS_Text, lang = lang)
                tts.save(audio_File)
                context['audio'] = f"{settings.MEDIA_URL}audio1/{audio_Filename}"
            else:
                AI_AiToUser_Answer = "No Answer From AI"
            request.session.modified = True
            if 'stop' in request.POST:
                context.pop('audio', None)
            context['AI_AiToUser_Answer'] = AI_AiToUser_Answer
            context['done'] = False
            context['Mode'] = "AI_AiToUser_Weakpoints"

        elif 'AI_HTML_Questions' in request.POST:
            context['done'] = False
            AI_UserToAi_Questions = request.POST.get('AI_UserToAi_Questions')
            history = studentdata.history

            if AI_UserToAi_Questions:

                history.append({
                    "role": "user",
                    "parts": [{"text": AI_UserToAi_Questions}]
                })
                studentdata.history = history
                studentdata.save()
                print("--- CURRENT CHAT HISTORY ---")
                print(history)

                AI_AiToUser_Chat_RawAnswer = logic.AI(Marks ,Results, AI_UserToAi_Questions, Mode="AI_AiToUser_Chat", history=history)
                AI_AiToUser_Chat_RawAnswerStripped = AI_AiToUser_Chat_RawAnswer.strip()
                TTS_Text = strip_markdown(AI_AiToUser_Chat_RawAnswerStripped)
                AI_AiToUser_Chat_Answer = markdown.markdown(AI_AiToUser_Chat_RawAnswer, extensions=['extra', 'nl2br']) if AI_AiToUser_Chat_RawAnswer else "No Response From AI"

                if AI_AiToUser_Chat_RawAnswer:
                    history.append({
                        "role": "model",
                        "parts": [{"text": AI_AiToUser_Chat_RawAnswer}]
                    })
                    studentdata.history = history
                    studentdata.save()

                    audio_dir = os.path.join(settings.MEDIA_ROOT, 'audio')
                    os.makedirs(audio_dir, exist_ok=True)

                    audio_filename = f"response_{request.session.session_key}.mp3"
                    audio_file = os.path.join(audio_dir, audio_filename)
                    try:
                        lang = detect(TTS_Text)
                    except Exception:
                        lang = 'en'
                    tts = gTTS(text=TTS_Text, lang=lang)
                    tts.save(audio_file)

                    context['audio_url'] = f"{settings.MEDIA_URL}audio/{audio_filename}"
                    print(f"{settings.MEDIA_URL}audio/{audio_filename}")
                request.session['history'] = history
                request.session.modified = True

                context['AI_AiToUser_Chat_Answer'] = AI_AiToUser_Chat_Answer
                context['Mode'] = "AI_AiToUser_Chat"

        elif 'AI_AiToUser_Chat' in request.POST:
            context['done'] = False
            context['Mode'] = "AI_AiToUser_Chat"
        elif 'AI_Clear' in request.POST:
            context['done'] = False
            request.session['history'] = []
            context['cleared'] = True
            context['Mode'] = "AI_AiToUser_Chat"
        else:
            context['AI_AiToUser_Answer'] = None
## NON LOGGED USERS PART
    elif not request.user.is_authenticated and request.session.get('didit') == True:
        context = {'done': False}

        if request.method == 'POST':

            def get_mark(field_name):
                v = request.POST.get(field_name, '')
                try:
                    if v != '':
                        return float(v)
                    else:
                        return 0.0

                except ValueError:
                    return 0.0
            Marks = {
                "Physics": get_mark('Physics'),
                "HistGeo": get_mark('HistGeo'),
                "ICT": get_mark('ICT'),
                "EduIslamic": get_mark('EduIslamic'),
                "English": get_mark('English'),
                "Arabic": get_mark('Arabic'),
                "French": get_mark('French'),
                "Maths": get_mark('Maths'),
                "SVT": get_mark('SVT'),
            }

            Results = logic.start(Marks)
            context.update(Results)

            if 'Calculate' in request.POST:
                context['done'] = True

            if 'download_pdf' in request.POST:
                context['done'] = True

                context = {'Marks': Marks, 'Results': Results}
                PlainHTML = render_to_string('HTMLtoPDF.html', context)

                response = HttpResponse(content_type='application/pdf')

                response[
                    'Content-Disposition'] = 'attachment; filename="Orientation Report.pdf"'

                status = pisa.CreatePDF(PlainHTML, dest=response)
                if status.err:
                    return HttpResponse('Error generating PDF', status=500)

                return response
            if 'GoBack' in request.POST:
                return redirect('Login')
        # AI part

        if 'AI_HTML_WeakPoints' in request.POST:
            AI_AiToUser_RawAnswer = logic.AI(Marks, Results, Mode="AI_AiToUser_WeakPoints")
            AI_AiToUser_Answer = markdown.markdown(AI_AiToUser_RawAnswer, extensions=['extra', 'nl2br']) if AI_AiToUser_RawAnswer else "No Response From AI"
            if AI_AiToUser_RawAnswer:
                AI_AiToUser_RawAnswerStripped = AI_AiToUser_RawAnswer.strip()
                TTS_Text = strip_markdown(AI_AiToUser_RawAnswerStripped)

                audio_Dir = os.path.join(settings.MEDIA_ROOT, 'audio1')
                os.makedirs(audio_Dir, exist_ok=True)

                audio_Filename = f"weakpoints_{int(time.time())}.mp3"
                audio_File = os.path.join(audio_Dir, audio_Filename)

                try:
                    lang = detect(TTS_Text)
                except Exception:
                    lang = "en"

                tts = gTTS(text=TTS_Text, lang = lang)
                tts.save(audio_File)
                context['audio'] = f"{settings.MEDIA_URL}audio1/{audio_Filename}"
            else:
                AI_AiToUser_Answer = "No Answer From AI"

            context['AI_AiToUser_Answer'] = AI_AiToUser_Answer
            context['done'] = False
            context['Mode'] = "AI_AiToUser_Weakpoints"

        elif 'AI_HTML_Questions' in request.POST:
            context['done'] = False
            AI_UserToAi_Questions = request.POST.get('AI_UserToAi_Questions')
            history = []

            if AI_UserToAi_Questions:

                history.append({
                    "role": "user",
                    "parts": [{"text": AI_UserToAi_Questions}]
                })
                print("--- CURRENT CHAT HISTORY ---")
                print(history)

                AI_AiToUser_Chat_RawAnswer = logic.AI(Marks ,Results, AI_UserToAi_Questions, Mode="AI_AiToUser_Chat", history=history)
                AI_AiToUser_Chat_RawAnswerStripped = AI_AiToUser_Chat_RawAnswer.strip()
                TTS_Text = strip_markdown(AI_AiToUser_Chat_RawAnswerStripped)
                AI_AiToUser_Chat_Answer = markdown.markdown(AI_AiToUser_Chat_RawAnswer, extensions=['extra', 'nl2br']) if AI_AiToUser_Chat_RawAnswer else "No Response From AI"

                if AI_AiToUser_Chat_RawAnswer:
                    history.append({
                        "role": "model",
                        "parts": [{"text": AI_AiToUser_Chat_RawAnswer}]
                    })

                    audio_dir = os.path.join(settings.MEDIA_ROOT, 'audio')
                    os.makedirs(audio_dir, exist_ok=True)

                    audio_filename = f"response_{request.session.session_key}.mp3"
                    audio_file = os.path.join(audio_dir, audio_filename)
                    try:
                        lang = detect(TTS_Text)
                    except Exception:
                        lang = 'en'
                    tts = gTTS(text=TTS_Text, lang=lang)
                    tts.save(audio_file)

                    context['audio_url'] = f"{settings.MEDIA_URL}audio/{audio_filename}"
                    print(f"{settings.MEDIA_URL}audio/{audio_filename}")
                request.session['history'] = history
                request.session.modified = True

                context['AI_AiToUser_Chat_Answer'] = AI_AiToUser_Chat_Answer
                context['Mode'] = "AI_AiToUser_Chat"

        elif 'AI_AiToUser_Chat' in request.POST:
            context['done'] = False
            context['Mode'] = "AI_AiToUser_Chat"
        elif 'AI_Clear' in request.POST:
            context['done'] = False
            request.session['history'] = []
            context['cleared'] = True
            context['Mode'] = "AI_AiToUser_Chat"
        else:
            context['AI_AiToUser_Answer'] = None
    else:
        return redirect('Login')
    return render(request, 'Orientation.html', context)