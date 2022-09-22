from fpdf import FPDF


class PDF(FPDF):
    def gambar(self, path: str) -> None:
        self.image(path, 36, 14, 22, 27)

    def judul(self, teks1: str, teks2: str, teks3: str, teks4: str, teks5: str) -> None:
        self.set_font('Times', '', 14)
        self.cell(35)
        self.cell(0, 5, teks1, 0, 1, 'C')
        self.cell(35)
        self.set_font('Times', 'B', 20)
        self.cell(0, 8, teks2, 0, 1, 'C')
        self.cell(35)
        self.set_font('Times', '', 11)
        self.cell(0, 5, teks3, 0, 1, 'C')
        self.cell(35)
        self.cell(0, 5, teks4, 0, 1, 'C')
        self.cell(35)
        self.cell(0, 5, teks5, 0, 1, 'C')
        self.cell(17)

    def garis(self):
        self.set_line_width(1)
        self.line(10, 55, 180, 55)
        self.set_line_width(0)
        self.line(10, 56, 208, 56)

    def isi(self):
        pass

    def kadis(self, jabatan, nama, tingkat, nip):
        self.set_font('Times', '', 12)
        self.Ln(4)
        self.Cell(130, 10)
        self.Cell(0, 5, jabatan, 0, 0, 'C')
        self.Ln(25)
        self.set_font('Times', 'BU', 12)
        self.Cell(130, 10)
        self.Cell(0, 5, nama, 0, 1, 'C')
        self.Cell(130, 10)
        self.set_font('Times', '', 12)
        self.Cell(0, 5, tingkat, 0, 1, 'C')
        self.Cell(130, 10)
        self.Cell(0, 5, nip, 0, 1, 'C')
        self.Ln(2)
