# -*- coding: utf-8 -*-
"""
Created on Thu Jan 11 09:17:12 2024

@author: Christian
"""    
from Report_Tool.report_lib import * 
from fpdf import FPDF
from datetime import datetime
import sys 
import locale


# Erstellen des Reports 
titel = 'Methode zur Prognose von Heizenergiebedafs mittels stochastischer Simulation'
author = 'Christian Knecht'
author_info = 'christian.xaver.knecht@uni-weimar.de'
logo = 'Report_Tool/Bauhaus_Logo_b.png'
locale.setlocale(locale.LC_TIME, 'de_DE.UTF-8')
current_datetime = datetime.now()
formatted_date = current_datetime.strftime('%d %B, %Y')
date = formatted_date
report_pdf = reportPDF(titel, author, author_info, date, logo)
report_pdf.set_left_margin(30)
report_pdf.set_right_margin(35)


# Cover Page 
report_pdf.cover(logo)


# Titel Page
row1 = "Studienarbeit:"
row2 = "Methode zur Darstellung von Heizenergiebedarf"
row3 = "mittels stochastischer Simulation."
report_pdf.titel_page(row1, row2, row3)



# Abstract 
titel = 'Abstract'
report_pdf.chapter_titel(titel)
body_text_path = "texte/abstract_eng.txt"
report_pdf.body_from_txt(body_text_path)
body_text_path = "texte/abstract_d.txt"
report_pdf.body_from_txt(body_text_path)


# Erstelle der Gliederung 
report_pdf.add_chapter('Kapitel 1: Einleitung', p=3)
report_pdf.add_chapter('Kapitel 2: Methode',p=6)
report_pdf.add_chapter('Kapitel 3: Ergebnisse', p=12)
report_pdf.add_chapter('Kapitel 4: Diskussion', p=18)
report_pdf.add_chapter('Kapitel 5: Fazit', p=18)
report_pdf.add_chapter('Kapitel 6: Quellen', p=18)
report_pdf.set_last_page(18)
report_pdf.table_of_contents()



# Einleitung 
titel = 'Einleitung'
report_pdf.chapter_titel(titel)
body_text_path = "texte/einleitung5.txt"
report_pdf.body_from_txt(body_text_path)

# Methodode  
titel = 'Methode'
report_pdf.chapter_titel(titel) 
body_text_path = "texte/methodologie2.txt"
report_pdf.body_from_txt(body_text_path)
figure_caption = "Vorgehen zur Erstellung von Modellen."
report_pdf.figure3("plots/rezept.png", "Abb. 1: ", figure_caption, 185) 
body_text_path = "texte/Musterquartiere.txt"
report_pdf.body_from_txt(body_text_path)

# Musterquartier 
titel = 'Generieren diskreter Datenpunkte'
report_pdf.chapter_titel2(titel)
body_text_path = "texte/m22.txt"
report_pdf.body_from_txt(body_text_path)


### Ergebnisse ### 
titel = 'Ergebnisse'
report_pdf.chapter_titel(titel)

# Body Abbildungsbeschreibung 
body_text_path = "texte/ergebnisse22.txt"
report_pdf.body_from_txt(body_text_path)

# Figure 2
figure_caption = """Abb. 2: Zusammenhang zwischen Außentemperatur und Heizenergiebedarf in 
Abhängigkeit vom Baujahr."""
#report_pdf.figure2(, figure_caption, 120)
caption_text = """Zusammenhang zwischen Außentemperatur und Heizenergiebedarf in 
Abhängigkeit vom Baujahr."""
report_pdf.figure3("plots/scatter_plot_Heating_Energy.jpg", "Abb. 4: ", caption_text, 120)
body_text_path = "texte/ergebnisse22teil2.txt"
report_pdf.body_from_txt(body_text_path)


text = r"""
$\frac{H \cdot \cos\left( a \cdot \pi \frac{(t - t_0)}{b \cdot T} \right) + H}{2}$
wobei:
- H: mittlere Heizenergie bei t0,
- t0: Außenteperatur bei maximaler Heizenergie,
- T: änderung der Außentemperatur  
- t: Außentemperatur
- a: freier Parameter 
- b: freier Parameter 
"""
report_pdf.body2(text)

body_text_path = "texte/ergebnisse32.txt"
report_pdf.body_from_txt(body_text_path)



# Figure 3
figure_caption = "Stochastischer Simulationsansatz basierend auf der Cosinus-Funktion."
report_pdf.figure3("plots/cosinus_with_noise.jpg", "Abb. 5: ", figure_caption, 120)
body_text_path = "texte/ergebnisse42.txt"
report_pdf.body_from_txt(body_text_path)




### Diskusion ###
titel = 'Diskussion'
report_pdf.chapter_titel(titel)
body_text_path = "texte/diskusion.txt"
report_pdf.body_from_txt(body_text_path)

# Tabelle
caption = "Abweichungen der stochastischen Simulation von den berechneten Daten unter Verwendung der Cosinus-Funktion mit beiden freien Parametern gleich 2."
TABLE_DATA = (
    ("Temperatur [°C]", "Abweichung andere J [%]", "Abweichung 2000 [%]"),
    ("-10°C bis -5°C", "3,67", "3,30"),
    ("-5°C bis 0°C", "3,14", "3,57"),
    ("0°C bis 5°C", "15,32", "19,33"),
    ("5°C bis 10°C", "22,76", "30,86"),
    ("-0°C bis 15°C", "27,37", "44,82"),
    ("15°C bis 20°C", "84,01", "127,02"),
    ("20°C bis 25°C", "84,71", "219,27"),
    ("25°C bis 30°C", "212,48", "476,15"),
    ("30°C bis 35°C", "-unendlich", "-unendlich"), 
    ("35°C bis 40°C", "-unendlich", "-unendlich"),
    ("-10°C bis 40°C", "56", "115")
)
report_pdf.add_table2(TABLE_DATA, "Tab. 1: ", caption)
body_text_path = "texte/diskusion3.txt"
report_pdf.body_from_txt(body_text_path)

# Figure 4 
figure_caption = "Eine Itteration der stochastische Simulation des Heizenergiebedarfs bei Verwendung der linearen Funktion."
report_pdf.figure2("plots/stochastic_sim.jpg", "Abb. 8: ", figure_caption, 120)
body_text_path = "texte/diskusion4.txt"
report_pdf.body_from_txt(body_text_path)





# Fazit 
titel = 'Fazit'
report_pdf.chapter_titel(titel)
body_text_path = "texte/ausblick.txt"
report_pdf.body_from_txt(body_text_path)

# Quellen  
titel = 'Quellen'
report_pdf.chapter_titel(titel)
body_text_path = "texte/quellen3.txt"
report_pdf.body_from_txt(body_text_path)
#titel = 'Quellen'
#report_pdf.chapter_titel(titel)
#body_text_path = "texte/quellen.txt"
#text_quellen = report_pdf.quellen_from_csv('Report_Tool/Quellen.ods')
#print(text_quellen)
#report_pdf.body(text_quellen)





report_pdf.output('report2.pdf')
