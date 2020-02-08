from net.corda.test.cordatest import BootstrapTest
from net.corda.test.cordapp.accounts import AccountsCorDapp
from net.corda.test.database import Databases

class PySysTest(BootstrapTest):

	def execute(self):
		self.localNode('PartyA', database=Databases.oracle11g, cordapps=[AccountsCorDapp])
		self.localNode('PartyB', database=Databases.oracle12c, cordapps=[AccountsCorDapp])

		# bootstrap the network and start
		self.bootstrapNetwork()
		self.startNetwork(devMode=True)

	def validate(self):
		self.assertGrep(file=self.partya.nodeLogfile, filedir=self.partya.nodeLogdir, expr='Loaded 3 CorDapp.*Accounts Test CorDapp Workflows')
		self.assertGrep(file=self.partyb.nodeLogfile, filedir=self.partyb.nodeLogdir, expr='Loaded 3 CorDapp.*Accounts Test CorDapp Workflows')



