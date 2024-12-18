import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, QTableWidget, QTableWidgetItem
from PIL import Image

class FolderSelector(QWidget):
    def __init__(self):
        super().__init__()
        
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.btn = QPushButton('Выбрать папку', self)
        self.btn.clicked.connect(self.showDialog)
        
        self.label = QLabel('Папка не выбрана', self)

        layout.addWidget(self.btn)  
        layout.addStretch(1)         
        layout.addWidget(self.label)  
        
        self.table = QTableWidget(self)
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(['Имя файла', 'Размер (пиксели)', 'Разрешение (dpi)', 'Глубина цвета', 'Сжатие'])
        layout.addWidget(self.table)
        
        self.setLayout(layout)
        
        self.setWindowTitle('Выбор папки')
        self.setGeometry(300, 300, 800, 600)
        self.show()

    def showDialog(self):
        folder = QFileDialog.getExistingDirectory(self, 'Выберите папку')

        if folder:
            self.label.setText(f'Вы выбрали: {folder}')
            self.loadImages(folder)
        else:
            self.label.setText('Папка не выбрана')

    def loadImages(self, folder):
        files = os.listdir(folder)

        image_files = [f for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff'))]

        self.table.setRowCount(len(image_files))

        for row, image_file in enumerate(image_files):
            file_path = os.path.join(folder, image_file)

            with Image.open(file_path) as img:
                self.table.setItem(row, 0, QTableWidgetItem(image_file))

                size = f"{img.width} x {img.height}"
                self.table.setItem(row, 1, QTableWidgetItem(size))

                dpi = img.info.get('dpi', (72, 72)) 
                self.table.setItem(row, 2, QTableWidgetItem(f"{dpi[0]} x {dpi[1]}"))

                # Для глубины цвета используем mode и количество каналов
                color_depth = self.get_color_depth(img)
                self.table.setItem(row, 3, QTableWidgetItem(color_depth))

                # Сжатие можно попробовать анализировать для форматов JPEG и PNG
                compression = self.get_compression(img, image_file)
                self.table.setItem(row, 4, QTableWidgetItem(compression))

    def get_color_depth(self, img):
        """Определение глубины цвета"""
        mode = img.mode
        if mode == "RGB":
            return "24 бит (RGB)"
        elif mode == "RGBA":
            return "32 бит (RGBA)"
        elif mode == "L":
            return "8 бит (Grayscale)"
        elif mode == "1":
            return "1 бит (Black & White)"
        else:
            return "Неизвестно"

    def get_compression(self, img, image_file):
        """Попытка определить тип сжатия"""
        # Для PNG
        if image_file.lower().endswith('.png'):
            return "Без потерь (Lossless)"
        # Для JPEG
        elif image_file.lower().endswith('.jpg') or image_file.lower().endswith('.jpeg'):
            return "С потерями (Lossy)"
        else:
            return "Неизвестно"


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FolderSelector()
    sys.exit(app.exec_())
