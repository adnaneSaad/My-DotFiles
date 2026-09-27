# Core Part


def start(marks):
    Physics = marks.get('Physics', 0)
    HistGeo = marks.get('HistGeo', 0)
    ICT = marks.get('ICT', 0)
    EduIslamic = marks.get('EduIslamic', 0)
    English = marks.get('English', 0)
    Arabic = marks.get('Arabic', 0)
    French = marks.get('French', 0)
    Maths = marks.get('Maths', 0)
    SVT = marks.get('SVT', 0)

    AuthenticEducation = (Physics * 0) + (HistGeo * 3) + (ICT * 2) + (
        EduIslamic * 4) + (English * 2) + (Arabic * 4) + (French * 3) + (
            Maths * 2) + (SVT * 2)

    ArtsAndHumanities = (Physics * 0) + (HistGeo * 4) + (ICT * 2) + (
        EduIslamic * 0) + (English * 3) + (Arabic * 4) + (French * 4) + (
            Maths * 2) + (SVT * 2)

    ScientificTrunk = (Physics * 4) + (HistGeo * 2) + (ICT * 2) + (
        EduIslamic * 0) + (English * 3) + (Arabic * 2) + (French * 3) + (
            Maths * 4) + (SVT * 4)

    TechnologicalStump = (Physics * 4) + (HistGeo * 2) + (ICT * 3) + (
        EduIslamic * 0) + (English * 3) + (Arabic * 2) + (French * 3) + (
            Maths * 4) + (SVT * 0)

    Best = max(AuthenticEducation, ArtsAndHumanities, ScientificTrunk,
               TechnologicalStump)

    TotalScore = AuthenticEducation + ArtsAndHumanities + ScientificTrunk + TechnologicalStump

    if TotalScore == 0:
        TotalScore = 1

    AuthenticEducationPercent = (AuthenticEducation / TotalScore) * 100
    ArtsAndHumanitiesPercent = (ArtsAndHumanities / TotalScore) * 100
    ScientificTrunkPercent = (ScientificTrunk / TotalScore) * 100
    TechnologicalStumpPercent = (TechnologicalStump / TotalScore) * 100

    if (Physics > 20 or Physics < 0 or HistGeo > 20 or HistGeo < 0 or ICT > 20
            or ICT < 0 or EduIslamic > 20 or EduIslamic < 0 or English > 20
            or English < 0 or Arabic > 20 or Arabic < 0 or French > 20
            or French < 0 or Maths > 20 or Maths < 0 or SVT > 20 or SVT < 0):

        return {"error": "VALUE-TOO-BIG/TOO-SMALL"}

    if (Best == AuthenticEducation):
        best_orientation = "Authentic Education"

    elif (Best == ArtsAndHumanities):
        best_orientation = "Arts And Humanities"

    elif (Best == ScientificTrunk):
        best_orientation = "Scientific Trunk"

    elif (Best == TechnologicalStump):
        best_orientation = "Technological Stump"

    BestPercent = max(AuthenticEducationPercent, ArtsAndHumanitiesPercent,
                      ScientificTrunkPercent, TechnologicalStumpPercent)
    BestPercent = round(BestPercent, 2)

    return {
        "BestPercent": BestPercent,
        "Best": best_orientation,
        "AuthenticEducationPercent": round(AuthenticEducationPercent, 2),
        "ArtsAndHumanitiesPercent": round(ArtsAndHumanitiesPercent, 2),
        "ScientificTrunkPercent": round(ScientificTrunkPercent, 2),
        "TechnologicalStumpPercent": round(TechnologicalStumpPercent, 2)
    }


# AI Part

import os
from google import genai
from google.genai import types


def AI(Marks, Results, AI_UserToAi_Questions=None, Mode=None, history=None):
    API = os.environ.get("GEMINI_API_KEY")

    if not API:
        return "API key unavailable..."

    AI_Client = genai.Client(api_key=API)

    if AI_UserToAi_Questions:
        AI_SystemInstruction = (
            "You are an intelligent, helpful educational assistant for Moroccan middle school students. "
            "maintain a continuous conversation"
            "Answer the user's questions accurately and directly. "
            "If they ask a general knowledge question (e.g., geography, translation), answer it directly. "
            "If they ask about their academic orientation or marks, use their provided profile data."
        )
        AI_Final_Prompt = f"""
    
        User Question: "{AI_UserToAi_Questions}"

        Context (Use ONLY if the user asks about their grades or orientation):
        - Student Marks (Out of 20): {Marks}
        - Stream Percentages: {Results}
        STRICT FORMATTING RULE:
        - Use clean standard Markdown.
        - Do NOT use LaTeX or dollar signs ($). Use standard visual symbols directly (e.g., use →, ←, ✓, ×, ±, ²) instead of math code.
        - Make it beautiful
        Keep your answer helpful, clear, and concise, note: keep it under 1000 words
        """

    elif Mode == "AI_AiToUser_WeakPoints":

        AI_SystemInstruction = (
            "You are the built-in AI advisor for the 'Smart Orientation Assistant', an official-grade "
            "tool for the Moroccan educational system assisting 2AC students.")
        AI_Final_Prompt = f"""
        STRICT RULE: Be extremely concise. 
        Give ONLY 5 short bullet points max:
        1. Primary weak point.
        2. Immediate fix.
        3. Recommended stream path.
        4. User's path towards future diplomas.
        STRICT FORMATTING RULE:
        - Use clean standard Markdown.
        - Do NOT use LaTeX or dollar signs ($). Use standard visual symbols directly (e.g., use →, ←, ✓, ×, ±, ²) instead of math code.
        - Make it beautiful

        Student Marks (Out of 20): {Marks}
        Calculated Stream Percentages (Out of 100): {Results}
        Provide a clear breakdown of their weak points and actionable advice.
        """

    else:
        AI_SystemInstruction = "You are an official orientation advisor for Moroccan 2AC students."
        AI_Final_Prompt = f"""
        Provide a brief summary of the student's academic profile:
        Student Marks (Out of 20): {Marks}
        Calculated Stream Percentages (Out of 100): {Results}
        STRICT FORMATTING RULE:
        - Use clean standard Markdown.
        - Do NOT use LaTeX or dollar signs ($). Use standard visual symbols directly (e.g., use →, ←, ✓, ×, ±, ²) instead of math code.
        - Make it beautiful
        """

    AI_Config = types.GenerateContentConfig(
        system_instruction=AI_SystemInstruction,
        temperature=0.7,
        max_output_tokens=1500)
    try:
        AI_AiToUser_Answer = AI_Client.models.generate_content(
            model="gemini-3.5-flash-lite",
            config=AI_Config,
            contents = history if history else AI_Final_Prompt)

        if AI_AiToUser_Answer.candidates:
            candidate = AI_AiToUser_Answer.candidates[0]
            if "MAX_TOKENS" in str(candidate.finish_reason):
                return AI_AiToUser_Answer.text + "\n\n⚠️ [Note: Response is limited due to length limit.]"

        return AI_AiToUser_Answer.text

    except Exception as e:
        error_str = str(e)
        if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
            return "⚠️ AI rate limit reached. Please wait ~2 minutes before trying again."
        return f"ERROR: {error_str}"
