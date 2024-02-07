import json
import csv
import pyperclip
import random

fileName = 'Base de dados - Planilha.csv'

colArray = []

listContact = []

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

#Pegar contas da planilha
with open(fileName, newline='', encoding='utf-8') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    index = 0
    for row in spamreader:
        index+= 1

        if(index == 1):
            continue

        contactName = row[colArray[findIndex(colArray, lambda col: col['colName'] == 'nome')]['index']]
        contactEmail = row[colArray[findIndex(colArray, lambda col: col['colName'] == 'email')]['index']]
        contactPhone = row[colArray[findIndex(colArray, lambda col: col['colName'] == 'telefone')]['index']]
        idConta = row[colArray[findIndex(colArray, lambda col: col['colName'] == 'id conta')]['index']]
        idOrganizacao = row[colArray[findIndex(colArray, lambda col: col['colName'] == 'id organizacao')]['index']]
        idContato = row[colArray[findIndex(colArray, lambda col: col['colName'] == 'id contato')]['index']]

        #Verifica se já não existe o contato na lista
        if(findIndex(listContact, lambda contact: contact['Email'].lower() == contactEmail.lower()) != '-1'):
            continue

        #Verifica se já não existe o contato no salesforce
        if(idContato != '#N/A'):
            continue

        firstName = contactName.split(' ')[0];
        lastName = 'Sem sobrenome'

        if(idConta == '#N/A'):
            idConta = ''
        
        if(idOrganizacao == '#N/A'):
            idOrganizacao = ''

        if(len(contactName.split(' ')) > 1):
            lastName = contactName.split(' ', 1)[1]

        contact = {
            "attributes": {
                "type": "Contact",
            },
            'FirstName': firstName,
            'LastName': lastName,
            'Email': contactEmail,
            'Phone': contactPhone,
            'AccountId': idConta,
            'Organization__c': idOrganizacao
        }

        listContact.append(contact)

pyperclip.copy(json.dumps(listContact, ensure_ascii=False).replace('\\"','\''))