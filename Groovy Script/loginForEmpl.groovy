def mass = loginForEmpl("Иванов")

def loginForEmpl(names){
    keys=""
    names=[names + '%']
    listNames = []
    names.each{
      usr=utils.find('employee',[title:op.like(it)])
      listNames = listNames + usr
      listNames = listNames.findAll{it.login != null}
        listNames.each{
          if(usr){
            keys+="${api.web.asLink(api.web.open(it, api.auth.getAccessKey(it?.login).setReusable().setDeadlineHours(1)), it.title)} <pre>\n</pre>"
          } else{
            keys = null
            }
        }
    }
    keys
}