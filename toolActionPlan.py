import json
import csv
import pyperclip
import json

fileName = 'Caminho para o CSV'

colArray = []

listCasesActionPlanJSON = []

def findIndex(list, filter):
    if filter == None or list == None:
        return '-1'
    index = -1
    
    for x in list:
        index += 1
        if filter(x):
            return index
    return '-1'
    
def formatDate(dateString):
    date = dateString.split(' ')[0]
    hours = dateString.split(' ')[1]

    day = date.split('/')[0]
    month = date.split('/')[1]
    year = date.split('/')[2]

    hour = hours.split(':')[0]
    minute = hours.split(':')[1]
    second = hours.split(':')[2]

    return year+'-'+month+'-'+day+'T'+hour+':'+minute+':'+second+'.000+0000'

#Pegar indices pelo nome da coluna
with open(fileName, newline='', encoding='utf-8') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    for row in spamreader:
        index = 0
        for rowCol in row:
            colArray.append({
                "colName": rowCol,
                "index": index
            })
            index += 1
        break

with open(fileName, newline='', encoding='utf8') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    index = 0
    for row in spamreader:
        index+= 1

        if(index == 1):
            continue

        externalId = row[colArray[findIndex(colArray, lambda col: col['colName'] == 'control_id')]['index']]
        contactId = row[colArray[findIndex(colArray, lambda col: col['colName'] == 'id contato')]['index']]
        accountId = row[colArray[findIndex(colArray, lambda col: col['colName'] == 'id conta')]['index']]
        descriptionCase = row[colArray[findIndex(colArray, lambda col: col['colName'] == 'Plano de ação')]['index']]
        tagCase = row[colArray[findIndex(colArray, lambda col: col['colName'] == 'tag_de_tratativa')]['index']]
        
        if(tagCase == ''):
            continue;

        listCasesActionPlanJSON.append({
            'attributes': {
                'type': 'Case',
            },
            'Subject': 'Plano de Ação',
            'Description': descriptionCase,
            'Tag__c': tagCase.replace('Resolvido-', ''),
            'ContactId': contactId,
            'AccountId': accountId,
            'RespostaPesquisaRelatorio__r:SurveyResponseReport__c:ExternalId__c': externalId
        })

pyperclip.copy(json.dumps(listCasesActionPlanJSON, ensure_ascii=False).replace('\\"','\''))