import json
import unittest
from datetime import datetime
from decimal import Decimal
from pathlib import Path

from borb.pdf.canvas.layout.layout_element import Alignment
from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from borb.pdf.canvas.layout.table.fixed_column_width_table import (
    FixedColumnWidthTable as Table,
)
from borb.pdf.canvas.layout.text.paragraph import Paragraph
from borb.pdf.document.document import Document
from borb.pdf.page.page import Page
from borb.pdf.pdf import PDF

unittest.TestLoader.sortTestMethodsUsing = None


class TestAppendEmbeddedFile(unittest.TestCase):
    """
    This test creates a PDF with a Paragraph object in it.
    An embedded file will later be added to this PDF.
    """

    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        # find output dir
        p: Path = Path(__file__).parent
        while "output" not in [x.stem for x in p.iterdir() if x.is_dir()]:
            p = p.parent
        p = p / "output"
        self.output_dir = Path(p, Path(__file__).stem.replace(".py", ""))
        if not self.output_dir.exists():
            self.output_dir.mkdir()

    def test_write_document(self):

        # create document
        pdf = Document()

        # add page
        page = Page()
        pdf.append_page(page)

        # add test information
        layout = SingleColumnLayout(page)
        layout.add(
            Table(number_of_columns=2, number_of_rows=3)
            .add(Paragraph("Date", font="Helvetica-Bold"))
            .add(Paragraph(datetime.now().strftime("%d/%m/%Y, %H:%M:%S")))
            .add(Paragraph("Test", font="Helvetica-Bold"))
            .add(Paragraph(Path(__file__).stem))
            .add(Paragraph("Description", font="Helvetica-Bold"))
            .add(
                Paragraph(
                    "This test creates a PDF with a Paragraph object in it. An embedded file will later be added to this PDF."
                )
            )
            .set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
        )

        layout.add(
            Paragraph(
                """
            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. 
            Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. 
            Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. 
            Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
            """,
                font_size=Decimal(10),
                vertical_alignment=Alignment.TOP,
                horizontal_alignment=Alignment.LEFT,
                padding_top=Decimal(5),
                padding_right=Decimal(5),
                padding_bottom=Decimal(5),
                padding_left=Decimal(5),
            )
        )

        # determine output location
        out_file = self.output_dir / "output_001.pdf"

        # attempt to store PDF
        with open(out_file, "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)

    def test_append_binary_file(self):

        input_file: Path = self.output_dir / "output_001.pdf"
        with open(input_file, "rb") as in_file_handle:
            doc = PDF.loads(in_file_handle)

        info_dict = doc["XRef"]["Trailer"]["Info"]
        info_dict_bytes: bytes = json.dumps(
            info_dict.to_json_serializable(), indent=4
        ).encode("latin1")

        doc.append_embedded_file("embedded_data.json", info_dict_bytes)

        # determine output location
        out_file = self.output_dir / "output_002.pdf"

        # attempt to store PDF
        with open(out_file, "wb") as in_file_handle:
            PDF.dumps(in_file_handle, doc)

    def test_extract_embedded_file(self):

        input_file: Path = self.output_dir / "output_001.pdf"
        with open(input_file, "rb") as in_file_handle:
            doc = PDF.loads(in_file_handle)

        info_dict = doc["XRef"]["Trailer"]["Info"]
        info_dict_json = info_dict.to_json_serializable()

        input_file: Path = self.output_dir / "output_002.pdf"
        with open(input_file, "rb") as in_file_handle:
            doc = PDF.loads(in_file_handle)

        info_dict_json_2 = json.loads(doc.get_embedded_file("embedded_data.json"))

        for k, v in info_dict_json.items():
            assert k in info_dict_json_2
            assert v == info_dict_json_2[k]
