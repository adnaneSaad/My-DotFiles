from django.shortcuts import render
from OrientationApp import logic
from django.http import HttpResponse
import os
from django.conf import settings
from gtts import gTTS

import markdown

def View(request):
    context = {'done': False}

    Marks = {}
    Results = {}

    if request.method == 'POST':

        def get_mark(field_name):
            val = request.POST.get(field_name, '')
            try:
                if val != '':
                    return float(val)
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
        context['done'] = True
        context.update(Results)

        if 'download_txt' in request.POST:
            file_content = (
                "=== \U0001F393 SMART ORIENTATION ASSISTANT REPORT \U0001F393 ===\n\n"
                f"==> Your Marks: \n"
                f"Physics                                 \u26A1  : {get_mark('Physics')}\n"
                f"History, Geography, and Civic Education \U0001F30D  : {get_mark('HistGeo')}\n"
                f"Informations and Communication Technology \U0001F4BB: {get_mark('ICT')}\n"
                f"Islamic Education                       \U0001F4D6  : {get_mark('EduIslamic')}\n"
                f"English                                  \U0001F1EC\U0001F1E7  : {get_mark('English')}\n"
                f"Arabic                                   \U0001F1F2\U0001F1E6  : {get_mark('Arabic')}\n"
                f"French                                   \U0001F1EB\U0001F1F7  : {get_mark('French')}\n"
                f"Maths                                   \U0001F4D0  : {get_mark('Maths')}\n"
                f"Life and Earth Sciences                 \U0001F9EC  : {get_mark('SVT')}\n\n"
                f"==> Recommended Orientations: {Results.get('Best')} \U0001F3C6 ({Results.get('BestPercent')}%)\n\n"
                "==> Detailed Breakdown:\n"
                f"- Authentic Education \U0001F4DA: {Results.get('AuthenticEducationPercent')}%\n"
                f"- Arts and Humanities \U0001F4DC: {Results.get('ArtsAndHumanitiesPercent')}%\n"
                f"- Scientific Trunk    \U0001F52C: {Results.get('ScientificTrunkPercent')}%\n"
                f"- Technological Stump \U0001F4BB: {Results.get('TechnologicalStumpPercent')}%\n\n"
            )

            response = HttpResponse(file_content,
                                    content_type='text/plain; charset=utf-8')

            response[
                'Content-Disposition'] = 'attachment; filename="Orientation Report.txt"'
            return response
# AI part
    AI_UserToAi_Questions = request.POST.get('AI_UserToAi_Questions')

    if 'AI_HTML_WeakPoints' in request.POST:
        AI_AiToUser_RawAnswer = logic.AI(Marks, Results, Mode="AI_AiToUser_WeakPoints")
        AI_AiToUser_Answer = markdown.markdown(AI_AiToUser_RawAnswer, extensions=['extra', 'nl2br']) if AI_AiToUser_RawAnswer else "No Response From AI"

        context['AI_AiToUser_Answer'] = AI_AiToUser_Answer
        context['done'] = False
        context['Mode'] = "AI_AiToUser_Weakpoints"

    elif 'AI_HTML_Questions' in request.POST:
        history = request.session.get('history', [])
        if AI_UserToAi_Questions:

            history.append({
                "role": "user",
                "parts": [{"text": AI_UserToAi_Questions}]
            })

        print("--- CURRENT CHAT HISTORY ---")
        print(history)

        AI_AiToUser_Chat_RawAnswer = logic.AI(Marks, Results, Mode="AI_AiToUser_Chat", history=history)
        AI_AiToUser_Chat_Answer = markdown.markdown(AI_AiToUser_Chat_RawAnswer, extensions=['extra', 'nl2br']) if AI_AiToUser_Chat_RawAnswer else "No Response From AI"

        if AI_AiToUser_Chat_RawAnswer:
            history.append({
                "role": "model",
                "parts": [{"text": AI_AiToUser_Chat_RawAnswer}]
            })
            # Ensure an active session key exists
if not request.session.session_key:
    request.session.create()

# Build directory path and force creation of missing folders
audio_dir = os.path.join(settings.MEDIA_ROOT, 'audio')
os.makedirs(audio_dir, exist_ok=True)

# Define file paths
audio_filename = f"response_{request.session.session_key}.mp3"
audio_filepath = os.path.join(audio_dir, audio_filename)

# Generate and save audio
tts = gTTS(text=ai_answer, lang='fr')
tts.save(audio_filepath)

context['audio_url'] = f"{settings.MEDIA_URL}audio/{audio_filename}"

            request.session['history'] = history
            request.session.modified = True

            context['AI_AiToUser_Answer'] = AI_AiToUser_Chat_Answer
            context['Mode'] = "AI_AiToUser_Chat"

    elif 'GoToBlur' in request.POST:
        context['AI_AiToUser_Answer'] = None
        context['done'] = False
        context['Mode'] = "GoToBlur"
    elif 'AI_Clear' in request.POST:
        context['done'] = False
        context['cleared'] = True
        request.session['history'] = []
        context['Mode'] = "GoToBlur"
    else:
            context['AI_AiToUser_Answer'] = None

    return render(request, 'Orientation.html', context)