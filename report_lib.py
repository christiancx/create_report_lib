# -*- coding: utf-8 -*-
"""
Created on Thu Jan 11 09:17:12 2024

@author: Christian
"""



from fpdf import FPDF
from PIL import Image
import re
from odf.opendocument import load
from odf.table import Table, TableRow, TableCell
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import numpy as np




class reportPDF(FPDF):

    def __init__(self,  titel, author, author_info, date, logo = "Bauhaus_logo_b.png"):
        super().__init__(unit='mm', format=(210, 297))  # Hochvormat für DIN A4
        self.cover_called = 0
        self.set_titel(titel)
        self.set_author(author)
        self.set_author_info(author_info)
        self.set_left_margin(30)
        self.set_right_margin(35)
        self.set_auto_page_break(auto = True, margin = 20)
        self.set_logo() 
        self.set_date(date)
        self.chapter_links = []

    def set_titel(self, titel):
        self.titel = titel

    def set_author(self, author):
        self.author = author

    def set_logo(self):
        self.logo = "Report_Tool/Bauhaus_logo_b.png"  # Speichere den Pfad zu deinem Logo als Attribut

    def set_author_info(self, author_info):
        self.author_info = author_info

    def set_date(self, date):
        self.date = date

    def set_last_page(self, page):
        self.last_page = page


    def cover(self, logo):

        # Set cover_called to 1 when cover method is called
        self.cover_called = 1

        self.add_page()

        # Set background color
        self.set_fill_color(183, 26, 72)  # RGB color code: R0_G107_B148
        self.rect(0, 0, self.w, self.h, 'F')  # Fill the entire page with the background color

        # Open the image file
        img = Image.open(logo)
        
        # Define the maximum width and height for the logo
        max_width = 100  # Adjust as needed
        max_height = 100  # Adjust as needed
        
        # Calculate the new width and height while maintaining aspect ratio
        width_ratio = max_width / img.width
        height_ratio = max_height / img.height
        scale_factor = min(width_ratio, height_ratio)
        new_width = int(img.width * scale_factor)
        new_height = int(img.height * scale_factor)
        
        # Calculate the position to center the image horizontally and vertically
        x_pos = (self.w - new_width) / 2
        y_pos = (self.h - new_height) / 2
        
        # Insert the image with the new size
        self.image(logo, x_pos, y_pos, new_width, new_height)
    

    def header(self): 

        # Schriftfarbe setzen (rgb(127, 127, 127) entspricht #7F7F7F)
        self.set_text_color(127, 127, 127)
        # Linie (Strich) Farbe setzen
        self.set_draw_color(127, 127, 127)  
        
        # Margin von 1 cm (10 mm)
        margin_top = 16  # 1 cm in mm
        
        # Logo auf der rechten Seite des Headers, 14 cm (140 mm) von oben
        logo_x = 210 - 35 - 49  # Gesamtbreite (210 mm) - Abstand vom rechten Rand (20 mm) - Logo-Breite (60 mm)
        logo_y = margin_top   # 14 cm (140 mm) unterhalb des oberen Rands
        self.image(self.logo, logo_x+1, logo_y+1, 49)
        
        # Schriftart auf Arial, Kursiv, Größe 9
        self.set_font('Arial', '', 9)
        
        # Der Text startet 10 mm unter dem oberen Rand (nach dem Margin)
        text_y = margin_top   # Der Text soll 5 mm unterhalb des Margins starten
        
        # Titel mit Strich anstelle von Rahmen, rechtsbündig, auf drei Zeilen aufgeteilt
        self.set_xy(29, text_y)  # Setze den Textbeginn auf 30 mm von links und 10 mm von oben
        self.cell(0, 4, "Bauhaus-Universität Weimar", ln=True, align='L')  # Erste Zeile
        self.set_xy(29, text_y+4)
        self.cell(0, 4, "Fakultät Bau- und Umweltingenieurwissenschaften", ln=True, align='L')  # Zweite Zeile
        self.set_xy(29, text_y+8)
        self.cell(0, 4, "Studiengang Master Management Bau und Infrastruktur", ln=True, align='L')  # Dritte Zeile

        # Linienstärke anpassen (z.B. auf 0.3 mm)
        self.set_line_width(0.2)  
        # Strich anstelle des Rahmens
        self.line(30, 15 + 14, 175, 15 + 14)  # Position des Strichs nach 14 cm

        # Zeilenumbruch
        self.ln(15)


    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', '', 9)

        # Check if it's the first page
        if self.page_no() == 1 and self.cover_called == 1:
        # Change text color for the first page
            self.set_text_color(183, 26, 72)  # Red color for text
            
        else:
        # Reset text color for subsequent pages
            self.set_text_color(0, 0, 0)  # Black color for text
            self.set_text_color(127, 127, 127)



        if self.cover_called == 1: 
            total_pages = self.page_no() - 1  # Total pages excluding cover
            total_pages = '{nb}'
        else: total_pages = '{nb}'

        # Page number
        page_number = str(self.page_no() ) if hasattr(self, 'cover_called') else str(self.page_no())

        self.cell(0, 10, f'Seite {page_number}/{total_pages}', new_x='right', new_y='top', align='C')

        
    def titel_page(self, row1, row2, row3):
        # Add a page for the titel
        self.add_page()
        self.ln(40)  # Add some vertical space
        # Set font for titel
        self.set_font('Arial', 'B', 18)
        # Titel
        self.cell(0, 10, row1, new_x='right', new_y='top', align='C')
        self.ln(20)
        self.cell(0, 10, row2, new_x='right', new_y='top', align='C')
        self.ln(20)
        self.cell(0, 10, row3, new_x='right', new_y='top', align='C')
        self.ln(20)
        self.ln(20)  # Add some vertical space
        # Set font for author and date
        self.set_font('Arial', '', 11)
        # Author
        self.cell(0, 10, 'Von ' + self.author, new_x='right', new_y='top', align='C')
        self.ln(20)  # Add some vertical space
        # Author information
        self.cell(0, 10, self.author_info,new_x='right', new_y='top', align='C')
        self.ln(20)  # Add some vertical space
        # Date
        self.cell(0, 10, 'Veröffentlich am ' + self.date, align='C')
        self.ln(20)  # Add some vertical space
        # Add some more vertical space
        self.ln(20)
        

    def add_chapter(self, title, p=2):
        """ Fügt einen Link für den Kapitel-Titel hinzu und speichert ihn """
        link = self.add_link(page=p)  # Erzeugt einen internen Link
        self.chapter_links.append((title, link))  # Speichert den Titel und Link
        return link  # Gibt den Link zurück, damit er im Kapitel verwendet werden kann

    def table_of_contents(self):
        """ Erstellt die Gliederung mit den internen Links """
        self.add_page()
        self.set_font('Arial', '', 18)
        self.cell(0, 10, 'Inhaltsverzeichnis', ln=True, align='L')
        self.ln(10)
        
        # Durchläuft alle gespeicherten Links und erstellt die Gliederung
        self.set_font('Arial', '', 18)
        for title, link in self.chapter_links:
            self.cell(0, 10, title, ln=True, link=link)
            self.ln(1)

    
        
    def chapter_titel(self, title, link_index=None):
        """ Fügt den Kapitel-Titel hinzu und speichert den Link mit tatsächlicher Seitenzahl """
        self.add_page()
        self.set_font('Arial', '', 18)

        # Add the chapter title with a link
        if link_index is not None:
            current_page = self.page_no()  # Get the current page number
            link = self.add_link(page=current_page)
            self.chapter_links[link_index] = (title, link)
            self.cell(0, 10, title, ln=True, align='L', link=link)
        else:
            self.cell(0, 10, title, ln=True, align='L')


    def chapter_titel2(self, title, link=None):
        """ Fügt den Kapitel-Titel hinzu und speichert den Link """
        self.set_font('helvetica', '', 14)
        #self.set_font('helvetica', 'BU', 14)
        self.set_x(20)
        self.ln(5)
        # Wenn der link vorhanden ist, wird er als interner Link gesetzt
        if link:
            self.cell(0, 10, title, ln=True, align='L', link=link)
        else:
            self.cell(0, 10, title, ln=True, align='L')



    def body(self, text):
        # Set font for body text
        self.set_font('Arial', '', 11)

        # Add body text
        self.multi_cell(0, 6, text)

        # Add some vertical space after the body text
        #self.ln(10)



    def body2(self, text):
        # Set font for body text
        self.set_font('Arial', '', 11)

        texts_formulas = re.split(r'(\$.*?\$)', text)

        for item in texts_formulas:
            if item.startswith("$") and item.endswith("$"):
                # Wenn das Element eine Formel ist
                self.formula3(item)

            else:
                # Wenn das Element ein Text ist
                self.body(item)



    def formula3(self, formula):
        # Set font for body text
        self.set_font('Arial', '', 11)
        self.set_auto_page_break(auto=True, margin=18)
        
        # Create figure with larger size
        fig = Figure(figsize=(18, 2), dpi=200)  # Größere Fläche für mehr Platz
        gca = fig.gca()
        
        
        x_position = 0.4  # X-Position in der Mitte (0.5 = Mitte von 0 bis 1 auf der Achse)
        y_position = 0.5  # Y-Position in der Mitte der Höhe
        
        # Den Text zentrieren und vergrößern (Schriftgröße 48, aber anpassbar)
        gca.text(x_position, y_position, formula, fontsize=52, ha='center', va='center')
        
        # Achsen ausschalten, da wir nur den Text sehen wollen
        gca.axis("off")
        
        # Zeichne die Grafik auf dem Canvas
        canvas = FigureCanvas(fig)
        canvas.draw()
        
        # Konvertiere die Grafik in ein Bild
        img = Image.fromarray(np.asarray(canvas.buffer_rgba()))
        
        # Füge das Bild in das PDF ein
        self.image(img, w=170)


    def body_from_txt(self, file_path):
        # Set font for body text
        self.set_font('Arial', '', 11)
        self.ln(5)

        # Read the content of the text file
        try:
            with open(file_path, 'r', encoding='utf-8') as file:

                text_content = file.read()
                #  Add body text with modified line spacing
                self.multi_cell(0, 8, text_content)  # Adjust the second parameter as neede
        except FileNotFoundError:
            print(f"Error: File not found - {file_path}")
        except Exception as e:
            print(f"Error reading file: {e}")
        


    def figure(self, image_path, caption):
        
        self.ln(5)
        #self.add_page()
        # Set font for body text
        self.set_font('Arial', '', 11)
        # Check if there is enough space on the current page for the figure
        if (self.h - self.get_y()) < 180:  # Adjust 190 based on the height needed for the figure and caption
            self.add_page()  # Start a new page if there isn't enough space
        # Insert figure
        self.image(image_path, x=20, y=self.get_y() + 10, w=145)
        # Add caption
        self.set_font('Arial', 'I', 11)
        self.cell(0, 10, caption, new_x='right', new_y='top', align='L')
        self.ln(120) #190

    def figure2(self, image_path, caption_prefix, caption_text, image_height):
        # Set font for body text
        self.set_font('Arial', '', 11)
        
        # Check if there is enough space on the current page for the figure
        if (self.h - self.get_y()) < 180:  # Adjust based on the height needed for the figure and caption
            self.add_page()  # Start a new page if there isn't enough space
        
        # Insert figure
        self.image(image_path, x=30, y=self.get_y() , w=145)
        
        # Position for the Caption (below the image)
        caption_y = self.get_y() + image_height - 20
        
        self.set_font('Arial', '', 11)  # Italics for the prefix "Abb. xy:"
        self.set_xy(30, caption_y)  # Position for the caption prefix
        self.cell(0, 10, caption_prefix, align='L')  # Left-aligned caption prefix
        
        # Now the description part (with indentation)
        self.set_font('Arial', '', 11)  # Regular font for the description text
        description_y = self.get_y() + 1  # Slightly below the prefix to align correctly
        
        self.set_xy(46, description_y)  # Indent the description (offset by 10 units)
        self.multi_cell(0, 8, caption_text)  # Wrap the description text
        
        self.ln(5)  # Add some space after the caption

    def figure3(self, image_path, caption_prefix, caption_text, image_height):
        # Set font for body text
        self.set_font('Arial', '', 11)
        
        # Check if there is enough space on the current page for the figure
        #if (self.h - self.get_y()) < 180:  # Adjust based on the height needed for the figure and caption
        #    self.add_page()  # Start a new page if there isn't enough space
        
        # Insert figure
        self.image(image_path, x=30, y=self.get_y() , w=145)
        
        # Position for the Caption (below the image)
        caption_y = self.get_y() + image_height - 20
        
        self.set_font('Arial', '', 11)  # Italics for the prefix "Abb. xy:"
        self.set_xy(30, caption_y)  # Position for the caption prefix
        self.cell(0, 10, caption_prefix, align='L')  # Left-aligned caption prefix
        
        # Now the description part (with indentation)
        self.set_font('Arial', '', 11)  # Regular font for the description text
        description_y = self.get_y() + 1  # Slightly below the prefix to align correctly
        
        self.set_xy(46, description_y)  # Indent the description (offset by 10 units)
        self.multi_cell(0, 8, caption_text)  # Wrap the description text
        
        self.ln(5)  # Add some space after the caption



    def quellen_from_calc(self, calc_file_path):
        # Lade das Calc-Dokument (ODS-Datei)
        doc = load(calc_file_path)

        # Suche nach der ersten Tabelle im Calc-Dokument
        table = doc.getElementsByType(Table)[0]  # Nimmt die erste Tabelle im Dokument

        # String für den gesamten Text
        text_content = ""

        # Gehe jede Zeile in der Tabelle durch (überspringe die erste Zeile)
        for i, row in enumerate(table.getElementsByType(TableRow)):
            # Überspringe die erste Zeile mit den Überschriften
            if i == 0:
                continue

            row_text = []

            # Gehe jede Zelle in der Zeile durch
            for idx, cell in enumerate(row.getElementsByType(TableCell)):
                cell_text = ""
                # Durchlaufe alle Kindknoten der Zelle und extrahiere den Text
                for node in cell.childNodes:
                    # Prüfen, ob der Knoten ein Textknoten ist
                    if node.nodeType == node.TEXT_NODE:
                        cell_text += node.data.strip()

                # Debugging: Ausgabe des Texts, um zu sehen, was extrahiert wird
                print(f"Zelle {idx} Text: {cell_text}")

                # Füge den Text der Zelle zur Zeilenliste hinzu, falls er nicht leer ist
                if cell_text.strip():  # Nur hinzufügen, wenn der Text nicht leer ist
                    row_text.append(cell_text)

            # Wenn wir eine neue Zeile haben, erstellen wir den Text:
            if row_text:
                number = row_text[0]  # Die Nummer (erste Zelle)
                data = ', '.join(row_text[1:])  # Die anderen Werte mit Komma trennen
                text_content += f"{number} {data}\n"

        # Rückgabe des gesamten Texts
        return text_content

    def quellen_from_csv(self, csv_file_path):
        # Lade die CSV-Datei in ein DataFrame
        df = pd.read_csv(csv_file_path)

        # String für den gesamten Text
        text_content = ""

        # Gehe durch jede Zeile des DataFrames (ab der zweiten Zeile, um die Überschrift zu überspringen)
        for _, row in df.iloc[1:].iterrows():
            # Extrahiere die Werte der Zeile
            number = row['Nummer']  # Die erste Spalte enthält die Nummer (z.B. [1])
            author = row['Autoren']  # Die zweite Spalte enthält den Autor
            title = row['Titel']  # Die dritte Spalte enthält den Titel
            journal = row['Zeitschrift/Verlag']  # Die vierte Spalte enthält die Zeitschrift oder den Verlag
            date = row['Datum']  # Die fünfte Spalte enthält das Datum

            # Erstelle die formatierte Zeile: [Nummer] Autor, Titel, Zeitschrift, Datum
            formatted_row = f"{number} {author}, {title}, {journal}, {date}"
            text_content += formatted_row + "\n"

        # Rückgabe des gesamten Texts
        return text_content   

    def add_table2(self, data, caption_prefix, caption_text, row_height=10, border=1, align="C", header_bg_color=(183, 26, 72), text_color=(255, 255, 255)):
        """
        Fügt eine Tabelle innerhalb eines festen Bereichs von 20 bis 60 mm hinzu.
        Setzt die Hintergrundfarbe der ersten Spalte (Überschriften).

        :param data: Eine Liste von Tupeln, die die Tabellenzeilen enthalten
        :param row_height: Die Höhe jeder Zeile (default 10)
        :param border: Der Rand der Zellen (default 1)
        :param align: Der Textausrichtungswert (default 'C' für Center)
        :param header_bg_color: Hintergrundfarbe der Kopfzeile (default: Blau)
        :param text_color: Textfarbe für die Kopfzeile (default: Weiß)
        """
        # Definiere den Bereich für die Tabelle
        left_margin = 30
        right_margin = 175
        table_width = right_margin - left_margin  # Die Breite des Tabellenbereichs

        col_count = len(data[0])  # Anzahl der Spalten in der Tabelle (Annahme, dass alle Zeilen gleich viele Spalten haben)
        
        # Berechne die Breite jeder Spalte, sodass die gesamte Tabelle den angegebenen Bereich ausfüllt
        col_widths = [table_width / col_count] * col_count  # Jede Spalte bekommt denselben Platz

        # Zuerst die Caption setzen (mit entsprechender Schriftart)
        self.set_font("Arial", "", 11)  # Normale Schrift für die Caption
        self.set_xy(left_margin, self.get_y())  # Position der Caption

        # Setze den Prefix "Abb. xy:"
        self.set_font('Arial', '', 11)  # Kursiv für den Prefix
        self.cell(0, 10, caption_prefix, align="L")  # Links ausrichten

        # Setze den Beschreibungstext, etwas eingerückt
        self.set_font('Arial', '', 11)  # Normale Schrift für den Beschreibungstext
        self.set_xy(left_margin + 16, self.get_y() + 1)  # Eingerückt
        self.multi_cell(0, 8, caption_text)  # Wrap text

        # Abstand nach der Caption
        self.ln(5)  # Abstand nach der Caption

        # Setze die Schriftart für die Tabelle
        self.set_font("Arial", size=11)

        # Loop über alle Zeilen
        for row_idx, row in enumerate(data):
            # Wenn es die erste Zeile (Kopfzeile) ist, wird sie anders formatiert
            if row_idx == 0:
                self.set_font("Arial", "B", 11)  # Fett für die Kopfzeile
                self.set_fill_color(*header_bg_color)  # Setze die Hintergrundfarbe für die Kopfzeile
                self.set_text_color(*text_color)  # Setze die Textfarbe für die Kopfzeile
            else:
                self.set_font("Arial", size=11)  # Normale Schriftart für den Rest der Tabelle
                self.set_fill_color(255, 255, 255)  # Weiß für den Rest
                self.set_text_color(0, 0, 0)  # Schwarzer Text für den Rest

            # Setze die Position (ab 20 mm von links) und beginne in der aktuellen Y-Position
            self.set_xy(left_margin, self.get_y())

            # Erstelle jede Zelle in der aktuellen Zeile
            for col_idx, cell_data in enumerate(row):
                # Falls es sich um die erste Spalte handelt, setze eine spezielle Hintergrundfarbe
                if row_idx == 0:  # Nur die erste Spalte in der Kopfzeile
                    self.set_fill_color(183, 26, 72)  # Dunkelblau für die erste Spalte in der Kopfzeile
                    self.set_text_color(255, 255, 255)  # Weißer Text
                else:
                    self.set_fill_color(255, 255, 255)  # Weiß für den Rest der Zellen
                    self.set_text_color(0, 0, 0)  # Schwarzer Text

                # Die Zelle erstellen
                self.cell(col_widths[col_idx], row_height, str(cell_data), border=border, align=align, fill=True)

            # Zeilenumbruch nach jeder Zeile
            self.ln(row_height)
        
 








class presentationPDF(FPDF):

    def __init__(self, titel, author):
        super().__init__(unit='mm', format=(297, 210))  # Querformat für DIN A4
        #self.alias_nb_pages()
        self.set_titel(titel)
        self.set_author(author)
        self.set_left_margin(20)
        self.set_right_margin(20)
        self.set_auto_page_break(auto = True, margin = 20)
        self.cover_called = 0
        
        

    def spellcheck_markdown_file(self, filename):
        # LanguageTool-Objekt initialisieren
        tool = language_tool_python.LanguageTool('de')

        # Markdown-Datei öffnen und den Text einlesen
        with open(filename, 'r', encoding='utf-8') as file:
            text = file.read()

        # Spellchecking
        matches = tool.check(text)

        # Durchlauf der Fehler und Ausgabe der Vorschläge
        for match in matches:
            print(f"Fehler in Zeile {match.line}: {match.message} Vorschläge: {match.replacements}")


    def cover(self, logo_path):

        # Set cover_called to 1 when cover method is called
        self.cover_called = 1

        self.add_page()

        # Set background color
        self.set_fill_color(0, 107, 148)  # RGB color code: R0_G107_B148
        self.rect(0, 0, self.w, self.h, 'F')  # Fill the entire page with the background color

        # Open the image file
        img = Image.open(logo_path)
        
        # Define the maximum width and height for the logo
        max_width = 100  # Adjust as needed
        max_height = 100  # Adjust as needed
        
        # Calculate the new width and height while maintaining aspect ratio
        width_ratio = max_width / img.width
        height_ratio = max_height / img.height
        scale_factor = min(width_ratio, height_ratio)
        new_width = int(img.width * scale_factor)
        new_height = int(img.height * scale_factor)
        
        # Calculate the position to center the image horizontally and vertically
        x_pos = (self.w - new_width) / 2
        y_pos = (self.h - new_height) / 2
        
        # Insert the image with the new size
        self.image(logo_path, x_pos, y_pos, new_width, new_height)

        
    
    def header(self):
        # Logo
        self.image(self.logo, 20, 14, 20)
        # Arial bold 15
        self.set_font('Arial', 'I', 8)
        # Titel
        self.cell(0, 20, titel, border=1, align='C')
        # Date in the top right corner
        self.set_xy(-50, 8)
        #self.cell(0, 10, date, ln=False, align='R')
        self.cell(0, 10, date, new_x='right', new_y='top', align='R')
        # Author information in the bottom right corner
        self.set_xy(-50, 22)
        #self.cell(0, 10, author_info, ln=False, align='R')
        self.cell(0, 10, author_info, new_x='right', new_y='top', align='R')
        # Line break
        self.ln(15)


    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)

        # Check if it's the first page
        if self.page_no() == 1 and self.cover_called == 1:
        # Change text color for the first page
            self.set_text_color(0, 107, 148)  # Red color for text
        else:
        # Reset text color for subsequent pages
            self.set_text_color(0, 0, 0)  # Black color for text



        if self.cover_called == 1: 
            total_pages = self.page_no() - self.cover_called  # Total pages excluding cover

        else: total_pages = '{nb}'

        # Page number
        page_number = str(self.page_no() - self.cover_called) if hasattr(self, 'cover_called') else str(self.page_no())

        self.cell(0, 10, f'Page {page_number}/{total_pages}', new_x='right', new_y='top', align='C')


    def titel_page(self, titel, author, date):
        # Add a page for the titel
        self.add_page()
        # Set font for titel
        self.set_font('Arial', 'B', 40)
        self.ln(30)  # Add some vertical space
        # Titel
        #self.cell(0, 10, titel, new_x='right', new_y='top', align='C')
        self.multi_cell(0, 20, titel, new_x='right', new_y='top', align='C')
        self.ln(20)  # Add some vertical space
        # Set font for author and date
        self.set_font('Arial', '', 11)
        # Author
        self.cell(0, 10, 'By ' + author, new_x='left', new_y='next', align='C')
        self.ln(20)  # Add some vertical space
        # Author information
        self.cell(0, 10, author_info, new_x='left', new_y='next', align='C')
        self.ln(20)  # Add some vertical space
        # Date
        #self.cell(0, 10, 'Published on ' + date, new_x='right', new_y='next', align='C')
        self.ln(20)  # Add some vertical space
        # Add some more vertical space
        self.ln(20)
    

    def chapter_titel(self, titel):
        # Add a new page for the chapter titel
        self.add_page()
        # Set font for chapter titel
        self.set_font('Arial', 'B', 26)
        # Chapter titel
        #self.cell(0, 10, titel, ln=True, align='L')
        self.cell(0, 10, titel, new_x='right', new_y='next', align='L')
        # Add some vertical space
        self.ln(5)
        
    def body(self, text):
        # Set font for body text
        self.set_font('Arial', '', 11)

        
        # Add body text
        self.multi_cell(0, 6, text)

        # Add some vertical space after the body text
        self.ln(10)
       

    def body_from_markdown(self, markdown_file): 

        self.set_auto_page_break(auto = True, margin = 20)

        with open(markdown_file, 'r', encoding='utf-8') as file:
            markdown_content = file.read()
        
        # Convert Markdown to HTML
        html_content = markdown.markdown(markdown_content)
        
        # Set font for body text
        self.set_font('Arial', '', 11)
        
        # Add HTML content to the body
        self.write_html(html_content)
        
        # Add some vertical space after the body text
       
        self.ln(10)



    def figure(self, image_path, caption):
        
        # Insert figure
        self.ln(8)
        self.image(image_path, x=45, y=self.get_y() + 10, w=190)

        # Add caption
        self.set_font('Arial', 'I', 11)
        self.cell(4, 2, ' ' + caption, new_x='right', new_y='next', align='L')


    def body_from_txt(self, file_path):
        # Set font for body text
        self.set_font('Arial', '', 11)

        # Read the content of the text file
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                text_content = file.read()

            #  Add body text with modified line spacing
            self.multi_cell(0, 8, text_content)  # Adjust the second parameter as needed

            # Add some vertical space after the body text
            self.ln(10)
        except FileNotFoundError:
            print(f"Error: File not found - {file_path}")
        except Exception as e:
            print(f"Error reading file: {e}")

    
