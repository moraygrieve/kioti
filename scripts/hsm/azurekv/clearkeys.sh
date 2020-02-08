kids=`az keyvault key list --vault-name 'vmqa-keyvault-01' | grep kid  | awk ' { print $2 }' | sed 's/[",]//g'`
for kid in $kids;
do
 az keyvault key delete --vault-name 'vmqa-keyvault-01' --id $kid
 echo $kid
done
