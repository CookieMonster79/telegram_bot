def clientParent = utils.find('ou$company',[removed:false,parent:op.isNull()])

def firstClientParent = utils.find('ou$company',[removed:false,parent:op.isNull()])[0]
int sizeClientParent = utils.count('ou$company',[removed:false,parent:op.isNull()])
def size = sizeClientParent - 1

def i = 0;
def map = []
def mapMaps = []

while(firstClientParent && i<size)
{
  map=[]

  def countClientSC = clientParent[i].serviceCalls.size() + clientParent[i].childOUs.serviceCalls.flatten().size()
  def countClientEmpl = clientParent[i].childOUs.employees.flatten().size() + clientParent[i].employees.size()
  def countClientPR = clientParent[i].periodicRules.size() + clientParent[i].childOUs.periodicRules.flatten().size()

  map << clientParent[i]
  map << countClientSC
  map << countClientEmpl
  map << countClientPR

  i++
    if(sizeClientParent >1){
      firstClientParent = utils.find('ou$company',[removed:false,parent:op.isNull()])[sizeClientParent-1];
      sizeClientParent--
    }
    mapMaps = mapMaps + map
}

return mapMaps
