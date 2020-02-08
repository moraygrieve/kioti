from net.kioti.test.cordatest import BootstrapTest
from net.kioti.test.cordapp.accounts import AccountsCorDapp
from net.kioti.test.cordapp.accounts import AccountsSSHClient


class PySysTest(BootstrapTest):

    def execute(self):
        # create a bootstrapped network
        self.localNetwork(nodes=['PartyA'], notaries=['Notary'], cordapps=[AccountsCorDapp])
        self.bootstrapNetwork()
        self.startNetwork()

        # start flow to create an account
        client = AccountsSSHClient(self)
        client.createAccount(node=self.partya, name='joeblogs')
        client.createAccount(node=self.partya, name='joeblogs')
        client.createAccount(node=self.partya, name='  ')
        client.createAccount(node=self.partya, name='-.%')

        # wait for completion and then query the vault
        self.waitForNodeLog(self.partya, expr='Completed: CreateAccount', timeout=10)

    def validate(self):
        exprList = []
        exprList.append('Created account, details')
        exprList.append('name:   joeblogs')
        exprList.append('There is already an account registered with the specified name joeblogs')
        exprList.append('name:     ')
        exprList.append('name:   -.%')
        self.assertOrderedGrep(file=self.partya.nodeLogfile, filedir=self.partya.nodeLogdir, exprList=exprList)
