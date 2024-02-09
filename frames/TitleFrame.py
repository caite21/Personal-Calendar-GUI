
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QLineEdit, QLabel, QPushButton, QFrame
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor, QPalette
from SharedData import SharedData


class TitleFrame(QFrame, SharedData):
	def __init__(self):
		super().__init__()
		# on startup, read these files
		# SharedData.get_style()
		# SharedData.get_format_data()
		# SharedData.get_event_data()
		# SharedData.get_icon_data()

		self.setFixedHeight(60)
		self.setObjectName("titleFrame")
		self.setStyleSheet(SharedData.style)
		self.style_sheet_copy = SharedData.style
		month_grid = QGridLayout()

		self.buttonL = QPushButton("<")
		self.buttonL.setObjectName("button")
		self.buttonL.setStyleSheet(SharedData.style)
		month_grid.addWidget(self.buttonL, 0, 1)

		self.title = QPushButton(f"{SharedData.cal_title}")
		self.title.setObjectName("monthTitle")
		self.title.setStyleSheet(SharedData.style)
		self.title.setToolTip('Click to set as default')
		month_grid.addWidget(self.title, 0, 2)

		self.buttonR = QPushButton(">")
		self.buttonR.setObjectName("button")
		self.buttonR.setStyleSheet(SharedData.style)
		# self.buttonR.setFixedSize(50, 30) # w, h
		month_grid.addWidget(self.buttonR, 0, 3)

		self.buttonRefresh = QPushButton("⟳")
		self.buttonRefresh.setObjectName("button")
		self.buttonRefresh.setStyleSheet(SharedData.style)
		month_grid.addWidget(self.buttonRefresh, 0, 5)
		self.buttonRefresh.setToolTip('Refresh')

		free_label = QLabel(f"<b> <b>")
		month_grid.addWidget(free_label, 0, 6)
		free_label.setStyleSheet("background-color: transparent;")		
		free_label.setFixedWidth(500)

		self.setLayout(month_grid)

	def change_default_title(self):
		file_name = "FormatDetails.txt"

		# change to the current index
		f = open(file_name, 'r')
		format_data = f.read().split("\n")
		f.close()
		# line 1, default calendar date: 2023,1,1
		line = format_data[0].split(",")
		line[0] = SharedData.year_str
		line[1] = str(SharedData.month)

		line = ",".join(line)
		format_data[0] = line
		format_data = "\n".join(format_data)
		f = open(file_name, 'w')
		f.write(format_data)		
		f.close()

	def buttonL_clicked(self):
		# changes data in SharedData
		SharedData.change_date(-1)
		self.title.setText(f"{SharedData.cal_title}")

	def buttonR_clicked(self):
		# changes data in SharedData
		SharedData.change_date(+1)
		self.title.setText(f"{SharedData.cal_title}")
