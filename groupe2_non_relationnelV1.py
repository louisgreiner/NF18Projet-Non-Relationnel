import re
from datetime import date
import numpy as np
import os
from pymongo import MongoClient

########## A CHANGER #########

client = MongoClient('mongodb://127.0.0.1:27017/?compressors=disabled&gssapiServiceName=mongodb')
db = client.NF18_nosql

##############################


def isDate(str):
    return (re.match('[0-9]{2}/[0-9]{2}/[0-9]{4}', str) and int(str[0:2]) <= 31 and int(str[3:5]) <= 12)


def isTime(str):
    if re.match('[0-9][0-9]?:[0-9][0-9]', str) :
        if str[1] == ':' and int(str[0:1]) <= 23 and int(str[2:4]) <= 59 :
            return True
        elif str[1] != ':' and int(str[0:2]) <= 23 and int(str[3:5]) <= 59 :
            return True
        else:
            return False


def isYear(str):
    return (re.match('[0-9]{4}', str))


def inputDate(inputMessage):
    dateInput = input(inputMessage)

    while not isDate(dateInput):
        dateInput = input('Veuillez saisir une date au format DD/MM/YYYY...\n\n' + inputMessage)

    return dateInput


def inputTime(inputMessage):
    timeInput = input(inputMessage)

    while not isTime(timeInput):
        timeInput = input('Veuillez saisir un horaire au format HH:MM...\n\n' + inputMessage)

    return timeInput


def inputYear(inputMessage):
    yearInput = input(inputMessage)

    while not isYear(yearInput):
        yearInput = input('Veuillez saisir une année au format YYYY...\n\n' + inputMessage)

    return yearInput

def printTitle(inputMessage):
    for _ in range(len(inputMessage) + 10):
        print('*', end='')
    print()
    
    print(f'*    {inputMessage}    *')
    
    for _ in range(len(inputMessage) + 10):
        print('*', end='')
    print()


def inputFromDict(dict):

    while True:
        # Affichage des choix disponibles
        for key in dict:
            print(f'  {key}: {dict[key]}')

        # Input d'un choix
        choix = input('\nVotre choix : ')

        # Si le choix est valide, on sort
        if choix in dict.keys():
            return (choix, dict[choix])

        print('Numéro choisi incorrect...\n')


def inputTel(inputMessage):
    telInput = input(inputMessage)

    while not re.match('[0-9]{10}', telInput):
        telInput = input('Veuillez saisir une numéro de téléphone valide...\n\n' + inputMessage)

    return telInput


def nextID():
    cursor =  db.personne.find({},{'_id':0})
    dictPersonne = cursorToDict(cursor)

    maxID = np.max(np.array(list(dictPersonne.keys())))
    return int(maxID + 1)



def cursorToDict(cursor, key = 'id'):
    dico = {}
    for document in cursor:
        dico[document[key]] = document
        # print(f"{document['id']}: {document['prenom']} {document['nom']}")

    return dico




def printSpectacle():
    
    cursor =  db.spectacle.find({},{'_id':0})
    dictSpectacle = cursorToDict(cursor)

    for idSpectacle in dictSpectacle:
        print(f"{idSpectacle}: {dictSpectacle[idSpectacle]['type']} ({dictSpectacle[idSpectacle]['duree']}), organisé par {dictSpectacle[idSpectacle]['association']['nom']}")
    
    return
    


def printAssociation():
    cursor =  db.association.find({},{'_id':0})
    dictAsso = cursorToDict(cursor, 'nom')

    for nomAsso in dictAsso:
        print(f"   {nomAsso} : {dictAsso[nomAsso]['description']} ({dictAsso[nomAsso]['categorie']})")

    return 



def choosePersonne():
        
    # Vérification qu'il existe un personne
    cursor =  db.personne.find({},{'_id':0})
    dictPersonne = cursorToDict(cursor)

    for idPersonne in dictPersonne:
        print(f"{idPersonne}: {dictPersonne[idPersonne]['prenom']} {dictPersonne[idPersonne]['nom']}")
        
    chosenID = int(input('\nChoisissez l\'ID de la personne : '))
    while chosenID not in dictPersonne.keys():
        chosenID = int(input('Saisie incorrecte...\n\nChoisissez l\'ID de la personne : '))

    return chosenID, dictPersonne[chosenID]


def printPersonne():
    
    cursor =  db.personne.find({},{'_id':0})
    dictPersonne = cursorToDict(cursor)

    for idPersonne in dictPersonne:
        print(f"{idPersonne}: {dictPersonne[idPersonne]['prenom']} {dictPersonne[idPersonne]['nom']}")
    
    return


def chooseEtudiant(inputMessage):
    
    # Vérification qu'il existe un personne
    cursor =  db.personne.find({'type' :'etudiant'},{'_id':0})
    dictPersonne = cursorToDict(cursor)

    for idPersonne in dictPersonne:
        print(f"{idPersonne}: {dictPersonne[idPersonne]['prenom']} {dictPersonne[idPersonne]['nom']}")
        
    chosenID = int(input(inputMessage))
    while chosenID not in dictPersonne.keys():
        chosenID = int(input('Saisie incorrecte... ' + inputMessage))

    return chosenID, dictPersonne[chosenID]

# Vérification qu'il existe un personne
def chooseEtudiantPersonnel():

    cursor =  db.personne.find( { '$or': [ { 'type': 'etudiant' }, { 'type': 'personnel' } ] } )
    dictPersonne = cursorToDict(cursor)

    for idPersonne in dictPersonne:
        print(f"{idPersonne}: {dictPersonne[idPersonne]['prenom']} {dictPersonne[idPersonne]['nom']}")

    chosenID = int(input('\nChoisissez l\'ID de la personne : '))
    while chosenID not in dictPersonne.keys():
        chosenID = int(input('Saisie incorrecte...\n\nChoisissez l\'ID de la personne : '))
        
    return chosenID, dictPersonne[chosenID]


def chooseAssociation():
    cursor =  db.association.find({},{'_id':0})
    dictAsso = cursorToDict(cursor, 'nom')

    for nomAsso in dictAsso:
        print(f"   [{nomAsso}] {dictAsso[nomAsso]['description']}")

    chosenID = input('\nChoisissez le nom de l\'asso : ')
    while chosenID not in dictAsso.keys():
        chosenID = input('Saisie incorrecte...\n\nChoisissez le nom de l\'asso : ')

    return chosenID, dictAsso[chosenID]


# ### 1. Ajout d'une association

def addAssociation():

    print()
    nom = input('Nom : ')
    description = input('Description : ')
    print('Choisissez la catégorie :')
    categories = {'1' : 'Artistique', '2' : 'Évènementiel', '3' : 'Solidaire'}
    _, categorieAsso = inputFromDict(categories)

    email = input('Email : ')
    dateCreation = inputDate('Date de création (DD/MM/YYYY) : ')
    d,m,y = dateCreation.split('/')
    dateCreation = y + '-' + m + '-' + d

    site = input('Site web (ENTRÉE si aucun) : ')
    site = None if site == '' else site
    print("\nPrésident :")
    _, president = chooseEtudiant('\nChoisissez l\'ID du président : ')
    print("\nTrésorier :")
    _, tresorier = chooseEtudiant('\nChoisissez l\'ID du trésorier : ')

    memberList = []
    while True:
        continuer = input('Voulez-vous insérer un nouveau membre ? [Y/N]\nvotre choix : ')
        if continuer == 'N' :
            break
        print("Nouveau Membre :")
        _, membre = chooseEtudiant('\nChoisissez l\'ID du membre : ')
        memberList.append(membre)

    newAsso = {
        "nom" : nom,
        "description" : description,
        "categorie" : categorieAsso,
        "email" : email,
        "dateCreation" : dateCreation,
        "siteWeb" : site,
        "president" : president,
        "tresorier" : tresorier,
        "membres" : memberList
    }

    print(newAsso)
    result = db.association.insert_one(newAsso)

    input('\nAssociation insérée avec succès !\nAppuyez sur Entrée pour continuer...')

    return


# ### 2. Ajout d'une personne

def addPersonne():

    print()
    prenom = input('Prénom : ')
    nom = input('Nom : ')
    print('Choisissez la catégorie :')
    statutPersonne = {'1' : 'etudiant', '2' : 'personnel', '3' : 'extérieur'}
    numCategorie, typePersonne = inputFromDict(statutPersonne)

    informations = {}
    if numCategorie == '1':
        numCin = input('Numéro CIN : ')
        informations["numCin"] = numCin
        
    if numCategorie == '2' :
        numCin = input('Numéro CIN : ')
        print('Choisissez le statut du personnel :')
        statut_dic = {'1' : 'Enseignant', '2' : 'Personnel Administratif', '3' : 'Personnel Technique'}
        _, statutPersonne = inputFromDict(statut_dic)
        informations["numCin"] = numCin
        informations["statut"] = statutPersonne

    if numCategorie == '3':
        contact = inputTel('Numéro de téléphone : ')
        organisme = input('Organisme : ')
        informations["organisme"] = organisme
        informations["contact"] = contact

    newUser = {
        "id" : nextID(),
        "prenom" : prenom,
        "nom" : nom,
        "type" : typePersonne,
        "informations" : informations
    }
    result = db.personne.insert_one(newUser)
    input('\nUtilisateur ajouté avec succès !\nAppuyez sur Entrée pour continuer...')

    return



# ### 3. Ajout d'un spectacle

def nextSpectacleID():
    cursor =  db.spectacle.find({},{'_id':0})
    dictSpectacle = cursorToDict(cursor)

    maxID = np.max(np.array(list(dictSpectacle.keys())))
    return int(maxID + 1)

def addSpectacle():
    print()
    duree = inputTime('Durée (HH:MM) : ') + ":00"
    print('Choisissez l\'organisateur du spectacle : ')
    nomAsso, association = chooseAssociation()

    print('Type du spectacle : ')
    typeSpectacleDict = {'1' : 'Stand-Up', '2' : 'Théâtre', '3' : 'Concert'}
    numType, typeSpectacle = inputFromDict(typeSpectacleDict)

    informations = {}
    if numType == '1':
        print('Choisissez le genre : ')
        typeStandUpDict = {'1' : 'Table Ronde', '2' : 'Spectacle Comique', '3' : 'Débat'}
        _, genre = inputFromDict(typeStandUpDict)
        informations["genre"] = genre
        
    if numType == '2' :
        auteur = input('Auteur : ')
        anneeParution = inputYear('Année de parution : ') + '-01-01'
        typeTheatre = {'1' : 'Drame', '2' : 'Comédie', '3' : 'Mélodrame'}
        _, genre = inputFromDict(typeTheatre)
        informations["auteur"] = auteur
        informations["anneeParution"] = anneeParution
        informations["genre"] = genre

    if numType == '3':
        compositeur = input('Compositeur : ')
        anneeParution = inputYear('Année de parution : ') + '-01-01'
        typeConcert = {'1' : 'Pop', '2' : 'Classique', '3' : 'Rock'}
        _, genre = inputFromDict(typeConcert)
        informations["compositeur"] = compositeur
        informations["anneeParution"] = anneeParution
        informations["genre"] = genre
        
        
    participantList = []
    while True:
        continuer = input('Voulez-vous insérer un nouveau participant ? [Y/N]\nvotre choix : ')
        if continuer == 'N' :
            break
        print("\nNouveau Participant :")
        _, participant = chooseEtudiantPersonnel()
        participantList.append(participant)
        input(f"Rôle de {participant['prenom']} : ")

        
    newSpectacle = {
        "id" : nextSpectacleID(),
        "duree" : duree,
        "association" : association,
        "type" : typeSpectacle,
        "informations" : informations
    }
    result = db.spectacle.insert_one(newSpectacle)

    input('\nSpectacle inséré avec succès !\nAppuyez sur Entrée pour continuer...')


def menuPrincipal():

    os.system('cls' if os.name == 'nt' else 'clear')

    while True :
        printTitle('UTX VERSION NOSQL (DEMO)')
        print('\nQue souhaitez vous faire ?')

        choix = input('  1: Gérer les utilisateurs\n  2: Gérer les spectacles\n  3: Gérer les associations\n  4: Quitter\n\nVotre choix : ')

        if choix == '1': # utilisateur
            os.system('cls' if os.name == 'nt' else 'clear')

            printTitle('Gestion des utilisateurs')
            while True:
                print('\nQue souhaitez vous faire ?')
                choixUser = input('  1: Ajouter un utilisateur\n  2: Afficher les utilisateurs\n  3: Retour\n\nVotre choix : ')

                if choixUser == '1':
                    os.system('cls' if os.name == 'nt' else 'clear')
                    printTitle('Ajout d\'un utilisateur')
                    addPersonne()
                    os.system('cls' if os.name == 'nt' else 'clear')
                    break
                elif choixUser == '2':
                    os.system('cls' if os.name == 'nt' else 'clear')
                    printTitle('Affichage des utilisateurs')
                    print()
                    printPersonne()
                    input('\nAppuyez sur Entrée pour continuer...')
                    os.system('cls' if os.name == 'nt' else 'clear')
                    break
                elif choixUser == '3':
                    os.system('cls' if os.name == 'nt' else 'clear')
                    break
                else:
                    print('Saisie non reconnue...')

        elif choix == '2': # spectacle
            os.system('cls' if os.name == 'nt' else 'clear')
            printTitle('Gestion des spectacles')

            while True:
                print('\nQue souhaitez-vous faire ?')
                choixSpec = input('   1: Ajouter un spectacle\n   2: Afficher les spectacles\n   3: Retour\n\nVotre choix : ')

                if choixSpec == '1':
                    os.system('cls' if os.name == 'nt' else 'clear')
                    printTitle('Ajout d\'un spectacle')
                    addSpectacle()
                    os.system('cls' if os.name == 'nt' else 'clear')
                    break
                elif choixSpec == '2':
                    os.system('cls' if os.name == 'nt' else 'clear')
                    printTitle('Affichage des spectacles')
                    print()
                    printSpectacle()
                    input('\nAppuyez sur Entrée pour continuer...')
                    os.system('cls' if os.name == 'nt' else 'clear')
                    break
                elif choixSpec == '3':
                    os.system('cls' if os.name == 'nt' else 'clear')
                    break
                else:
                    print('Saisie non reconnue...')

        elif choix == '3': # association
            os.system('cls' if os.name == 'nt' else 'clear')
            printTitle('Gestion des associations')

            while True:
                print('\nQue souhaitez-vous faire ?')
                choixAsso = input('  1: Ajouter une association\n  2: Afficher les associations\n  3: Retour\n\nVotre choix : ')
                
                if choixAsso == '1':
                    os.system('cls' if os.name == 'nt' else 'clear')
                    printTitle('Ajout d\'une association')    
                    addAssociation()
                    os.system('cls' if os.name == 'nt' else 'clear')
                    break
                elif choixAsso == '2':
                    os.system('cls' if os.name == 'nt' else 'clear')
                    printTitle('Affichage des associations')
                    print()
                    printAssociation()
                    input('\nAppuyez sur Entrée pour continuer...')
                    os.system('cls' if os.name == 'nt' else 'clear')
                    break
                elif choixAsso == '3':
                    os.system('cls' if os.name == 'nt' else 'clear')
                    break
                else:
                    print('Saisie non reconnue...')

        elif choix == '4': # Retour
            print('A bientôt :)')
            break
        else:
            # input('Saisie non reconnue... Appuyez sur Entrée pour continuer...')
            print('Saisie non reconnue...\n')

menuPrincipal()
