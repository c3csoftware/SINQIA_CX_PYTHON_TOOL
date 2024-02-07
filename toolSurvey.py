import json
import csv
import pyperclip
import random

fileName = 'Base de dados - Planilha.csv'

colArray = []

listAccount = []

#Função de busca em array de objeto
def findIndex(list, filter):
    if filter == None or list == None:
        return '-1'
    index = -1
    
    for x in list:
        index += 1
        if filter(x):
            return index
    return '-1'

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

listSurvey = []

#Formata data da planilha para a forma que o salesforce entende
def formatDatetime(dateString):
    #print (dateString)
    date = dateString.split(' ')[0]
    hours = dateString.split(' ')[1]

    day = date.split('/')[0]
    month = date.split('/')[1]
    year = date.split('/')[2]

    hour = hours.split(':')[0]
    minute = hours.split(':')[1]
    second = hours.split(':')[2]

    return year+'-'+month+'-'+day+'T'+hour+':'+minute+':'+second

with open(fileName, newline='', encoding='utf-8') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    index = 0
    for row in spamreader:
        index+= 1

        if(index == 1):
            continue

        metric = 'CSAT'

        auxMetric = row[colArray[findIndex(colArray, lambda col: col['colName'] == 'metrica')]['index']]

        if(auxMetric == 'nps-0-10'):
            metric = 'NPS'

        emailContact = row[colArray[findIndex(colArray, lambda col: col['colName'] == 'email')]['index']]
        externalId = row[colArray[findIndex(colArray, lambda col: col['colName'] == 'control_id')]['index']]
        channel = row[colArray[findIndex(colArray, lambda col: col['colName'] == 'canal')]['index']]
        surveyName = row[colArray[findIndex(colArray, lambda col: col['colName'] == 'questionário')]['index']]
        caseExternalId = row[colArray[findIndex(colArray, lambda col: col['colName'] == 'chamado')]['index']]
        productName = row[colArray[findIndex(colArray, lambda col: col['colName'] == 'produto')]['index']]
        responseDatetime = row[colArray[findIndex(colArray, lambda col: col['colName'] == 'data_resposta')]['index']]
        inviteDate = row[colArray[findIndex(colArray, lambda col: col['colName'] == 'data_do_convite')]['index']]
        vertical = row[colArray[findIndex(colArray, lambda col: col['colName'] == 'vertical')]['index']]
        caseId = row[colArray[findIndex(colArray, lambda col: col['colName'] == 'id caso')]['index']]
        contatoId = row[colArray[findIndex(colArray, lambda col: col['colName'] == 'id contato')]['index']]

        vertical = vertical.replace('*', '')

        surveyNameReplaced = surveyName.replace('*','')
        caseExternalIdReplaced = caseExternalId.replace('SD-','')
        if(channel == 'e-mail'):
            channel = 'Email'

        if(contatoId == '#N/A'):
            contatoId = ''

        #Verifica se já não existe a pesquisa na lista
        if(findIndex(listSurvey, lambda survey: survey['ExternalId__c'] == externalId) != '-1'):
            continue

        status = 'Concluído'

        if(caseId == '#N/A'):
            caseId = ''

        survey = {
            "attributes": {
                "type": "SurveyResponseReport__c",
            },
            'ExternalId__c': externalId,
            'ContactId__c': contatoId,
            'Channel__c': channel,
            'Metric__c': metric,
            'Status__c': status,
            'Name': surveyNameReplaced + ' - ' + status,
            'SurveyName__c': surveyNameReplaced,
            'Vertical__c': vertical,
            'CaseId__c': caseId,
            'ProductName__c': productName,
            'DatetimeResponse__c': formatDatetime(responseDatetime),
            'DataConvite__c': formatDatetime(inviteDate)
        }

        listSurvey.append(survey)

pyperclip.copy(json.dumps(listSurvey, ensure_ascii=False).replace('\\"','\''))