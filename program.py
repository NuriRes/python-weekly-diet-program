import tkinter as tk
from tkinter import ttk, messagebox
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import os
import math

def simulate_ai_response(name, weight, height, bmi, body_fat, goal, budget):
    # Yapay zeka modelinin çıktısını taklit eder
    response = f"""
    Merhaba {name},
    
    Haftalık beslenme ve egzersiz programınız hazır!

    Hedefiniz: {goal}
    Bütçeniz: {budget}
    
    Genel Bilgiler:
    - Kilo: {weight} kg
    - Boy: {height} cm
    - Vücut Kütle İndeksi (BMI): {bmi:.2f}
    - Vücut Yağ Yüzdesi: {body_fat:.2f}%
    
    Haftalık Programınız:
    """
    
    # Dinamik haftalık egzersiz ve beslenme planları
    if goal == "Zayıflama":
        response += """
        Pazartesi: 30 dakika yürüyüş, 3 porsiyon sebze ve meyve.
        Salı: 45 dakika koşu, 2 porsiyon protein ve sebze.
        Çarşamba: 30 dakika yoga, 1 porsiyon tam tahıl.
        Perşembe: 45 dakika yürüyüş, 3 porsiyon meyve.
        Cuma: 30 dakika koşu, 2 porsiyon protein.
        Cumartesi: 1 saat yüzme, 1 porsiyon sebze.
        Pazar: Dinlenme ve hafif esneme.
        """
    elif goal == "Kas Kazanma":
        response += """
        Pazartesi: 60 dakika ağırlık çalışması, 3 porsiyon protein.
        Salı: 45 dakika koşu, 2 porsiyon karbonhidrat.
        Çarşamba: 1 saat ağırlık çalışması, 2 porsiyon protein.
        Perşembe: 30 dakika yürüyüş, 3 porsiyon karbonhidrat.
        Cuma: 60 dakika ağırlık çalışması, 2 porsiyon protein.
        Cumartesi: 45 dakika koşu, 1 porsiyon sebze.
        Pazar: Dinlenme ve hafif esneme.
        """
    elif goal == "Kilo Alma":
        response += """
        Pazartesi: 45 dakika ağırlık çalışması, 4 porsiyon yüksek kalorili gıdalar.
        Salı: 60 dakika yürüyüş, 3 porsiyon protein ve karbonhidrat.
        Çarşamba: 45 dakika ağırlık çalışması, 2 porsiyon karbonhidrat.
        Perşembe: 60 dakika yürüyüş, 3 porsiyon protein.
        Cuma: 45 dakika ağırlık çalışması, 3 porsiyon yüksek kalorili gıdalar.
        Cumartesi: 1 saat koşu, 2 porsiyon sebze ve meyve.
        Pazar: Dinlenme ve hafif esneme.
        """
    
    # Bütçeye göre öneriler
    if budget == "Düşük":
        response += "\nEkonomik malzemeler kullanın ve basit tarifler tercih edin."
    elif budget == "Orta":
        response += "\nOrta fiyatlı malzemeler kullanın ve dengeli tarifler seçin."
    elif budget == "Fazla":
        response += "\nYüksek kaliteli malzemeler kullanın ve lüks tarifler deneyin."
    
    # Dinamik öneriler ekleme
    if body_fat > 25 and goal == "Zayıflama":
        response += "\nVücut yağ yüzdesi yüksek. Kalori alımını dikkatli kontrol edin ve egzersizlere ağırlık verin."
    elif body_fat < 10 and goal == "Kas Kazanma":
        response += "\nDüşük vücut yağ yüzdesi, kas kazanımını destekleyecek yeterli kalori ve protein aldığınızdan emin olun."

    return response

def generate_pdf(name, weight, height, bmi, body_fat, goal, budget, program):
    filename = os.path.join(os.path.expanduser("~/Masaüstü"), "haftalik_program.pdf")
    if not os.path.exists(os.path.dirname(filename)):
        os.makedirs(os.path.dirname(filename))

    c = canvas.Canvas(filename, pagesize=letter)
    
    pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf'))
    c.setFont('Arial', 12)
    c.drawString(100, 750, "Haftalık Beslenme ve Egzersiz Programı")

    c.drawString(100, 730, f"İsim: {name}")
    c.drawString(100, 710, f"Boy: {height} cm")
    c.drawString(100, 690, f"Kilo: {weight} kg")
    c.drawString(100, 670, f"Vücut Kütle İndeksi (BMI): {bmi:.2f}")
    c.drawString(100, 650, f"Vücut Yağ Yüzdesi: {body_fat:.2f}%")
    c.drawString(100, 630, f"Hedef: {goal}")
    c.drawString(100, 610, f"Butçe: {budget}")

    c.drawString(100, 590, "Haftalık Program:")
    y_start = 570
    for line in program.splitlines():
        c.drawString(100, y_start, line.strip())
        y_start -= 15

    c.save()
    messagebox.showinfo("Başarılı", f"Haftalık program başarıyla oluşturuldu: {filename}")
    os.startfile(filename)

def calculate_body_fat(weight, height, gender):
    if gender == "Kadın":
        body_fat = 0.29669 * weight + 0.71956 * math.log(height) - 28.515
    elif gender == "Erkek":
        body_fat = 1.162 * weight / (height/100)**2 - 0.072 * 20 - 10.8

    return max(body_fat, 0)

def calculate_bmi(weight, height):
    height_m = height / 100
    bmi = weight / (height_m ** 2)
    return bmi

def on_generate_button_click():
    name = entry_name.get()
    weight = float(entry_weight.get())
    height = float(entry_height.get())
    goal = combo_goal.get()
    budget = combo_budget.get()
    gender = combo_gender.get()

    bmi = calculate_bmi(weight, height)
    body_fat = calculate_body_fat(weight, height, gender)

    program = simulate_ai_response(name, weight, height, bmi, body_fat, goal, budget)
    generate_pdf(name, weight, height, bmi, body_fat, goal, budget, program)

# Tkinter GUI
root = tk.Tk()
root.title("Haftalık Beslenme ve Egzersiz Programı Oluşturucu")

# Kullanıcıdan bilgi alma
label_name = ttk.Label(root, text="İsim:")
label_name.grid(row=0, column=0, padx=10, pady=10)
entry_name = ttk.Entry(root)
entry_name.grid(row=0, column=1, padx=10, pady=10)

label_weight = ttk.Label(root, text="Kilo (kg):")
label_weight.grid(row=1, column=0, padx=10, pady=10)
entry_weight = ttk.Entry(root)
entry_weight.grid(row=1, column=1, padx=10, pady=10)

label_height = ttk.Label(root, text="Boy (cm):")
label_height.grid(row=2, column=0, padx=10, pady=10)
entry_height = ttk.Entry(root)
entry_height.grid(row=2, column=1, padx=10, pady=10)

label_gender = ttk.Label(root, text="Cinsiyet:")
label_gender.grid(row=3, column=0, padx=10, pady=10)
combo_gender = ttk.Combobox(root, values=["Kadın", "Erkek"])
combo_gender.grid(row=3, column=1, padx=10, pady=10)
combo_gender.current(0)

label_goal = ttk.Label(root, text="Hedef:")
label_goal.grid(row=4, column=0, padx=10, pady=10)
combo_goal = ttk.Combobox(root, values=["Zayıflama", "Kas Kazanma", "Kilo Alma"])
combo_goal.grid(row=4, column=1, padx=10, pady=10)
combo_goal.current(0)

label_budget = ttk.Label(root, text="Butçe:")
label_budget.grid(row=5, column=0, padx=10, pady=10)
combo_budget = ttk.Combobox(root, values=["Düşük", "Orta", "Fazla"])
combo_budget.grid(row=5, column=1, padx=10, pady=10)
combo_budget.current(0)

generate_button = ttk.Button(root, text="Oluştur", command=on_generate_button_click)
generate_button.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

root.mainloop()
