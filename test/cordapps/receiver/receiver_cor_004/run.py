from net.kioti.test.cordatest import BootstrapTest
from net.kioti.test.cordapp.receiver import ReceiverCorDapp, ReceiverCorDappRPCClient

class PySysTest(BootstrapTest):

	def execute(self):
		# create a bootstrapped network
		self.localNetwork(nodes=['PartyA', 'PartyB'], cordapps=[ReceiverCorDapp])
		self.bootstrapNetwork()
		self.startNetwork()

		# create the RPC client and kick off flows
		rpcClient = ReceiverCorDappRPCClient(self)
		rpcClient.run(self.partya)

	def validate(self):
		exprList = ['Starting']
		exprList.append('Performing initiate flow')
		exprList.append('Receiving response from responder')
		exprList.append('Received all responses from responder')
		exprList.append('Done')
		self.assertOrderedGrep(file='receiver-run.out', filedir=self.partya.directory, exprList=exprList)