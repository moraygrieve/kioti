import os, re
from net.kioti.test.cordatest import BootstrapTest
from net.kioti.test.cordapp.confidentities import ConfidentitiesCorDapp, ConfidentitiesSSHClient

class PySysTest(BootstrapTest):

	def execute(self):
		# create a bootstrapped network
		self.localNetwork(nodes=['PartyA', 'PartyB', 'PartyC'], notaries=['Notary'], cordapps=[ConfidentitiesCorDapp])
		self.bootstrapNetwork()
		self.startNetwork()

		# create the SSH client and blow the whistle on partyb anonymously
		client = ConfidentitiesSSHClient(self)
		client.blowWhistle(self.partya, self.partyb, self.partyc, flow='BlowWhistleFlowOld', stdout='blow.out', stderr='blow.err')
		client.blowWhistleList(self.partyc, flow='BlowWhistleFlowOldList', stdout='list.out', stderr='list.err')
		client.vaultQuery(self.partyc, contractStateType='net.corda.test.confidentities.contracts.BlowWhistleAnonymousState', stdout='query.out', stderr='query.err')

	def validate(self):
		wid, iid = self.getIDs(os.path.join(self.partyc.directory, 'query.out'))
		self.log.info('Originator id = %s' % wid)
		self.log.info('Investigator id = %s' % iid)
		self.assertTrue(wid is not None and wid!=self.partya.config.myLegalName)
		self.assertTrue(iid is not None and iid!=self.partyc.config.myLegalName)

	def getIDs(self, file):
		expr1 = re.compile('^whistleBlower: "(?P<wid>.*)"$', re.M)
		expr2 = re.compile('^investigator: "(?P<iid>.*)"$', re.M)
		wid = None
		iid = None
		with open(file, 'r') as fp:
			for line in fp.readlines():
				l = line.strip()
				if expr1.search(line) is not None: wid = re.match(expr1, l).group('wid').replace(' ','')
				if expr2.search(line) is not None: iid = re.match(expr2, l).group('iid').replace(' ','')
		return wid, iid
