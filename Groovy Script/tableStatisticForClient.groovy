def clientParent = utils.find('ou$company',[removed:false,parent:op.isNull()])
def firstClientParent = utils.find('ou$company',[removed:false,parent:op.isNull()])[0]
int sizeClientParent = utils.count('ou$company',[removed:false,parent:op.isNull()])

def i = 0;
def map = [:]

while(firstClientParent && i<9)
{
  Circle = clientParent[i]
  map[Circle]=[:]

  def countClientSC = clientParent[i].serviceCalls.size() + clientParent[i].childOUs.serviceCalls.flatten().size()
  def countClientEmpl = clientParent[i].childOUs.employees.flatten().size() + clientParent[i].employees.size()
  def countClientPR = clientParent[i].periodicRules.size() + clientParent[i].childOUs.periodicRules.flatten().size()

  map[Circle] << ['Заявки за всё время' : '<td>' + countClientSC + '</td>']
  map[Circle] << ['Сотрудников клиента' : '<td>' + countClientEmpl + '</td>']
  map[Circle] << ['Регламентные работы' : '<td>' + countClientPR + '</td>']

  i++
    if(sizeClientParent >1){
      firstClientParent = utils.find('ou$company',[removed:false,parent:op.isNull()])[sizeClientParent-1];
      sizeClientParent--
    }
}

str = """<style type="text/css">
A {
text-decoration: none;
color: #0a2c47;
}
A:hover {
text-decoration: underline;
color: #0a2c47;
}
td   {width: 150px;border-bottom: 1px solid #ddd;face: 'Arial';font-size: 9pt;}
p    {width: 150px;border-bottom: 0px solid #ddd;face: 'Arial';font-size: 9pt;}
</style>
<table>
<tbody>
<tr>
<td style='text-align: left;border-bottom: 2px solid #ddd;color: #a6a6a6;face: "Arial";font-size: 9pt;'>Ссылка на клиента </td>
<td style='text-align: left;border-bottom: 2px solid #ddd;color: #a6a6a6;face: "Arial";font-size: 9pt;'>Заявки за всё время </td>
<td style='text-align: left;border-bottom: 2px solid #ddd;color: #a6a6a6;face: "Arial";font-size: 9pt;'>Сотрудников клиента </td>
<td style='text-align: left;border-bottom: 2px solid #ddd;color: #a6a6a6;face: "Arial";font-size: 9pt;'>Регламентные работы </td>
</th>
</tr>"""
map.eachWithIndex { val1, n ->
  str = str + "<td>"+ api.web.asLink(api.web.open(clientParent[n], api.auth.getAccessKey('system')),clientParent[n]?.title.toString())
  str = str + val1.value.'Заявки за всё время'.toString().toString()
  str = str + val1.value.'Сотрудников клиента'.toString()
  str = str + val1.value.'Регламентные работы'.toString()
  str = str + "</tr>"
}
str = str + '</tbody></table>'
str = str.replace('null','')

return str