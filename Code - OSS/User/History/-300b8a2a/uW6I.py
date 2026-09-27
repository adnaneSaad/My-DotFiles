def start():
    #!/usr/bin/env python3
    # coding: utf-8
    # Upwards I'm just telling your PC to run this as a Python code "the first line isn't needed in Windows"
    # In the second line I'm adding support to imogies, french accents and arabic letters "in case I needed them"
    #==========================================================================================================================================#
    # Saving mechanism; grabs grades and the best orientation and put'em in a file called: Orientation_Result.txt
    def save_to_file(result, marks):
        import os

        file_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "Orientation_Result.txt"
        )

        with open(file_path, "w", encoding="utf-8") as file:
            file.write("=== Here Are Your Marks And Your Best Orientation! ===\n")
            for subject, value in marks.items():
                file.write(f"{subject}: {value}\n")
            file.write(f"Best Orientation: {result}\n\n")
    #===========================================================================================================================================#
    # Basically this is the core of the program "plus the last part" here, I'm grabbing user inputs, getting sure that the user had filled all entries with supported answers, counting the best Orientation, creating a label with it, and finally calling the saving mechanism whenever the user click that Submit button

    def Submit():
        try:
            global Physics, HistGeo, ICT, EduIslamic, English, Arabic, French, Maths, SVT
        
        except ValueError:
            messagebox.showerror("Input Error", "Please fill all fields with numbers only.")

            return
        AuthenticEducation = (Physics * 0) + (HistGeo * 3) + (ICT * 2) + (EduIslamique * 4) + (English * 2) + (Arabic * 4) + (French * 3) + (Maths * 2) + (SVT * 2)

        ArtsAndHumanities  = (Physics * 0) + (HistGeo * 4) + (ICT * 2) + (EduIslamique * 0) + (English * 3) + (Arabic * 4) + (French * 4) + (Maths * 2) + (SVT * 2)

        ScientificTrunk    = (Physics * 4) + (HistGeo * 2) + (ICT * 2) + (EduIslamique * 0) + (English * 3) + (Arabic * 2) + (French * 3) + (Maths * 4) + (SVT * 4)

        TechnologicalStump = (Physics * 4) + (HistGeo * 2) + (ICT * 3) + (EduIslamique * 0) + (English * 3) + (Arabic * 2) + (French * 3) + (Maths * 4) + (SVT * 0)

        Best = max(AuthenticEducation, ArtsAndHumanities, ScientificTrunk, TechnologicalStump)

        TotalScore = AuthenticEducation + ArtsAndHumanities + ScientificTrunk + TechnologicalStump

        AuthenticEducationPercent = (AuthenticEducation / TotalScore) * 100
        ArtsAndHumanitiesPercent  = (ArtsAndHumanities  / TotalScore) * 100
        ScientificTrunkPercent    = (ScientificTrunk    / TotalScore) * 100
        TechnologicalStumpPercent = (TechnologicalStump / TotalScore) * 100
        if (Physics > 20 or Physics < 0):
            messagebox.showerror("Input Error", "Please put values between 0 and 20")
        elif (HistGeo > 20 or HistGeo < 0):
            messagebox.showerror("Input Error", "Please put values between 0 and 20")
        elif (ICT > 20 or ICT < 0):
            messagebox.showerror("Input Error", "Please put values between 0 and 20")
        elif (EduIslamique > 20 or EduIslamique < 0):
            messagebox.showerror("Input Error", "Please put values between 0 and 20")
        elif (English > 20 or English < 0):
            messagebox.showerror("Input Error", "Please put values between 0 and 20")
        elif (Arabic > 20 or Arabic < 0):
            messagebox.showerror("Input Error", "Please put values between 0 and 20")
        elif (French > 20 or French < 0):
            messagebox.showerror("Input Error", "Please put values between 0 and 20")
        elif (Maths > 20 or Maths < 0):
            messagebox.showerror("Input Error", "Please put values between 0 and 20")
        elif (SVT > 20 or SVT < 0):
            messagebox.showerror("Input Error", "Please put values between 0 and 20")
        if (Best == AuthenticEducation):
            best_orientation = "Authentic Education"

        elif(Best == ArtsAndHumanities):
            best_orientation = "Arts And Humanities"

        elif(Best == ScientificTrunk):
            best_orientation = "Scientific Trunk"

        elif(Best == TechnologicalStump):
            best_orientation = "Technological Stump"
        if (abs(AuthenticEducationPercent - ArtsAndHumanitiesPercent) <= 10 or
        abs(AuthenticEducationPercent - ScientificTrunkPercent) <= 10 or
        abs(AuthenticEducationPercent - TechnologicalStumpPercent) <= 10 or
        abs(ArtsAndHumanitiesPercent - ScientificTrunkPercent) <= 10 or
        abs(ArtsAndHumanitiesPercent - TechnologicalStumpPercent) <= 10 or
        abs(ScientificTrunkPercent - TechnologicalStumpPercent) <= 10):
            messagebox.showinfo(
                "Analysis Results",
                f"The Best Orientation For You is: {best_orientation}\n\n"
                f"Authentic Education: {AuthenticEducationPercent:.0f}%\n"
                f"Arts And Humanities: {ArtsAndHumanitiesPercent:.0f}%\n"
                f"Scientific Trunk: {ScientificTrunkPercent:.0f}%\n"
                f"Technological Stump: {TechnologicalStumpPercent:.0f}%\n\n"
                f"Note: Percentages are close, it is way better to ask your teacher for your best orientation !\n"
                )
        else:
            messagebox.showinfo(
                "Analysis Results",
                f"The Best Orientation For You is: {best_orientation}\n\n"
                f"Authentic Education: {AuthenticEducationPercent:.0f}%\n"
                f"Arts And Humanities: {ArtsAndHumanitiesPercent:.0f}%\n"
                f"Scientific Trunk: {ScientificTrunkPercent:.0f}%\n"
                f"Technological Stump: {TechnologicalStumpPercent:.0f}%\n"
                )
        marks = {
        "Physics": Physics,
        "Hist.Geo": HistGeo,
        "ICT": ICT,
        "Edu.Islamique": EduIslamique,
        "English": English,
        "Arabic": Arabic,
        "French": French,
        "Maths": Maths,
        "SVT": SVT
        }

        save_to_file(best_orientation, marks)
    #==========================================================================================================================================#
    # Creating the Submit button
    SubmitButton = tk.Button(Frame, text = "Submit", bg = "gray", command = Submit)
    SubmitButton.grid(row = 10, column = 0, columnspan = 2, pady = 10)
    #==========================================================================================================================================#
    root.mainloop()
    # This last line is important for that the app runs well and normally
