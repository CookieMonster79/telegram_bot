use(groovy.time.TimeCategory) {
  	def str1 = (new Date()-1.day).format('dd-MM-yyyy')
    def str2 =  new Date().format('dd-MM-yyyy')

  return utils.count('serviceCall',['creationDate' : op.between(new Date().parse('dd-MM-yyyy', str1), new Date().parse('dd-MM-yyyy', str2))])
}