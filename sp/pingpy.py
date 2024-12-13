import subprocess, os, datetime, signal
from math import ceil

class ping():
	def __init__(self, timeout, IP="1.1.1.1"):
		output = ping.start(timeout, IP)

		self.avgPing = output[0]
		self.minPing = output[1]
		self.maxPing = output[2]
		self.packetLoss = output[3]

	def start(timeout, IP):
		args = ["ping", IP, "-q"]
		output = ""
		with subprocess.Popen(args=args, stdout=subprocess.PIPE) as pingProc:
			try:
				pingProc.communicate(timeout=timeout)
			except subprocess.TimeoutExpired:
				pingProc.send_signal(signal.SIGINT)
				output = pingProc.communicate()[0].decode("utf-8")

		if output != "":
			output = output[output.find("---\n")+4:-1].splitlines()

			outputTop = output[0].split(", ")[2]
			packetLoss = outputTop[0:outputTop.find("%")]

			outputBottom = output[1][output[1].find("=")+2:-1].split("/")
			avgPing = round(float(outputBottom[1]))
			minPing = round(float(outputBottom[0]))
			maxPing = round(float(outputBottom[2][0:-3]))
		else:
			packetLoss = ""
			avgPing = ""
			minPing = ""
			maxPing = ""

		return [avgPing, minPing, maxPing, packetLoss]

# TODO add error return instead of sending empty strings