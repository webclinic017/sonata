
import easytrader

#user = easytrader.use('ht_client')
#user.prepare(user='666625966986', password='745143', comm_password='7451430zy')


#from easytrader import server
#server.run(port=1430)

from easytrader import remoteclient
user = remoteclient.use('ht_client', host='169.254.132.98', port='1430')
user.prepare(user='666625966986', password='745143', comm_password='7451430zy')
print(user.position)

