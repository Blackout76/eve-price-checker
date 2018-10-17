import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGroupBox, QHBoxLayout, QGridLayout, QVBoxLayout, QLabel, QLineEdit
from PyQt5.QtGui import QIcon, QIntValidator
from PyQt5.QtCore import pyqtSlot, QThread, pyqtSignal
import checker
import locale
from playsound import playsound
from win10toast import ToastNotifier

PRICE_LIMIT_ACTIVATION = 10000000
ALARM_SOUND = 'sounds/nudge.wav'
class Worker(QThread):
	pricesSignal = pyqtSignal('PyQt_PyObject')

	def __init__(self,limit):
		self.limit = limit
		self.clipboard = None
		self.toaster = ToastNotifier()
		QThread.__init__(self)

	def __del__(self):
		self.wait()

	def run(self):
		while 1:
			new_clipboard = checker.get_clipboard()
			if new_clipboard != self.clipboard:
				print ("Thread active, new clipboard")
				evepraisal = checker.fetch_evepraisal(new_clipboard)
				if evepraisal and "appraisal" in evepraisal:
					prices = evepraisal["appraisal"]["totals"]
					self.pricesSignal.emit(prices)
					if float(prices["sell"]) > int(self.limit):
						#playsound(ALARM_SOUND)
						self.toaster.show_toast("EVE Online price checker","Price: " + str("{:,}".format(float(format(prices["sell"], '.2f'))) + " ISK"))
						print ('BINGO!!!')
				self.clipboard = new_clipboard
			self.sleep(1)

	def change_limit(self,limit):
		self.limit = limit

class App(QWidget):
 
	def __init__(self):
		super().__init__()
		self.title = 'Fast price checker'
		self.left = 100
		self.top = 100
		self.width = 320
		self.height = 200
		self.initUI()
 
	def initUI(self):
		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)
		

		self.createGridLayout()

		windowLayout = QVBoxLayout()
		windowLayout.addWidget(self.horizontalGroupBox)
		self.setLayout(windowLayout)

		self.worker = Worker(self.limitbox.text())

		self.button_start.clicked.connect(self.on_click_start)
		self.button_stop.clicked.connect(self.on_click_stop)
		self.worker.pricesSignal.connect(self.set_box_prices)
		self.limitbox.textChanged.connect(self.on_limit_change)

		self.show()
 
	def createGridLayout(self):
		self.horizontalGroupBox = QGroupBox("Prices")

		layout = QGridLayout()

		# Limit
		self.onlyInt = QIntValidator()
		label_limit = QLabel('Limit activation')
		self.limitbox = QLineEdit(str(PRICE_LIMIT_ACTIVATION))
		self.limitbox.setValidator(self.onlyInt)
		layout.addWidget(label_limit,0,0) 
		layout.addWidget(self.limitbox,0,1) 
		limitBoxSignal = pyqtSignal('PyQt_PyObject')

		# Prices
		label_buy = QLabel('Buy')
		label_sell = QLabel('Sell')
		label_volume = QLabel('volume')
		self.label_buy_out = QLabel('0')
		self.label_sell_out = QLabel('0')
		self.label_volume_out = QLabel('0')
		self.label_buy_out.setStyleSheet('font-size: 18pt; font-family: system-ui;')
		self.label_sell_out.setStyleSheet('font-size: 18pt; font-family: system-ui;')
		self.label_volume_out.setStyleSheet('font-size: 12pt; font-family: system-ui;')

		layout.addWidget(label_buy,1,0) 
		layout.addWidget(label_sell,2,0) 
		layout.addWidget(label_volume,3,0) 
		layout.addWidget(self.label_buy_out,1,1) 
		layout.addWidget(self.label_sell_out,2,1) 
		layout.addWidget(self.label_volume_out,3,1) 

		# Engines 
		self.button_start = QPushButton('Start', self)
		self.button_start.setToolTip('Start auto clipboard check')
		layout.addWidget(self.button_start,4,0)

		self.button_stop = QPushButton('Stop', self)
		self.button_stop.setToolTip('stop auto clipboard check')
		layout.addWidget(self.button_stop,4,1)

		# Main layout
		self.horizontalGroupBox.setLayout(layout)
	
	@pyqtSlot()
	def on_click_start(self):
		self.worker.start()
		self.button_stop.setEnabled(True)
		self.button_start.setEnabled(False)
		print('Start worker')

	@pyqtSlot()
	def on_click_stop(self):
		self.worker.terminate()
		self.button_stop.setEnabled(False)
		self.button_start.setEnabled(True)
		print('stop worker')

	@pyqtSlot()
	def on_limit_change(self):
		PRICE_LIMIT_ACTIVATION = int(self.limitbox.text())
		self.worker.change_limit(PRICE_LIMIT_ACTIVATION)
		print('limit changed')

	def set_box_prices(self,prices):
		self.label_buy_out.setText(str("{:,}".format(float(format(prices["buy"], '.2f')))) + " ISK")
		self.label_sell_out.setText(str("{:,}".format(float(format(prices["sell"], '.2f')))) + " ISK")
		self.label_volume_out.setText(str("{:,}".format(float(format(prices["volume"], '.2f')))) + " m3")
 
if __name__ == '__main__':
	locale.setlocale(locale.LC_ALL, '')
	app = QApplication(sys.argv)
	ex = App()
	sys.exit(app.exec_())