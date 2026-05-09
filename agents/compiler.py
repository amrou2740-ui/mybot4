from fpdf import FPDF
import arabic_reshaper
from bidi.algorithm import get_display

class Compiler:

    def ar(self, text):

        reshaped = arabic_reshaper.reshape(text)

        return get_display(reshaped)

    def compile(self, topic, chapters, images):

        pdf = FPDF()

        pdf.set_auto_page_break(
            auto=True,
            margin=15
        )

        pdf.add_font(
            "DejaVu",
            "",
            "fonts/DejaVuSans.ttf"
        )

        pdf.add_page()

        pdf.set_font("DejaVu", size=22)

        pdf.cell(
            0,
            15,
            self.ar(topic),
            new_x="LMARGIN",
            new_y="NEXT",
            align="C"
        )

        pdf.ln(10)

        for title, content in chapters.items():

            pdf.set_font("DejaVu", size=18)

            pdf.multi_cell(
                0,
                10,
                self.ar(title)
            )

            pdf.ln(4)

            pdf.set_font("DejaVu", size=12)

            pdf.multi_cell(
                0,
                8,
                self.ar(content)
            )

            pdf.ln(8)

        for img in images:

            pdf.add_page()

            pdf.image(img, w=180)

        output = "output/research.pdf"

        pdf.output(output)

        return output