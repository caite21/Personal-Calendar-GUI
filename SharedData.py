from PyQt5.QtCore import QDate

class SharedData():
	test_str = "test string in shared data"
	month = 0
	data_index = 0
	event_data = []
	format_details = []
	icon_data = []
	cal_title = "Error"
	style = ""

	today = QDate.currentDate()
	today_year = today.year()
	today_month = today.month()
	today_date = today.day()

	date = QDate()
	first_day = 0
	last_date = 0
	extend_cal = False

	tag_color = {}
	icon_dict = {}
	# "A": "red", 
	# "B": "orange", 
	# "C": "yellow", 
	# "D": "green",
	# "E": "blue",
	# "F": "#807CBD"
	# }

	# green 7BBD8B
	# blue 7DAEBD
	# teal 7CBDB5
	# purple 807CBD
	# pink AC7CBD

	def write_event_data():
		file_name = "EventData.txt"
		# file_name = "test_file2.txt"
		with open(file_name, "w") as f:
			for line in SharedData.event_data:
				f.write(str(line[0]))
				for token in line[1:]:
					f.write("," + str(token))
				f.write("\n")
		f.close()

	def write_icon_data():
		file_name = "IconData.txt"
		# file_name = "test_file2.txt"
		with open(file_name, "w") as f:
			for line in SharedData.icon_data:
				f.write(str(line[0]))
				for token in line[1:]:
					f.write("," + str(token))
				f.write("\n")
		f.close()

	@classmethod
	def get_style(self, command):
		if command is None:
			setting = ""
		elif command == "green":
			setting = "_Green"
		elif command == "dark":
			setting = "_Dark"

		# StyleSheet
		file_name = "Style" + setting + ".css"
		f = open(file_name, 'r')
		self.style = f.read()
		f.close()

		# event color coding
		file_name = "EventColors" + setting + ".txt"
		f = open(file_name, 'r')
		while True:
			line = f.readline()
			line = line.strip() # remove trailing \n		
			if not line:
				# EOF reached
				break
			tag, color = line.split(",")
			self.tag_color[tag] = color
		f.close()	

		# icon color coding
		# file_name = "IconColors" + setting + ".txt"
		file_name = "IconColors" + ".txt"
		f = open(file_name, 'r', encoding="unicode-escape")
		while True:
			line = f.readline()	
			line = line.strip() # remove trailing \n		
			if not line:
				# EOF reached
				break
			text, color, symbol = line.split(",")
			self.icon_dict[text] = [color, symbol]
		f.close()	


	@classmethod
	def get_format_data(self):
		# get file data
		file_name = "FormatDetails.txt"
		f = open(file_name, 'r')
		self.format_details = f.read().split("\n")
		f.close()

		# line 1: default calendar month
		self.year_str, month_temp, self.day_str = self.format_details[0].split(",")
		self.year = int(self.year_str)
		self.month = int(month_temp)
		self.day = int(self.day_str)

		self.change_date(0)

	@classmethod
	def get_event_data(self):
		file_name = "EventData.txt"
		i_status = 6
		line_count = 0
		# read file
		f = open(file_name, 'r')
		while True:
			line = f.readline()
			line_count += 1
			
			if not line:
				# EOF reached
				break
			line = line.strip() # remove trailing \n
			tokens = line.split(",")
			if len(tokens)>i_status and tokens[i_status]=="deleted":
				pass
			else:
				self.event_data.append(tokens)

		f.close()
		# removes all "deleted" events
		self.write_event_data()

	@classmethod
	def get_icon_data(self):
		file_name = "IconData.txt"
		i_status = 4
		line_count = 0
		# read file
		f = open(file_name, 'r', encoding="unicode-escape")
		while True:
			line = f.readline()
			line_count += 1
			
			if not line:
				# EOF reached
				break
			line = line.strip() # remove trailing \n
			tokens = line.split(",")
			if len(tokens)>i_status and tokens[i_status]=="deleted":
				pass
			else:
				self.icon_data.append(tokens)

		f.close()

	@classmethod
	def change_date(self, delta):
		# delta is +1 or -1 month
		self.month = self.month + delta
		if self.month > 12:
			self.month = 1
			self.year += 1
		elif self.month < 1:
			self.month = 12
			self.year -= 1
			self.year_str = str(self.year)
		self.month_str = QDate.longMonthName(self.month)
		self.date.setDate(self.year, self.month, self.day)
		self.cal_title = self.month_str + " " + self.year_str

		# TODO: change +1
		self.first_day = self.date.dayOfWeek() + 1
		if self.first_day == 8:
			self.first_day = 1
		self.last_date = self.date.daysInMonth()

		last_day = self.last_date + self.first_day
		if last_day > (7*5 + 1):
			self.extend_cal = True
		else:
			self.extend_cal = False

	@classmethod
	def delete_event(self, line_num):
		i_status = 6
		self.event_data[line_num][i_status] = "deleted"		
		self.write_event_data()

	@classmethod
	def add_event(self, date, time, event, tag, status):
		i_status = 6
		line = [self.year, self.month, date, time, event, tag, status]
		self.event_data.append(line)
		self.write_event_data()

	@classmethod
	def delete_icon(self, line_num):
		i_status = 4
		self.icon_data[line_num][i_status] = "deleted"		
		self.write_icon_data()

	@classmethod
	def add_icon(self, date, text, status):
		i_status = 4
		line = [self.year, self.month, date, text, status]
		self.icon_data.append(line)
		self.write_icon_data()

	@classmethod
	def cross_event(self, line_num):
		i_status = 6
		# print(self.event_data[line_num])
		self.event_data[line_num][i_status] = "crossed"
		self.write_event_data()

	@classmethod
	def reset_event(self, line_num):
		i_status = 6
		self.event_data[line_num][i_status] = ""
		self.write_event_data()

