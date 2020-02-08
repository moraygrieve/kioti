import os, re
from net.corda.test.cordapp.doublespend import DoublespendCorDapp, DoublespendRPCClient
from net.corda.test.cordatest import BootstrapTest

class PySysTest(BootstrapTest):

	def execute(self):
		# create a bootstrapped network
		self.localNetwork(nodes=['PartyA'], notaries=['NotaryA', 'NotaryB', 'NotaryC'], cordapps=[DoublespendCorDapp])
		self.bootstrapNetwork()
		self.startNetwork()

		# create the SSH client and initiate a flow of doubpe spend attempts
		client = DoublespendRPCClient(self)
		client.run(self.partya, doubleSpendRatio='0.5', numberOfSpends='100', notary=self.notaryb)
		self.waitForSignal(file=self.partya.nodeLogfile, filedir=self.partya.nodeLogdir, expr='Run completed')

	def validate(self):
		self.assertGrep(file=self.notarya.nodeLogfile, filedir=self.notarya.nodeLogdir, expr='Received a notarisation request for Tx', contains=False)
		self.assertGrep(file=self.notarya.nodeLogfile, filedir=self.notaryb.nodeLogdir, expr='Received a notarisation request for Tx')
		self.assertGrep(file=self.notarya.nodeLogfile, filedir=self.notaryc.nodeLogdir, expr='Received a notarisation request for Tx', contains=False)