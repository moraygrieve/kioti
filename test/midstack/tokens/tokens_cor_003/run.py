from net.corda.test.cordapp.tokens import TokensCorDapp
from net.corda.test.cordatest import BootstrapTest
from net.corda.test.database import Databases

class PySysTest(BootstrapTest):

	def execute(self):
		# create nodes ready for bootstrapping
		self.localNode('PartyA', database=Databases.sqlserver, cordapps=[TokensCorDapp])

		# bootstrap the network and start
		self.bootstrapNetwork()
		self.startNetwork(devMode=True)

	def validate(self):
		self.assertGrep(file=self.partya.nodeLogfile, filedir=self.partya.nodeLogdir, expr='Loaded 5 CorDapp.*Tokens Test CorDapp Workflows')



