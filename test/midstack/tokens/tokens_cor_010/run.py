from net.kioti.test.cordatest import BootstrapTest
from net.kioti.test.cordapp.tokens import TokensCorDapp, TokensSSHClient

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
		self.waitForNodeLog(self.partya,  expr='Completed: IssueCashResponder', timeout=10)
		client.queryFungibleToken(self.partya, stdout='query.out', stderr='query.err')

	def validate(self):
		# check log messages in the receiving party
		exprList = []
		exprList.append('Starting: IssueCashResponder')
		exprList.append('Transaction dependencies resolution completed')
		exprList.append('Successfully received fully signed tx. Sending it to the vault for processing')
		exprList.append('Successfully recorded received transaction locally')
		exprList.append('Completed: IssueCashResponder')
		self.assertOrderedGrep(file=self.partya.nodeLogfile, filedir=self.partya.nodeLogdir, exprList=exprList)

		# check the vault query output
		self.assertGrep(file='query.out', filedir=self.partya.directory, expr='amount:.*100.00 TokenType\(tokenIdentifier=\'GBP\'')

