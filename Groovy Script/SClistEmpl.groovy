def mass = loginForEmpl("Иванов")

def loginForEmpl(names){
    keys=[:]
    names=[names + '%']
    listNames = []
    names.each{
      usr=utils.find('employee',[title:op.like(it)])
      listNames = listNames + usr
      listNames = listNames.findAll{it.login != null}
        listNames.each{
          if(usr){
            keys[it?.title] = utils.find('serviceCall',[clientEmployee:it.UUID,state:op.not('closed')]).UUID
          } else{
            keys = null
            }
        }
    }
    keys
}
