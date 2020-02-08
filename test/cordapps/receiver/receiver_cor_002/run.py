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
		client.startFlow(self.partya, self.partyb, initiator='ReceiveFlowLoop')

	def validate(self):
		exprList = []
		for x in range(0,400):
			exprList.append('ReceiveFlowLoop iteration=%d, returned=%d' % (x,x))
		self.assertOrderedGrep(file=self.partya.nodeLogfile, filedir=self.partya.nodeLogdir, exprList=exprList)