import re
import os

from typus import ru_typus
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import ParagraphStyle
from pdf2image import convert_from_path

TEXT_LIMIT = 2200
WIDTH = 48
LINES = 18

LINEBREAK_SYMBOL = "\U00102800"
CAROUSEL_SYMBOL = "\U0010FE0F"

# WATERMARK = 'by LikeUp.me'
WATERMARK = ''


class Renderer:

    def __init__(self):
        self.caruosel_send = "\n\nПродолжение в карусели "

    def _get_chunks(self, lines):
        for i in range(0, len(lines), LINES):
            yield lines[i:i + LINES]

    def preprocess(self, text):

        text = ru_typus(text)

        regrex_pattern = re.compile(pattern="["
                                            u"\U0001F600-\U0001F64F"  # emoticons
                                            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                            u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                            u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                            "]+", flags=re.UNICODE)
        text = regrex_pattern.sub(r'', text)

        return text

    def _get_chunk_pos(self, text, allowed_length):

        last_linebreak_pos = None
        last_stop_pos = None
        last_space_pos = None

        for i in range(allowed_length, allowed_length - 100, -1):
            character = text[i]
            if character == "\n":
                last_linebreak_pos = i
            if character == ".":
                last_stop_pos = i
            if character == " " and not last_space_pos:
                last_space_pos = i

        if last_linebreak_pos:
            chunk_pos = last_linebreak_pos
        elif last_stop_pos:
            chunk_pos = last_stop_pos + 2
        elif last_space_pos:
            chunk_pos = last_space_pos + 1
        else:
            chunk_pos = allowed_length

        return chunk_pos

    def _draw_pictures(self, text):

        image_name = "picture"

        pdfmetrics.registerFont(TTFont('DejaVuSans', 'DejaVuSans.ttf'))
        styleN = ParagraphStyle(name='Normal', fontName='DejaVuSans', fontSize=10, spaceAfter=6)

        story = []

        pdf_name = f'{image_name}.pdf'
        doc = SimpleDocTemplate(
            pdf_name,
            pagesize=(10*cm, 10*cm),
            bottomMargin=0.7*cm,
            topMargin=0.7*cm,
            rightMargin=0.8*cm,
            leftMargin=0.8*cm)

        text = text.split("\n")
        text = [p for p in text if p]

        for p in text:
            P = Paragraph(p, styleN)
            story.append(P)

        doc.build(
            story,
        )

        images = convert_from_path(f'{image_name}.pdf')
        dir_path = os.path.dirname(os.path.realpath(__file__))
        image_paths = []
        for it, image in enumerate(images):
            image_path = dir_path + f"{image_name}_{it}.jpeg"
            image.save(image_path, "JPEG")
            image_paths.append(image_path)

        return image_paths

    def render(self, text):

        linebreak = "\n" + LINEBREAK_SYMBOL + "\n"
        text.replace("\n\n", linebreak)

        if len(text) < TEXT_LIMIT:
            return text, None

        carousel_text = self.caruosel_send + CAROUSEL_SYMBOL
        allowed_length = TEXT_LIMIT - len(carousel_text)

        chunk_pos = self._get_chunk_pos(text, allowed_length)

        caption = text[0:chunk_pos] + self.caruosel_send

        text = text[chunk_pos:]
        text = self.preprocess(text=text)

        image_paths = self._draw_pictures(text=text)

        return caption, image_paths
