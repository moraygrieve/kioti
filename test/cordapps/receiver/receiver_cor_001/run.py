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
		client.startFlow(self.partya, self.partyb, initiator='ReceiveFlowTwoSends')

	def validate(self):
		self.assertGrep(file=self.partya.nodeLogfile, filedir=self.partya.nodeLogdir, expr='ReceiveFlowTwoSends returned=0')
		self.assertLineCount(file=self.partya.nodeLogfile, filedir=self.partya.nodeLogdir, expr='ReceiveFlowTwoSends returned', condition='==1')

		exprList=[]
		exprList.append('ReceiveFlowTwoSendsResponder has sent done with value 0')
		exprList.append('ReceiveFlowTwoSendsResponder has sent done with value 1')
		self.assertOrderedGrep(file=self.partyb.nodeLogfile, filedir=self.partyb.nodeLogdir, exprList=exprList)
		self.assertLineCount(file=self.partyb.nodeLogfile, filedir=self.partyb.nodeLogdir, expr='ReceiveFlowTwoSendsResponder has sent done with value', condition='==2')
