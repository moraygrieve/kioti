from net.kioti.test.cordapp.tokens import TokensCorDapp
from net.kioti.test.cordatest import BootstrapTest
from net.kioti.test.database import Databases

class PySysTest(BootstrapTest):

	def execute(self):
		# create nodes ready for bootstrapping
		self.localNode('PartyA', database=Databases.postgres96, cordapps=[TokensCorDapp])
		self.localNode('PartyB', database=Databases.postgres1010, cordapps=[TokensCorDapp])
		self.localNode('PartyC', database=Databases.postgres115, cordapps=[TokensCorDapp])

		# bootstrap the network and start
		self.bootstrapNetwork()
		self.startNetwork(devMode=True)

	def validate(self):
		self.assertGrep(file=self.partya.nodeLogfile, filedir=self.partya.nodeLogdir, expr='Loaded 5 CorDapp.*Tokens Test CorDapp Workflows')
		self.assertGrep(file=self.partyb.nodeLogfile, filedir=self.partyb.nodeLogdir, expr='Loaded 5 CorDapp.*Tokens Test CorDapp Workflows')
		self.assertGrep(file=self.partyc.nodeLogfile, filedir=self.partyc.nodeLogdir, expr='Loaded 5 CorDapp.*Tokens Test CorDapp Workflows')



