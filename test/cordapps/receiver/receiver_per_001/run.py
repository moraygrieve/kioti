import re
from pysys.constants import INSPECT
from net.kioti.test.cordatest import BootstrapTest
from net.kioti.test.cordapp.receiver import ReceiverCorDapp, ReceiverCorDappSSHClient

class PySysTest(BootstrapTest):

	def execute(self):
		## create a bootstrapped network
		self.localNetwork(nodes=['PartyA', 'PartyB'], cordapps=[ReceiverCorDapp])
		self.bootstrapNetwork()
		self.startNetwork()

		# create the SSH client and kick off flows
		client = ReceiverCorDappSSHClient(self)
		client.startFlow(self.partya, self.partyb, initiator='ReceiveFlowLoop')

	def validate(self):
		first, average, median, nnperc = self.getStats()
		self.log.info("Stats: first   = %f ms" % first)
		self.log.info("Stats: average = %f ms" % average)
		self.log.info("Stats: median  = %f ms" % median)
		self.log.info("Stats: 99th    = %f ms" % nnperc)

		# results should be manually inspected for validation
		self.addOutcome(INSPECT)

	def getStats(self):
		self.log.info('')
		self.log.info('Calculating stats for receive call duration')
		regex = re.compile('ReceiveFlowLoop.*finished in (?P<time>[0-9]+) ms', re.M)

		values=[]
		with open(self.partya.nodeLog, 'r') as fp:
			for line in fp.readlines():
				match = regex.search(line.strip())
				if match is not None: values.append(float(match.group('time')))

		first = values.pop(0)
		values.sort()
		l = len(values)
		average = (sum(values)/l)
		median = values[int(0.5*l)]
		nnperc = values[int(0.99*l)]
		return first, average, median, nnperc


