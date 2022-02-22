def mass = infoForCall("1000")

def infoForCall(call){
    def subj = utils.findFirst('serviceCall',[number:call])
    map = ['Тема':subj.shortDescr, 'Описание':subj.descriptionRTF.toString(), 'Статус': api.metainfo.getStateTitle(subj).toString(), 'Ответственный':subj.responsibleEmployee.toString()+ '/'+ subj.responsibleTeam.toString()]

    return map
}