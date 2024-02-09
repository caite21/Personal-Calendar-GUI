
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QLineEdit, QLabel, QFrame
from PyQt5.QtCore import Qt, QDate
from DayFrame import DayFrame
from SharedData import SharedData


class CalFrame(QFrame, SharedData):
	def __init__(self):
		super().__init__()

		self.inner_grid = QGridLayout()
		self.setLayout(self.inner_grid)
		self.days = []
		self.extended = False

		self.setObjectName("calFrame")
		self.setStyleSheet(SharedData.style)
		
		self.setup()


	def setup(self):	
		# Write weekdays
		for column in range(7):
			# first day is Sunday (day 7)
			if column == 0:
				column = 7
			label = QLabel(f"{QDate.shortDayName(column)}")
			label.setObjectName("subTitle")
			label.setStyleSheet(SharedData.style)
			if column == 7:
				column = 0

			label.setFixedHeight(20)
			self.inner_grid.addWidget(label, 0, column)

		r = 6
		if SharedData.extend_cal == True:
			self.extended = True
			r = 7
		# Create x rows and 7 columns of DayFrames
		count = 0;	
		for row in range(1,r):
			for column in range(7):
				day_frame = DayFrame('')
				day_frame.widgets[0].clicked.connect(self.date_clicked)
				if column == 0 or column == 6:
					day_frame.setObjectName("weekendDayFrame")
				else:
					day_frame.setObjectName("dayFrame")
				day_frame.setStyleSheet(SharedData.style)
				self.inner_grid.addWidget(day_frame)
				self.days.append(day_frame)

		# set all 7 columns to stretch evenly
		for i in range(7):
			self.inner_grid.setColumnStretch(i, 1)

		# move to the currently set year and month
		self.move_cal()


	def move_cal(self):
		# extend cal or shrink cal
		if SharedData.extend_cal == self.extended:
			pass # do nothing
		elif SharedData.extend_cal == False and self.extended == True:
			# need to shrink
			for column in range(7):
				right_index = len(self.days) - 1
				self.inner_grid.removeWidget(self.days[right_index])
				self.days[right_index].deleteLater()
				del self.days[right_index]

			self.extended = False
		elif SharedData.extend_cal == True and self.extended == False:
			# need to expand
			count = 0	
			for column in range(7):
				day_frame = DayFrame('')
				# day_frame.widgets[0].clicked.connect(self.date_clicked)
				if column == 0 or column == 6:
					day_frame.setObjectName("weekendDayFrame")
				else:
					day_frame.setObjectName("dayFrame")
				day_frame.setStyleSheet(SharedData.style)
				self.inner_grid.addWidget(day_frame)
				self.days.append(day_frame)
			self.extended = True


		# draw calendar dates on calendar
		count = 0
		for d in self.days:
			d.empty()
			count += 1
			if (count >= SharedData.first_day and count <= SharedData.last_date + SharedData.first_day - 1):
				text = str(count - SharedData.first_day + 1)
				d.set_date(text)
			else:
				d.set_no_date()

		self.insert_event_data() 
		self.insert_icon_data()


	def insert_event_data(self):
		num_cols = 0
		line_count = 0
		
		for line in SharedData.event_data:
			if line[0] == '$':
				# first line of file: $,5
				num_cols = int(line[1])
			else:
				if num_cols == 0:
					print("missing first line: $,number", line_count)
				elif len(line) == num_cols:
					year, month, date, time, text, tag, status = line
					if status != "deleted" and int(year) == SharedData.year and int(month) == SharedData.month:
						date = int(date)
						days_index = SharedData.first_day + date - 2
						self.days[days_index].add_event(line_count, time, text, tag, status)
						# widget_index = len(self.days[days_index].widgets) - 1
						# self.days[days_index].widgets[widget_index].clicked.connect(self.event_clicked)
				else:
					print("Unexpected line of data on line", line_count, ":", line)
			line_count += 1

		self.set_today()

	def insert_icon_data(self):
		num_cols = 0
		line_count = 0
		
		for line in SharedData.icon_data:
			if line[0] == '$':
				# first line of file: $,5
				num_cols = int(line[1])
			else:
				if num_cols == 0:
					print("missing first line: $,number", line_count)
				elif len(line) == num_cols:
					year, month, date, text, status = line
					if status != "deleted" and int(year) == SharedData.year and int(month) == SharedData.month:
						date = int(date)
						days_index = SharedData.first_day + date - 2
						self.days[days_index].add_icon(text, line_count)
						# widget_index = len(self.days[days_index].widgets) - 1
						# self.days[days_index].widgets[widget_index].clicked.connect(self.event_clicked)
				else:
					print("Unexpected line of data on line", line_count, ":", line)
			line_count += 1



	def buttonRefresh_clicked(self):
		# remove all data
		for i in self.days:
			i.empty()
		self.insert_event_data()
		self.insert_icon_data()

	def date_clicked(self):
		pass
		# print("date clicked")

	def event_clicked(self, line_num):
		pass
		# print("event clicked")

	def set_today(self):
		if SharedData.year == SharedData.today_year and SharedData.month == SharedData.today_month:
			self.days[SharedData.first_day + SharedData.today_date - 2].add_today()

