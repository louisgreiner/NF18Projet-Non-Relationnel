##### A CHANGER  #####

# arguments = "dbname='dbnf18p073' user='nf18p073' host='tuxa.sme.utc' password='96ScTkSo'"
# arguments = "dbname='dbnf18p083' user='nf18p083' host='tuxa.sme.utc' password='SGcA8loh'"
arguments = "dbname='benji' user='benji' host='localhost' password=''"

######################

import psycopg2
import re
from datetime import date
import os


def run(sql,args):
    conn = psycopg2.connect(arguments)
    cur = conn.cursor()
    try:
        pass
    except Exception as e:
        raise
    cur.execute(sql,args)

    if cur.description: # Si la requête renvoie des informations (e.g. SELECT)
        results = cur.fetchall()
    else:
        results = False

    conn.commit()
    cur.close()
    conn.close()
    return results


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


def isPrice(str):
    return re.match('[0-9]{1,3}(\.[0-9])?[0-9]?', str)


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


def inputNumber(inputMessage):
    numInput = input(inputMessage)

    while not re.match('[0-9]{1,5}', numInput):
        numInput = input('Veuillez saisir un nombre correct...\n\n' + inputMessage)

    return numInput


def inputYear(inputMessage):
    yearInput = input(inputMessage)

    while not isYear(yearInput):
        yearInput = input('Veuillez saisir une année au format YYYY...\n\n' + inputMessage)

    return yearInput


def inputTel(inputMessage):
    telInput = input(inputMessage)

    while not re.match('[0-9]{10}', telInput):
        telInput = input('Veuillez saisir une numéro de téléphone valide...\n\n' + inputMessage)

    return telInput


def inputFromDict(dict):

    while True:
        # Affichage des choix disponibles
        for key in dict:
            print(f'  {key}: {dict[key]}')

        # Input d'un choix
        choix = input('\nVotre choix : ')

        # Si le choix est valide, on sort
        if choix in dict.keys():
            return dict[choix]

        print('Numéro choisi incorrect...\n')


def inputPrice(inputMessage):
    priceInput = input(inputMessage)

    while not isPrice(priceInput):
        priceInput = input('Saisie Invalide ...\n\n' + inputMessage)

    return priceInput


def printTitle(inputMessage):
    for _ in range(len(inputMessage) + 10):
        print('*', end='')
    print()
    
    print(f'*    {inputMessage}    *')
    
    for _ in range(len(inputMessage) + 10):
        print('*', end='')
    print()

def printTable(table, header_list, width_list, length):

    # Affichage du header
    for i in range(len(header_list)):
        print(f'| {str(header_list[i]):{width_list[i]}}', end = " ")
    print('|')

    # Ligne de séparation
    for _ in range(length):
        print('-', end='')
    print()

    # Affichage du corps
    id_list = []
    for row in table:
        for i in range(len(row)):
            print(f'| {str(row[i]):{width_list[i]}}', end = " ")
        print('|')

        id_list.append(str(row[0]))

    return id_list


def chooseSpectacle():

    # Vérification qu'il existe un spectacle
    listSpect = run('SELECT * FROM spectacle_medium ORDER BY ID',())
    if not listSpect:
        print('Vous n\'avez créé aucun spectacle...')
        return

    print('\nChoisissez le spectacle :\n')

    # Affichage des spectacles
    header_list = ['ID', 'Organisateur', 'Durée', 'Genre', 'Catégorie']
    width_list = [4, 15, 8, 12, 9]
    length = 64
    id_list = printTable(listSpect, header_list, width_list, length)

    # Choix du spectacle
    idSpectacle = input('\nID du spectacle : ')
    while idSpectacle not in id_list:
        idSpectacle = input('Veuillez saisir un des IDs de la première colonne... \n\nVotre choix : ')

    return int(idSpectacle)


def printSpectacle():

    # Vérification qu'il existe un spectacle
    listSpect = run('SELECT * FROM spectacle_medium ORDER BY ID',())
    print()
    if not listSpect:
        print('Vous n\'avez créé aucun spectacle...')
        return

    # Affichage des spectacles
    header_list = ['ID', 'Organisateur', 'Durée', 'Genre', 'Catégorie']
    width_list = [4, 15, 8, 12, 9]
    length = 64
    id_list = printTable(listSpect, header_list, width_list, length)

    return


def chooseAssociation():

    # Vérification qu'il existe une association
    listAsso = run('SELECT nom, description FROM association ORDER BY nom',())
    if not listAsso:
        print('\nVous n\'avez créé aucune association...')
        return

    print('\nChoisissez l\'association :\n')

    # Affichage des associations
    header_list = ['Nom', 'Description']
    width_list = [15, 50]
    length = 72
    id_list = printTable(listAsso, header_list, width_list, length)

    # Choix de l'association
    nomAsso = input('\nNom : ')
    while nomAsso not in id_list:
        nomAsso = input('Veuillez saisir un des noms de la première colonne... \n\nVotre choix : ')

    return nomAsso


def printAssociation():

    # Vérification qu'il existe une association
    listAsso = run('SELECT nom, description, categorie FROM association ORDER BY nom',())
    print()

    if not listAsso:
        print('Vous n\'avez créé aucune association...')
        return

    # Affichage des associations
    header_list = ['Nom', 'Description','Catégorie']
    width_list = [15, 50,15]
    length = 90
    id_list = printTable(listAsso, header_list, width_list, length)

    return


def chooseSalle():

    # Vérification qu'il existe un batiment
    listBat = run('SELECT * FROM batiment ORDER BY numBat',())
    if not listBat:
        print('Vous n\'avez créé aucun batiment...')
        return

    print('\nChoisissez le bâtiment :\n')

    # Affichage des batiments
    header_list = ['Numéro']
    width_list = [8]
    length = 12
    id_list = printTable(listBat, header_list, width_list, length)

    # Choix du batiment
    numBat = input('\nNuméro : ')
    while numBat not in id_list:
        numBat = input('Veuillez saisir un numéro valide... \n\nVotre choix : ')

    # Vérification qu'il existe une salle
    listSalle = run('SELECT t.numsalle, capacite, libelletype FROM typesalle t, salle s WHERE t.numsalle=s.numsalle AND numBat=%s ORDER BY numSalle',(numBat,))
    if not listSalle:
        print('Il n\'existe aucune salle dans ce batiment...')
        return

    print('\nChoisissez la salle dans ce bâtiment :\n')

    # Affichage des salles
    header_list = ['Numéro', 'Capacité', 'Type']
    width_list = [8, 12, 11]
    length = 41
    id_list = printTable(listSalle, header_list, width_list, length)

    # Choix de la salle
    numSalle = input('\nNuméro : ')
    while numSalle not in id_list:
        numSalle = input('Veuillez saisir un numéro valide... \n\nVotre choix : ')

    return int(numBat), int(numSalle)

def chooseReservation():

    numBat, numSalle = chooseSalle()

    # Vérification qu'il existe une date
    listRes = run('SELECT date, nom FROM reservation WHERE numBat=%s and numSalle=%s',(numBat,numSalle))
    if not listRes:
        print('Il n\'existe aucune réservation pour cette salle...')
        return False

    print('Choisissez la date de la réservation :\n')

    # Affichage des réservation
    header_list = ['Date', 'Association']
    width_list = [10, 16]
    length = 33
    id_list = printTable(listRes, header_list, width_list, length)

    # Choix de la date
    chosenDate = input('\nDate (YYYY-MM-DD) : ')
    while chosenDate not in id_list:
        chosenDate = input('Veuillez saisir une des dates proposées... \n\nVotre choix : ')

    return int(numBat), int(numSalle), str(chosenDate)


def printSalle():

    # Vérification qu'il existe un batiment
    listSalle = run('SELECT * FROM typesalle ORDER BY numBat',())
    print()
    if not listSalle:
        print('Vous n\'avez créé aucune salle...')
        return

    # Affichage des salles
    header_list = ['Bâtiment', 'Numéro', 'Type']
    width_list = [8, 8, 11]
    length = 37
    id_list = printTable(listSalle, header_list, width_list, length)

    return


def choosePersonne():

    # Vérification qu'il existe une personne
    listPers = run('SELECT * FROM personne ORDER BY idPersonne',())
    if not listPers:
        print('\nIl n\'existe aucun utilisateur dans la base...')
        return

    print('\nChoisissez l\'utilisateur :\n')

    # Affichage des personnes
    header_list = ['ID', 'Nom', 'Prénom']
    width_list = [4, 16, 16]
    length = 46
    id_list = printTable(listPers, header_list, width_list, length)

    # Choix de la personne
    idPers = input('\nID de la personne : ')
    while idPers not in id_list:
        idPers = input('Veuillez saisir un des IDs de la première colonne... \n\nVotre choix : ')

    return int(idPers)


def chooseBillet():

    # Vérification qu'il existe une personne
    listBillet = run('SELECT idBillet, nom, prenom, date, horairedebut FROM billet b, personne p, seance s where b.idacheteur=p.idPersonne and s.idseance=b.idseance ORDER BY idBillet',())
    if not listBillet:
        print('Il n\'existe aucun billet dans la base...')
        return False

    print('Choisissez l\'ID du billet :\n')

    # Affichage des billets
    header_list = ['ID', 'Nom', 'Prénom', 'Date', 'Horaire']
    width_list = [4, 16, 16, 10, 8]
    length = 70
    id_list = printTable(listBillet, header_list, width_list, length)

    # Choix de la personne
    idBillet = input('\nID du billet : ')
    while idBillet not in id_list:
        idBillet = input('Veuillez saisir un des IDs de la première colonne... \n\nVotre choix : ')

    return int(idBillet)



def printPersonne():

    # Vérification qu'il existe une personne
    listPers = run('SELECT * FROM personne_medium ORDER BY id',())
    print()

    if not listPers:
        print('Il n\'existe aucun utilisateur dans la base...')
        return

    # Affichage des personnes
    header_list = ['ID', 'Nom', 'Prénom', 'Catégorie']
    width_list = [4, 16, 16,10]
    length = 59
    printTable(listPers, header_list, width_list, length)

    return


def chooseEtudiant():

    # Vérification qu'il existe une personne
    listPers = run('SELECT p.idPersonne, p.nom, p.prenom FROM personne p, etudiant e where e.idPersonne = p.idPersonne ORDER BY idPersonne',())
    if not listPers:
        print('\nIl n\'existe aucun étudiant dans la base...')
        return

    print('\nChoisissez l\'étudiant :\n')

    # Affichage des personnes
    header_list = ['ID', 'Nom', 'Prénom']
    width_list = [4, 16, 16]
    length = 46
    id_list = printTable(listPers, header_list, width_list, length)

    # Choix de la personne
    idPers = input('\nID de l\'étufiant : ')
    while idPers not in id_list:
        idPers = input('Veuillez saisir un des IDs de la première colonne... \n\nVotre choix : ')

    return int(idPers)


def choosePersonnel():

    # Vérification qu'il existe un personnel
    listPers = run('SELECT p.idPersonne, p.nom, p.prenom FROM personne p, personnel where personnel.idPersonne = p.idPersonne ORDER BY idPersonne',())
    if not listPers:
        print('\nIl n\'existe aucun personnel dans la base...')
        return

    print('\nChoisissez le personnel :\n')

    # Affichage des personnes
    header_list = ['ID', 'Nom', 'Prénom']
    width_list = [4, 16, 16]
    length = 46
    id_list = printTable(listPers, header_list, width_list, length)

    # Choix de la personne
    idPers = input('\nID du personnel : ')
    while idPers not in id_list:
        idPers = input('Veuillez saisir un des IDs de la première colonne... \n\nVotre choix : ')

    return int(idPers)

def chooseExterieur():

    # Vérification qu'il existe un exterieur
    listExte = run('SELECT p.idPersonne, p.nom, p.prenom, e.organisme FROM personne p, exterieur e where e.idPersonne = p.idPersonne ORDER BY idPersonne',())
    if not listExte:
        print('Il n\'existe aucune personne extérieure dans la base...')
        return

    print('Choisissez la personne extérieure :\n')

    # Affichage des personnes
    header_list = ['ID', 'Nom', 'Prénom', 'Organisme']
    width_list = [4, 16, 16,20]
    length = 68
    id_list = printTable(listExte, header_list, width_list, length)

    # Choix de la personne
    idExte = input('\nID de la personne extérieure : ')
    while idExte not in id_list:
        idExte = input('Veuillez saisir un des IDs de la première colonne... \n\nVotre choix : ')

    return int(idExte)


def chooseSeance():

    # Vérification qu'il existe une séance
    listSeance = run('select idseance, date, horaireDebut, numBat, numSalle, categorie from seance se, spectacle_medium sp where id = idSpectacle;',())

    if not listSeance:
        print('Il n\'existe aucune séance...')
        return

    print('Choisissez la séance :\n')

    # Affichage des séances
    header_list = ['ID', 'Date', 'Heure', 'Salle', 'Bâtiment', 'Catégorie']
    width_list = [3, 10, 8, 6, 8, 12]
    length = 66
    id_list = printTable(listSeance, header_list, width_list, length)

    # Choix de la séance
    idSeance = input('\nID de la séance : ')
    while idSeance not in id_list:
        idSeance = input('Veuillez saisir un des IDs de la première colonne... \n\nVotre choix : ')

    return int(idSeance)


def chooseGenreConcert():

    # Vérification qu'il existe un genre
    listgenre = run('SELECT * FROM genreconcert',())
    if not listgenre:
        print('Il n\'y a aucun genre de concert prédéfini...')
        return

    print('Choisissez le genre :\n')

    # Affichage des genres
    header_list = ['Nom']
    width_list = [14]
    length = 18
    id_list = printTable(listgenre, header_list, width_list, length)

    # Choix du genre
    nomGenre = input('\nNom du genre : ')
    while nomGenre not in id_list:
        nomGenre = input('Veuillez saisir un des noms de la première colonne... \n\nVotre choix : ')

    return nomGenre


def chooseGenreTheatre():

    # Vérification qu'il existe un genre
    listgenre = run('SELECT * FROM genretheatre',())
    if not listgenre:
        print('Il n\'y a aucun genre prédéfini pour les pièces de théâtre ...')
        return

    print('Choisissez le genre :\n')

    # Affichage des genres
    header_list = ['Nom']
    width_list = [14]
    length = 18
    id_list = printTable(listgenre, header_list, width_list, length)

    # Choix du genre
    nomGenre = input('\nNom du genre : ')
    while nomGenre not in id_list:
        nomGenre = input('Veuillez saisir un des noms de la première colonne... \n\nVotre choix : ')

    return nomGenre


def chooseGenreStandUp():

    # Vérification qu'il existe un genre
    listgenre = run('SELECT * FROM genrestandup',())
    if not listgenre:
        print('Il n\'y a aucun genre prédéfini pour le Stand-Up ...')
        return

    print('Choisissez le genre :\n')

    # Affichage des genres
    header_list = ['Nom']
    width_list = [14]
    length = 18
    id_list = printTable(listgenre, header_list, width_list, length)

    # Choix du genre
    nomGenre = input('\nNom du genre : ')
    while nomGenre not in id_list:
        nomGenre = input('Veuillez saisir un des noms de la première colonne... \n\nVotre choix : ')

    return nomGenre


def chooseCategorie():

    # Vérification qu'il existe une catégorie
    listCat = run('SELECT * FROM categorie',())
    if not listCat:
        print('Il n\'y a aucune catégorie de billet prédéfinie dans la base...')
        return

    print('Choisissez la catégorie :\n')

    # Affichage des catégories
    header_list = ['Nom']
    width_list = [18]
    length = 22
    id_list = printTable(listCat, header_list, width_list, length)

    # Choix du genre
    nomCat = input('\nNom de la catégorie : ')
    while nomCat not in id_list:
        nomCat = input('Veuillez saisir un des noms de la première colonne... \n\nVotre choix : ')

    return nomCat



# ### 1. Ajout d'une association

def addAssociation():

    # Renseignement du nom
    nom = input('Nom de l\'association : ')

    # Vérification du nom
    foundAsso = run('SELECT * FROM association WHERE nom=%s',(nom,))

    while foundAsso:
        print(f'Le nom \'{nom}\' est déjà pris...\n')
        nom = input('Nom de l\'association : ')
        foundAsso = run('SELECT * FROM association WHERE nom=%s',(nom,))

    print('Qui sera président de cette association ?')
    idPresident = chooseEtudiant()

    print('Qui sera trésorier de cette association ?')
    idTresorier = chooseEtudiant()

    # Renseignement des autres champs
    description = input('Description l\'association : ')
    categorie = input('Catégorie : ')
    email = input('Adresse email : ')
    dateCreation = inputDate('Date de création (DD/MM/YYYY) : ')

    site = input('Site web (ENTRÉE si aucun) : ')
    site = None if site == '' else site

    insert = 'INSERT INTO association VALUES (%s, %s, %s, %s, TO_DATE(%s, \'DD/MM/YYYY\'), %s)'
    run(insert,(nom,description,categorie,email,dateCreation,site))
    run('insert into compose values (%s, %s, %s)', (idPresident, nom, 'Président'))
    run('insert into compose values (%s, %s, %s)', (idTresorier, nom, 'Trésorier'))

    print(f'\nL\'association {nom} a été ajoutée avec succès')
    input('\nAppuyez sur Entrée pour continuer...')
    return


# ### 2. Ajout d'une personne

def addPersonne():

    # choix personnel, etu, autre
    print('\nChoisissez le type de personne à ajouter :\n  1: Étudiant\n  2: Personnel\n  3: Extérieur\n  4: Retour au menu\n')

    choix = input('Votre choix : ')

    if choix == '1': # Etudiant
        print('\nAjout d\'un etudiant :')
        addEtudiant()

    elif choix == '2': # Personnel
        print('\nAjout d\'un membre du personnel :')
        addPersonnel()
    elif choix == '3': # Exterieur
        print('\nAjout d\'un membre extérieur :')
        addExterieur()
    elif choix != '4': # Retour
        print('Veuillez saisir un nombre entre 1 et 4.')
        addPersonne()

    return


def addEtudiant():

    # Renseignement du numéro CIN
    numCIN = input('Numéro CIN : ')

    # Vérification du numero CIN
    foundCIN = run('SELECT numeroCIN FROM etudiant WHERE numeroCIN=%s UNION SELECT numeroCIN FROM personnel WHERE numeroCIN=%s',(numCIN,numCIN))

    while foundCIN:
        print(f'Le numéro CIN \'{numCIN}\' est déjà pris...\n')
        numCIN = input('Numéro CIN : ')
        foundCIN = run('SELECT numeroCIN FROM etudiant WHERE numeroCIN=%s UNION SELECT numeroCIN FROM personnel WHERE numeroCIN=%s',(numCIN,numCIN))

    # Renseignement des autres champs
    nom = input('Nom : ')
    prenom = input('Prénom : ')

    # Ajout de l'étudiant
    idPersonne = run('INSERT INTO personne (nom, prenom) VALUES (%s,%s) RETURNING idPersonne', (nom, prenom))[0][0]
    run('INSERT INTO etudiant VALUES (%s,%s)',(idPersonne, numCIN))
    print(f'L\'étudiant suivant a bien été ajouté :\nID : {idPersonne}\n{prenom} {nom}\nCIN : {numCIN}')
    input('\nAppuyez sur Entrée pour continuer...')

    return


def addPersonnel():

    # Renseignement du numéro CIN
    numCIN = input('Numéro CIN : ')

    # Vérification du numero CIN
    foundCIN = run('SELECT numeroCIN FROM etudiant WHERE numeroCIN=%s UNION SELECT numeroCIN FROM personnel WHERE numeroCIN=%s',(numCIN,numCIN))

    while foundCIN:
        print(f'Le numéro CIN \'{numCIN}\' est déjà pris...\n')
        numCIN = input('Numéro CIN : ')
        foundCIN = run('SELECT numeroCIN FROM etudiant WHERE numeroCIN=%s UNION SELECT numeroCIN FROM personnel WHERE numeroCIN=%s',(numCIN,numCIN))

    # Renseignement des autres champs
    nom = input('Nom : ')
    prenom = input('Prénom : ')

    print('Statut : ')
    statut_dic = {'1' : 'Enseignant', '2' : 'Personnel Administratif', '3' : 'Personnel Technique'}
    statut = inputFromDict(statut_dic)

    # Ajout du personnel
    idPersonne = run('INSERT INTO personne (nom, prenom) VALUES (%s,%s) RETURNING idPersonne', (nom, prenom))[0][0]
    run('INSERT INTO personnel VALUES (%s,%s,%s)',(idPersonne, numCIN,statut))
    print(f'Le personnel suivant a bien été ajouté :\nID : {idPersonne}\n{prenom} {nom}\nCIN : {numCIN}\nStatut : {statut}')
    input('\nAppuyez sur Entrée pour continuer...')
    return


def addExterieur():

    # Renseignement du contact
    contact = inputTel('Numéro de téléphone : ')

    # Vérification du contact
    foundExt = run('SELECT * FROM exterieur WHERE contact=%s',(contact,))

    while foundExt:
        print(f'Le numéro \'{contact}\' existe déjà...\n')
        contact = input('Numéro de téléphone : ')
        foundExt = run('SELECT * FROM exterieur WHERE contact=%s',(contact,))

    # Renseignement des autres champs
    nom = input('Nom : ')
    prenom = input('Prénom : ')
    organisme = input('Organisme de la personne exterieure : ')

    # Ajout de la personne extérieure
    idPersonne = run('INSERT INTO personne (nom, prenom) VALUES (%s,%s) RETURNING idPersonne', (nom, prenom))[0][0]
    run('INSERT INTO exterieur VALUES (%s,%s,%s)',(idPersonne, organisme, contact))
    print(f'La personne suivante a bien été ajoutée :\nID : {idPersonne}\n{prenom} {nom}\n{organisme}\n{contact}')
    input('\nAppuyez sur Entrée pour continuer...')
    return


# ### 3. Ajout d'un spectacle


def addSpectacle():
    association = chooseAssociation()

    while True:

        # choix concert, théâtre, stand-up
        print('\nChoisissez le type de spectacle à créer :\n  1: Concert\n  2: Théâtre\n  3: Stand-Up\n  4: Retour au menu\n')

        choix = input('Votre choix : ')

        if choix == '1': # Concert
            print('\nAjout d\'un concert :')
            addConcert(association)
            return
        elif choix == '2': # Théâtre
            print('\nAjout d\'une pièce de théâtre :')
            addTheatre(association)
            return
        elif choix == '3': # Stand-Up
            print('\nAjout d\'un Stand-Up :')
            addStandUp(association)
            return
        elif choix == '4': # Retour
            return
        else:
            print('Veuillez saisir un nombre entre 1 et 4.')


def addConcert(association):

    # Renseignement des champs
    compositeur = input('Compositeur : ')
    genre = chooseGenreConcert()
    duree = inputTime('Durée (ex 1:30) : ')
    anneeParution = inputYear('Année de parution : ')

    # Ajout du concert
    idSpectacle = run('INSERT INTO spectacle (duree, nomAsso) VALUES (TO_TIMESTAMP(%s, \'HH24:MI\'),%s) RETURNING idSpectacle', (duree, association))[0][0]
    run('INSERT INTO concert VALUES (%s,%s,%s,TO_TIMESTAMP(%s, \'YYYY\'))',(idSpectacle, compositeur, genre, anneeParution))
    print(f'Le concert suivant a bien été ajouté :\nID : {idSpectacle}\nCompositeur : {compositeur}\nGenre : {genre}\nDurée : {duree}\nAnnée de parution : {anneeParution}')
    input('\nAppuyez sur Entrée pour continuer...')
    return


def addTheatre(association):

    # Renseignement des champs
    auteur = input('Auteur : ')
    genre = chooseGenreTheatre()
    duree = inputTime('Durée (ex 1:30) : ')
    anneeParution = inputYear('Année de parution : ')

    # Ajout de la pièce
    idSpectacle = run('INSERT INTO spectacle (duree, nomAsso) VALUES (TO_TIMESTAMP(%s, \'HH24:MI\'),%s) RETURNING idSpectacle', (duree, association))[0][0]
    run('INSERT INTO theatre VALUES (%s,%s,TO_TIMESTAMP(%s, \'YYYY\'),%s)',(idSpectacle, auteur, anneeParution, genre))
    print(f'La pièce de théâtre suivante a bien été ajoutée :\nID : {idSpectacle}\nAuteur : {auteur}\nGenre : {genre}\nDurée : {duree}\nAnnée de parution : {anneeParution}')
    input('\nAppuyez sur Entrée pour continuer...')
    return


def addStandUp(association):

    # Renseignement des champs
    genre = chooseGenreStandUp()
    duree = inputTime('Durée (ex 1:30) : ')

    # Ajout du stand-up
    idSpectacle = run('INSERT INTO spectacle (duree, nomAsso) VALUES (TO_TIMESTAMP(%s, \'HH24:MI\'),%s) RETURNING idSpectacle', (duree, association))[0][0]
    run('INSERT INTO standup VALUES (%s,%s)',(idSpectacle, genre))
    print(f'Le stand-up suivant a bien été ajouté :\nID : {idSpectacle}\nGenre : {genre}\nDurée : {duree}')
    input('\nAppuyez sur Entrée pour continuer...')
    return


# ### 4. Ajout d'une salle

def addSalle():

    # Renseignement des champs
    numSalle = inputNumber('\nNumero de la Salle : ')
    capacite = inputNumber('Capacité : ')
    numBat = inputNumber('Numéro du batiment : ')

    # Vérification de la salle
    foundSalle = run('SELECT * FROM typesalle where numBat=%s AND numSalle=%s',(numBat, numSalle))

    if foundSalle:
        print(f'La salle \'{numSalle}\' existe déjà dans le bâtiment {numBat}')
        input('\nAppuyez sur Entrée pour continuer...')
        return

    # Renseignement du type
    print('Type de la salle : ')
    types_dic = {'1' : 'Cours', '2' : 'Amphitéâtre', '3' : 'Bureau'}
    libelleType = inputFromDict(types_dic)

    # Création de la salle
    foundSalle = run('SELECT * FROM salle where numsalle=%s', (numSalle,))
    foundBat = run('SELECT * FROM batiment where numbat=%s', (numBat,))

    if not foundSalle:
        run('insert into salle values (%s,%s)', (numSalle,capacite))
    if not foundBat:
        run('insert into batiment values (%s)', (numBat, ))
    run('insert into typeSalle values (%s,%s,%s)', (numBat, numSalle, libelleType))

    print(f'La salle suivante a bien été ajoutée :\nNuméro : {numSalle}\nBâtiment : {numBat}\nCapacité : {capacite}\nType : {libelleType}')
    input('\nAppuyez sur Entrée pour continuer...')
    return


# ### 5. Ajout d'une séance

def addSeance():

    idSpectacle = chooseSpectacle()
    print('\nChoisissez la salle dans laquelle le spectacle sera joué :')
    numBat, numSalle = chooseSalle()
    date = inputDate("Date de la séance (ex 30/06/2021) : ")
    horaireDebut = inputTime('Horaire de début (ex 20:45) : ')
    idSeance = run('insert into seance(date, horairedebut, idspectacle, numbat, numsalle) values (TO_DATE(%s,\'DD/MM/YYYY\'), TO_TIMESTAMP(%s, \'HH24:MI\'), %s,%s,%s) returning idSeance', (date, horaireDebut, idSpectacle, numBat, numSalle))[0][0]

    print(f'La séance suivante a bien été ajoutée :\nID : {idSeance}\nDate : {date}\nHoraire : {horaireDebut}\nSpectacle : {idSpectacle}\nSalle {numSalle}, bâtiment {numBat}')
    input('\nAppuyez sur Entrée pour continuer...')
    return


# ### 6. Ajout d'un billet

def addBillet():

    # Choix de la personne
    idPersonne = choosePersonne()

    # Choix de la séance
    idSeance = chooseSeance()

    # Choix de la catégorie
    categorie = chooseCategorie()

    # Choix du tarif
    tarif = inputPrice('\nTarif (ex 25.3 pour 25€30, 22 pour 22€00) : ' )
    dateCreation = date.today().strftime("%d/%m/%Y")

    # Ajout du billet
    idBillet = run('insert into billet(categorie, dateCreation, tarif, idSeance, idAcheteur) values (%s, TO_DATE(%s,\'DD/MM/YYYY\'), %s,%s,%s) returning idBillet', (categorie, dateCreation, tarif, idSeance, idPersonne))[0][0]

    print(f'Le billet suivant a bien été créé :\nID : {idBillet}\nDate de Création : {dateCreation}\nTarif : {tarif}€\nSéance : {idSeance}\nAcheteur {idPersonne}')
    input('\nAppuyez sur Entrée pour continuer...')
    return

def addReservation():

    # Renseignement des différents champs
    association = chooseAssociation()
    numBat, numSalle = chooseSalle()
    date = inputDate("Date de la réservation (ex 30/06/2021) : ")

    foundReservation = run('SELECT * FROM reservation WHERE numBat=%s AND numSalle=%s AND date=TO_DATE(%s,\'DD/MM/YYYY\') ',(numBat, numSalle, date))

    if foundReservation:
        print(f'Désolé, cette salle est déjà le soir du {date}')
        return

    # Ajout de la réservation
    run('insert into reservation values (%s, %s, %s, TO_DATE(%s,\'DD/MM/YYYY\'))', (association, numSalle, numBat, date))

    print(f'La salle {numSalle}, Bâtiment {numBat} a bien été réservée')
    input('\nAppuyez sur Entrée pour continuer...')
    return

def addCompose():

    # Renseignement des différents champs
    association = chooseAssociation()
    idEtudiant = chooseEtudiant()

    foundEtu = run('SELECT * FROM compose WHERE idEtudiant=%s AND nomAsso=%s',(idEtudiant, association))

    if foundEtu:
        print(f'Cet étudiant est déjà inscrit à {association}')
        input('Appuyez sur Entrée pour continuer...')

        return

    # Ajout de l'étudiant
    run('insert into compose values (%s, %s, %s)', (idEtudiant, association, 'Membre'))

    print(f'L\'étudiant {idEtudiant} a bien été inscrit à {association}')
    input('\nAppuyez sur Entrée pour continuer...')
    return

def addParticipeEtudiant():

    # Renseignement des différents champs
    idEtudiant = chooseEtudiant()
    idSpectacle = chooseSpectacle()

    role = input('Rôle de l\'étudiant dans le spectacle : ')

    foundEtu = run('SELECT * FROM participeetudiant WHERE idEtudiant=%s AND idSpectacle=%s',(idEtudiant, idSpectacle))

    if foundEtu:
        print(f'Cet étudiant participe déjà au spectacle n°{idSpectacle}')
        return

    # Ajout de l'étudiant
    run('insert into participeetudiant values (%s, %s, %s)', (idEtudiant, idSpectacle, role))

    print(f'L\'étudiant {idEtudiant} a bien été inscrit au spectacle n°{idSpectacle}')
    input('\nAppuyez sur Entrée pour continuer...')
    return

def addParticipePersonnel():

    # Renseignement des différents champs
    idPersonnel = choosePersonnel()
    idSpectacle = chooseSpectacle()

    role = input('Rôle du personnel dans le spectacle : ')

    foundPers = run('SELECT * FROM participepersonnel WHERE idPersonnel=%s AND idSpectacle=%s',(idPersonnel, idSpectacle))

    if foundPers:
        print(f'Ce membre du personnel participe déjà au spectacle n°{idSpectacle}')
        return

    # Ajout du personnel
    run('insert into participepersonnel values (%s, %s, %s)', (idPersonnel, idSpectacle, role))

    print(f'Le personnel n°{idPersonnel} a bien été inscrit au spectacle n°{idSpectacle}')
    input('\nAppuyez sur Entrée pour continuer...')
    return

# Ensemble des fonctions relatives à la suppression de personne
def deletePersonne():

    # choix personnel, etu, autre
    print('\nChoisissez le type de personne à supprimer :\n  1: Étudiant\n  2: Personnel\n  3: Extérieur\n  4: Retour au menu\n')

    choix = input('Votre choix : ')

    if choix == '1': # Etudiant
        print('\nSuppression d\'un etudiant :')
        deleteEtudiant()
    elif choix == '2': # Personnel
        print('\nSuppression d\'un membre du personnel :')
        deletePersonnel()
    elif choix == '3': # Exterieur
        print('\nSuppression d\'un membre extérieur :')
        deleteExterieur()
    elif choix != '4': # Retour
        print('Veuillez saisir un nombre entre 1 et 4.')
        deletePersonne()

    return

def deleteEtudiant():

    idEtudiant = chooseEtudiant()
    if deleteEtudiantCompose(idEtudiant):
        deleteBilletEtudiant(idEtudiant)
        deleteParticipationEtudiant(idEtudiant)
    
        run('delete from etudiant where idPersonne = %s', (idEtudiant,))
        run('delete from personne where idPersonne = %s', (idEtudiant,))
        print(f'L\'étudiant {idEtudiant} a bien été supprimé')
    input('\nAppuyez sur Entrée pour continuer...')
    return

def deleteBilletEtudiant(idEtudiant):

    # Suppression des billets d'un étudiant
    run('delete from billet where idAcheteur = %s', (idEtudiant,))
    return

def deleteParticipationEtudiant(idEtudiant):

    # Suppression des participations à un spectacle d'un étudiant
    run('delete from participeetudiant where idEtudiant = %s', (idEtudiant,))
    return

def deleteEtudiantCompose(idEtudiant):

    # Suppression de l'étudiant d'une association
    R1 = run('SELECT * FROM compose WHERE idEtudiant = %s',(idEtudiant,))
    
    for participation in R1:
        nomAsso = participation[1]
        nbParticipants = run('select nomasso, count(nomasso) from compose where nomAsso=%s group by nomasso ORDER BY count;', (nomAsso,))[0][1]
        if nbParticipants <= 2:
            print('L\’étudiant n\'a pas pu être supprimé, son association a atteint l\'effectif minimum')
            return False

    for row in R1:

        nomAsso = row[1]
        statut = row[2]
        # si l'étudiant est président ou trésorier
        if(statut != 'Membre'):
            R2 = run('SELECT * FROM compose WHERE nomAsso = %s',(nomAsso,))
            # si l'asso ne comporte pas d'autre membre que le président et le trésorier

            R3 = run('SELECT * FROM compose WHERE nomAsso = %s and statut = \'Membre\'',(nomAsso,))[0]
            idNewEtu = R3[0]
            # On affecte le rôle supprimé à un autre membre de l'association (le premier de la liste)
            run('UPDATE compose SET statut = %s WHERE idEtudiant = %s',(statut,idNewEtu))
            run('DELETE from compose where idEtudiant = %s',(idEtudiant,))
        else:
            run('DELETE from compose where idEtudiant = %s',(idEtudiant,))

    return True

def deletePersonnel():

    idPersonnel = choosePersonnel()
    deleteBilletPersonnel(idPersonnel)
    deleteParticipationPersonnel(idPersonnel)
    run('delete from personnel where idPersonne = %s', (idPersonnel,))
    run('delete from personne where idPersonne = %s', (idPersonnel,))
    print(f'Le membre {idPersonnel} a bien été supprimé')
    input('\nAppuyez sur Entrée pour continuer...')
    return

def deleteBilletPersonnel(idPersonnel):

    # Suppression des billets d'un personnel
    run('delete from billet where idAcheteur = %s', (idPersonnel,))

    return

def deleteParticipationPersonnel(idPersonnel):

    # Suppression des participations à un spectacle d'un personnel
    run('delete from participepersonnel where idPersonnel = %s', (idPersonnel,))

    return

def deleteExterieur():

    idExterieur = chooseExterieur()
    deleteBilletExterieur(idExterieur)
    run('delete from exterieur where idPersonne = %s', (idExterieur,))
    run('delete from personne where idPersonne = %s', (idExterieur,))
    print(f'L\'utilisateur {idExterieur} a bien été supprimé')
    input('\nAppuyez sur Entrée pour continuer...')
    return

def deleteBilletExterieur(idExterieur):

    # Suppression des billets d'une personne extérieure
    run('delete from billet where idAcheteur = %s', (idExterieur,))

    return
# Fin des fonctions relatives à la suppression de personne

# Ensemble des fonctions relatives à la suppression de association
def deleteAssociation():

    nom = chooseAssociation()

    deleteComposeAssociation(nom)

    R1 = run('SELECT * FROM spectacle WHERE nomAsso = %s',(nom,))
    for row1 in R1:
        R2 = run('SELECT * FROM seance WHERE idSpectacle = %s',(row1[0],))
        idSeance = R2
        for row2 in R2:
            deleteBilletSeance(row2[0])
        deleteSeanceSpectacle(row1[0])
        deleteParticipationSpectacle(row1[0])

    deleteSpectacleAssociation(nom)
    deleteReservationAssociation(nom)

    run('delete from association where nom = %s', (nom,))
    print(f'L\'association {nom} a bien été supprimée')
    input('\nAppuyez sur Entrée pour continuer...')

    return

def deleteComposeAssociation(nom):

    # Suppression des membres d'association à supprimer
    run('delete from compose where nomAsso = %s', (nom,))

    return

def deleteBilletSeance(idSeance):

    # Suppression des billets associés à une séance
    run('delete from billet where idSeance = %s', (idSeance,))

    return

def deleteSeanceSpectacle(idSpectacle):

    # Suppression des séances associées à un spectacle
    run('delete from seance where idSpectacle = %s', (idSpectacle,))

    return

def deleteParticipationSpectacle(idSpectacle):

    # Suppression des participations associées à un spectacle
    run('delete from participeetudiant where idSpectacle = %s', (idSpectacle,))
    run('delete from participepersonnel where idSpectacle = %s', (idSpectacle,))

    return

def deleteSpectacleAssociation(nom):

    # Suppression des spectacles associéss à une association
    run('delete from spectacle where nomAsso = %s', (nom,))

    return

def deleteReservationAssociation(nom):

    # Suppression des réservations de salle associéss à une association
    run('delete from reservation where nom = %s', (nom,))

    return
# Fin des fonctions relatives à la suppression de association

# Ensemble des fonctions relatives à la suppression de spectacle
def deleteSpectacle():

    idSpectacle = chooseSpectacle()

    R1 = run('SELECT * FROM seance WHERE idSpectacle = %s',(idSpectacle,))
    for row in R1:
        deleteBilletSeance(row[0])

    deleteSeanceSpectacle(idSpectacle)
    deleteParticipationSpectacle(idSpectacle)

    run('delete from spectacle where idSpectacle = %s', (idSpectacle,))
    print(f'Le spectacle {idSpectacle} a bien été supprimé')
    input('\nAppuyez sur Entrée pour continuer...')

    return
# Fin des fonctions relatives à la suppression de spectacle

# Ensemble des fonctions relatives à la suppression de séance
def deleteSeance():

    idSeance = chooseSeance()

    deleteBilletSeance(idSeance)

    run('delete from seance where idSeance = %s', (idSeance,))
    print(f'La séance {idSeance} a bien été supprimée')
    input('\nAppuyez sur Entrée pour continuer...')

    return
# Fin des fonctions relatives à la suppression de séance

# Fonction pour supprimer un étudiant d'une association
def deleteCompose():

    idPersonne = choosePersonne()
    nomAsso = chooseAssociation()

    R1 = run('SELECT * FROM compose where idEtudiant = %s and nomAsso = %s',(idPersonne,nomAsso))
    if not R1:
        print('Cet étudiant n\'est pas cette association')
        input('\nAppuyez sur Entrée pour continuer...')

    else:
        statut = R1[0][2]
        R2 = run('SELECT * FROM compose WHERE nomAsso = %s',(nomAsso,))
        if(len(R2) <= 2):
            print('Suppression d\'association impossible, effectif minimum atteint.')

        else:
            R3 = run('SELECT * FROM compose WHERE nomAsso = %s and statut = \'Membre\'',(nomAsso,))[0]
            idNewEtu = R3[0]
            # On affecte le rôle supprimé à un autre membre de l'association (le premier de la liste)
            run('UPDATE compose SET statut = %s WHERE idEtudiant = %s',(statut,idNewEtu))
            run('DELETE from compose where idEtudiant = %s and nomAsso = %s',(idPersonne,nomAsso))
            print('Etudiant bien supprimé de l\'association.')
        input('\nAppuyez sur Entrée pour continuer...')

    return

# Fonction pour supprimer une réservation de salle
def deleteReservation():

    reservation =  chooseReservation()
    if not reservation:
        return
    print('La réserv', reservation)
    numBat, numSalle, choosenDate = reservation
    run('delete from reservation where numSalle = %s and numBat = %s and date = TO_DATE(%s,\'YYYY-MM-DD\') ', (numSalle,numBat, choosenDate))
    print('Réservation bien supprimée.')
    input('\nAppuyez sur Entrée pour continuer...')
    return

# Fonction pour supprimer un billet d'une personne
def deleteBillet():

    idBillet = chooseBillet()
    if idBillet:
        run('delete from billet where idBillet = %s', (idBillet,))
        print('Billet bien supprimé.')
    input('\nAppuyez sur Entrée pour continuer...')
    return

# Fonction pour supprimer la participation à un spectacle d'une personne
def deleteParticipation():

    # choix personnel, etu, autre
    print('\nChoisissez le type de personne à supprimer d\'un spectacle :\n  1: Étudiant\n  2: Personnel\n  3: Retour au menu\n')

    choix = input('Votre choix : ')

    if choix == '1': # Etudiant
        print('\nSuppression de la participation d\'un étudiant à un spectacle :')
        idEtudiant = chooseEtudiant()
        idSpectacle = chooseSpectacle()
        R1 = run('SELECT * FROM participeetudiant where idEtudiant = %s and idSpectacle = %s',(idEtudiant,idSpectacle))
        if not R1:
            print('Cet étudiant ne participe pas à ce spectacle')
        else:
            run('delete from participeetudiant where idEtudiant = %s and idSpectacle = %s', (idEtudiant,idSpectacle))
            print('Participation de cet étudiant à ce spectacle a été bien effectué.')
    elif choix == '2': # Personnel
        print('\nSuppression de la participation d\'un membre du personne à un spectacle:')
        idPersonnel = choosePersonnel()
        idSpectacle = chooseSpectacle()
        R1 = run('SELECT * FROM participepersonnel where idPersonnel = %s and idSpectacle = %s',(idPersonnel,idSpectacle))
        if not R1:
            print('Ce membre du personnel ne participe pas à ce spectacle')
        else:
            run('delete from participepersonnel where idPersonnel = %s and idSpectacle = %s', (idPersonnel,idSpectacle))
            print('Participation de ce membre du personnel à ce spectacle a été bien effectué.')
    elif choix != '3': # Retour
        print('Veuillez saisir un nombre entre 1 et 3.')
        deleteParticipation()
    input('\nAppuyez sur Entrée pour continuer...')
    return


def updateAssociation():
    nom = chooseAssociation()
    sql1='SELECT  description, categorie, email, dateCreation, siteWeb FROM association WHERE nom=%s'
    description, categorie, email, dateCreation, siteWeb = run(sql1,(nom,))[0]
    modif=True
    while True:
        print('Choisissez le champ à modifier :\n  1: Description\n  2: Catégorie\n  3: Email\n  4: Date de Création\n  5: Site Web\n  6: Retour au menu\n\n')

        choix = input('Votre choix : ')

        if choix == '1': # Description
            description = input('Nouvelle description : ')
            break

        elif choix == '2': # Catégorie
            categorie = input('Nouvelle catégorie : ')
            break

        elif choix == '3': # Email
            email = input('Nouvel email : ')
            break

        elif choix == '4': # Date de création
            dateCreation = inputDate('Nouvelle date de création (ex: DD/MM/YYYY) : ')
            break

        elif choix == '5': # Site
            siteWeb = input('Nouveau site : ')
            break
        elif choix == '6':
            modif=False
            break
    if modif:
        dateCreation = str(dateCreation)
        if dateCreation[4] == '-':
            y,m,d = dateCreation.split('-')
            dateCreation = d + '/' + m + '/' + y
        run('UPDATE association SET nom=%s, description=%s, dateCreation=TO_DATE(%s, \'DD/MM/YYYY\'), categorie=%s, email=%s, siteWeb=%s WHERE nom=%s',(nom, description, str(dateCreation), categorie, email, siteWeb, nom))
        print(f'L\'association {nom} a bien été modifiée')
        input('\nAppuyez sur Entrée pour continuer...')
    return


def updatePersonne():
    idPersonne = choosePersonne()
    nom, prenom, categorie = run('SELECT nom, prenom, categorie FROM personne_medium WHERE id=%s', (idPersonne,))[0]
    modif=True
    # print(f"HEY HEY {nom}, {prenom}, {categorie}")
    # print("Wesh euhh la catégorie : ", categorie)
    if categorie == 'Étudiant':

        sql2 = 'SELECT numeroCIN FROM etudiant WHERE idPersonne=%s'
        numeroCIN = run(sql2, (idPersonne,))[0][0]

        while True:

            print('Choisissez le champ à modifier :\n  1: Nom\n  2: Prenom\n  3: Numéro CIN\n  4: Retour au menu\n\n')

            choix = input('Votre choix : ')

            if choix == '1': # Nom
                nom = input('Nouveau nom : ')
                break

            elif choix == '2': # Prenom
                prenom = input('Nouveau prenom : ')
                break

            elif choix == '3': # Numéro CIN
                numeroCIN = input('Nouveau numCIN : ')
                break

            elif choix == '4':
                modif = False
                break
            else:
                print('Saisie non reconnue...')

        run('UPDATE etudiant SET numeroCIN=%s WHERE idPersonne=%s',(numeroCIN, idPersonne))

    elif categorie == 'Personnel':

        sql2= 'SELECT numeroCIN, statut FROM personnel WHERE idPersonne=%s'
        numeroCIN, statut = run(sql2, (idPersonne,))[0]


        while True:

            print('Choisissez le champ à modifier :\n  1: Nom\n  2: Prenom\n  3: Numéro CIN\n  4: Statut\n  5: Retour au menu\n\n')

            choix = input('Votre choix : ')

            if choix == '1': # Nom
                nom = input('Nouveau nom : ')
                break

            elif choix == '2': # Prenom
                prenom = input('Nouveau prenom : ')
                break

            elif choix == '3': # Numéro CIN
                numeroCIN = input('Nouveau numCIN : ')
                break

            elif statut == '4': #Statut
                print('Nouveau statut : ')
                statut_dic = {'1' : 'Enseignant', '2' : 'Personnel Administratif', '3' : 'Personnel Technique'}
                statut = inputFromDict(statut_dic)
                break

            elif choix == '5':
                modif = False
                break
            else:
                print('Saisie non reconnue...')

        run('UPDATE personnel SET numeroCIN=%s, statut=%s WHERE idPersonne=%s',(numeroCIN, statut, idPersonne))

    elif categorie == 'Extérieur':
        sql2= 'SELECT organisme, contact FROM exterieur WHERE idPersonne=%s'
        organisme, contact = run(sql2, (idPersonne,))[0]

        while True:
            print('Choisissez le champ à modifier :\n  1: Nom\n  2: Prenom\n  3: Organisme\n  4: Contact\n  5: Retour au menu\n\n')

            choix = input('Votre choix : ')

            if choix == '1': # Nom
                nom = input('Nouveau nom : ')
                break

            elif choix == '2': # Prenom
                prenom = input('Nouveau prenom : ')
                break

            elif choix == '3':
                organisme = input('Nouvel organisme : ')
                break

            elif choix == '4':
                contact = inputTel('Nouveau contact : ')
                break

            elif choix == '5':
                modif = False
                break
            else:
                print('Saisie non reconnue...')

        run('UPDATE exterieur SET organisme=%s, contact=%s WHERE idPersonne=%s', (organisme,contact, idPersonne))

    run('UPDATE personne SET nom=%s, prenom=%s WHERE idPersonne=%s',(nom, prenom, idPersonne))
    if modif:
        print(f'L\'utilisateur n°{idPersonne} a bien été modifié\n')
        input('Appuyez sur Entrée pour continuer...')

    return


def updateSpectacle(): 
    idSpectacle = chooseSpectacle()
    sql1 = 'SELECT organisateur, duree, genre,categorie FROM spectacle_medium WHERE id=%s'
    organisateur, duree, genre,categorie = run(sql1, (idSpectacle,))[0]

    if categorie == 'Concert':

        sql2 = 'SELECT compositeur, anneeParution FROM concert WHERE idConcert=%s'
        compositeur, anneeParution = run(sql2, (idSpectacle,))[0]

        while True:

            print('Choisissez le champ à modifier :\n  1: Durée\n  2: Genre\n  3: Compositeur\n  4: Année de Parution\n  5: Retour au menu\n\n')

            choix = input('Votre choix : ')

            if choix == '1':
                duree = inputTime('Nouvelle durée (ex 1:30) : ')
                break

            elif choix == '2':
                genre = chooseGenreConcert()
                break

            elif choix == '3':
                compositeur = input('Nouveau compositeur : ')
                break

            elif choix == '4':
                anneeParution= inputYear('Nouvelle année de parution : ')
                break

            elif choix == '5':
                break

        run('UPDATE Concert SET genre=%s, compositeur=%s, anneeParution=TO_DATE(%s,\'YYYY\') WHERE idConcert=%s',(genre, compositeur, str(anneeParution), idSpectacle))


    if categorie == 'Théâtre':

        sql2 = 'SELECT auteur, anneeParution FROM theatre WHERE idTheatre=%s'
        auteur, anneeParution = run(sql2, (idSpectacle,))[0]

        while True:

            print('Choisissez le champ à modifier :\n  1: Durée\n  2: Genre\n  3: Auteur\n  4: Année de Parution\n  5: Retour au menu\n\n')

            choix = input('Votre choix : ')

            if choix == '1':
                duree = inputTime('Nouvelle durée (ex 1:30) : ')
                break

            elif choix == '2':
                genre = chooseGenreTheatre()
                break

            elif choix == '3':
                auteur = input('Nouvel auteur : ')
                break

            elif choix == '4':
                anneeParution= inputYear('Nouvelle année de parution : ')
                break

            elif choix == '5':
                break

        run('UPDATE theatre SET genre=%s, auteur=%s, anneeParution=TO_DATE(%s,\'YYYY\') WHERE idTheatre=%s',(genre, auteur, str(anneeParution), idSpectacle))

    if categorie == 'Stand-Up':


        while True:

            print('Choisissez le champ à modifier :\n  1: Durée\n  2: Genre\n  3: Retour au menu\n\n')

            choix = input('Votre choix : ')

            if choix == '1':
                duree = inputTime('Nouvelle durée (ex 1:30) : ')
                break

            elif choix == '2':
                genre = chooseGenreStandUp('Nouveau genre : ')
                break

            elif choix == '3':
                break

        run('UPDATE standup SET genre=%s WHERE idStandUp=%s',(genre, idSpectacle))


    run('UPDATE spectacle SET nomAsso=%s, duree=TO_TIMESTAMP(%s, \'HH24:MI\') WHERE idSpectacle=%s',(organisateur, str(duree), idSpectacle))
    print(f'Le spectacle n°{idSpectacle} a bien été modifié')
    input('Appuyez sur Entrée pour continuer...')

    return


def updateSalle():
    salle = chooseSalle()
    sql1 = 'SELECT capacite FROM salle JOIN typeSalle ON salle.numSalle=typeSalle.numSalle WHERE (numBat,salle.numSalle)=%s'
    capacite = run(sql1,(salle,))[0][0]
    sql2 = 'SELECT libelleType FROM typeSalle WHERE (numBat,numSalle)=%s'
    libelleType = run(sql2,(salle,))[0][0]
    modif = True
    while True:
        print('Choisissez le champ à modifier :\n  1: Capacité\n  2: Libellé du type de salle\n  3: Retour au menu\n\n')

        choix = input('Votre choix : ')

        if choix == '1':
            capacite = inputNumber('Nouvelle capacité : ')
            break

        elif choix == '2':
            print('Nouveau libellé du type de la salle : ')
            types_dic = {'1' : 'Cours', '2' : 'Amphitéâtre', '3' : 'Bureau'}
            libelleType = inputFromDict(types_dic)
            break

        elif choix == '3':
            modif = False
            break

    if modif:
        run('UPDATE salle SET capacite=%s WHERE numsalle=%s',(capacite,salle[1]))
        run('UPDATE typeSalle SET libelleType=%s where numBat=%s and numSalle=%s',(libelleType,salle[0], salle[1]))
        print(f'La salle {salle} a bien été modifiée')
        input('Appuyez sur Entrée pour continuer...')
    return


def menuPrincipal():

    os.system('cls' if os.name == 'nt' else 'clear')

    while True :
        printTitle('Menu Principal')
        print('\nQue souhaitez vous faire ?')

        choix = input('  1: Gérer les utilisateurs\n  2: Gérer les spectacles\n  3: Gérer les salles\n  4: Gérer les associations\n  5: Quitter\n\nVotre choix : ')

        if choix == '1': # utilisateur
            os.system('cls' if os.name == 'nt' else 'clear')

            printTitle('Gestion des utilisateurs')
            while True:
                print('\nQue souhaitez vous faire ?')
                choixUser = input('  1: Ajouter un utilisateur\n  2: Afficher les utilisateurs\n  3: Modifier un utilisateur\n  4: Supprimer un utilisateur\n  5: Annuler une réservation à un spectacle\n  6: Retour\n\nVotre choix : ')

                if choixUser == '1':
                    os.system('cls' if os.name == 'nt' else 'clear')
                    printTitle('Ajout d\'un utilisateur')
                    addPersonne()
                    os.system('cls' if os.name == 'nt' else 'clear')
                    break
                elif choixUser == '2':
                    os.system('cls' if os.name == 'nt' else 'clear')
                    printTitle('Affichage d\'un utilisateur')
                    printPersonne()
                    input('\nAppuyez sur Entrée pour continuer...')
                    os.system('cls' if os.name == 'nt' else 'clear')
                    break
                elif choixUser == '3':
                    os.system('cls' if os.name == 'nt' else 'clear')
                    printTitle('Modification d\'un utilisateur')
                    updatePersonne()
                    os.system('cls' if os.name == 'nt' else 'clear')
                    break
                elif choixUser == '4':
                    os.system('cls' if os.name == 'nt' else 'clear')
                    printTitle('Suppression d\'un utilisateur')
                    deletePersonne()
                    os.system('cls' if os.name == 'nt' else 'clear')
                    break
                elif choixUser == '5':
                    os.system('cls' if os.name == 'nt' else 'clear')
                    printTitle('Suppression d\'un utilisateur')
                    deleteBillet()
                    os.system('cls' if os.name == 'nt' else 'clear')
                    break
                elif choixUser == '6':
                    os.system('cls' if os.name == 'nt' else 'clear')
                    break
                else:
                    print('Saisie non reconnue...')

        elif choix == '2': # spectacle
            os.system('cls' if os.name == 'nt' else 'clear')
            printTitle('Gestion des spectacles')

            while True:
                print('\nQue souhaitez-vous faire ?')
                choixSpec = input('   1: Ajouter un spectacle\n   2: Afficher les spectacles\n   3: Ajouter une séance à un spectacle\n   4: Faire participer un étudiant à un spectacle\n   5: Faire participer un membre du personnel à un spectacle\n   6: Supprimer la participation à un spectacle\n   7: Modifier un spectacle\n   8: Acheter un billet pour un spectacle\n   9: Supprimer un spectacle\n  10: Supprimer une séance\n  11: Retour\n\nVotre choix : ')

                if choixSpec == '1':
                    os.system('cls' if os.name == 'nt' else 'clear')
                    printTitle('Ajout d\'un spectacle')
                    addSpectacle()
                    os.system('cls' if os.name == 'nt' else 'clear')
                    break
                elif choixSpec == '2':
                    os.system('cls' if os.name == 'nt' else 'clear')
                    printTitle('Affichage des spectacles')
                    printSpectacle()
                    input('\nAppuyez sur Entrée pour continuer...')
                    os.system('cls' if os.name == 'nt' else 'clear')
                    break
                elif choixSpec == '3':
                    os.system('cls' if os.name == 'nt' else 'clear')
                    printTitle('Ajout d\'une séance')
                    addSeance()
                    os.system('cls' if os.name == 'nt' else 'clear')
                    break
                elif choixSpec == '4':
                    os.system('cls' if os.name == 'nt' else 'clear')
                    printTitle('Ajout d\'un participant étudiant')
                    addParticipeEtudiant()
                    os.system('cls' if os.name == 'nt' else 'clear')
                    break
                elif choixSpec == '5':
                    os.system('cls' if os.name == 'nt' else 'clear')
                    printTitle('Ajout d\'un participant du personnel')
                    addParticipePersonnel()
                    os.system('cls' if os.name == 'nt' else 'clear')
                    break
                elif choixSpec == '6':
                    os.system('cls' if os.name == 'nt' else 'clear')
                    printTitle('Annulation d\'une participation')
                    deleteParticipation()
                    os.system('cls' if os.name == 'nt' else 'clear')
                    break
                elif choixSpec == '7':
                    os.system('cls' if os.name == 'nt' else 'clear')
                    printTitle('Modification d\'un spectacle')
                    updateSpectacle()
                    os.system('cls' if os.name == 'nt' else 'clear')
                    break
                elif choixSpec == '8':
                    os.system('cls' if os.name == 'nt' else 'clear')
                    printTitle('Achat d\'un billet')
                    addBillet()
                    os.system('cls' if os.name == 'nt' else 'clear')
                    break
                elif choixSpec == '9':
                    os.system('cls' if os.name == 'nt' else 'clear')
                    printTitle('Suppression d\'un spectacle')
                    deleteSpectacle()
                    os.system('cls' if os.name == 'nt' else 'clear')
                    break
                elif choixSpec == '10':
                    os.system('cls' if os.name == 'nt' else 'clear')
                    printTitle('Suppression d\'une séance')
                    deleteSeance()
                    os.system('cls' if os.name == 'nt' else 'clear')
                    break
                elif choixSpec == '11':
                    os.system('cls' if os.name == 'nt' else 'clear')
                    break
                else:
                    print('Saisie non reconnue...')

        elif choix == '3': # salle
            os.system('cls' if os.name == 'nt' else 'clear')
            printTitle('Gestion des salles')

            while True:
                print('\nQue souhaitez-vous faire ?')
                choixSalle = input('  1: Ajouter une salle\n  2: Afficher la liste des salles\n  3: Réserver une salle\n  4: Modifier les informations d\'une salle\n  5: Supprimer une réservation de salle\n  6: Retour\n\nVotre choix : ')

                if choixSalle == '1':
                    os.system('cls' if os.name == 'nt' else 'clear')
                    printTitle('Ajout d\'une salle')
                    addSalle()
                    os.system('cls' if os.name == 'nt' else 'clear')
                    break
                elif choixSalle == '2':
                    os.system('cls' if os.name == 'nt' else 'clear')
                    printTitle('Affichage des salles')
                    printSalle()
                    input('\nAppuyez sur Entrée pour continuer...')
                    os.system('cls' if os.name == 'nt' else 'clear')
                    break
                elif choixSalle == '3':
                    os.system('cls' if os.name == 'nt' else 'clear')
                    printTitle('Réservation d\'une salle')
                    addReservation()
                    os.system('cls' if os.name == 'nt' else 'clear')
                    break
                elif choixSalle == '4':
                    os.system('cls' if os.name == 'nt' else 'clear')
                    printTitle('Modification des informations d\'une salle')
                    updateSalle()
                    os.system('cls' if os.name == 'nt' else 'clear')
                    break
                elif choixSalle == '5':
                    os.system('cls' if os.name == 'nt' else 'clear')
                    printTitle('Suppression d\'une réservation de salle')
                    deleteReservation()
                    os.system('cls' if os.name == 'nt' else 'clear')
                    break
                elif choixSalle == '6':
                    os.system('cls' if os.name == 'nt' else 'clear')
                    break
                else:
                    print('Saisie non reconnue...')

        elif choix == '4': # association
            os.system('cls' if os.name == 'nt' else 'clear')
            printTitle('Gestion des associations')

            while True:
                print('\nQue souhaitez-vous faire ?')
                choixAsso = input('  1: Ajouter une association\n  2: Afficher les associations\n  3: Inscrire un étudiant à une association\n  4: Désinscrire un étudiant d\'une association\n  5: Supprimer une association\n  6: Modifier une association\n  7: Retour\n\nVotre choix : ')
                

                if choixAsso == '1':
                    os.system('cls' if os.name == 'nt' else 'clear')
                    printTitle('Ajout d\'une association')    
                    addAssociation()
                    os.system('cls' if os.name == 'nt' else 'clear')
                    break
                elif choixAsso == '2':
                    os.system('cls' if os.name == 'nt' else 'clear')
                    printTitle('Affichage des associations')
                    printAssociation()
                    input('\nAppuyez sur Entrée pour continuer...')
                    os.system('cls' if os.name == 'nt' else 'clear')
                    break
                elif choixAsso == '3':
                    os.system('cls' if os.name == 'nt' else 'clear')
                    printTitle('Inscription d\'un étudiant')
                    addCompose()
                    os.system('cls' if os.name == 'nt' else 'clear')
                    break
                elif choixAsso == '4':
                    os.system('cls' if os.name == 'nt' else 'clear')
                    printTitle('Désinscription d\'un étudiant')
                    deleteCompose()
                    os.system('cls' if os.name == 'nt' else 'clear')
                    break
                elif choixAsso == '5':
                    os.system('cls' if os.name == 'nt' else 'clear')
                    printTitle('Supprimer une association')
                    deleteAssociation()
                    os.system('cls' if os.name == 'nt' else 'clear')
                    break
                elif choixAsso == '6':
                    os.system('cls' if os.name == 'nt' else 'clear')
                    printTitle('Modification d\'une association')
                    updateAssociation()
                    os.system('cls' if os.name == 'nt' else 'clear')
                    break
                elif choixAsso == '7':
                    os.system('cls' if os.name == 'nt' else 'clear')
                    break
                else:
                    print('Saisie non reconnue...')

        elif choix == '5': # Retour
            print('A bientôt :)')
            break
        else:
            # input('Saisie non reconnue... Appuyez sur Entrée pour continuer...')
            print('Saisie non reconnue...\n')

menuPrincipal()
