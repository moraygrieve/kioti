import re
from net.kioti.test.cordatest import BootstrapTest
from net.kioti.test.cordapp.receiver import ReceiverCorDapp, ReceiverCorDappSSHClient

class PySysTest(BootstrapTest):

	def execute(self):
		# create a bootstrapped network
		self.localNetwork(nodes=['PartyA', 'PartyB'], cordapps=[ReceiverCorDapp])
		self.bootstrapNetwork()
		self.startNetwork()

		# create the SSH client and kick off flows
		client = ReceiverCorDappSSHClient(self)
		client.startFlow(self.partya, self.partyb, initiator='ReceiveFlowLoopSleep')

	def validate(self):
		t1 = self.getDuration(self.partya.nodeLog)
		t2 = self.getDuration(self.partyb.nodeLog)
		self.log.info('Initiator receive block took %f ms' % t1)
		self.log.info('Responder send block took %f ms' % t2)

		# the receiver should take longer than 50 * 400 ms, whilst the sender should be less
		self.assertEval(evalstring='{value} > 20000', value=t1)
		self.assertEval(evalstring='{value} < 20000', value=t2)

	def getDuration(self, file):
		regex = re.compile('Completed ReceiveFlowLoopSleep.*duration (?P<time>[0-9]+) ms', re.M)

		with open(file, 'r') as fp:
			for line in fp.readlines():
				match = regex.search(line.strip())
				if match is not None: return float(match.group('time'))



