#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
#import json #nécessaire pour pprint (affichage des données JSON sur plusieurs lignes)
import pprint #nécessaire pour pprint (affichage des données JSON sur plusieurs lignes)
import re
from datetime import datetime

url = "https://www.wikidata.org/w/api.php"

award_received = 0 # pour balayer les différents P166 de la personne
award_received_total = 0 # nombre de P166 de la personne
decoration = 0 # pour balayer les différentes décorations (listées ci-dessous) possibles
decoration_nom = ["Chevalier ONM", "Officier ONM", "Commandeur ONM", "Grand Officier ONM", "Grand'Croix ONM", "ONM",\
"Chevalier LH", "Officier LH", "Commandeur LH", "Grand Officier LH", "Grand'Croix LH", "LH"]
decoration_total = len(decoration_nom)
decoration_Q = ["Q13422138", "Q13422140", "Q13422141", "Q13422142", "Q13422143", "Q652962", \
"Q10855271", "Q10855195", "Q10855212", "Q10855216", "Q10855226", "Q163700"]
decoration_img = ["https://upload.wikimedia.org/wikipedia/commons/thumb/9/92/Ordre_national_du_Merite_Chevalier_ribbon.svg/218px-Ordre_national_du_Merite_Chevalier_ribbon.svg.png", \
"https://upload.wikimedia.org/wikipedia/commons/thumb/5/52/Ordre_national_du_Merite_Officier_ribbon.svg/218px-Ordre_national_du_Merite_Officier_ribbon.svg.png", \
"https://upload.wikimedia.org/wikipedia/commons/thumb/8/82/Ordre_national_du_Merite_Commandeur_ribbon.svg/218px-Ordre_national_du_Merite_Commandeur_ribbon.svg.png", \
"https://upload.wikimedia.org/wikipedia/commons/thumb/b/b2/Ordre_national_du_Merite_GO_ribbon.svg/218px-Ordre_national_du_Merite_GO_ribbon.svg.png", \
"https://upload.wikimedia.org/wikipedia/commons/thumb/8/82/Ordre_national_du_Merite_GC_ribbon.svg/218px-Ordre_national_du_Merite_GC_ribbon.svg.png", \
"https://upload.wikimedia.org/wikipedia/commons/thumb/c/cc/Ordre_national_du_merite_chevalier_FRANCE.jpg/86px-Ordre_national_du_merite_chevalier_FRANCE.jpg", \
"https://upload.wikimedia.org/wikipedia/commons/thumb/e/e6/Legion_Honneur_Chevalier_ribbon.svg/218px-Legion_Honneur_Chevalier_ribbon.svg.png", \
"https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Legion_Honneur_Officier_ribbon.svg/218px-Legion_Honneur_Officier_ribbon.svg.png", \
"https://upload.wikimedia.org/wikipedia/commons/thumb/e/ef/Legion_Honneur_Commandeur_ribbon.svg/218px-Legion_Honneur_Commandeur_ribbon.svg.png", \
"https://upload.wikimedia.org/wikipedia/commons/thumb/a/af/Legion_Honneur_GO_ribbon.svg/218px-Legion_Honneur_GO_ribbon.svg.png", \
"https://upload.wikimedia.org/wikipedia/commons/thumb/b/ba/Legion_Honneur_GC_ribbon.svg/218px-Legion_Honneur_GC_ribbon.svg.png", \
"https://upload.wikimedia.org/wikipedia/commons/8/81/De_la_legion_d_honneur_Recto.png"]
decoration_obtenue = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
decoration_date = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

try:
    with open("in.html", 'r') as file:
        filedata = file.read()
except IOError:
    print("Erreur: Enregistrez une page de décret depuis Légifrance sous le nom \"in.html\" dans le dossier du programme.")

print("RECHERCHE DES INFOS DE BASE DU DECRET...")
NOR = filedata[filedata.find("NOR :")+6:filedata.find("NOR :")+6+12] #récupère "PRER2104806D" dans "NOR : PRER2104806D"
print("Identifiant NOR du décret ?   Par défaut (reconnu dans in.html) :", NOR)
NOR = input() or NOR
print("NOR =", NOR)

date_decret = filedata[filedata.find("Décret du")+10:filedata.find("portant promotion")-1]
print("date_decret =", date_decret)
annee_decret = date_decret[len(date_decret)-4:]
print("annee_decret =", annee_decret)
jour_decret = date_decret[:date_decret.find(" ")]
if jour_decret == "1er": jour_decret = 1
if len(str(jour_decret)) == 1 : jour_decret = "0" + str(jour_decret)
print("jour_decret =", jour_decret)
mois_decret = date_decret[date_decret.find(" ")+1:len(date_decret)-5]
print("mois_decret =", mois_decret)
if mois_decret == "janvier": date_decret_ISO = str(annee_decret) + "-01-" + str(jour_decret)
elif mois_decret == "février": date_decret_ISO = str(annee_decret) + "-02-" + str(jour_decret)
elif mois_decret == "mars": date_decret_ISO = str(annee_decret) + "-03-" + str(jour_decret)
elif mois_decret == "avril": date_decret_ISO = str(annee_decret) + "-04-" + str(jour_decret)
elif mois_decret == "mai": date_decret_ISO = str(annee_decret) + "-05-" + str(jour_decret)
elif mois_decret == "juin": date_decret_ISO = str(annee_decret) + "-06-" + str(jour_decret)
elif mois_decret == "juillet": date_decret_ISO = str(annee_decret) + "-07-" + str(jour_decret)
elif mois_decret == "août": date_decret_ISO = str(annee_decret) + "-08-" + str(jour_decret)
elif mois_decret == "septembre": date_decret_ISO = str(annee_decret) + "-09-" + str(jour_decret)
elif mois_decret == "octobre": date_decret_ISO = str(annee_decret) + "-10-" + str(jour_decret)
elif mois_decret == "novembre": date_decret_ISO = str(annee_decret) + "-11-" + str(jour_decret)
elif mois_decret == "décembre": date_decret_ISO = str(annee_decret) + "-12-" + str(jour_decret)
else: date_decret_ISO = ""
print("Date du décret au format AAAA-MM-JJ ?   Par défaut (reconnu dans in.html) :", date_decret_ISO)
date_decret_ISO = input() or date_decret_ISO
print("date_decret_ISO =", date_decret_ISO)
date_decret_ISO_wiki = "+" + date_decret_ISO + "T00:00:00Z/11"
print("date_decret_ISO_wiki =", date_decret_ISO_wiki)

ordre = ""
#ordre_ligne_nomination = filedata[filedata.find("nomination"):filedata.find("nomination")+1000]
#print("ordre_ligne_nomination =", ordre_ligne_nomination)
#ordre_ligne_promotion = filedata[filedata.find("promotion"):filedata.find("promotion")+1000]
#print("ordre_ligne_promotion =", ordre_ligne_promotion)
#ordre_ligne_chancellerie = filedata[filedata.find("Chancellerie"):filedata.find("Chancellerie")+1000]
#print("ordre_ligne_chancellerie =", ordre_ligne_chancellerie)
#if filedata[ordre_ligne_nominationfiledata.find("ordre"):filedata.find("ordre")+24] == "ordre national du Mérite" or "ordre national du mérite":
if filedata.find("Grande chancellerie de la Légion d'honneur") != -1: ordre = "LH"
if filedata.find("Chancellerie de l'ordre national du Mérite") != -1: ordre = "ONM"
if filedata.find("Grande chancellerie de la Légion d'honneur") != -1  and filedata.find("Chancellerie de l'ordre national du Mérite") != -1: ordre = ""
print("Ordre ? LH ou ONM ?   Par défaut (reconnu dans in.html) :", ordre)
ordre = input() or ordre
print("ordre =", ordre)
if (ordre != "LH") and (ordre != "ONM"): raise SystemExit("Erreur : ordre doit être LH (Légion d'Honneur) ou ONM (Ordre National du Mérite)")

print("MISE EN FORME DES TITRES DU DECRET...")
if ordre == "ONM":
    filedata = filedata.replace("Au grade de chevalier", "Au grade de chevalier <img src=\"" + decoration_img[0] + "\" width=\"150\"><style type=\"text/css\"> form, table {display:inline;margin:0px;padding:0px;}</style>")
    filedata = filedata.replace("Au grade d'officier", "Au grade d'officier <img src=\"" + decoration_img[1] + "\" width=\"150\"><style type=\"text/css\"> form, table {display:inline;margin:0px;padding:0px;}</style>")
    filedata = filedata.replace("Au grade de commandeur", "Au grade de commandeur <img src=\"" + decoration_img[2] + "\" width=\"150\"><style type=\"text/css\"> form, table {display:inline;margin:0px;padding:0px;}</style>")
    filedata = filedata.replace("A la dignité de grand officier", "A la dignité de grand officier <img src=\"" + decoration_img[3] + "\" width=\"150\"><style type=\"text/css\"> form, table {display:inline;margin:0px;padding:0px;}</style>")
    filedata = filedata.replace("A la dignité de grand'croix", "A la dignité de grand'croix <img src=\"" + decoration_img[4] + "\" width=\"150\"><style type=\"text/css\"> form, table {display:inline;margin:0px;padding:0px;}</style>")
if ordre == "LH":
    filedata = filedata.replace("Au grade de chevalier", "Au grade de chevalier <img src=\"" + decoration_img[6] + "\" width=\"150\"><style type=\"text/css\"> form, table {display:inline;margin:0px;padding:0px;}</style>")
    filedata = filedata.replace("Au grade d'officier", "Au grade d'officier <img src=\"" + decoration_img[7] + "\" width=\"150\"><style type=\"text/css\"> form, table {display:inline;margin:0px;padding:0px;}</style>")
    filedata = filedata.replace("Au grade de commandeur", "Au grade de commandeur <img src=\"" + decoration_img[8] + "\" width=\"150\"><style type=\"text/css\"> form, table {display:inline;margin:0px;padding:0px;}</style>")
    filedata = filedata.replace("A la dignité de grand officier", "A la dignité de grand officier <img src=\"" + decoration_img[9] + "\" width=\"150\"><style type=\"text/css\"> form, table {display:inline;margin:0px;padding:0px;}</style>")
    filedata = filedata.replace("A la dignité de grand'croix", "A la dignité de grand'croix <img src=\"" + decoration_img[10] + "\" width=\"150\"><style type=\"text/css\"> form, table {display:inline;margin:0px;padding:0px;}</style>")

def traitement():
    global rang_personne
    global filedata
    global date_decret_ISO_wiki
    global NOR
    offset = 0 # pour décaler le texte après la 1ère décoration de la 1ère personne
    #while rang_personne < 10:
    while rang_personne < len(xxx):
        print("rang_personne =", rang_personne)
        print("RECHERCHE ET FORMATAGE DU NOM DANS LE DECRET...")
        print(xxx[rang_personne], "+", offset, ":", filedata[xxx[rang_personne]+offset:xxx[rang_personne]+offset+5000]) #105412 : Mme Dupont, née Durant (Jeanne, Marie, Hélène), dirigeante d'entrep
        ouverture_parenthese = filedata[xxx[rang_personne]+offset:xxx[rang_personne]+offset+5000].find("(")
        fermeture_parenthese = filedata[xxx[rang_personne]+offset:xxx[rang_personne]+offset+5000].find(")")
        prenoms = filedata[xxx[rang_personne]+offset+ouverture_parenthese+1:xxx[rang_personne]+offset+fermeture_parenthese]
        print("prenoms =", prenoms) #prenoms = Jeanne, Marie, Hélène
        if prenoms.find(",") == -1:
            prenom = prenoms
        else:
            prenom = prenoms[0:prenoms.find(",")]
        print("prenom =", prenom) #prenom = Jeanne
        if filedata[xxx[rang_personne]+offset:xxx[rang_personne]+offset+4] == "Mme ":
            print("titre = Mme ")
            longueur_titre = 4
        if filedata[xxx[rang_personne]+offset:xxx[rang_personne]+offset+3] == "M. ":
            print("titre = M.")
            longueur_titre = 3
        #longueur_titre = 4
        print("longueur_titre =", longueur_titre)
        nom_complet = filedata[xxx[rang_personne]+offset+longueur_titre:xxx[rang_personne]+offset+ouverture_parenthese]
        print("nom complet =", nom_complet) #Mme Dupont, née Durant
        if nom_complet.find(",") == -1:
            nom = nom_complet
        else:
            nom = nom_complet[0:nom_complet.find(",")]
        print("nom =", nom) #nom = Dupont

        personne_listee = prenom + " " + nom
        print("personne_listee =", personne_listee) #personne_listee = Jeanne Dupont

        print("RECHERCHE DE LA PERSONNE SUR WIKIDATA...")
        query = personne_listee
        params1 = {
        "action" : "wbsearchentities",
        "language" : "fr",
        "format" : "json",
        "search" : query
        }
        data = requests.get(url,params=params1)

        rang_personne_Q = 0 # pour balayer les différents homonymes
        id = ""

        while id != "KO":
            print("rang_personne_Q =", rang_personne_Q)
            try:
                id = data.json()["search"][rang_personne_Q]["id"]
            except KeyError:
                id = "KO"
            except IndexError:
                id = "KO"
            print("id =", id)

            if id != "KO":
                try:
                    label = data.json()["search"][rang_personne_Q]["label"]
                except KeyError:
                    label = ""
                except IndexError:
                    label = ""
                print("label= ", label)
                try:
                    description = data.json()["search"][rang_personne_Q]["description"]
                except KeyError:
                    description = ""
                except IndexError:
                    description = ""
                print("description =", description)

                print(rang_personne, "/", rang_personne_Q, ": " + id + " : " + label + ", " + description)
                #print(data.json()["search"][rang_personne_Q]["title"])
                #print(data.json()["search"][rang_personne_Q]["match"]["text"])
                #pprint.pprint(data.json())

                #print("RECHERCHE SI 1ERE OCCUPATION ET 1ERE POSITION HELD SUR WIKIDATA...")   pas fonctionnel ; il faudrait continuer pour récuperer le NOM à partir de l'id de l'occupation
                #params11 = {
                #"action" : "wbgetclaims",
                #"format" : "json",
                #"entity" : id,
                #"property" : "P106"
                #}
                #data11 = requests.get(url,params=params11)
                #pprint.pprint(data11.json())
                #params12 = {
                #"action" : "wbgetclaims",
                #"format" : "json",
                #"entity" : id,
                #"property" : "P39"
                #}
                #data12 = requests.get(url,params=params12)
                #pprint.pprint(data12.json())

                print("RECHERCHE DES DECORATIONS (ONM ET LH) SUR WIKIDATA...")
                params2 = {
                "action" : "wbgetclaims",
                "format" : "json",
                "entity" : id,
                "property" : "P166"
                }
                data2 = requests.get(url,params=params2)
                #pprint.pprint(data.json())
                #print("-----")
                #pprint.pprint(data2.json()["claims"]["P166"][0])
                #print("-----")
                #pprint.pprint(data2.json()["claims"]["P166"][0]["mainsnak"]["datavalue"]["value"]["id"])
                #pprint.pprint(data.json()["claims"]["P166"][0]["qualifiers"]["P585"][0]["datavalue"]["value"]["time"])
                #pprint.pprint(data.json()["claims"]["P166"][0]["qualifiers"])
                #print("qualifiers" in data2.json()["claims"]["P166"][0])
                #print("P585" in data.json()["claims"]["P166"][0]["qualifiers"])
                #print("---------")

                j=0
                while j < decoration_total:
                    decoration_obtenue[j] = 0
                    decoration_date[j] = 0
                    j = j + 1

                try:
                    award_received_total = len(data2.json()["claims"]["P166"])
                except KeyError:
                    award_received_total = 0
                print("award_received_total =", award_received_total)

                if award_received_total > 0:
                    award_received = 0
                    while award_received < award_received_total:
                        #print("check le P166 N°", award_received, "...")
                        decoration = 0
                        while decoration < decoration_total:
                            if data2.json()["claims"]["P166"][award_received]["mainsnak"]["datavalue"]["value"]["id"] == decoration_Q[decoration]:
                                #print(decoration_nom[decoration], "trouvé")
                                decoration_obtenue[decoration] = 1
                                if "qualifiers" in data2.json()["claims"]["P166"][award_received]:
                                    #print("qualifier trouvé dans P166 N°", award_received)
                                    if "P585" in data2.json()["claims"]["P166"][award_received]["qualifiers"]:
                                        #print("qualifier P585 trouvé dans P166 N°", award_received)
                                        decoration_date[decoration] = data2.json()["claims"]["P166"][award_received]["qualifiers"]["P585"][0]["datavalue"]["value"]["time"]
                                        #print("date =", decoration_date[decoration])
                            decoration = decoration + 1
                        award_received = award_received + 1
                print(decoration_nom)
                print(decoration_obtenue)
                print(decoration_date)

                print("RECHERCHE DES DATES DE NAISSANCE ET DE DECES SUR WIKIDATA...")
                params3 = {
                "action" : "wbgetclaims",
                "format" : "json",
                "entity" : id,
                "property" : "P569"
                }
                data3 = requests.get(url,params=params3)
                #pprint.pprint(data3.json()["claims"]["P569"][0]["mainsnak"]["datavalue"]["value"]["time"])
                try:
                    date_naissance = data3.json()["claims"]["P569"][0]["mainsnak"]["datavalue"]["value"]["time"][1:5]
                except KeyError:
                    date_naissance = ""
                print("date_naissance =", date_naissance)
                params4 = {
                "action" : "wbgetclaims",
                "format" : "json",
                "entity" : id,
                "property" : "P570"
                }
                data4 = requests.get(url,params=params4)
                #pprint.pprint(data3.json()["claims"]["P570"][0]["mainsnak"]["datavalue"]["value"]["time"])
                try:
                    date_deces = data4.json()["claims"]["P570"][0]["mainsnak"]["datavalue"]["value"]["time"][1:5]
                except KeyError:
                    date_deces = ""
                print("date_deces =", date_deces)

                print("AFFICHAGE DES DECORATIONS (ONM ET LH) WIKIDATA DANS LE DECRET...")

                print(xxx[rang_personne], "+", offset, ":", filedata[xxx[rang_personne]+offset:xxx[rang_personne]+offset+5000])
                br_suivant = filedata[xxx[rang_personne]+offset:xxx[rang_personne]+offset+5000].find("<br>")
                print("br_suivant :", br_suivant)
                if br_suivant == -1 : br_suivant = 10000
                p_suivant = filedata[xxx[rang_personne]+offset:xxx[rang_personne]+offset+5000].find("</p>")
                print("p_suivant :", p_suivant)
                if p_suivant == -1 : p_suivant = 10000
                saut_suivant = min(br_suivant, p_suivant)
                print("saut_suivant :", saut_suivant)

                print("début injection")
                injection_index = xxx[rang_personne]+offset + saut_suivant
                print("injection_index =", injection_index)
                injection_str = "<style type=\"text/css\"> form, table {display:inline;margin:0px;padding:0px;}</style><br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" + str(rang_personne) + "/" + str(rang_personne_Q) + \
                " : <b><a href=\"https://www.wikidata.org/wiki/" + id + "\">" + id + " : " + \
                label + " (" + date_naissance + "-" + date_deces + "), " + description + "</b></a>"
                #ajout des boutons pour QuickStatements
                #injection_str = injection_str + "<style type=\"text/css\"> form, table {display:inline;margin:0px;padding:0px;}</style>"
                if ordre == "LH": QS_range_bouton_decoration = [10,9,8,7,6]
                if ordre == "ONM": QS_range_bouton_decoration = [4,3,2,1,0]
                for QS_compteur_bouton_decoration in QS_range_bouton_decoration:
                    injection_str = injection_str + " <form onclick=\"QS_ajout_ligne('" + id + "|P166|" + decoration_Q[QS_compteur_bouton_decoration] + "|P585|" + date_decret_ISO_wiki + "|S464|','" + NOR + "','" + id + decoration_Q[QS_compteur_bouton_decoration] + \
                    "')\"><input type=\"button\" id=\"" + id + decoration_Q[QS_compteur_bouton_decoration] + "\" value=\"" + decoration_nom[QS_compteur_bouton_decoration] + "\"></form>"
                #ajout des éventuelles décorations existantes
                #k = 0
                #while k < decoration_total:
                #    if decoration_obtenue[k] == 1:
                #        injection_str = injection_str + "<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<img src=\"" + decoration_img[k] + "\" width=\"50\"> &nbsp;" + "<a href=\"https://www.wikidata.org/wiki/" + id + "#P166\">" + decoration_nom[k] + "</a>"
                #        if decoration_date[k] != 0:
                #            date_ISO_reformatee = decoration_date[k][1:] # pour passer de +2008-09-12T00:00:00Z à 2008-09-12T00:00:00Z
                #            date_ISO_reformatee = date_ISO_reformatee[:10] # pour passer de 2008-09-12T00:00:00 à 2008-09-12
                #            injection_str = injection_str + " du " + date_ISO_reformatee
                #    k = k + 1

                for k in [10,9,8,7,6,11,4,3,2,1,0,5]: #pour affichage des plus hautes décorations en premier
                    if decoration_obtenue[k] == 1:
                        injection_str = injection_str + "<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<img src=\"" + decoration_img[k] + "\" width=\"50\"> &nbsp;" + "<a href=\"https://www.wikidata.org/wiki/" + id + "#P166\">" + decoration_nom[k] + "</a>"
                        if decoration_date[k] != 0:
                            date_ISO_reformatee = decoration_date[k][1:] # pour passer de +2008-09-12T00:00:00Z à 2008-09-12T00:00:00Z
                            date_ISO_reformatee = date_ISO_reformatee[:10] # pour passer de 2008-09-12T00:00:00 à 2008-09-12
                            injection_str = injection_str + " du " + date_ISO_reformatee

                print("injection_str =", injection_str)
                filedata = filedata[:injection_index] + injection_str + filedata[injection_index:]
                offset = offset + len(injection_str)
                print("offset =", offset)
                print("fin injection")

                rang_personne_Q = rang_personne_Q + 1

        print("-------------------------------")

        rang_personne = rang_personne + 1

def QS_ajout_script():
    global filedata
    filedata = filedata[:filedata.find("</html>")] + "<script language=\"Javascript\"> function QS_ajout_ligne(champ1,champ2,ID_bouton) { \
      if (document.getElementById(ID_bouton).style.backgroundColor != \"green\") { \
        var paragraph = document.getElementById(\"p\"); \
        var text = document.createTextNode(champ1 + '\"' + champ2 + '\"'); \
        paragraph.appendChild(text); \
        var text = document.createElement(\"br\"); \
        paragraph.appendChild(text); \
        document.getElementById(ID_bouton).style.color = \"white\"; \
        document.getElementById(ID_bouton).style.backgroundColor = \"green\"; \
      } \
    } \
    </script> \
    </p><b>Texte à utiliser dans <a href =\"https://quickstatements.toolforge.org/#/\">QuickStatements</a> pour exporter les nouvelles décorations dans Wikidata :</b> \
    <p id=\"p\"></p>" + filedata[filedata.find("</html>"):]

print("RECUPERATION DES LIGNES ASSOCIEES ASSOCIEES A CHAQUE PERSONNE...")
rang_personne = 0
xxx = [] #tableau des chaînes de caractères correspondante aux passages du décret concernant chaque personne
i = 0
for m in re.finditer("M\. ", filedata):
    xxx.append(m.start())
    print(xxx[i])
    i = i + 1
traitement()
for m in re.finditer("Mme ", filedata): #relit les données pour les Mme. (une fois que les M. ont été traité et aient offseté les données)
    xxx.append(m.start())
    print(xxx[i])
    i = i + 1
traitement()

QS_ajout_script()

with open("out.html", 'w') as file:
    file.write(filedata)

print("TRAITEMENT TERMINE. OUVREZ LE FICHIER \"out.html\".")
