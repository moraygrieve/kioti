from net.kioti.test.cordatest import BootstrapTest
from net.kioti.test.database import Databases
from net.kioti.test.model.node import Notary
from net.kioti.test.cordapp.finance import FinanceCorDapp, FinanceCorDappSSHClient

class PySysTest(BootstrapTest):

    def execute(self):
        # create nodes ready for bootstrapping ... note each call will assign self.<name> to the node with name <name>
        # for ease of later reference e.g. self.partya for "PartyA" etc
        self.localNode('PartyA', database=Databases.postgres96, cordapps=[FinanceCorDapp])
        self.localNode('PartyB', database=Databases.sqlserver, cordapps=[FinanceCorDapp])
        self.localNode('Notary', notary=Notary(False))

        # bootstrap the network and start
        self.bootstrapNetwork()
        self.startNetwork()

        # create the SSH client and issue some cash on PartyA, pay PartyB, and request balances
        client = FinanceCorDappSSHClient(self)
        client.cashIssue(self.partya, '100 USD')
        client.cashPayment(self.partya, '20 USD', self.partyb, anonymous=True)
        map(lambda x: client.cashBalance(x), [self.partya, self.partyb])

    def validate(self):
        self.assertOrderedGrep(file='cash-balance.out', filedir=self.partya.directory, exprList=['amount.*80.00 USD issued by O=PartyA'])
        self.assertLineCount(file='cash-balance.out', filedir=self.partya.directory, expr='- state:', condition='==1')
        self.assertOrderedGrep(file='cash-balance.out', filedir=self.partyb.directory, exprList=['amount.*20.00 USD issued by O=PartyA'])
        self.assertLineCount(file='cash-balance.out', filedir=self.partyb.directory, expr='- state:', condition='==1')
