from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QLineEdit, QLabel, QPushButton, QDateEdit, QPlainTextEdit, QFrame, QComboBox
from PyQt5.QtCore import Qt
from SharedData import SharedData

class DataFrame(QFrame, SharedData):
	def __init__(self):
		super().__init__()

		text_height = 25
		
		self.inner_grid = QGridLayout()

		# title and save 
		self.titleLabel = QLabel(f"To Do List")
		self.titleLabel.setFixedHeight(text_height)
		self.titleLabel.setObjectName("subTitle")
		self.titleLabel.setStyleSheet(SharedData.style)
		self.inner_grid.addWidget(self.titleLabel, 0, 0, 1, 4)

		self.buttonSave = QPushButton("Save")
		self.buttonSave.setObjectName("button")
		self.buttonSave.setStyleSheet(SharedData.style)
		self.inner_grid.addWidget(self.buttonSave, 0, 3)		
		
		# list box 
		self.list_box = QPlainTextEdit()
		# self.list_box.setFixedHeight(300)
		self.list_box.setObjectName("textBox")
		self.list_box.setStyleSheet(SharedData.style)
		self.inner_grid.addWidget(self.list_box, 1, 0, 1, 4)
		self.display_text()

		# data entry
		data_enter_title_row = 2
		data_enter_row = 3
		self.date_label = QLabel(f"Date:")
		self.date_label.setFixedHeight(text_height)
		self.date_label.setObjectName("subTitle")
		self.date_label.setStyleSheet(SharedData.style)
		self.inner_grid.addWidget(self.date_label, data_enter_title_row, 0)
		self.date_box = QLineEdit()
		self.date_box.setFixedSize(40, text_height) # w, h
		self.date_box.setObjectName("textBox")
		self.date_box.setStyleSheet(SharedData.style)
		self.inner_grid.addWidget(self.date_box, data_enter_row, 0)

		self.time_label = QLabel(f"Time:")
		self.time_label.setFixedHeight(text_height)
		self.time_label.setObjectName("subTitle")
		self.time_label.setStyleSheet(SharedData.style)
		self.inner_grid.addWidget(self.time_label, data_enter_title_row, 1)
		self.time_box = QLineEdit()
		self.time_box.setFixedSize(70, text_height) # w, h
		self.time_box.setObjectName("textBox")
		self.time_box.setStyleSheet(SharedData.style)
		self.inner_grid.addWidget(self.time_box, data_enter_row, 1)

		self.event_label = QLabel(f"Event:")
		self.event_label.setFixedHeight(text_height)
		self.event_label.setObjectName("subTitle")
		self.event_label.setStyleSheet(SharedData.style)
		self.inner_grid.addWidget(self.event_label, data_enter_title_row, 2)
		self.event_box = QLineEdit()
		self.event_box.setObjectName("textBox")
		self.event_box.setStyleSheet(SharedData.style)
		self.inner_grid.addWidget(self.event_box, data_enter_row, 2)

		self.buttonEnter = QPushButton("Enter")
		self.buttonEnter.setObjectName("button")
		self.buttonEnter.setStyleSheet(SharedData.style)
		self.inner_grid.addWidget(self.buttonEnter, data_enter_title_row, 3)

		self.tag_box = QComboBox()
		self.tag_box.addItems(list(SharedData.tag_color.keys()))
		self.tag_box.setObjectName("textBox")
		self.tag_box.setStyleSheet(SharedData.style)
		self.inner_grid.addWidget(self.tag_box, data_enter_row, 3)

		self.setObjectName("dataFrame")
		self.setStyleSheet(SharedData.style)
		self.setLayout(self.inner_grid)


	def set_entry_boxes(self, date, time, event, tag):
		self.date_box.setText(date)
		self.time_box.setText(time)
		self.event_box.setText(event)
		self.tag_box.setCurrentText(tag)

	def data_entered(self):
		# clean entered text
		date = self.date_box.text().strip()
		time = self.time_box.text().strip()
		event = self.event_box.text().strip()
		tag = self.tag_box.currentText().strip()
		status = ""

		# ignore if date or event is empty or date isn't a number
		if date!="" and event!="":
			try:
				date = int(date)
			except ValueError:
				print("Error in date value")
				return
			SharedData.add_event(date, time, event, tag, status)
			self.date_box.setText("")

	def keyPressEvent(self, event):
		if event.key() == Qt.Key_S and event.modifiers() == Qt.ControlModifier:
			# CTRL-S
			self.save_text()

	def save_text(self):
		file_name = "List.txt"
		text = self.list_box.toPlainText()
		f = open(file_name, 'w')
		f.write(text)
		f.close()

	def display_text(self):
		file_name = "List.txt"
		f = open(file_name, 'r')
		text = f.read()
		self.list_box.setPlainText(text)
		f.close()

	def do_when_print_signal(self, date, time, event, tag):
		self.set_entry_boxes(date, time, event, tag)
