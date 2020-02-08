from net.kioti.test.cordatest import NetworkTest
from net.kioti.test.database import Databases
from net.kioti.test.cordapp.tokens import TokensCorDapp, TokensSSHClient

class PySysTest(NetworkTest):

	def execute(self):
		# create the nodes
		self.partya = self.startNode('PartyA', cordapps=[TokensCorDapp])
		self.partyb = self.startNode('PartyB', cordapps=[TokensCorDapp], database=Databases.postgres96)

		# create the SSH client, ensure nodes are resolved on the network, and issue tokens
		client = TokensSSHClient(self)
		client.waitForParty(self.partya, self.partyb)
		client.waitForParty(self.partyb, self.partya)
		client.issueCash(self.partya, issueTo=self.partya, amount=100)
		self.waitForNodeLog(self.partya, expr='Completed: IssueCash', timeout=10)

		# move tokens and then query the vaults
		client.moveCash(self.partya, moveTo=self.partyb, amount=10)
		self.waitForNodeLog(self.partyb, expr='Completed: MoveCashResponder', timeout=10)
		client.moveCash(self.partyb, moveTo=self.partya, amount=5)
		self.waitForNodeLog(self.partyb, expr='Completed: MoveCashResponder', timeout=10)

		# query the vault
		client.queryFungibleToken(self.partya, stdout='query1.out', stderr='query1.err')
		client.queryFungibleToken(self.partyb, stdout='query2.out', stderr='query2.err')

	def validate(self):
		# check the vault query outputs
		self.assertGrep(file='query1.out', filedir=self.partya.directory, expr='amount:.*90.00 TokenType\(tokenIdentifier=\'GBP\'')
		self.assertGrep(file='query1.out', filedir=self.partya.directory, expr='amount:.*5.00 TokenType\(tokenIdentifier=\'GBP\'')
		self.assertGrep(file='query2.out', filedir=self.partyb.directory, expr='amount:.*5.00 TokenType\(tokenIdentifier=\'GBP\'')
