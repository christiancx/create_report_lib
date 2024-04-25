# -*- coding: utf-8 -*-
"""
Created on Thu Jan 11 09:17:12 2024

@author: Christian
"""
import sys
from fpdf import FPDF
import markdown
import language_tool_python
from PIL import Image


class reportPDF(FPDF):

    def __init__(self, title, author):
        super().__init__(unit='mm', format=(210, 297))  # Hochvormat für DIN A4
        self.set_auto_page_break(auto=True, margin=20)
        #self.alias_nb_pages()
        self.set_title(title)
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
        self.image(logo, 20, 14, 20)
        # Arial bold 15
        self.set_font('helvetica', 'I', 8)
        # Title
        self.cell(0, 20, title, border=1, align='C')
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
        self.set_font('helvetica', 'I', 8)

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

        
    def title_page(self, title, author, date):
        # Add a page for the title
        self.add_page()
        self.ln(40)  # Add some vertical space
        # Set font for title
        self.set_font('helvetica', 'B', 18)
        # Title
        self.cell(0, 10, title, new_x='right', new_y='top', align='C')
        self.ln(20)  # Add some vertical space
        # Set font for author and date
        self.set_font('helvetica', '', 12)
        # Author
        self.cell(0, 10, 'By ' + author, new_x='left', new_y='next', align='C')
        self.ln(20)  # Add some vertical space
        # Author information
        self.cell(0, 10, author_info, new_x='left', new_y='next', align='C')
        self.ln(20)  # Add some vertical space
        # Date
        self.cell(0, 10, 'Published on ' + date, new_x='right', new_y='next', align='C')
        self.ln(20)  # Add some vertical space
        # Add some more vertical space
        self.ln(20)
        
    def abstract_section(self, textbox1, textbox2):
        # Add a page for the abstract section
        self.add_page()
        # Add some vertical space between text boxes
        self.ln(10)
        # Set font for the abstract text
        self.set_font('helvetica', '', 12)
        # Textbox 1
        self.multi_cell(0, 10, textbox1)
        # Add some vertical space between text boxes
        self.ln(10)
        # Textbox 2
        self.multi_cell(0, 10, textbox2)

    def chapter_title(self, title):
        # Add a new page for the chapter title
        self.add_page()
        # Set font for chapter title
        self.set_font('helvetica', 'B', 16)
        # Chapter title
        #self.cell(0, 10, title, ln=True, align='L')
        self.cell(0, 10, title, new_x='right', new_y='next', align='L')
        # Add some vertical space
        self.ln(5)
        
    def body(self, text):
        # Set font for body text
        self.set_font('helvetica', '', 12)

        
        # Add body text
        self.multi_cell(0, 6, text)

        # Add some vertical space after the body text
        self.ln(10)
       

    def body_from_markdown(self, markdown_file): 

        #self.spellcheck_markdown_file(markdown_file)

        with open(markdown_file, 'r', encoding='utf-8') as file:
            markdown_content = file.read()
        
        # Convert Markdown to HTML
        html_content = markdown.markdown(markdown_content)
        
        # Set font for body text
        self.set_font('helvetica', '', 12)
        
        # Add HTML content to the body
        self.write_html(html_content)
        
        # Add some vertical space after the body text
        #pdf.ln(10)
        self.ln(10)


    def figure(self, image_path, caption):
        
        #self.add_page()
        # Set font for body text
        self.set_font('helvetica', '', 12)
        # Check if there is enough space on the current page for the figure
        if (self.h - self.get_y()) < 180:  # Adjust 190 based on the height needed for the figure and caption
            self.add_page()  # Start a new page if there isn't enough space
        # Insert figure
        self.image(image_path, x=20, y=self.get_y() + 10, w=170)
        # Add caption
        self.set_font('helvetica', 'I', 8)
        self.cell(0, 10, caption, new_x='right', new_y='next', align='L')
        self.ln(190)

    def body_from_txt(self, file_path):
        # Set font for body text
        self.set_font('helvetica', '', 12)

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
        
 

class presentationPDF(FPDF):

    def __init__(self, title, author):
        super().__init__(unit='mm', format=(297, 210))  # Querformat für DIN A4
        #self.alias_nb_pages()
        self.set_title(title)
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
        self.image(logo, 20, 14, 20)
        # Arial bold 15
        self.set_font('helvetica', 'I', 8)
        # Title
        self.cell(0, 20, title, border=1, align='C')
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
        self.set_font('helvetica', 'I', 8)

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


    def title_page(self, title, author, date):
        # Add a page for the title
        self.add_page()
        # Set font for title
        self.set_font('helvetica', 'B', 40)
        self.ln(30)  # Add some vertical space
        # Title
        #self.cell(0, 10, title, new_x='right', new_y='top', align='C')
        self.multi_cell(0, 20, title, align='C')
        self.ln(20)  # Add some vertical space
        # Set font for author and date
        self.set_font('helvetica', '', 12)
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
    

    def chapter_title(self, title):
        # Add a new page for the chapter title
        self.add_page()
        # Set font for chapter title
        self.set_font('helvetica', 'B', 26)
        # Chapter title
        #self.cell(0, 10, title, ln=True, align='L')
        self.cell(0, 10, title, new_x='right', new_y='next', align='L')
        # Add some vertical space
        self.ln(5)
        
    def body(self, text):
        # Set font for body text
        self.set_font('helvetica', '', 12)

        
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
        self.set_font('helvetica', '', 12)
        
        # Add HTML content to the body
        self.write_html(html_content)
        
        # Add some vertical space after the body text
       
        self.ln(10)



    def figure(self, image_path, caption):
        
        # Insert figure
        self.ln(8)
        self.image(image_path, x=45, y=self.get_y() + 10, w=190)

        # Add caption
        self.set_font('helvetica', 'I', 12)
        self.cell(4, 2, ' ' + caption, new_x='right', new_y='next', align='L')


    def body_from_txt(self, file_path):
        # Set font for body text
        self.set_font('helvetica', '', 12)

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

    



title = 'Small Task Mathematics for Risk Management Group: 3'
author = 'Christian '
author_info = 'myEmail@uni-weimar.de '
logo = 'Bauhaus_Logo.png'
date = 'January 11, 2024 '


    #        #
    # Report #
    #        #

report_pdf = reportPDF(title, author)

# Titel Page
report_pdf.cover(logo)
report_pdf.title_page(title, author, date)
report_pdf.set_left_margin(20)
report_pdf.set_right_margin(20)
# Abstract 
abstract_text1 = "This is the content of the first text box in the abstract."
abstract_text2 = "This is the content of the second text box in the abstract."
report_pdf.abstract_section(abstract_text1, abstract_text2)
# Chapter 1
report_pdf.chapter_title("1 Distributions")
# Body1 #
body_text = "lalalalal \nlalalalla"
report_pdf.body(body_text)
# Body2 #
body_text_path = "test.txt"
report_pdf.body_from_txt(body_text_path)
# Body3 #
report_pdf.body_from_markdown('test.md')

# Chapter 1.1
report_pdf.chapter_title("1.1 Distributions")
# Figure 1
figure_caption = "Figure 1: negative_Binomial_PMF r=8, p=0.8, x=25"
report_pdf.figure("negativBinomial_PMF_25.png", figure_caption)


report_pdf.output('report.pdf')


    #              #
    # Presentation #
    #              #

presentation_pdf = presentationPDF(title, author)

# Titel Page
presentation_pdf.cover(logo)
presentation_pdf.title_page(title, author, date)
# Abstract 
#abstract_text1 = "This is the content of the first text box in the abstract."
#abstract_text2 = "This is the content of the second text box in the abstract."
#presentation_pdf.abstract_section(abstract_text1, abstract_text2)
# Chapter 1
presentation_pdf.chapter_title("1 Distributions")
# Body1 #
body_text = "lalalalal \nlalalalla"
presentation_pdf.body(body_text)
# Body2 #
body_text_path = "test.txt"
presentation_pdf.body_from_txt(body_text_path)
# Body3 #
presentation_pdf.body_from_markdown('test.md')
# Chapter 1.1
presentation_pdf.chapter_title("1.1 Distributions")
# Figure 1
figure_caption = "Figure 1: negative_Binomial_PMF r=8, p=0.8, x=25"
presentation_pdf.figure("negativBinomial_PMF_25.png", figure_caption)



presentation_pdf.output("präsentation.pdf")