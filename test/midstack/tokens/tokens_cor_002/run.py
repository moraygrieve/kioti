from net.kioti.test.cordapp.tokens import TokensCorDapp
from net.kioti.test.cordatest import BootstrapTest
from net.kioti.test.database import Databases

class PySysTest(BootstrapTest):

	def execute(self):
		# create nodes ready for bootstrapping
		self.localNode('PartyA', database=Databases.oracle11g, cordapps=[TokensCorDapp])
		self.localNode('PartyB', database=Databases.oracle12c, cordapps=[TokensCorDapp])

		# bootstrap the network and start
		self.bootstrapNetwork()
		self.startNetwork(devMode=True)

	def validate(self):
		self.assertGrep(file=self.partya.nodeLogfile, filedir=self.partya.nodeLogdir, expr='Loaded 5 CorDapp.*Tokens Test CorDapp Workflows')
		self.assertGrep(file=self.partyb.nodeLogfile, filedir=self.partyb.nodeLogdir, expr='Loaded 5 CorDapp.*Tokens Test CorDapp Workflows')



