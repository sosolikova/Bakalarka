from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QComboBox, QVBoxLayout
import pandas as pd

class ComboBoxes(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Dynamický výběr ze dvou comboboxů')

        self.krajCombo = QComboBox(self)
        self.mestoCombo = QComboBox(self)

        self.krajCombo.addItem('Vyberte kraj')
        for kraj in data['Evident_Kraj'].unique():
            self.krajCombo.addItem(kraj)

        self.krajCombo.currentIndexChanged.connect(self.updateMestoCombo)

        vbox = QVBoxLayout()
        vbox.addWidget(QLabel('Kraj:'))
        vbox.addWidget(self.krajCombo)
        vbox.addWidget(QLabel('Mesto:'))
        vbox.addWidget(self.mestoCombo)

        self.setLayout(vbox)
        self.show()

    def updateMestoCombo(self, index):
        self.mestoCombo.clear()
        self.mestoCombo.addItem('Vyberte mesto')
        kraj = self.krajCombo.currentText()
        for mesto in data.loc[data['Evident_Kraj'] == kraj, 'Evident_Nazev'].unique():
            self.mestoCombo.addItem(mesto)

if __name__ == '__main__':
    data = pd.read_csv('200110.csv')
    app = QApplication([])
    cb = ComboBoxes()
    app.exec_()