import typing
import unittest
from datetime import datetime
from decimal import Decimal
from pathlib import Path

from borb.pdf.canvas.layout.layout_element import Alignment
from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from borb.pdf.canvas.layout.table.fixed_column_width_table import FixedColumnWidthTable
from borb.pdf.canvas.layout.text.paragraph import Paragraph
from borb.pdf.document.document import Document
from borb.pdf.page.page import Page
from borb.pdf.pdf import PDF
from tests.test_util import compare_visually_to_ground_truth


class TestRotatePage(unittest.TestCase):
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

    def test_create_document(self):

        # create document
        pdf = Document()

        # add page
        page = Page()
        pdf.append_page(page)

        # add test information
        layout = SingleColumnLayout(page)
        layout.add(
            FixedColumnWidthTable(number_of_columns=2, number_of_rows=3)
            .add(Paragraph("Date", font="Helvetica-Bold"))
            .add(Paragraph(datetime.now().strftime("%d/%m/%Y, %H:%M:%S")))
            .add(Paragraph("Test", font="Helvetica-Bold"))
            .add(Paragraph(Path(__file__).stem))
            .add(Paragraph("Description", font="Helvetica-Bold"))
            .add(
                Paragraph(
                    "This test creates a PDF with an empty Page, and a Paragraph of text. "
                    "A subsequent test will rotate a Page from this Document."
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

        # attempt to store PDF
        with open(self.output_dir / "output_001.pdf", "wb") as out_file_handle:
            PDF.dumps(out_file_handle, pdf)

        # compare visually
        compare_visually_to_ground_truth(self.output_dir / "output_001.pdf")

    def test_rotate_page_right(self):

        doc: typing.Optional[Document] = None
        with open(self.output_dir / "output_001.pdf", "rb") as in_file_handle:
            doc = PDF.loads(in_file_handle)

        assert doc is not None

        # rotate
        doc.get_page(0).rotate_right()

        # attempt to store PDF
        with open(self.output_dir / "output_002.pdf", "wb") as out_file_handle:
            PDF.dumps(out_file_handle, doc)

        # compare visually
        compare_visually_to_ground_truth(self.output_dir / "output_002.pdf")

    def test_rotate_page_left(self):

        doc: typing.Optional[Document] = None
        with open(self.output_dir / "output_001.pdf", "rb") as in_file_handle:
            doc = PDF.loads(in_file_handle)

        assert doc is not None

        # rotate
        doc.get_page(0).rotate_left()

        # attempt to store PDF
        with open(self.output_dir / "output_003.pdf", "wb") as out_file_handle:
            PDF.dumps(out_file_handle, doc)

        # compare visually
        compare_visually_to_ground_truth(self.output_dir / "output_003.pdf")
