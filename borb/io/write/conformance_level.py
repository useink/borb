import enum


class ConformanceLevel(enum.Enum):
    """
    In turn, each PDF/A standard supports different conformance levels (a & b for PDF/A-1; and a, b & u for PDF/A-2 and -3).
    These conformance levels control the “accessibility” requirements of a file that impact the ability of machines and people to understand the content.
    """

    PDFA_1A = 2
    PDFA_1B = 3
    PDFA_2A = 5
    PDFA_2B = 7
    PDFA_2U = 11
    PDFA_3A = 13
    PDFA_3B = 17
    PDFA_3U = 19

    def get_standard(self) -> int:
        if self in [ConformanceLevel.PDFA_1A, ConformanceLevel.PDFA_1B]:
            return 1
        if self in [
            ConformanceLevel.PDFA_2A,
            ConformanceLevel.PDFA_2B,
            ConformanceLevel.PDFA_2U,
        ]:
            return 2
        if self in [
            ConformanceLevel.PDFA_3A,
            ConformanceLevel.PDFA_3B,
            ConformanceLevel.PDFA_3U,
        ]:
            return 3
        assert False

    def get_conformance_level(self) -> str:
        if self in [ConformanceLevel.PDFA_1A, ConformanceLevel.PDFA_2A]:
            return "A"
        if self in [
            ConformanceLevel.PDFA_1B,
            ConformanceLevel.PDFA_2B,
            ConformanceLevel.PDFA_3B,
        ]:
            return "B"
        if self in [ConformanceLevel.PDFA_2U, ConformanceLevel.PDFA_3U]:
            return "U"
        assert False
