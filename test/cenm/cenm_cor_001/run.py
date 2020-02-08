import jks, os
from pysys.constants import FAILED, PASSED
from net.kioti.test.cenm.pkitool import PKIToolHelper
from net.kioti.test.cenmtest import CENMTest

class PySysTest(CENMTest):

	def execute(self):
		tool = PKIToolHelper.create(self, defaultPassword='passw0rd')
		tool.run()

	def validate(self):
		ts = os.path.join(self.output, 'trust-stores','network-root-truststore.jks')
		self.checkExists(ts)
		self.checkInvalidPassword(ts)
		self.checkCerts(ts)

	def checkExists(self, ts):
		if not os.path.exists(ts): self.addOutcome(FAILED, 'Trustore not created')

	def checkInvalidPassword(self, ts):
		self.log.info('Attempt to open truststore with an incorrect password')
		try:
			jks.KeyStore.load(ts, 'passphrase')
			self.addOutcome(FAILED, outcomeReason='Trustore opened with incorrect password')
		except jks.KeystoreSignatureException:
			self.addOutcome(PASSED)

	def checkCerts(self, ts):
		self.log.info('Attempt to open truststore with correct password')
		try:
			ots = jks.KeyStore.load(ts, 'passw0rd')
			self.assertTrue(u'cordarootca' in ots.certs.keys(), assertMessage='Check cordarootca in certs')
			self.assertTrue(u'cordatlscrlsigner' in ots.certs.keys(), assertMessage='Check cordatlscrlsigner in certs')
			self.assertTrue(len(ots.certs)==2, assertMessage='Check only two certs')
		except jks.KeystoreSignatureException:
			self.addOutcome(FAILED, outcomeReason='Unable to open trustore with correct password')