
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QLineEdit, QLabel, QPushButton, QFrame
from PyQt5.QtCore import Qt, pyqtSignal
from SharedData import SharedData
from EventWidget import EventWidget


class DayFrame(QFrame, SharedData):
	info_signal = pyqtSignal(str, str, str, str)
	max_top_widgets = 6

	def __init__(self, date):
		super().__init__()

		self.inner_grid = QGridLayout()	
		self.inner_grid.setAlignment(Qt.AlignTop)
		self.inner_grid.setContentsMargins(1, 0, 1, 0) #l,t,r,b

		self.widgets = [QPushButton(f"{date}")]
		self.widgets[0].setObjectName("date")
		self.widgets[0].setStyleSheet(SharedData.style)

		self.icons = []

		if isinstance(date, int):
			self.set_date(str(date))
		else:
			self.set_no_date()
		
		self.inner_grid.addWidget(self.widgets[0], 0, 0, 1, self.max_top_widgets)
		self.setLayout(self.inner_grid)

	def set_date(self, text):
		self.date = int(text)
		self.widgets[0].setText(text)
		self.widgets[0].setObjectName("date")
		self.widgets[0].setStyleSheet(SharedData.style)

	def set_no_date(self):
		self.widgets[0].setText('')

	def empty(self):
		right_index = len(self.widgets) - 1
		# del events that are not already removed
		for i in range(len(self.widgets) - 1): # -1 for not date widget
			if self.widgets[right_index].isDeleted == False:
				self.inner_grid.removeWidget(self.widgets[right_index])
				self.widgets[right_index].deleteLater()
				del self.widgets[right_index]
			right_index-=1

		right_index = len(self.icons) - 1
		# del icons that are not already removed
		for i in range(len(self.icons)):
			if self.icons[right_index].isDeleted == False:
				self.inner_grid.removeWidget(self.icons[right_index])
				self.icons[right_index].deleteLater()
			del self.icons[right_index]
			right_index-=1



	def add_event(self, line_count, time, text, tag, status):
		if time=="":
			self.widgets.append(EventWidget(f"{text}", line_count, self.date, len(self.widgets)))
		else:
			self.widgets.append(EventWidget(f"{time} {text}", line_count, self.date, len(self.widgets)))

		new_index = len(self.widgets) - 1
		self.widgets[new_index].backspacePressedEvent.connect(self.remove_event)
		self.widgets[new_index].type = "Event"

		def cross_out(line_num):
			i = new_index
			if not self.widgets[i].isCrossed:
				self.widgets[i].setStyleSheet(SharedData.style.replace("text-decoration: none;", "text-decoration: line-through;"))
				SharedData.cross_event(line_num)
				self.widgets[i].isCrossed = True
			else:
				self.widgets[i].setStyleSheet(SharedData.style.replace("text-decoration: line-through;", "text-decoration: none;"))
				self.widgets[i].setStyleSheet(SharedData.style.replace("background-color: transparent;", f"background-color: {SharedData.tag_color[tag]};"))
				SharedData.reset_event(line_num)
				self.widgets[i].isCrossed = False

		self.widgets[new_index].setWordWrap(True)
		self.widgets[new_index].setObjectName(f"event")
		if tag in SharedData.tag_color:
			color = SharedData.tag_color[tag]
			self.widgets[new_index].setStyleSheet(SharedData.style.replace("background-color: transparent;", f"background-color: {color};"))
		else:
			self.widgets[new_index].setStyleSheet(SharedData.style)
		
		if status == "crossed":
			# removes color change
			self.widgets[new_index].setStyleSheet(SharedData.style.replace("text-decoration: none;", "text-decoration: line-through;"))
			self.widgets[new_index].isCrossed = True
		self.widgets[new_index].clicked.connect(cross_out)
		self.widgets[new_index].clicked.connect(self.send_info_signal)
		self.inner_grid.addWidget(self.widgets[new_index], new_index, 0, 1, self.max_top_widgets)

	def add_icon(self, text, line_count):
		color, symbol = SharedData.icon_dict[text]
		# self.icons.append(QPushButton(f'{symbol}'))
		self.icons.append(EventWidget(f'{symbol}', line_count, self.date, len(self.icons)))
		new_index = len(self.icons) - 1
		self.icons[new_index].type = "Icon"
		self.icons[new_index].backspacePressedIcon.connect(self.remove_icon)
		
		def fade_out(line_num):
			# this action is not saved (TODO)
			i = new_index
			if not self.icons[i].isCrossed:
				self.icons[i].setStyleSheet(SharedData.style.replace(f"background-color: {color};", "background-color: transparent;"))
				self.icons[i].isCrossed = True
			else:
				self.icons[i].setStyleSheet(SharedData.style.replace("background-color: transparent;", f"background-color: {color};"))
				self.icons[i].isCrossed = False
		
		self.icons[new_index].setObjectName("event")
		self.icons[new_index].setStyleSheet(SharedData.style)
		self.icons[new_index].setStyleSheet(SharedData.style.replace("background-color: transparent;", f"background-color: {color};"))

		self.icons[new_index].clicked.connect(fade_out)
		self.inner_grid.addWidget(self.icons[new_index], 0, new_index+1)	
		

	def add_today(self):
		self.widgets[0].setObjectName("todayDate")
		self.widgets[0].setStyleSheet(SharedData.style)

	def send_info_signal(self, line_count):
		year, month, date, time, event, tag, status = SharedData.event_data[line_count]
		self.info_signal.emit(str(date), time, event, tag)

	def date_clicked(self):
		print("clicked on date:", self.widgets[0].text())

	def remove_event(self, index):
		self.inner_grid.removeWidget(self.widgets[index])
		self.widgets[index].deleteLater()
		# widget stays in self.widgets to maintain index order
		self.widgets[index].isDeleted = True

	def remove_icon(self, index):
		self.inner_grid.removeWidget(self.icons[index])
		self.icons[index].deleteLater()
		self.icons[index].isDeleted = True
