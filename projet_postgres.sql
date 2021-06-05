DROP TABLE IF EXISTS association CASCADE;
CREATE TABLE IF NOT EXISTS association (
  nom varchar(50) NOT NULL,
  description text NOT NULL,
  categorie varchar(50) NOT NULL,
  email varchar(100) NOT NULL,
  dateCreation date NOT NULL,
  siteWeb text,
  PRIMARY KEY (nom),
  UNIQUE(email)
) ;

--
-- Déchargement des données de la table association
--

-- --------------------------------------------------------

--
-- Structure de la table batiment
--

DROP TABLE IF EXISTS batiment CASCADE;
CREATE TABLE IF NOT EXISTS batiment (
  numBat int NOT NULL,
  PRIMARY KEY (numBat)
) ;

-- --------------------------------------------------------

--
-- Structure de la table billet
--

DROP TABLE IF EXISTS billet CASCADE;
CREATE TABLE IF NOT EXISTS billet (
  idBillet SERIAL,
  categorie varchar(50) DEFAULT NULL references categorie(nom),
  dateCreation date NOT NULL,
  tarif decimal(10,0) DEFAULT NULL,
  idSeance int DEFAULT NULL,
  idAcheteur int DEFAULT NULL,
  PRIMARY KEY (idBillet)
) ;

-- --------------------------------------------------------

--
-- Structure de la table categorie
--

DROP TABLE IF EXISTS categorie CASCADE;
CREATE TABLE IF NOT EXISTS categorie (
  nom varchar(50) primary key
) ;

-- --------------------------------------------------------

--
-- Structure de la table compose
--

DROP TABLE IF EXISTS compose CASCADE;
CREATE TABLE IF NOT EXISTS compose (
  idEtudiant int NOT NULL references etudiant(idPersonne),
  nomAsso varchar(100) NOT NULL references association(nom),
  statut varchar(50) NOT NULL,
  PRIMARY KEY (idEtudiant,nomAsso, statut),
  CHECK (statut='Président' or statut='Trésorier' or statut='Membre')
) ;

-- --------------------------------------------------------

--
-- Structure de la table concert
--

DROP TABLE IF EXISTS concert CASCADE;
CREATE TABLE IF NOT EXISTS concert (
  idConcert int NOT NULL references spectacle(idSpectacle),
  compositeur varchar(100) NOT NULL,
  genre varchar(50) DEFAULT NULL references genreconcert(genreConcert),
  anneeParution date DEFAULT NULL,
  PRIMARY KEY (idConcert)
) ;

-- --------------------------------------------------------

--
-- Structure de la table etudiant
--

DROP TABLE IF EXISTS etudiant CASCADE;
CREATE TABLE IF NOT EXISTS etudiant (
  idPersonne int NOT NULL references personne(idPersonne),
  numeroCIN int NOT NULL,
  PRIMARY KEY (idPersonne),
  UNIQUE(numeroCIN)
) ;

-- --------------------------------------------------------

--
-- Structure de la table exterieur
--

DROP TABLE IF EXISTS exterieur CASCADE;
CREATE TABLE IF NOT EXISTS exterieur (
  idPersonne int NOT NULL references personne(idPersonne),
  organisme varchar(50) NOT NULL,
  contact varchar(10) NOT NULL,
  PRIMARY KEY (idPersonne),
  UNIQUE (contact)
) ;

-- --------------------------------------------------------

--
-- Structure de la table genreconcert
--

DROP TABLE IF EXISTS genreconcert CASCADE;
CREATE TABLE IF NOT EXISTS genreconcert (
  genreConcert varchar(50) NOT NULL,
  PRIMARY KEY (genreConcert)
) ;

-- --------------------------------------------------------

--
-- Structure de la table genrestandup
--

DROP TABLE IF EXISTS genrestandup CASCADE;
CREATE TABLE IF NOT EXISTS genrestandup (
  genreStandUp varchar(50) NOT NULL,
  PRIMARY KEY (genreStandUp)
) ;

-- --------------------------------------------------------

--
-- Structure de la table genretheatre
--

DROP TABLE IF EXISTS genretheatre CASCADE;
CREATE TABLE IF NOT EXISTS genretheatre (
  genreTheatre varchar(50) NOT NULL,
  PRIMARY KEY (genreTheatre)
) ;

-- --------------------------------------------------------

--
-- Structure de la table participeetudiant
--

DROP TABLE IF EXISTS participeetudiant CASCADE;
CREATE TABLE IF NOT EXISTS participeetudiant (
  idEtudiant int NOT NULL references etudiant(idPersonne),
  idSpectacle int NOT NULL references spectacle(idSpectacle),
  role varchar(50) NOT NULL,
  PRIMARY KEY (idEtudiant,idSpectacle)
) ;

-- --------------------------------------------------------

--
-- Structure de la table participepersonnel
--

DROP TABLE IF EXISTS participepersonnel CASCADE;
CREATE TABLE IF NOT EXISTS participepersonnel (
  idPersonnel int NOT NULL references personnel(idPersonne),
  idSpectacle int NOT NULL references spectacle(idSpectacle),
  role varchar(50) NOT NULL,
  PRIMARY KEY (idPersonnel,idSpectacle)
) ;

-- --------------------------------------------------------

--
-- Structure de la table personne
--

DROP TABLE IF EXISTS personne CASCADE;
CREATE TABLE IF NOT EXISTS personne (
  idPersonne SERIAL,
  nom varchar(50) NOT NULL,
  prenom varchar(50) NOT NULL,
  PRIMARY KEY (idPersonne)
) ;

-- --------------------------------------------------------

--
-- Structure de la table personnel
--

DROP TABLE IF EXISTS personnel CASCADE;
CREATE TABLE IF NOT EXISTS personnel (
  idPersonne int NOT NULL references personne(idPersonne),
  numeroCIN int UNIQUE NOT NULL,
  statut varchar(150) NOT NULL,
  PRIMARY KEY (idPersonne),
  UNIQUE(numeroCIN)
) ;

-- --------------------------------------------------------

--
-- Structure de la table reservation
--

DROP TABLE IF EXISTS reservation CASCADE;
CREATE TABLE IF NOT EXISTS reservation (
  nom varchar(50) NOT NULL,
  numSalle int NOT NULL references salle(numsalle),
  numBat int NOT NULL references batiment(numBat),
  date date NOT NULL,
  PRIMARY KEY (numSalle,numBat, date)
) ;

-- --------------------------------------------------------

--
-- Structure de la table salle
--

DROP TABLE IF EXISTS salle CASCADE;
CREATE TABLE IF NOT EXISTS salle (
  numSalle int NOT NULL,
  capacite int NOT NULL,
  PRIMARY KEY (numSalle)
) ;

-- --------------------------------------------------------

--
-- Structure de la table seance
--

DROP TABLE IF EXISTS seance CASCADE;
CREATE TABLE IF NOT EXISTS seance (
  idSeance SERIAL,
  date date NOT NULL,
  horaireDebut time NOT NULL,
  idSpectacle int DEFAULT NULL,
  numBat int DEFAULT NULL,
  numSalle int DEFAULT NULL,
  PRIMARY KEY (idSeance)
) ;

-- --------------------------------------------------------

--
-- Structure de la table spectacle
--

DROP TABLE IF EXISTS spectacle CASCADE;
CREATE TABLE IF NOT EXISTS spectacle (
  idSpectacle SERIAL,
  duree time NOT NULL,
  nomAsso varchar(100) DEFAULT NULL,
  PRIMARY KEY (idSpectacle)
) ;

-- --------------------------------------------------------

--
-- Structure de la table standup
--

DROP TABLE IF EXISTS standup CASCADE;
CREATE TABLE IF NOT EXISTS standup (
  idStandUp int NOT NULL,
  genre varchar(50) DEFAULT NULL references genrestandup(genrestandup),
  PRIMARY KEY (idStandUp)
) ;

-- --------------------------------------------------------

--
-- Structure de la table theatre
--

DROP TABLE IF EXISTS theatre CASCADE;
CREATE TABLE IF NOT EXISTS theatre (
  idTheatre int NOT NULL,
  auteur varchar(100) NOT NULL,
  anneeParution date NOT NULL,
  genre varchar(50) DEFAULT NULL references genretheatre(genretheatre),
  PRIMARY KEY (idTheatre)
) ;

-- --------------------------------------------------------

--
-- Structure de la table typesalle
--

DROP TABLE IF EXISTS typesalle CASCADE;
CREATE TABLE IF NOT EXISTS typesalle (
  numBat int NOT NULL references batiment(numBat),
  numSalle int NOT NULL references salle(numSalle),
  libelleType varchar(50) NOT NULL,
  PRIMARY KEY (numBat,numSalle),
  CHECK (libelleType ='Cours' or libelleType ='Amphitéâtre' or libelleType ='Bureau')
);

-- Ajout de vues

create view spectacle_small as select idtheatre as ID, genre, 'Théâtre' as categorie from theatre                                                                                                                                  union select idconcert as ID, genre, 'Concert' as categorie from concert                                                                                                                                    union select idstandup as ID, genre, 'Stand-Up' as categorie from standup;

create view spectacle_medium as select id, nomAsso as organisateur, duree, genre, categorie from spectacle_small v, spectacle s where idspectacle=id;


create view personne_small as select idpersonne as ID, 'Étudiant' as categorie from etudiant                                                                                                                                  union select idPersonne as ID, 'Personnel' as categorie from personnel                                                                                                                                    union select idPersonne as ID, 'Extérieur' as categorie from exterieur;

create view personne_medium as select id, nom, prenom, categorie from personne_small ps, personne p where idpersonne=id;

-- Quelques exemples
 
insert into categorie values('Invitation');
insert into categorie values('Billet Étudiant');
insert into categorie values('Billet Personnel');
insert into categorie values('Billet Extérieur');


insert into genreconcert values('Pop');
insert into genreconcert values('Rock');
insert into genreconcert values('Rap');
insert into genreconcert values('Classique');


insert into genretheatre values('Comédie');
insert into genretheatre values('Tragédie');
insert into genretheatre values('Drame');
insert into genretheatre values('Mélodrame');


insert into genrestandup values('Comique');
insert into genrestandup values('Débat');
insert into genrestandup values('Table Ronde');

INSERT INTO association VALUES ('Piano UT', 'Le piano parce qu''on est trop beaux', 'Artistique', 'piano@ut.fr', TO_DATE('12/05/2018', 'DD/MM/YYYY'), 'piano.utx.fr');
INSERT INTO association VALUES ('Ski UT', 'Le ski, la vie', 'Évènementiel', 'ski@ut.fr', TO_DATE('24/12/2019', 'DD/MM/YYYY'), '');
INSERT INTO association VALUES ('Data Venture', 'La meilleure des assos', 'Technologie', 'dataventure@ut.fr', TO_DATE('03/01/2018', 'DD/MM/YYYY'), 'dataventure.github.io');

INSERT INTO personne VALUES (107, 'Missaoui', 'Benjamin');
INSERT INTO personne VALUES (108, 'Trump', 'Donald');
INSERT INTO personne VALUES (109, 'Cook', 'Tim');
INSERT INTO personne VALUES (110, 'Musk', 'Elon');
INSERT INTO personne VALUES (111, 'Merkel', 'Angela');
INSERT INTO personne VALUES (112, 'Spider', 'Man');

INSERT INTO etudiant VALUES (107, 2147);
INSERT INTO etudiant VALUES (108, 9870);
INSERT INTO etudiant VALUES (112, 3145);

INSERT INTO personnel VALUES (109, 1243, 'Enseignant');
INSERT INTO personnel VALUES (110, 7567, 'Personnel Technique');

INSERT INTO exterieur VALUES (111, 'Reichtag & co', '0613261876');

INSERT INTO spectacle VALUES (34, TO_TIMESTAMP('1:43', 'HH24:MI'), 'Piano UT');
INSERT INTO spectacle VALUES (35, TO_TIMESTAMP('0:45', 'HH24:MI'), 'Ski UT');
INSERT INTO spectacle VALUES (36, TO_TIMESTAMP('2:59', 'HH24:MI'), 'Data Venture');
INSERT INTO spectacle VALUES (37, TO_TIMESTAMP('1:02', 'HH24:MI'), 'Piano UT');

INSERT INTO concert VALUES (34, 'Beethoven', 'Classique', TO_TIMESTAMP('1824', 'YYYY'));
INSERT INTO theatre VALUES (36, 'Molière', TO_TIMESTAMP('1665', 'YYYY'), 'Drame');
INSERT INTO standup VALUES (35, 'Comique');
INSERT INTO standup VALUES (37, 'Table Ronde');

insert into salle values (105,120);
insert into salle values (403,35);
insert into salle values (518,30);
insert into salle values (610,40);

insert into batiment values (3);
insert into batiment values (5);

insert into typeSalle values (3, 105, 'Amphitéâtre');
insert into typeSalle values (3, 403, 'Cours');
insert into typeSalle values (3, 518, 'Cours');
insert into typeSalle values (5, 610, 'Bureau');

insert into seance values(12, TO_TIMESTAMP('2021-08-09', 'YYYY-MM-DD'), TO_TIMESTAMP('20:45', 'HH24:MI'),1, 5, 610);
insert into seance values(13, TO_TIMESTAMP('2021-08-10', 'YYYY-MM-DD'), TO_TIMESTAMP('10:30', 'HH24:MI'),1, 3, 403);

insert into reservation values('Ski UT', 610, 5, TO_TIMESTAMP('2021-05-18', 'YYYY-MM-DD'));
