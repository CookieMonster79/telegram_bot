def clientParent = utils.find('ou$company',[removed:false,parent:op.isNull()])

def firstClientParent = utils.find('ou$company',[removed:false,parent:op.isNull()])[0]
int sizeClientParent = utils.count('ou$company',[removed:false,parent:op.isNull()])
def size = sizeClientParent - 1

def i = 0;
def map = [:]

while(firstClientParent && i<size)
{
  Circle = clientParent[i]
  map[Circle]=[:]

  def countClientSC = clientParent[i].serviceCalls.size() + clientParent[i].childOUs.serviceCalls.flatten().size()
  def countClientEmpl = clientParent[i].childOUs.employees.flatten().size() + clientParent[i].employees.size()
  def countClientPR = clientParent[i].periodicRules.size() + clientParent[i].childOUs.periodicRules.flatten().size()

  map[Circle] << ['Заявки за всё время' : countClientSC]
  map[Circle] << ['Сотрудников клиента' : countClientEmpl]
  map[Circle] << ['Регламентные работы' : countClientPR]

  i++
    if(sizeClientParent >1){
      firstClientParent = utils.find('ou$company',[removed:false,parent:op.isNull()])[sizeClientParent-1];
      sizeClientParent--
    }
}

return map