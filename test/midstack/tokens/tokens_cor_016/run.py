import os
from net.kioti.test.cordatest import BootstrapTest
from net.kioti.test.cordapp.tokens import TokensCorDapp, TokensSSHClient

class PySysTest(BootstrapTest):

	def execute(self):
		# configure and bootstrap a network, but dont start
		self.localNetwork(nodes=['PartyA', 'PartyB'], notaries=['NotaryA', 'NotaryB'], cordapps=[TokensCorDapp])
		self.bootstrapNetwork()

		# configure to use notarya and start the network
		for party in [self.partya, self.partyb]:
			confs = map(lambda x: os.path.basename(x).replace('jar','conf'), TokensCorDapp.getjars())
			workflows = filter(lambda x: 'workflows' in x, confs)[0]
			with open(os.path.join(party.directory, 'cordapps', 'config', workflows), 'w') as fp:
				fp.writelines('notary=\"%s\"\n' % (self.notarya.config.myLegalName))
				fp.flush
		self.startNetwork()

		# create the SSH client and issue tokens from the issuer to party
		client = TokensSSHClient(self)
		client.issueCash(self.partya, issueTo=self.partya, amount=100)
		self.waitForNodeLog(self.partya, expr='Completed: IssueCash', timeout=10)

		# move tokens and then query the vaults
		client.moveCash(self.partya, moveTo=self.partyb, amount=10)
		self.waitForNodeLog(self.partyb, expr='Completed: MoveCashResponder', timeout=10)
		client.queryFungibleToken(self.partya, stdout='query1.out', stderr='query1.err')
		client.queryFungibleToken(self.partyb, stdout='query2.out', stderr='query2.err')

	def validate(self):
		# check the vault query outputs
		self.assertGrep(file='query1.out', filedir=self.partya.directory, expr='amount:.*90.00 TokenType\(tokenIdentifier=\'GBP\'')
		self.assertGrep(file='query2.out', filedir=self.partyb.directory, expr='amount:.*10.00 TokenType\(tokenIdentifier=\'GBP\'')

		exprList=[]
		exprList.append('Loaded network parameters: NetworkParameters')
		exprList.append('notaries=\[NotaryInfo\(identity=O=NotaryB.* NotaryInfo\(identity=O=NotaryA')
		exprList.append('Received a notarisation request for Tx')
		exprList.append('Transaction.*successfully notarised, sending signature back to')
		self.assertOrderedGrep(file=self.notarya.nodeLogfile, filedir=self.notarya.nodeLogdir, exprList=exprList)