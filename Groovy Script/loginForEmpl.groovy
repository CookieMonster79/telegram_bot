def mass = loginForEmpl("Иванов")

def loginForEmpl(names){
    keys=""
    names=[names + '%']
    listNames = []
    names.each{
      usr=utils.find('employee',[title:op.like(it)])
      listNames = listNames + usr
        listNames.each{
          if(usr){
            keys+="${api.web.asLink(api.web.open(it, api.auth.getAccessKey(it.login).setDisposable().setDeadlineDays(5)), it.title)} <pre>\n</pre>"
          } else{
            keys = null
            }
        }
    }
    keys
}