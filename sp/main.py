#!/bin/python3

from datahandler import databaseHandler
from pingpy import ping
from speedtestpy import speedtestCLI

import datetime
from math import ceil
from time import sleep


class SpeedTest():
	def __init__(self):
		####################
		self.Interval = [1, 0, 0] #Hours Minutes Seconds, the total of all the time is how long inbetween speedtests
		self.Server = None
		#################### TODO make env var based

		self.dataH = databaseHandler()

		self.main()

	def main(self):
		while True:
			print("It is currently safe to exit the script. (CTRL + C)")
			data = ["", "", "", "", "", "", "", "", "", "", ""]
			p = ping(timeout=self.nextInterval())
			if p.packetLoss != "":
				data[6:9] = str(p.avgPing), str(p.maxPing), str(p.minPing), str(round(float(p.packetLoss), 1)) + "%"
			else:
				data[6:9] = str(""), str(""), str(""), str("")
				sleep(self.nextInterval())

			count = 0
			while count < 3:
				print("Starting Speed Test")
				st = speedtestCLI(self.Server)
				if (st.exitCode == 0) and (st.packetLoss != "N/A"):
					data[1:5] = str(st.serverName), str(round(int(st.downloadSpeed) / 125000, 2)), str(round(int(st.uploadSpeed) / 125000, 2)), str(round(float(st.packetLoss), 1)) + "%", str(st.shareUrl)
					count = 3
				else:
					data[10] = str(st.error)
					count += 1

			data[0] = datetime.datetime.now()
			print("\n" * 100)
			self.dataH.saveData(data)

	def nextInterval(self):
		delta = datetime.timedelta(hours=self.Interval[0], minutes=self.Interval[1], seconds=self.Interval[2])
		now = datetime.datetime.now()
		outDatetime = datetime.datetime.min + ceil((now - datetime.datetime.min) / delta) * delta
		return int(outDatetime.timestamp() - now.timestamp())

SpeedTest()

# TODO CONSIDER CHANGING THE WAY PING IS STARTED TO ALLOW FOR CONTINUOUS ATTEMPTS TO START ON ERROR.
