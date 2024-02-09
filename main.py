from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets

from TitleFrame import TitleFrame
from CalFrame import CalFrame
from DataFrame import DataFrame
import sys
from SharedData import SharedData


def main():
	app = QApplication([])
	window = QMainWindow()
	window.setWindowTitle("Calendar")
	central_widget = QWidget()
	window.setCentralWidget(central_widget)
	window.resize(1200, 700)


	def take_screenshot():
		widget = window
		pixmap = widget.grab()
		if not pixmap.isNull():
			pixmap.save("C:/Users/caite/Documents/Projects/Calendar/screenshot.png", "PNG")


	if len(sys.argv) == 2:
		mode = sys.argv[1]
	else:
		mode = None
	SharedData.get_style(mode)
	SharedData.get_format_data()
	SharedData.get_event_data()
	SharedData.get_icon_data()

	# 6 rows x 3 columns
	main_grid = QGridLayout(central_widget)

	title_frame = TitleFrame()
	main_grid.addWidget(title_frame, 0, 0, 1, 13)

	window.setObjectName("textBox")
	window.setStyleSheet(title_frame.style_sheet_copy)

	cal_frame = CalFrame()
	main_grid.addWidget(cal_frame, 1, 0, 7, 9)

	data_frame = DataFrame()
	main_grid.addWidget(data_frame, 1, 9, 7, 4)

	title_frame.buttonL.clicked.connect(title_frame.buttonL_clicked)
	title_frame.buttonL.clicked.connect(cal_frame.move_cal)

	title_frame.buttonR.clicked.connect(title_frame.buttonR_clicked)
	title_frame.buttonR.clicked.connect(cal_frame.move_cal)

	title_frame.buttonRefresh.clicked.connect(cal_frame.buttonRefresh_clicked)
	title_frame.buttonRefresh.clicked.connect(take_screenshot)
	title_frame.title.clicked.connect(title_frame.change_default_title)

	data_frame.buttonEnter.clicked.connect(data_frame.data_entered)
	data_frame.buttonEnter.clicked.connect(cal_frame.buttonRefresh_clicked)
	data_frame.event_box.returnPressed.connect(data_frame.data_entered)
	data_frame.event_box.returnPressed.connect(cal_frame.buttonRefresh_clicked)

	data_frame.buttonSave.clicked.connect(data_frame.save_text)

	for i in range(len(cal_frame.days)):
		cal_frame.days[i].info_signal.connect(data_frame.set_entry_boxes)



	window.show()
	app.exec_()

if __name__ == "__main__":
	main()