from net.kioti.test.cordatest import NetworkTest
from net.kioti.test.cordapp.finance import FinanceCorDapp, FinanceCorDappRPCClient

class PySysTest(NetworkTest):

	def execute(self):
		# start two nodes
		self.partya = self.startNode('PartyA', cordapps=[FinanceCorDapp])
		self.partyb = self.startNode('PartyB', cordapps=[FinanceCorDapp])

		# create the RPC client and issue some cash on partyA
		client = FinanceCorDappRPCClient(self)
		client.cashIssue(self.partya, '100 USD')

		# make sure nodes are resolved and perform cash payment transactions
		client.resolveParty(self.partya, self.partyb)
		client.cashPayment(self.partya, '50 USD', self.partyb, anonymous=True)
		client.resolveParty(self.partyb, self.partya)
		client.cashPayment(self.partyb, '25 USD', self.partya, anonymous=True)

		# request the balance from both nodes
		client.cashBalance(self.partya)
		client.cashBalance(self.partyb)

	def validate(self):
		self.assertOrderedGrep(file='cash-balance.out', filedir=self.partya.directory, exprList=['Total Cash:','75 USD'])
		self.assertOrderedGrep(file='cash-balance.out', filedir=self.partyb.directory, exprList=['Total Cash:','25 USD'])
