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


col_aditional_questions_names = []


types = [
    'csat',
    'nps',
    'picklist',
    'campo aberto'
]

#Pegar indices pelo nome da coluna
with open(fileName, newline='', encoding='utf-8') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    for row in spamreader:
        index = 0
        for rowCol in row:
            questionType = ''
            rowColLowerWithoutSpace = rowCol.lower().strip()
            
            #Take tipo pergunta
            for type in types:
                if(type.lower()+';' in rowColLowerWithoutSpace.lower()): 
                    questionType = type
                    col_aditional_questions_names.append(rowColLowerWithoutSpace)
                    break

            colArray.append({
                "colName": rowColLowerWithoutSpace,
                "index": index,
                "questionType": questionType
            })

            index += 1
        break

listQuestionResponse = []

with open(fileName, newline='', encoding='utf-8') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    index = 0
    for row in spamreader:
        index+= 1
        if(index == 1):
            continue

        questionTypeOrder1 = ''
        metric = 'CSAT'

        auxMetric = row[colArray[findIndex(colArray, lambda col: col['colName'] == 'metrica')]['index']]

        if(auxMetric == 'nps-0-10'):
            metric = 'NPS'
            questionTypeOrder1 = 'NPS'

        if(metric == 'CSAT'):
            questionTypeOrder1 = 'Rating'

        firstAnswer = row[colArray[findIndex(colArray, lambda col: col['colName'] == 'nota pergunta principal')]['index']]
        secondAnswer = row[colArray[findIndex(colArray, lambda col: col['colName'] == 'feedback')]['index']]
        externalId = row[colArray[findIndex(colArray, lambda col: col['colName'] == 'control_id')]['index']]

        if(str(firstAnswer) != ''):
            listQuestionResponse.append(
                {
                    "attributes": {
                        "type": "SurveyQuestionResponseReport__c",
                    },
                    'Answer__c': firstAnswer,
                    'Question__c': metric,
                    'ShortQuestion__c': metric,
                    'Name': str(firstAnswer).replace('\n', ' ')[0:80],
                    'QuestionOrder__c': '1',
                    'QuestionType__c' : questionTypeOrder1,
                    'SurveyResponseReportId__r:SurveyResponseReport__c:ExternalId__c': externalId
                })
        if(str(secondAnswer) != ''):
            listQuestionResponse.append(
                {
                    "attributes": {
                        "type": "SurveyQuestionResponseReport__c",
                    },
                    'Answer__c': str(secondAnswer),
                    'Question__c': 'Pergunta aberto',
                    'ShortQuestion__c': 'Pergunta aberto',
                    'Name': str(secondAnswer).replace('\n', ' ')[0:80],
                    'QuestionOrder__c': '2',
                    'QuestionType__c' : 'ShortText',
                    'SurveyResponseReportId__r:SurveyResponseReport__c:ExternalId__c': externalId
                }
            )

        questionOrder = 3

        #Perguntas adicionais
        for i in range(len(col_aditional_questions_names)):
            if(col_aditional_questions_names[i] != ''):
                colInfos = colArray[findIndex(colArray, lambda col: col['colName'] == col_aditional_questions_names[i])]
                answer = row[colInfos['index']]
                questionType = colInfos['questionType']

                questionName = col_aditional_questions_names[i].split(';')[1]

                if(questionType == 'csat'):
                    questionType = 'Rating'

                if(questionType == 'campo aberto'):
                    questionType = 'FreeText'

                if(answer != ''):
                    listQuestionResponse.append({
                        "attributes": {
                            "type": "SurveyQuestionResponseReport__c",
                        },
                        'Answer__c': answer,
                        'Question__c': questionName,
                        'ShortQuestion__c': questionName.replace('\n', ' ')[0:80],
                        'Name': answer.replace('\n', ' ')[0:80],
                        'QuestionOrder__c': str(questionOrder),
                        'QuestionType__c' : questionType,
                        'SurveyResponseReportId__r:SurveyResponseReport__c:ExternalId__c': externalId
                    })
                    questionOrder+=1

pyperclip.copy(json.dumps(listQuestionResponse, ensure_ascii=False).replace('\\"','\''))