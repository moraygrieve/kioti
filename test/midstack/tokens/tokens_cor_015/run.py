from net.kioti.test.cordatest import BootstrapTest
from net.kioti.test.cordapp.tokens import TokensCorDapp, TokensSSHClient

class PySysTest(BootstrapTest):

	def execute(self):
		# create a bootstrapped network
		self.localNetwork(nodes=['PartyA', 'PartyB'], notaries=['Notary'], cordapps=[TokensCorDapp])
		self.bootstrapNetwork()
		self.startNetwork()

		# create the SSH client and issue tokens from the issuer to party
		client = TokensSSHClient(self)
		client.issueCash(self.partya, issueTo=self.partya, amount=100)

		# wait for completion and then query the vault
		self.waitForNodeLog(self.partya, expr='Completed: IssueCash', timeout=10)
		client.queryFungibleToken(self.partya, stdout='query.out', stderr='query.err')

		# move tokens and then query the vaults
		client.moveCash(self.partya, moveTo=self.partyb, amount=10)
		self.waitForNodeLog(self.partyb, expr='Completed: MoveCashResponder', timeout=10)
		client.queryFungibleToken(self.partya, stdout='query1.out', stderr='query1.err')
		client.queryFungibleToken(self.partyb, stdout='query2.out', stderr='query2.err')

	def validate(self):
		exprList=[]
		exprList.append("Starting: IssueCash - Issuing 100 to.*PartyA")
		exprList.append("No need to notarise this transaction")
		exprList.append("Recording transaction locally")
		exprList.append("Recorded transaction locally successfully")
		exprList.append("All parties received the transaction successfully")
		exprList.append("Completed: IssueCash")
		self.assertOrderedGrep(file=self.partya.nodeLogfile, filedir=self.partya.nodeLogdir, exprList=exprList)

		# check the vault query outputs
		self.assertGrep(file='query.out', filedir=self.partya.directory, expr='amount:.*100.00 TokenType\(tokenIdentifier=\'GBP\'')
		self.assertGrep(file='query1.out', filedir=self.partya.directory, expr='amount:.*90.00 TokenType\(tokenIdentifier=\'GBP\'')
		self.assertGrep(file='query2.out', filedir=self.partyb.directory, expr='amount:.*10.00 TokenType\(tokenIdentifier=\'GBP\'')



