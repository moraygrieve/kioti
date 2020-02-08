from net.kioti.test.cordatest import BootstrapTest
from net.kioti.test.cordapp.accounts import AccountsCorDapp
from net.kioti.test.database import Databases

class PySysTest(BootstrapTest):

	def execute(self):
		self.localNode('PartyA', database=Databases.azuresql, cordapps=[AccountsCorDapp])

		# bootstrap the network and start
		self.bootstrapNetwork()
		self.startNetwork(devMode=True)

	def validate(self):
		self.assertGrep(file=self.partya.nodeLogfile, filedir=self.partya.nodeLogdir, expr='Loaded 3 CorDapp.*Accounts Test CorDapp Workflows')




