# delete the old if it exists
az keyvault delete --name 'vmqa-keyvault-01'

# create the keyvault
az keyvault create --name 'vmqa-keyvault-01' --resource-group 'R3QA-01' --location 'UK South'

# create the service principle
az ad sp create-for-rbac --name servprin01 --create-cert > servprin01.json

# set the policies
spn=`cat servprin01.json  | grep appId | awk ' { print $2 } ' | sed 's/"//g' | sed 's/,//g'`
az keyvault set-policy --name 'vmqa-keyvault-01' --spn $spn --key-permissions sign verify create list update get --secret-permissions get set list

# convert to openssl
file=`cat servprin01.json  | grep fileWithCert | awk ' { print $2 } ' | sed 's/"//g' | sed 's/,//g'`
openssl pkcs12 -export -in $file -out out.pkcs12


