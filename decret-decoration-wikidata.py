#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# https://github.com/Sovxx/decret-decoration-wikidata

#python : supérieure ou égale à v3.6
import requests
#import json #nécessaire pour pprint (affichage des données JSON sur plusieurs lignes)
import pprint #nécessaire pour pprint (affichage des données JSON sur plusieurs lignes)
import re
from datetime import datetime

debug = False

url = "https://www.wikidata.org/w/api.php"

decoration_nom = ["Chevalier ONM", "Officier ONM", "Commandeur ONM", "Grand Officier ONM", "Grand'Croix ONM", "ONM", \
    "Chevalier LH", "Officier LH", "Commandeur LH", "Grand Officier LH", "Grand'Croix LH", "LH", \
    "Chevalier AL", "Officier AL", "Commandeur AL", "AL"]
decoration_total = len(decoration_nom)
decoration_Q = ["Q13422138", "Q13422140", "Q13422141", "Q13422142", "Q13422143", "Q652962", \
    "Q10855271", "Q10855195", "Q10855212", "Q10855216", "Q10855226", "Q163700", \
    "Q13452528", "Q13452524", "Q13452531", "Q716909"]
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
    "https://upload.wikimedia.org/wikipedia/commons/8/81/De_la_legion_d_honneur_Recto.png", \
    "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6a/Ordre_des_Arts_et_des_Lettres_Chevalier_ribbon.svg/218px-Ordre_des_Arts_et_des_Lettres_Chevalier_ribbon.svg.png", \
    "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2a/Ordre_des_Arts_et_des_Lettres_Officier_ribbon.svg/218px-Ordre_des_Arts_et_des_Lettres_Officier_ribbon.svg.png", \
    "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ef/Ordre_des_Arts_et_des_Lettres_Commandeur_ribbon.svg/218px-Ordre_des_Arts_et_des_Lettres_Commandeur_ribbon.svg.png", \
    "https://upload.wikimedia.org/wikipedia/commons/9/9c/Chevalier_arts_et_lettres.jpg"]

def definition_NOR(filedata):
    NOR = filedata[filedata.find("NOR :")+6:filedata.find("NOR :")+6+12] #récupère "PRER2104806D" dans "NOR : PRER2104806D"
    print(f"Identifiant NOR du décret ?   Par défaut (reconnu dans in.html) : {NOR}")
    NOR = input() or NOR
    print(f"NOR = {NOR}")
    return NOR

def check_date(date_a_checker):
    if len(date_a_checker) != 10: return "date KO ; len != 10"
    try:
        if int(date_a_checker[0:4]) < 1800: return "date KO ; AAAA < 1800"
        if int(date_a_checker[0:4]) > 2100: return "date KO ; AAAA > 2100"
        if int(date_a_checker[5:7]) < 1: return "date KO ; mois non valide"
        if int(date_a_checker[5:7]) > 12: return "date KO ; mois non valide"
    except (ValueError,TypeError):
        return "date KO ; erreur de type"
    return "date valide"

def definition_date_decret_ISO_wiki(filedata):
    date_decret = "[non trouvé]"
    if filedata.find("Décret du") != -1:
        if filedata.find("portant nomination") != -1: date_decret = filedata[filedata.find("Décret du")+10:filedata.find("portant nomination")-1]
        if filedata.find("portant promotion") != -1: date_decret = filedata[filedata.find("Décret du")+10:filedata.find("portant promotion")-1]
        if filedata.find("portant élévation") != -1: date_decret = filedata[filedata.find("Décret du")+10:filedata.find("portant élévation")-1]
    if filedata.find("Arrêté du") != -1:
        if filedata.find("portant nomination") != -1: date_decret = filedata[filedata.find("Arrêté du")+10:filedata.find("portant nomination")-1]
        if filedata.find("portant promotion") != -1: date_decret = filedata[filedata.find("Arrêté du")+10:filedata.find("portant promotion")-1]
    if debug: print(f"date_decret = {date_decret}")
    date_decret_ISO = "[non trouvé]"
    if date_decret != "[non trouvé]":
        annee_decret = date_decret[len(date_decret)-4:]
        if debug: print(f"annee_decret = {annee_decret}")
        jour_decret = date_decret[:date_decret.find(" ")]
        if jour_decret == "1er": jour_decret = 1
        if len(str(jour_decret)) == 1 : jour_decret = "0" + str(jour_decret)
        if debug: print(f"jour_decret = {jour_decret}")
        mois_decret = date_decret[date_decret.find(" ")+1:len(date_decret)-5]
        if debug: print(f"mois_decret = {mois_decret}")
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
        else: date_decret_ISO = "[format non reconnu]"
    if debug: print(f"date_decret_ISO = {date_decret_ISO}")
    print(f"Date du décret au format AAAA-MM-JJ ?   Par défaut (reconnu dans in.html) : {date_decret_ISO}")
    date_decret_ISO = input() or date_decret_ISO
    print(f"date_decret_ISO = {date_decret_ISO}")
    if debug: print(f"check_date(date_decret_ISO) = {check_date(date_decret_ISO)}")
    if check_date(date_decret_ISO) != "date valide": raise SystemExit("Erreur : date du décret invalide, pas au format AAAA-MM-JJ ; réessayez en la tapant manuellement")
    date_decret_ISO_wiki = "+" + date_decret_ISO + "T00:00:00Z/11"
    if debug: print(f"date_decret_ISO_wiki = {date_decret_ISO_wiki}")
    return date_decret_ISO_wiki

def definition_ordre(filedata):
    ordre = "[non trouvé]"
    if filedata.find("Grande chancellerie de la Légion d'honneur") != -1: ordre = "LH"
    if filedata.find("Grande chancellerie de la Légion d’honneur") != -1: ordre = "LH" # apostrophe différente de celle de la ligne du dessus !
    if filedata.find("Chancellerie de l'ordre national du Mérite") != -1: ordre = "ONM"
    if filedata.find("Chancellerie de l’ordre national du Mérite") != -1: ordre = "ONM" # apostrophe différente de celle de la ligne du dessus !
    if filedata.find("Grande chancellerie de la Légion d'honneur") == -1  and filedata.find("Chancellerie de l'ordre national du Mérite") == -1:
        if filedata.find("exécution par le chancelier de l'ordre national du Mérite") != -1: ordre = "ONM"
        if filedata.find("et de grand officier de l'ordre national du Mérite") != -1: ordre = "ONM"
        if filedata.find("exécution par le grand chancelier de l'ordre national de la Légion d'honneur") != -1: ordre ="LH"
        if filedata.find("exécution par le grand chancelier de la Légion d'honneur") != -1: ordre ="LH"
        if filedata.find("et de grand officier de l'ordre national du Mérite") != -1: ordre = "ONM"
        if filedata.find("portant élévation dans l'ordre national de la Légion d'honneur") != -1: ordre ="LH"
        if filedata.find("ORDRE NATIONAL DU MERITE Décret du") != -1: ordre = "ONM"
        if filedata.find("sont élevés dans l'ordre national du Mérite") != -1: ordre = "ONM"
        if filedata.find("est élevé dans l'ordre national du Mérite") != -1: ordre = "ONM"
    if filedata.find("dans l'ordre des Arts et des Lettres") != -1: ordre = "AL"
    print("Ordre ? LH, ONM ou AL (AL n'est pas encore fonctionnel) ?   Par défaut (reconnu dans in.html) :", ordre)
    ordre = input() or ordre
    print("ordre =", ordre)
    if (ordre == "LH") or (ordre == "ONM") or (ordre == "AL"): return ordre
    raise SystemExit("Erreur : ordre doit être LH (Légion d'Honneur), ONM (Ordre National du Mérite) ou AL (Arts et Lettres)")

def definition_boutons_simplifies():
    print("Boutons simplifiés (O/N) ?   Par défaut et recommandé : O")
    boutons_simplifies = input() or "O"
    if boutons_simplifies in {"O", "o", "Y", "y"}:
        print("boutons_simplifies = True")
        return True
    if boutons_simplifies in {"N", "n"}:
        print("boutons_simplifies = False")
        return False
    raise SystemExit("Erreur : doit être O ou N")

def mise_en_forme_titres(filedata, ordre):
    if ordre == "ONM":
        filedata = filedata.replace("Au grade de chevalier", "<b>Au grade de chevalier</b> <img src=\"" + decoration_img[0] + "\" width=\"150\"><style type=\"text/css\"> form, table {display:inline;margin:0px;padding:0px;}</style>")
        filedata = filedata.replace("Au grade d'officier", "<b>Au grade d'officier</b> <img src=\"" + decoration_img[1] + "\" width=\"150\"><style type=\"text/css\"> form, table {display:inline;margin:0px;padding:0px;}</style>")
        filedata = filedata.replace("Au grade d’officier", "<b>Au grade d’officier</b> <img src=\"" + decoration_img[1] + "\" width=\"150\"><style type=\"text/css\"> form, table {display:inline;margin:0px;padding:0px;}</style>") # apostrophe différente de celle de la ligne du dessus !
        filedata = filedata.replace("Au grade de commandeur", "<b>Au grade de commandeur</b> <img src=\"" + decoration_img[2] + "\" width=\"150\"><style type=\"text/css\"> form, table {display:inline;margin:0px;padding:0px;}</style>")
        filedata = filedata.replace("A la dignité de grand officier", "<b>A la dignité de grand officier</b> <img src=\"" + decoration_img[3] + "\" width=\"150\"><style type=\"text/css\"> form, table {display:inline;margin:0px;padding:0px;}</style>")
        filedata = filedata.replace("A la dignité de grand'croix", "<b>A la dignité de grand'croix</b> <img src=\"" + decoration_img[4] + "\" width=\"150\"><style type=\"text/css\"> form, table {display:inline;margin:0px;padding:0px;}</style>")
        filedata = filedata.replace("A la dignité de grand’croix", "<b>A la dignité de grand’croix</b> <img src=\"" + decoration_img[4] + "\" width=\"150\"><style type=\"text/css\"> form, table {display:inline;margin:0px;padding:0px;}</style>") # apostrophe différente de celle de la ligne du dessus !
    if ordre == "LH":
        filedata = filedata.replace("Au grade de chevalier", "<b>Au grade de chevalier</b> <img src=\"" + decoration_img[6] + "\" width=\"150\"><style type=\"text/css\"> form, table {display:inline;margin:0px;padding:0px;}</style>")
        filedata = filedata.replace("Au grade d'officier", "<b>Au grade d'officier</b> <img src=\"" + decoration_img[7] + "\" width=\"150\"><style type=\"text/css\"> form, table {display:inline;margin:0px;padding:0px;}</style>")
        filedata = filedata.replace("Au grade d’officier", "<b>Au grade d’officier</b> <img src=\"" + decoration_img[7] + "\" width=\"150\"><style type=\"text/css\"> form, table {display:inline;margin:0px;padding:0px;}</style>") # apostrophe différente de celle de la ligne du dessus !
        filedata = filedata.replace("Au grade de commandeur", "<b>Au grade de commandeur</b> <img src=\"" + decoration_img[8] + "\" width=\"150\"><style type=\"text/css\"> form, table {display:inline;margin:0px;padding:0px;}</style>")
        filedata = filedata.replace("A la dignité de grand officier", "<b>A la dignité de grand officier</b> <img src=\"" + decoration_img[9] + "\" width=\"150\"><style type=\"text/css\"> form, table {display:inline;margin:0px;padding:0px;}</style>")
        filedata = filedata.replace("A la dignité de grand'croix", "<b>A la dignité de grand'croix</b> <img src=\"" + decoration_img[10] + "\" width=\"150\"><style type=\"text/css\"> form, table {display:inline;margin:0px;padding:0px;}</style>")
        filedata = filedata.replace("A la dignité de grand’croix", "<b>A la dignité de grand’croix</b> <img src=\"" + decoration_img[10] + "\" width=\"150\"><style type=\"text/css\"> form, table {display:inline;margin:0px;padding:0px;}</style>") # apostrophe différente de celle de la ligne du dessus !
    if ordre == "AL":
        filedata = filedata.replace("au grade de commandeur de l'ordre des Arts et des Lettres", "<b>au grade de commandeur de l'ordre des Arts et des Lettres</b> <img src=\"" + decoration_img[14] + "\" width=\"150\"><style type=\"text/css\"> form, table {display:inline;margin:0px;padding:0px;}</style>")
        filedata = filedata.replace("au grade d'officier de l'ordre des Arts et des Lettres", "<b>au grade d'officier de l'ordre des Arts et des Lettres</b> <img src=\"" + decoration_img[13] + "\" width=\"150\"><style type=\"text/css\"> form, table {display:inline;margin:0px;padding:0px;}</style>")
        filedata = filedata.replace("au grade de chevalier de l'ordre des Arts et des Lettres", "<b>au grade de chevalier de l'ordre des Arts et des Lettres</b> <img src=\"" + decoration_img[12] + "\" width=\"150\"><style type=\"text/css\"> form, table {display:inline;margin:0px;padding:0px;}</style>")
    return filedata

def traitement(filedata, NOR, date_decret_ISO_wiki, ordre, boutons_simplifies):
    xxx = construction_index(filedata) # index de la position de chaque personne dans le decret
    rang_personne = 0
    offset = 0 # pour décaler le texte après la 1ère décoration de la 1ère personne
    while rang_personne < len(xxx):
        if debug: print(f"rang_personne = {rang_personne}")
        if debug: print("RECHERCHE ET FORMATAGE DU NOM DANS LE DECRET...")
        personne_listee = get_nom(filedata,xxx,rang_personne,offset,ordre)
        liste_des_id = [] #juste pour éviter plusieurs fois le même id (Q wikidata) si trouvé pour différents alias
        for alias in personne_listee:
            #print(f"{rang_personne} / {len(xxx)-1} : {personne_listee}")
            print(f"{rang_personne} / {len(xxx)-1} : *****{alias}*****")
            if debug: print("RECHERCHE DE LA PERSONNE SUR WIKIDATA...")
            params1 = {
                "action" : "wbsearchentities",
                "language" : "fr",
                "format" : "json",
                "search" : alias
            }
            data1 = requests.get(url, params=params1)
            rang_personne_Q = 0 # pour balayer les différents homonymes
            id = ""
            while id != "KO":
                if debug: print(f"rang_personne_Q = {rang_personne_Q}")
                id = get_id(data1,rang_personne_Q)
                if id != "KO" and liste_des_id.count(id) == 0:
                    if debug: print("RECHERCHE DES LABEL ET DESCRIPTION SUR WIKIDATA...")
                    label = get_label(data1,rang_personne_Q)
                    description = get_description(data1,rang_personne_Q)
                    print(f"{rang_personne} / {len(xxx)-1} - {rang_personne_Q} : {id} : {label}, {description}")
                    description = filtre_description(description)
                    if debug: print("RECHERCHE DES DECORATIONS (ONM ET LH) SUR WIKIDATA...")
                    decoration_obtenue, decoration_date = get_decorations(id)
                    if debug: print("RECHERCHE DES DATES DE NAISSANCE ET DE DECES SUR WIKIDATA...")
                    date_naissance = get_date_naissance(id)
                    date_naissance = filtre_date_naissance(date_naissance,date_decret_ISO_wiki)
                    date_deces = get_date_deces(id)
                    date_deces = filtre_date_deces(date_deces,date_decret_ISO_wiki)
                    if debug: print("INJECTION DES INFOS ET DECORATIONS (ONM ET LH) WIKIDATA DANS LE DECRET...")
                    filedata, offset = injection_personne(filedata,xxx,NOR,date_decret_ISO_wiki,ordre,boutons_simplifies,rang_personne,rang_personne_Q,offset,id,label,date_naissance,date_deces,description,decoration_obtenue,decoration_date)
                    liste_des_id.append(id)
                rang_personne_Q = rang_personne_Q + 1
        print("-------------------------------")
        rang_personne = rang_personne + 1
    return filedata

def construction_index(filedata):
    prefixes = ["M\. ", "Mme ","M\.\&nbsp\;", "Mme\&nbsp\;"]
    xxx = [] #tableau des chaînes de caractères correspondante aux passages du décret concernant chaque personne
    for prefixe in prefixes:
        for m in re.finditer(prefixe, filedata):
            xxx.append(m.start())
    if debug: print(xxx)
    xxx.sort()
    if debug: print(xxx)
    # Pour éviter bug si retour à la ligne manquant dans le décret. ex: M. Malet (Désiré) dans PREX9310861D
    # vérification qu'il y a une forme de retour à la ligne entre chaque personne, sinon on supprime la personne suivante
    xxx = check_retour_a_la_ligne(filedata,xxx)
    return xxx

def check_retour_a_la_ligne(filedata,xxx):
    valeurs_a_suppr = []
    for i in range(len(xxx)-1):
        if debug: print(f"Vérification couple {i}/{i+1} : {xxx[i]}/{xxx[i+1]}")
        if max(filedata[xxx[i]:xxx[i+1]].find("<br>"),filedata[xxx[i]:xxx[i+1]].find("<br/>"),filedata[xxx[i]:xxx[i+1]].find("<p"),filedata[xxx[i]:xxx[i+1]].find("</p>")) == -1:
            print(f"position {xxx[i+1]} supprimée de l'index car pas de retour à la ligne")
            print(f"filedata[{xxx[i]}:{xxx[i+1]}+10]) : {filedata[xxx[i]:xxx[i+1]+10]}")
            #xxx[i+1] = "ko"
            valeurs_a_suppr.append(xxx[i+1])
    if debug: print(f"valeurs_a_suppr : {valeurs_a_suppr}")
    if debug: print(f"xxx avant check_retour_a_la_ligne : {xxx}")
    #xxx = [value for value in xxx if value != "ko"]
    xxx = [value for value in xxx if value not in valeurs_a_suppr]
    if debug: print(f"xxx après check_retour_a_la_ligne : {xxx}")
    return xxx

def get_nom(filedata,xxx,rang_personne,offset,ordre):

    #remplacement des &nbsp; dans la ligne
    ligne = filedata[xxx[rang_personne]+offset:xxx[rang_personne]+offset+get_saut_suivant(filedata,xxx,rang_personne,offset)]
    print(ligne)
    longueur_ligne_avant_remplacement = len(ligne)
    ligne = ligne.replace("&nbsp;"," ")
    print(ligne)
    print(f"avant modif : {filedata[xxx[rang_personne]+offset-10:xxx[rang_personne]+offset+150]}")
    filedata=filedata[:xxx[rang_personne]+offset] + ligne + filedata[xxx[rang_personne]+offset+longueur_ligne_avant_remplacement:]
    print(f"après modif : {filedata[xxx[rang_personne]+offset-10:xxx[rang_personne]+offset+150]}")

    personne_listee = []
    if debug: print(f"{xxx[rang_personne]} + {offset} : {filedata[xxx[rang_personne]+offset:xxx[rang_personne]+offset+5000]}") #105412 : Mme Dupont, née Durant (Jeanne dite Jeannine, Marie, Hélène), dirigeante d'entrep

    if filedata[xxx[rang_personne]+offset:xxx[rang_personne]+offset+4] == "Mme ":
        if debug: print("titre = Mme")
        longueur_titre = 4
    if filedata[xxx[rang_personne]+offset:xxx[rang_personne]+offset+3] == "M. ":
        if debug: print("titre = M.")
        longueur_titre = 3
    if filedata[xxx[rang_personne]+offset:xxx[rang_personne]+offset+9] == "Mme&nbsp;":
        if debug: print("titre = Mme")
        longueur_titre = 9
    if filedata[xxx[rang_personne]+offset:xxx[rang_personne]+offset+5] == "Mme  ":
        if debug: print("titre = Mme")
        longueur_titre = 5
    if filedata[xxx[rang_personne]+offset:xxx[rang_personne]+offset+6] == "Mme   ":
        if debug: print("titre = Mme")
        longueur_titre = 6
    if filedata[xxx[rang_personne]+offset:xxx[rang_personne]+offset+7] == "Mme    ":
        if debug: print("titre = Mme")
        longueur_titre = 7
    if filedata[xxx[rang_personne]+offset:xxx[rang_personne]+offset+8] == "M.&nbsp;":
        if debug: print("titre = M.")
        longueur_titre = 8
    if debug: print(f"longueur_titre = {longueur_titre}")

    if ordre == "LH" or ordre == "ONM":
        ouverture_parenthese = filedata[xxx[rang_personne]+offset:xxx[rang_personne]+offset+5000].find("(")
        fermeture_parenthese = filedata[xxx[rang_personne]+offset:xxx[rang_personne]+offset+5000].find(")")
        prenoms = filedata[xxx[rang_personne]+offset+ouverture_parenthese+1:xxx[rang_personne]+offset+fermeture_parenthese]

        print(f"{rang_personne} / {len(xxx)-1} : prénoms = {prenoms}") #prénoms = Jeanne dite Jeannine, Marie, Hélène
        if prenoms.find(",") == -1: prenom = prenoms
        else:
            prenom = prenoms[0:prenoms.find(",")]
        if prenom.find(" dit ") != -1:
            prenom = prenom[0:prenom.find(" dit ")]
        if prenom.find(" dite ") != -1:
            prenom = prenom[0:prenom.find(" dite ")]
        if debug: print(f"prenom = {prenom}") #prenom = Jeanne

        nom_complet = filedata[xxx[rang_personne]+offset+longueur_titre:xxx[rang_personne]+offset+ouverture_parenthese-1]

    if ordre == "AL":
        prenoms = "Jacqueline"

        print(f"ligne : {filedata[xxx[rang_personne]+offset+longueur_titre:xxx[rang_personne]+offset+150]}")
        fin_nom_de_famille = 0
        while not filedata[xxx[rang_personne]+offset+longueur_titre+fin_nom_de_famille:xxx[rang_personne]+offset+longueur_titre+fin_nom_de_famille+1].islower():
            fin_nom_de_famille += 1
        fin_nom_de_famille -= 2
        nom_complet = filedata[xxx[rang_personne]+offset+longueur_titre:xxx[rang_personne]+offset+longueur_titre+fin_nom_de_famille]
        print(f"nom_complet : **{nom_complet}**")

        double_espace_suivant = get_double_espace_suivant(filedata,xxx,rang_personne,offset,longueur_titre)
        print(f"double_espace_suivant : {double_espace_suivant}")
        prenom_avant_double_espace = filedata[xxx[rang_personne]+offset+longueur_titre+fin_nom_de_famille+1:xxx[rang_personne]+offset+longueur_titre+double_espace_suivant]
        print(f"prenom_avant_double_espace : **{prenom_avant_double_espace}**")

        prenom = prenom_avant_double_espace

    if debug: print(f"nom complet = {nom_complet}")
    print(f"{rang_personne} / {len(xxx)-1} : nom complet = {nom_complet}") #nom complet = Mme Dupont, née Durant
    if nom_complet.find(",") == -1:
        nom = nom_complet
    else:
        nom = nom_complet[0:nom_complet.find(",")]
    if debug: print("nom =", nom) #nom = Dupont
    personne_listee.append(prenom + " " + nom)
    if debug: print(f"personne_listee = {personne_listee[0]}") #personne_listee = Jeanne Dupont
    #Recherche d'autres alias à rechercher sur wikidata
    nom_de_naissance = ""
    if nom_complet.find(", né ") != -1:
        nom_de_naissance = nom_complet[nom_complet.find(", né ")+5:len(nom_complet)]
        if debug: print(f"nom_de_naissance = {nom_de_naissance}")
        personne_listee.append(prenom + " " + nom_de_naissance)
    if nom_complet.find(", née ") != -1:
        nom_de_naissance = nom_complet[nom_complet.find(", née ")+6:len(nom_complet)]
        if debug: print(f"nom_de_naissance = {nom_de_naissance}")
        personne_listee.append(prenom + " " + nom_de_naissance) #Jeanne Durant
    if prenoms.find(" dit ") != -1:
        prenom_d_usage = prenoms[prenoms.find(" dit ")+5:len(prenoms)]
        if debug: print(f"prenom_d_usage = {prenom_d_usage}")
        personne_listee.append(prenom_d_usage + " " + nom)
        if nom_complet.find(", né ") != -1:
            nom_de_naissance = nom_complet[nom_complet.find(", né ")+5:len(nom_complet)]
            if debug: print(f"nom_de_naissance = {nom_de_naissance}")
            personne_listee.append(prenom + " " + nom_de_naissance)
        if nom_complet.find(", née ") != -1:
            nom_de_naissance = nom_complet[nom_complet.find(", née ")+6:len(nom_complet)]
            if debug: print(f"nom_de_naissance = {nom_de_naissance}")
            personne_listee.append(prenom_d_usage + " " + nom_de_naissance)
    if prenoms.find(" dite ") != -1:
        prenom_d_usage = prenoms[prenoms.find(" dite ")+6:len(prenoms)]
        if debug: print(f"prenom_d_usage = {prenom_d_usage}")
        personne_listee.append(prenom_d_usage + " " + nom) #Jeannine Dupont
        if nom_complet.find(", né ") != -1:
            nom_de_naissance = nom_complet[nom_complet.find(", né ")+5:len(nom_complet)]
            if debug: print(f"nom_de_naissance = {nom_de_naissance}")
            personne_listee.append(prenom + " " + nom_de_naissance)
        if nom_complet.find(", née ") != -1:
            nom_de_naissance = nom_complet[nom_complet.find(", née ")+6:len(nom_complet)]
            if debug: print(f"nom_de_naissance = {nom_de_naissance}")
            personne_listee.append(prenom_d_usage + " " + nom_de_naissance) #Jeannine Durant
    return personne_listee

def get_id(data1,rang_personne_Q):
    try:
        id = data1.json()["search"][rang_personne_Q]["id"]
    except KeyError:
        id = "KO"
    except IndexError:
        id = "KO"
    if debug: print(f"id = {id}")
    return id

def get_label(data1,rang_personne_Q):
    try:
        label = data1.json()["search"][rang_personne_Q]["label"]
    except (KeyError, IndexError):
        label = ""
    if debug: print(f"label = {label}")
    return label

def get_description(data1,rang_personne_Q):
    try:
        description = data1.json()["search"][rang_personne_Q]["description"]
    except (KeyError, IndexError):
        description = ""
    if debug: print(f"description = {description}")
    return description

def filtre_description(description):
    if description == "Wikimedia disambiguation page": description = f"<font color=\"red\">Wikimedia disambiguation page</font>"
    if description == "page d'homonymie d'un projet Wikimédia": description = f"<font color=\"red\">page d'homonymie d'un projet Wikimédia</font>"
    return  description

def get_decorations(id):
    params2 = {
        "action" : "wbgetclaims",
        "format" : "json",
        "entity" : id,
        "property" : "P166"
    }
    data2 = requests.get(url, params=params2)
    try:
        award_received_total = len(data2.json()["claims"]["P166"])  # nombre de P166 de la personne
    except KeyError:
        award_received_total = 0
    if debug: print(f"award_received_total = {award_received_total}")
    decoration = 0 # pour balayer les différentes décorations (listées ci-dessous) possibles
    decoration_obtenue = [0] * decoration_total
    decoration_date = [0] * decoration_total
    if award_received_total > 0:
        award_received = 0 # pour balayer les différents P166 de la personne
        while award_received < award_received_total:
            decoration = 0
            while decoration < decoration_total:
                if data2.json()["claims"]["P166"][award_received]["mainsnak"]["datavalue"]["value"]["id"] == decoration_Q[decoration]:
                    decoration_obtenue[decoration] = 1
                    if "qualifiers" in data2.json()["claims"]["P166"][award_received]:
                        if "P585" in data2.json()["claims"]["P166"][award_received]["qualifiers"]:
                            try:
                                decoration_date[decoration] = data2.json()["claims"]["P166"][award_received]["qualifiers"]["P585"][0]["datavalue"]["value"]["time"]
                            except KeyError:
                                decoration_date[decoration] = ""
                decoration = decoration + 1
            award_received = award_received + 1
    if debug: print(decoration_nom)
    if debug: print(decoration_obtenue)
    if debug: print(decoration_date)
    return decoration_obtenue, decoration_date

def get_date_naissance(id):
    params3 = {
        "action" : "wbgetclaims",
        "format" : "json",
        "entity" : id,
        "property" : "P569"
    }
    data3 = requests.get(url, params=params3)
    try:
        date_naissance = data3.json()["claims"]["P569"][0]["mainsnak"]["datavalue"]["value"]["time"][1:5]
    except KeyError:
        date_naissance = ""
    if debug: print(f"date_naissance = {date_naissance}")
    return date_naissance

def filtre_date_naissance(date_naissance,date_decret_ISO_wiki):
    if date_naissance == "": return ""
    if int(date_naissance) < int(date_decret_ISO_wiki[1:5]) - 125: return f"<font color=\"red\">{date_naissance}</font>"
    if int(date_naissance) > int(date_decret_ISO_wiki[1:5]) - 18: return f"<font color=\"red\">{date_naissance}</font>"
    if int(date_naissance) > int(date_decret_ISO_wiki[1:5]) - 28: return f"<font color=\"orange\">{date_naissance}</font>"
    return date_naissance

def get_date_deces(id):
    params4 = {
        "action" : "wbgetclaims",
        "format" : "json",
        "entity" : id,
        "property" : "P570"
    }
    data4 = requests.get(url, params=params4)
    try:
        date_deces = data4.json()["claims"]["P570"][0]["mainsnak"]["datavalue"]["value"]["time"][1:5]
    except KeyError:
        date_deces = ""
    if debug: print(f"date_deces = {date_deces}")
    return date_deces

def filtre_date_deces(date_deces,date_decret_ISO_wiki):
    if date_deces == "": return ""
    if int(date_deces) < int(date_decret_ISO_wiki[1:5]) - 2: return f"<font color=\"red\">{date_deces}</font>"
    if int(date_deces) < int(date_decret_ISO_wiki[1:5]): return f"<font color=\"orange\">{date_deces}</font>"
    return date_deces

def get_saut_suivant(filedata,xxx,rang_personne,offset):
    if debug: print(f"{xxx[rang_personne]} + (offset) {offset} : {filedata[xxx[rang_personne]+offset:xxx[rang_personne]+offset+5000]}")
    #recherche du saut suivant
    br_suivant = filedata[xxx[rang_personne]+offset:xxx[rang_personne]+offset+5000].find("<br>")
    if br_suivant == -1: br_suivant = 10000
    brslash_suivant = filedata[xxx[rang_personne]+offset:xxx[rang_personne]+offset+5000].find("<br/>")
    if brslash_suivant == -1: brslash_suivant = 10000
    p_suivant = filedata[xxx[rang_personne]+offset:xxx[rang_personne]+offset+5000].find("</p>")
    if p_suivant == -1: p_suivant = 10000
    saut_suivant = min(br_suivant,brslash_suivant,p_suivant)
    if debug: print(f"saut_suivant : {saut_suivant}")
    return saut_suivant

def get_double_espace_suivant(filedata,xxx,rang_personne,offset,longueur_titre): #longueur_titre prise en compte
    if debug: print(f"{xxx[rang_personne]} + (offset) {offset} : {filedata[xxx[rang_personne]+offset:xxx[rang_personne]+offset+5000]}")
    #recherche du double espace suivant
    double_espace_suivant = filedata[xxx[rang_personne]+offset+longueur_titre:xxx[rang_personne]+offset+5000].find("  ")
    if double_espace_suivant == -1: double_espace_suivant = 10000
    if debug: print(f"double_espace_suivant : {double_espace_suivant}")
    return double_espace_suivant

def injection_personne(filedata,xxx,NOR,date_decret_ISO_wiki,ordre,boutons_simplifies,rang_personne,rang_personne_Q,offset,id,label,date_naissance,date_deces,description,decoration_obtenue,decoration_date):
    saut_suivant = get_saut_suivant(filedata,xxx,rang_personne,offset)    #position d'injection
    if debug: print("début injection")
    injection_index = xxx[rang_personne] + offset + saut_suivant
    if debug: print(f"injection_index = {injection_index}")
    if debug: print(f"(injection_index) {injection_index} : {filedata[injection_index:injection_index+1000]}")
    #ajout de la personne trouvée sur wikidata
    injection_str = "<style type=\"text/css\"> form, table {display:inline;margin:0px;padding:0px;}</style><br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" + str(rang_personne) + "/" + str(rang_personne_Q) + \
        " : <b><a href=\"https://www.wikidata.org/wiki/" + id + "\">" + id + " : " + \
    label + " (" + date_naissance + "-" + date_deces + "), " + description + "</b></a>"
    #ajout des boutons pour QuickStatements
    if debug: print(f"injection_index avant recherche du grade en cours : {injection_index}")
    grade_en_cours = get_grade_en_cours(filedata[0:injection_index],ordre)
    if boutons_simplifies == True:
        QS_range_bouton_decoration = [grade_en_cours]
    if boutons_simplifies == False:
        if ordre == "LH": QS_range_bouton_decoration = [10,9,8,7,6]
        if ordre == "ONM": QS_range_bouton_decoration = [4,3,2,1,0]
        if ordre == "AL": QS_range_bouton_decoration = [14,13,12]
    for QS_compteur_bouton_decoration in QS_range_bouton_decoration:
        bold1 = ""
        bold2 = ""
        style_bolded = ""
        if QS_compteur_bouton_decoration == grade_en_cours:
            if ordre == "ONM" or ordre == "LH":
                bold1 = "<b>"
                bold2 = "</b>"
            if ordre == "AL":
                style_bolded = """class="bolded" """
        injection_str = injection_str + bold1 + " <form onclick=\"QS_ajout_ligne('" + id + "|P166|" + decoration_Q[QS_compteur_bouton_decoration] + "|P585|" + date_decret_ISO_wiki + "|S464|','" + NOR + "','" + id + decoration_Q[QS_compteur_bouton_decoration] + \
            "')\"><input type=\"button\"" + style_bolded + " id=\"" + id + decoration_Q[QS_compteur_bouton_decoration] + "\" value=\"" + decoration_nom[QS_compteur_bouton_decoration] + "\"></form>" + bold2
    #ajout des éventuelles décorations existantes
    for k in [10,9,8,7,6,11,4,3,2,1,0,5,14,13,12,15]: #pour affichage des plus hautes décorations en premier
        if decoration_obtenue[k] == 1:
            injection_str = injection_str + "<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<img src=\"" + decoration_img[k] + "\" width=\"50\"> &nbsp;" + "<a href=\"https://www.wikidata.org/wiki/" + id + "#P166\">" + decoration_nom[k] + "</a>"
            if decoration_date[k] != 0:
                date_ISO_reformatee = decoration_date[k][1:] # pour passer de +2008-09-12T00:00:00Z à 2008-09-12T00:00:00Z
                date_ISO_reformatee = date_ISO_reformatee[:10] # pour passer de 2008-09-12T00:00:00 à 2008-09-12
                injection_str = injection_str + " du " + date_ISO_reformatee
    #injection dans filedata
    if debug: print(f"injection_str = {injection_str}")
    filedata = filedata[:injection_index] + injection_str + filedata[injection_index:]
    offset = offset + len(injection_str)
    if debug: print(f"offset = {offset}")
    if debug: print("fin injection")
    return filedata, offset

def get_grade_en_cours(texte,ordre): # sert juste à mettre en gras le bouton concerné
    if ordre == "LH": #[10,9,8,7,6]
        rangs_precedents = {
            10 : max(texte.rfind("A la dignité de grand'croix"),texte.rfind("A la dignité de grand’croix")),
            9 : texte.rfind("A la dignité de grand officier"),
            8 : texte.rfind("Au grade de commandeur"),
            7 : max(texte.rfind("Au grade d'officier"),texte.rfind("Au grade d’officier")),
            6 : texte.rfind("Au grade de chevalier")
        }
        if debug: print(rangs_precedents)
        max_key = max(rangs_precedents, key=rangs_precedents.get)
        if debug: print(max_key)
        return max_key
    if ordre == "ONM": #[4,3,2,1,0]
        rangs_precedents = {
            4 : max(texte.rfind("A la dignité de grand'croix"),texte.rfind("A la dignité de grand’croix")),
            3 : texte.rfind("A la dignité de grand officier"),
            2 : texte.rfind("Au grade de commandeur"),
            1 : max(texte.rfind("Au grade d'officier"),texte.rfind("Au grade d’officier")),
            0 : texte.rfind("Au grade de chevalier")
        }
        if debug: print(rangs_precedents)
        max_key = max(rangs_precedents, key=rangs_precedents.get)
        if debug: print(max_key)
        return max_key
    if ordre == "AL": #[14,13,12]
        rangs_precedents = {
            14 : texte.rfind("au grade de commandeur"),
            13 : max(texte.rfind("au grade d'officier"),texte.rfind("au grade d’officier")),
            12 : texte.rfind("au grade de chevalier")
        }
        if debug: print(rangs_precedents)
        max_key = max(rangs_precedents, key=rangs_precedents.get)
        if debug: print(max_key)
        return max_key

def QS_ajout_script(filedata):
    filedata = filedata[:filedata.find("</html>")] + "<script language=\"Javascript\"> \
        function QS_ajout_ligne(champ1,champ2,ID_bouton) { \
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
    return filedata

def suppression_debut(filedata,ordre):
    if ordre != "AL":
        return filedata
    #supprime tout avant le "<p class="excerpt">"
    position_p = filedata.rfind("""<p class="excerpt">""")
    filedata = filedata[position_p:]
    #supprime tout après le 1er "</div>" après "Bulletin officiel" (à la fin de l'arrêté)
    position_bulletin = filedata.rfind("""Bulletin officiel""")
    position_div = filedata[position_bulletin:].find("""</div>""")
    filedata = filedata[:position_bulletin+position_div+6]
    #mise en forme
    filedata = """<html><head><link rel="stylesheet" href="style.css"></head>""" + filedata + """</html>"""
    return filedata

def suppression_p(filedata,ordre):
    #sans cette fonction, il y a un retour à la ligne non souhaité avant le 1er bouton de chaque grade
    xxxgrade = [] #tableau des chaînes de caractères correspondantes aux débuts de chaque grade
    if ordre == "LH" or ordre == "ONM":
        for m in re.finditer("<b>Au grade d", filedata):
            xxxgrade.append(m.start())
        for m in re.finditer("<b>A la dignité de", filedata):
            xxxgrade.append(m.start())
        xxxgrade.sort()
    if ordre == "AL":
        for m in re.finditer("<b>au grade d", filedata):
            xxxgrade.append(m.start())
    print(xxxgrade)
    if ordre == "AL":
        filedata = filedata.replace("""<p style="text-align:left;">""","<p>")
    offset = 0
    for paragraphe in xxxgrade:
        emplacement_p = filedata[paragraphe-offset:].find("<p>") #position dans l'extrait
        emplacement_p = emplacement_p + paragraphe - offset #position globale
        print(f"emplacement_p-5 : {filedata[emplacement_p-5:emplacement_p+30]}")
        filedata = filedata[:emplacement_p] + filedata[emplacement_p+3:]
        print(f"emplacement_p-5 : {filedata[emplacement_p-5:emplacement_p+30]}")
        offset = offset + 3
    return filedata

def main():

    print("OUVERTURE DU FICHIER \"in.html\"...")
    try:
        with open("in.html", 'r') as file:
            filedata = file.read()
    except IOError:
        raise SystemExit("Erreur: Enregistrez une page de décret depuis Légifrance sous le nom \"in.html\" dans le dossier du programme.")

    print("RECHERCHE DES INFOS DE BASE DU DECRET...")
    NOR = definition_NOR(filedata)
    date_decret_ISO_wiki = definition_date_decret_ISO_wiki(filedata)
    ordre = definition_ordre(filedata)
    boutons_simplifies = definition_boutons_simplifies()

    print("MISE EN FORME DES TITRES DU DECRET...")
    filedata = mise_en_forme_titres(filedata, ordre)

    print("RECUPERATION DES LIGNES ASSOCIEES A CHAQUE PERSONNE...")
    print("==================================================")
    filedata = traitement(filedata, NOR, date_decret_ISO_wiki, ordre, boutons_simplifies)

    print("NETTOYAGE...")
    filedata = suppression_debut(filedata,ordre)
    filedata = suppression_p(filedata,ordre)

    print("AJOUT DU CHAMP QUICKSTATEMENTS A LA FIN DU FICHIER...")
    filedata = QS_ajout_script(filedata)

    print("ENREGISTREMENT DU FICHIER \"out.html\"...")
    with open("out.html", 'w') as file:
        file.write(filedata)

    print("==================================================")
    print("TRAITEMENT TERMINE. OUVREZ LE FICHIER \"out.html\".")

if __name__ == "__main__":
    main()
