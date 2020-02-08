from net.corda.test.cordatest import BootstrapTest
from net.corda.test.cordapp.tokens import TokensCorDapp, TokensSSHClient

class PySysTest(BootstrapTest):

	def execute(self):
		# create a bootstrapped network
		self.localNetwork(nodes=['Issuer', 'PartyA'], notaries=['Notary'], cordapps=[TokensCorDapp])
		self.bootstrapNetwork()
		self.startNetwork()

		# create the SSH client and issue tokens from the issuer to party
		client = TokensSSHClient(self)
		client.issueCash(self.issuer, issueTo=self.partya, amount=100)

		# wait for completion and then query the vault
		self.waitForNodeLog(self.partya, expr='Completed: IssueCashResponder', timeout=10)
		client.queryFungibleToken(self.partya, stdout='query.out', stderr='query.err')

		# select the tokens
		client.selectCash(self.partya, amount=100, stdout='select1.out')
		client.selectCash(self.partya, amount=10, stdout='select2.out')
		self.waitForNodeLog(self.partya, expr='Completed: SelectCash', condition='==2', timeout=30)

	def validate(self):
		exprList = []
		exprList.append('Starting: SelectCash - Selecting 100')
		exprList.append('State: TransactionState\(data=100.00 TokenType\(tokenIdentifier=\'GBP\'')
		exprList.append('Starting: SelectCash - Selecting 10')
		exprList.append('State: TransactionState\(data=100.00 TokenType\(tokenIdentifier=\'GBP\'')
		self.assertOrderedGrep(file=self.partya.nodeLogfile, filedir=self.partya.nodeLogdir, exprList=exprList)