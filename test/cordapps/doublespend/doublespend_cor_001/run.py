import os, re
from net.kioti.test.cordapp.doublespend import DoublespendCorDapp, DoublespendRPCClient
from net.kioti.test.cordatest import BootstrapTest

class PySysTest(BootstrapTest):

	def execute(self):
		# create a bootstrapped network
		self.localNetwork(nodes=['PartyA'], notaries=['Notary'], cordapps=[DoublespendCorDapp])
		self.bootstrapNetwork()
		self.startNetwork()

		# create the SSH client and initiate a flow of doubpe spend attempts
		client = DoublespendRPCClient(self)
		client.run(self.partya, doubleSpendRatio='0.5', numberOfSpends='100')
		self.waitForSignal(file=self.partya.nodeLogfile, filedir=self.partya.nodeLogdir, expr='Run completed')

	def validate(self):
		nt, nda, nd = self.getStats(os.path.join(self.partya.nodeLogdir, self.partya.nodeLogfile))
		self.log.info('Number of successful double spends = %s' % nd)
		self.assertTrue(int(nd) == 0)

	def getStats(self, file):
		expr1 = re.compile('.* Number of transactions: (?P<nt>[0-9]+) .*$', re.M)
		expr2 = re.compile('.* Number of double spend attemnpts: (?P<nda>[0-9]+) .*$', re.M)
		expr3 = re.compile('.* Number of double spends: (?P<nd>[0-9]+) .*$', re.M)
		nt, nda, nd = None, None, None
		with open(file, 'r') as fp:
			for line in fp.readlines():
				l = line.strip()
				if expr1.search(line) is not None: nt = re.match(expr1, l).group('nt').replace(' ','')
				if expr2.search(line) is not None: nda = re.match(expr2, l).group('nda').replace(' ','')
				if expr3.search(line) is not None: nd = re.match(expr3, l).group('nd').replace(' ','')
		return nt, nda, nd