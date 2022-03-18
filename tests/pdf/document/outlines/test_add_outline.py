import unittest
from datetime import datetime
from decimal import Decimal
from pathlib import Path

from borb.pdf.canvas.layout.annotation.link_annotation import DestinationType
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


class TestAddOutline(unittest.TestCase):
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
                    "This test creates a PDF with a Paragraph object in it. The Paragraph is aligned TOP, LEFT. "
                    "A series of outlines will later be added to this PDF."
                )
            )
            .set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
        )

        for _ in range(0, 5):
            page = Page()
            pdf.append_page(page)
            layout = SingleColumnLayout(page)
            for _ in range(0, 3):
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

    def test_add_outline(self):

        input_file: Path = self.output_dir / "output_001.pdf"
        with open(input_file, "rb") as in_file_handle:
            doc = PDF.loads(in_file_handle)

        doc.add_outline("Lorem", 0, page_nr=0, destination_type=DestinationType.FIT)
        doc.add_outline("Ipsum", 0, page_nr=1, destination_type=DestinationType.FIT)
        doc.add_outline("Dolor", 1, page_nr=0, destination_type=DestinationType.FIT)
        doc.add_outline("Sit", 2, page_nr=1, destination_type=DestinationType.FIT)
        doc.add_outline("Amet", 3, page_nr=0, destination_type=DestinationType.FIT)
        doc.add_outline(
            "Consectetur", 3, page_nr=1, destination_type=DestinationType.FIT
        )
        doc.add_outline(
            "Adipiscing", 3, page_nr=0, destination_type=DestinationType.FIT
        )
        doc.add_outline("Elit", 1, page_nr=1, destination_type=DestinationType.FIT)

        # determine output location
        out_file = self.output_dir / "output_002.pdf"

        # attempt to store PDF
        with open(out_file, "wb") as in_file_handle:
            PDF.dumps(in_file_handle, doc)

    def test_outline_exists(self):

        input_file: Path = self.output_dir / "output_002.pdf"
        with open(input_file, "rb") as in_file_handle:
            doc = PDF.loads(in_file_handle)

        assert int(doc["XRef"]["Trailer"]["Root"]["Outlines"]["Count"]) == 8
