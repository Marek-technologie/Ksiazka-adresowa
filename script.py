import sys
import json
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QListWidget, QMessageBox
)

class KsiazkaAdresowa(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ksiazka Adresowa")
        self.setGeometry(100, 100, 600, 400)
        self.setStyleSheet("""
                   QWidget {
                       background-color: #0F1C2E;
                       color: white;
                       font-size: 14px;
                   }
                   QPushButton {
                       background-color: #2A3B4C;
                       color: #5DD8FF;
                       border: none;
                       padding: 8px 16px;
                       border-radius: 8px;
                   }
                   QPushButton:hover {
                       background-color: #33485C;
                   }
                   QLineEdit, QListWidget {
                       background-color: #1E2A38;
                       border: 1px solid #5DD8FF;
                       border-radius: 6px;
                       padding: 6px;
                       color: white;
                   }
               """)
        self.kontakty = []
        self.initUI()
        self.wczytaj_kontakty()

    def initUI(self):
        layout = QHBoxLayout()
        lewaKolumna = QVBoxLayout()
        prawaKolumna = QVBoxLayout()

        self.kontaktListWidget = QListWidget()
        lewaKolumna.addWidget(self.kontaktListWidget)

        self.filtrInput = QLineEdit()
        self.filtrInput.setPlaceholderText("Szukaj...")
        self.filtrInput.textChanged.connect(self.filtruj_kontakty)
        lewaKolumna.addWidget(self.filtrInput)

        self.imieInput = QLineEdit()
        self.imieInput.setPlaceholderText("Imie")
        self.nazwiskoInput = QLineEdit()
        self.nazwiskoInput.setPlaceholderText("Nazwisko")
        self.miastoInput = QLineEdit()
        self.miastoInput.setPlaceholderText("Miasto")
        self.ulicaInput = QLineEdit()
        self.ulicaInput.setPlaceholderText("Ulica")
        self.telefonInput = QLineEdit()
        self.telefonInput.setPlaceholderText("Telefon")

        for field in [self.imieInput, self.nazwiskoInput, self.miastoInput, self.ulicaInput, self.telefonInput]:
            prawaKolumna.addWidget(field)

        self.dodajButton = QPushButton("Dodaj kontakt")
        self.dodajButton.clicked.connect(self.dodaj_kontakt)
        prawaKolumna.addWidget(self.dodajButton)

        self.edytujButton = QPushButton("Edytuj kontakt")
        self.edytujButton.clicked.connect(self.edytuj_kontakt)
        prawaKolumna.addWidget(self.edytujButton)

        self.usunButton = QPushButton("Usun kontakt")
        self.usunButton.clicked.connect(self.usun_kontakt)
        prawaKolumna.addWidget(self.usunButton)

        layout.addLayout(lewaKolumna, 2)
        layout.addLayout(prawaKolumna, 3)
        self.setLayout(layout)

    def dodaj_kontakt(self):
        kontakt = self.pobierz_dane_z_formularza()
        if kontakt:
            self.kontakty.append(kontakt)
            self.zapisz_kontakty()
            self.wyczysc_formularz()
            self.filtruj_kontakty()

    def edytuj_kontakt(self):
        indeks = self.kontaktListWidget.currentRow()
        if indeks < 0:
            return
        kontakt = self.pobierz_dane_z_formularza()
        if kontakt:
            self.kontakty[indeks] = kontakt
            self.zapisz_kontakty()
            self.wyczysc_formularz()
            self.filtruj_kontakty()

    def usun_kontakt(self):
        indeks = self.kontaktListWidget.currentRow()
        if indeks >= 0:
            del self.kontakty[indeks]
            self.zapisz_kontakty()
            self.filtruj_kontakty()

    def pobierz_dane_z_formularza(self):
        imie = self.imieInput.text()
        nazwisko = self.nazwiskoInput.text()
        miasto = self.miastoInput.text()
        ulica = self.ulicaInput.text()
        telefon = self.telefonInput.text()

        if not imie or not nazwisko or not miasto or not telefon:
            QMessageBox.warning(self, "Blad", "Wymagane: Imie, Nazwisko, Miasto, Telefon")
            return None

        return {
            "imie": imie,
            "nazwisko": nazwisko,
            "miasto": miasto,
            "ulica": ulica,
            "telefon": telefon
        }

    def filtruj_kontakty(self):
        filtr = self.filtrInput.text().lower()
        self.kontaktListWidget.clear()
        for kontakt in self.kontakty:
            tekst = f"{kontakt['imie']} {kontakt['nazwisko']} - {kontakt['miasto']}, {kontakt['ulica']} - tel: {kontakt['telefon']}"
            if filtr in tekst.lower():
                self.kontaktListWidget.addItem(tekst)

    def wyczysc_formularz(self):
        for pole in [self.imieInput, self.nazwiskoInput, self.miastoInput, self.ulicaInput, self.telefonInput]:
            pole.clear()

    def zapisz_kontakty(self):
        try:
            with open("kontakty.json", "w", encoding="utf-8") as f:
                json.dump(self.kontakty, f, ensure_ascii=False, indent=2)
        except Exception as e:
            QMessageBox.critical(self, "Blad zapisu", str(e))

    def wczytaj_kontakty(self):
        if os.path.exists("kontakty.json"):
            try:
                with open("kontakty.json", "r", encoding="utf-8") as f:
                    self.kontakty = json.load(f)
                self.filtruj_kontakty()
            except Exception as e:
                QMessageBox.critical(self, "Blad odczytu", str(e))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = KsiazkaAdresowa()
    window.show()
    sys.exit(app.exec_())
