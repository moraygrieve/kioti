from net.corda.test.cordatest import BootstrapTest
from net.corda.test.cordapp.finance import FinanceCorDapp, FinanceCorDappSSHClient

class PySysTest(BootstrapTest):

	def execute(self):
		# create a bootstrapped network using convenience method (defaults used) ... nnote this call will assign self.<name> to the node
		# with name <name> for ease of later reference e.g. self.partya for "PartyA" etc
		self.localNetwork(nodes=['PartyA', 'PartyB', 'PartyC'], notaries=['Notary'], cordapps=[FinanceCorDapp])

		# bootstrap the network and start
		self.bootstrapNetwork()
		self.startNetwork()

		# create the SSH client and issue some cash on PartyA, pay PartyB and PartyC, and request balances
		client = FinanceCorDappSSHClient(self)
		client.cashIssue(self.partya, '100 USD')
		client.cashPayment(self.partya, '20 USD', self.partyb, anonymous=True)
		client.cashPayment(self.partya, '30 USD', self.partyc, anonymous=True)
		map(lambda x: client.cashBalance(x), [self.partya, self.partyb, self.partyc])

	def validate(self):
		self.assertOrderedGrep(file='cash-balance.out', filedir=self.partya.directory, exprList=['amount.*50.00 USD issued by O=PartyA'])
		self.assertLineCount(file='cash-balance.out', filedir=self.partya.directory, expr='- state:', condition='==1')
		self.assertOrderedGrep(file='cash-balance.out', filedir=self.partyb.directory, exprList=['amount.*20.00 USD issued by O=PartyA'])
		self.assertLineCount(file='cash-balance.out', filedir=self.partyb.directory, expr='- state:', condition='==1')
		self.assertOrderedGrep(file='cash-balance.out', filedir=self.partyc.directory, exprList=['amount.*30.00 USD issued by O=PartyA'])
		self.assertLineCount(file='cash-balance.out', filedir=self.partyc.directory, expr='- state:', condition='==1')