import re, os
from pysys.constants import INSPECT
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
		self.log.info('Issuing cash in small units')
		for i in range(0,200): client.issueCash(self.issuer, issueTo=self.partya, amount=5, logOut=False)

		self.log.info('Waiting for responder messages')
		self.waitForNodeLog(self.partya, expr='Completed: IssueCashResponder', condition='==200', timeout=20)

		# select the tokens using database
		client.selectCash(self.partya, amount=78, stdout='select1.out', localSelector=False)
		self.waitForNodeLog(self.partya, expr='Database selection of tokens took', timeout=30)

		# select the tokens using local
		client.selectCash(self.partya, amount=78, stdout='select2.out', localSelector=True)
		self.waitForNodeLog(self.partya, expr='Local selection of tokens took', timeout=30)


	def validate(self):
		db_time = self.getTime(type='Database', file=os.path.join(self.partya.nodeLogdir, self.partya.nodeLogfile))
		local_time = self.getTime(type='Local', file=os.path.join(self.partya.nodeLogdir, self.partya.nodeLogfile))

		self.log.info('Time for db selection was %d' % db_time)
		self.log.info('Time for local selection was %d' % local_time)

		# results should be manually inspected for validation
		self.addOutcome(INSPECT)


	def getTime(self, type, file):
		expr1 = re.compile('.*%s selection of tokens took (?P<t>.*) ms.*' % type, re.M)
		t = None
		with open(file, 'r') as fp:
			for line in fp.readlines():
				l = line.strip()
				if expr1.search(line) is not None:
					t = re.match(expr1, l).group('t')
		return int(t)