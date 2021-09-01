use(groovy.time.TimeCategory) {
    return utils.find('serviceCall',['removed':false,'creationDate': op.between(new Date()-1.day, new Date())]).size()
}