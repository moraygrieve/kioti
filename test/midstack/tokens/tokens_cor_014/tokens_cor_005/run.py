from net.corda.test.cordatest import BootstrapTest
from net.corda.test.cordapp.tokens import TokensCorDapp, TokensSSHClient

class PySysTest(BootstrapTest):

	def execute(self):
		# create a bootstrapped network
		self.localNetwork(nodes=['Issuer', 'PartyA', 'PartyB'], notaries=['Notary'], cordapps=[TokensCorDapp])
		self.bootstrapNetwork()
		self.startNetwork()

		# create the SSH client and issue tokens from the issuer to party
		client = TokensSSHClient(self)
		client.issueCash(self.issuer, issueTo=self.partya, amount=100)
		self.waitForNodeLog(self.partya, expr='Completed: IssueCashResponder', timeout=10)

		# move tokens and then query the vaults
		client.moveCash(self.partya, moveTo=self.partyb, amount=10)
		self.waitForNodeLog(self.partyb, expr='Completed: MoveCashResponder', timeout=10)

		client.moveCash(self.partyb, moveTo=self.partya, amount=2)
		self.waitForNodeLog(self.partyb, expr='Completed: MoveCashResponder', timeout=10)

		client.queryFungibleToken(self.partya, stdout='querya.out', stderr='querya.err')
		client.queryFungibleToken(self.partyb, stdout='queryb.out', stderr='queryb.err')

	def validate(self):
		# check the vault query outputs
		exprList=[]
		exprList.append('amount:.*90.00 TokenType\(tokenIdentifier=\'GBP\'')
		exprList.append('amount:.*2.00 TokenType\(tokenIdentifier=\'GBP\'')
		self.assertOrderedGrep(file='querya.out', filedir=self.partya.directory, exprList=exprList)

		exprList=[]
		exprList.append('amount:.*8.00 TokenType\(tokenIdentifier=\'GBP\'')
		self.assertOrderedGrep(file='queryb.out', filedir=self.partyb.directory, exprList=exprList)
