import unittest
from datetime import datetime
from pathlib import Path

from borb.io.read.types import Decimal
from borb.pdf.canvas.color.color import HexColor
from borb.pdf.canvas.layout.image.barcode import Barcode, BarcodeType
from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from borb.pdf.canvas.layout.table.fixed_column_width_table import (
    FixedColumnWidthTable as Table,
)
from borb.pdf.canvas.layout.text.paragraph import Paragraph
from borb.pdf.document.document import Document
from borb.pdf.page.page import Page
from borb.pdf.pdf import PDF
from tests.test_util import compare_visually_to_ground_truth


class TestWriteSimpleBarcode(unittest.TestCase):
    """
    This test creates a PDF with a BarcodeType.CODE_128 barcode in yellow(ish).
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

        # create empty document
        pdf: Document = Document()

        # create empty page
        page: Page = Page()

        # add page to document
        pdf.append_page(page)

        # set layout
        layout = SingleColumnLayout(page)

        # add test information
        layout.add(
            Table(number_of_columns=2, number_of_rows=3)
            .add(Paragraph("Date", font="Helvetica-Bold"))
            .add(Paragraph(datetime.now().strftime("%d/%m/%Y, %H:%M:%S")))
            .add(Paragraph("Test", font="Helvetica-Bold"))
            .add(Paragraph(Path(__file__).stem))
            .add(Paragraph("Description", font="Helvetica-Bold"))
            .add(
                Paragraph(
                    "This test creates a PDF with a yellow-colored BarcodeType.CODE_128 barcode."
                )
            )
            .set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
        )

        # add barcode
        layout.add(
            Barcode(
                data="123456789128",
                type=BarcodeType.CODE_128,
                width=Decimal(128),
                height=Decimal(128),
                stroke_color=HexColor("f1cd2e"),
            )
        )

        # write
        file = self.output_dir / "output.pdf"
        with open(file, "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, pdf)

        # compare visually
        compare_visually_to_ground_truth(self.output_dir / "output.pdf")


if __name__ == "__main__":
    unittest.main()
