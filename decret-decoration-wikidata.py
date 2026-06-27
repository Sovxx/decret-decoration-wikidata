#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# https://github.com/Sovxx/decret-decoration-wikidata
# Version modifiée : lecture depuis in.txt (texte copié depuis Légifrance via le bouton "Texte copié")
# Ordres gérés : LH (Légion d'Honneur) et ONM (Ordre National du Mérite)

#python : supérieure ou égale à v3.6

import requests
import re

debug = False

url = "https://www.wikidata.org/w/api.php"

decoration_nom = ["Chevalier ONM", "Officier ONM", "Commandeur ONM", "Grand Officier ONM", "Grand'Croix ONM", "ONM", \
                  "Chevalier LH",  "Officier LH",  "Commandeur LH",  "Grand Officier LH",  "Grand'Croix LH",  "LH"]

decoration_total = len(decoration_nom)

decoration_Q = ["Q13422138", "Q13422140", "Q13422141", "Q13422142", "Q13422143", "Q652962", \
                "Q10855271", "Q10855195", "Q10855212", "Q10855216", "Q10855226", "Q163700"]

decoration_img = [
    "https://upload.wikimedia.org/wikipedia/commons/thumb/9/92/Ordre_national_du_Merite_Chevalier_ribbon.svg/218px-Ordre_national_du_Merite_Chevalier_ribbon.svg.png",
    "https://upload.wikimedia.org/wikipedia/commons/thumb/5/52/Ordre_national_du_Merite_Officier_ribbon.svg/218px-Ordre_national_du_Merite_Officier_ribbon.svg.png",
    "https://upload.wikimedia.org/wikipedia/commons/thumb/8/82/Ordre_national_du_Merite_Commandeur_ribbon.svg/218px-Ordre_national_du_Merite_Commandeur_ribbon.svg.png",
    "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b2/Ordre_national_du_Merite_GO_ribbon.svg/218px-Ordre_national_du_Merite_GO_ribbon.svg.png",
    "https://upload.wikimedia.org/wikipedia/commons/thumb/8/82/Ordre_national_du_Merite_GC_ribbon.svg/218px-Ordre_national_du_Merite_GC_ribbon.svg.png",
    "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cc/Ordre_national_du_merite_chevalier_FRANCE.jpg/86px-Ordre_national_du_merite_chevalier_FRANCE.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e6/Legion_Honneur_Chevalier_ribbon.svg/218px-Legion_Honneur_Chevalier_ribbon.svg.png",
    "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Legion_Honneur_Officier_ribbon.svg/218px-Legion_Honneur_Officier_ribbon.svg.png",
    "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ef/Legion_Honneur_Commandeur_ribbon.svg/218px-Legion_Honneur_Commandeur_ribbon.svg.png",
    "https://upload.wikimedia.org/wikipedia/commons/thumb/a/af/Legion_Honneur_GO_ribbon.svg/218px-Legion_Honneur_GO_ribbon.svg.png",
    "https://upload.wikimedia.org/wikipedia/commons/thumb/b/ba/Legion_Honneur_GC_ribbon.svg/218px-Legion_Honneur_GC_ribbon.svg.png",
    "https://upload.wikimedia.org/wikipedia/commons/8/81/De_la_legion_d_honneur_Recto.png",
]


# ---------------------------------------------------------------------------
# Conversion du texte brut (in.txt) en HTML interne de travail
# ---------------------------------------------------------------------------

def txt_to_html(texte_brut):
    """
    Convertit le texte copié depuis Légifrance (bouton "Texte copié") en HTML
    interne compatible avec le reste du programme.

    Le texte brut ressemble à :
        Décret du 14 mai 2024 portant promotion et nomination dans l'ordre national...
        NOR : PREX2409876D
        ...
        Au grade de chevalier
        M. Dupont (Jean, Pierre), ingénieur principal des mines...
        Mme Durant, née Martin (Marie, Hélène), directrice...
        Au grade d'officier
        M. Leroy (Jacques), ...
    """
    lignes = texte_brut.splitlines()
    html_lignes = []
    for ligne in lignes:
        ligne_echappee = (ligne
                          .replace("&", "&amp;")
                          .replace("<", "&lt;")
                          .replace(">", "&gt;"))
        html_lignes.append(ligne_echappee + "<br>")
    return "\n".join(html_lignes)


# ---------------------------------------------------------------------------
# Extraction des méta-données du décret
# ---------------------------------------------------------------------------

def definition_NOR(filedata):
    NOR = ""
    # Cherche "NOR : XXXXXXXXXX" (avec espace normal ou espace insécable)
    for sep in ["NOR : ", "NOR :\u00a0", "NOR :"]:
        pos = filedata.find(sep)
        if pos != -1:
            candidat = filedata[pos + len(sep):pos + len(sep) + 12].strip()
            if " " not in candidat and len(candidat) >= 10:
                NOR = candidat
                break

    print(f"Identifiant NOR du décret ou de l'arrêté ? Par défaut (reconnu dans in.txt) : {NOR}")
    NOR = input() or NOR
    print(f"NOR = {NOR}")
    return NOR


def check_date(date_a_checker):
    if len(date_a_checker) != 10:
        return "date KO ; len != 10"
    try:
        if int(date_a_checker[0:4]) < 1800: return "date KO ; AAAA < 1800"
        if int(date_a_checker[0:4]) > 2100: return "date KO ; AAAA > 2100"
        if int(date_a_checker[5:7]) < 1:    return "date KO ; mois non valide"
        if int(date_a_checker[5:7]) > 12:   return "date KO ; mois non valide"
    except (ValueError, TypeError):
        return "date KO ; erreur de type"
    return "date valide"


def definition_date_decret_ISO_wiki(filedata):
    date_decret = "[non trouvé]"

    for verbe in ["portant nomination", "portant promotion", "portant élévation"]:
        for intro in ["Décret du ", "Arrêté du "]:
            if filedata.find(intro) != -1 and filedata.find(verbe) != -1:
                date_decret = filedata[filedata.find(intro) + len(intro):filedata.find(verbe) - 1]
                break
        if date_decret != "[non trouvé]":
            break

    if debug: print(f"date_decret = {date_decret}")

    date_decret_ISO = "[non trouvé]"
    if date_decret != "[non trouvé]":
        annee_decret = date_decret[len(date_decret) - 4:]
        jour_decret = date_decret[:date_decret.find(" ")]
        if jour_decret == "1er": jour_decret = 1
        if len(str(jour_decret)) == 1: jour_decret = "0" + str(jour_decret)
        mois_decret = date_decret[date_decret.find(" ") + 1:len(date_decret) - 5]

        mois_map = {
            "janvier": "01", "février": "02", "mars": "03", "avril": "04",
            "mai": "05", "juin": "06", "juillet": "07", "août": "08",
            "septembre": "09", "octobre": "10", "novembre": "11", "décembre": "12"
        }
        mois_key = mois_decret.lower()
        if mois_key in mois_map:
            date_decret_ISO = f"{annee_decret}-{mois_map[mois_key]}-{jour_decret}"
        else:
            date_decret_ISO = "[format non reconnu]"

    if debug: print(f"date_decret_ISO = {date_decret_ISO}")

    print(f"Date du décret au format AAAA-MM-JJ ? Par défaut (reconnu dans in.txt) : {date_decret_ISO}")
    date_decret_ISO = input() or date_decret_ISO
    print(f"date_decret_ISO = {date_decret_ISO}")

    if check_date(date_decret_ISO) != "date valide":
        raise SystemExit("Erreur : date du décret invalide, pas au format AAAA-MM-JJ ; réessayez en la tapant manuellement")

    date_decret_ISO_wiki = "+" + date_decret_ISO + "T00:00:00Z/11"
    if debug: print(f"date_decret_ISO_wiki = {date_decret_ISO_wiki}")
    return date_decret_ISO_wiki


def definition_ordre(filedata):
    ordre = "[non trouvé]"

    # Détection LH
    for marqueur_lh in [
        "Grande chancellerie de la Légion d\u2019honneur",
        "Grande chancellerie de la Légion d'honneur",
        "exécution par le grand chancelier de l'ordre national de la Légion d'honneur",
        "exécution par le grand chancelier de la Légion d'honneur",
        "portant élévation dans l'ordre national de la Légion d'honneur",
        "LÉGION D'HONNEUR",
        "LEGION D'HONNEUR",
    ]:
        if filedata.find(marqueur_lh) != -1:
            ordre = "LH"
            break

    # Détection ONM
    for marqueur_onm in [
        "Chancellerie de l\u2019ordre national du Mérite",
        "Chancellerie de l'ordre national du Mérite",
        "exécution par le chancelier de l'ordre national du Mérite",
        "ORDRE NATIONAL DU MERITE",
        "ORDRE NATIONAL DU MÉRITE",
        "sont élevés dans l'ordre national du Mérite",
        "est élevé dans l'ordre national du Mérite",
    ]:
        if filedata.find(marqueur_onm) != -1:
            ordre = "ONM"
            break

    print(f"Ordre ? LH ou ONM ? Par défaut (reconnu dans in.txt) : {ordre}")
    ordre = input() or ordre
    print(f"ordre = {ordre}")

    if ordre in {"LH", "ONM"}:
        return ordre
    raise SystemExit("Erreur : ordre doit être LH (Légion d'Honneur) ou ONM (Ordre National du Mérite)")


def definition_boutons_simplifies():
    print("Boutons simplifiés (O/N) ? Par défaut et recommandé : O")
    boutons_simplifies = input() or "O"
    if boutons_simplifies in {"O", "o", "Y", "y"}:
        print("boutons_simplifies = True")
        return True
    if boutons_simplifies in {"N", "n"}:
        print("boutons_simplifies = False")
        return False
    raise SystemExit("Erreur : doit être O ou N")


# ---------------------------------------------------------------------------
# Mise en forme des titres de grade
# ---------------------------------------------------------------------------

def mise_en_forme_titres(filedata, ordre):
    img_idx = {
        "ONM": {"chevalier": 0, "officier": 1, "commandeur": 2, "grand_officier": 3, "grand_croix": 4},
        "LH":  {"chevalier": 6, "officier": 7, "commandeur": 8, "grand_officier": 9, "grand_croix": 10},
    }
    i = img_idx[ordre]
    style = """<style type="text/css"> form, table {display:inline;margin:0px;padding:0px;}</style>"""

    def remplace(texte, cherche, idx):
        remplacement = f'<b>{cherche}</b> <img src="{decoration_img[idx]}" width="150">{style}'
        return texte.replace(cherche, remplacement)

    filedata = remplace(filedata, "Au grade de chevalier",             i["chevalier"])
    filedata = remplace(filedata, "Au grade d\u2019officier",          i["officier"])
    filedata = remplace(filedata, "Au grade d'officier",               i["officier"])
    filedata = remplace(filedata, "Au grade de commandeur",            i["commandeur"])
    filedata = remplace(filedata, "A la dignité de grand officier",    i["grand_officier"])
    filedata = remplace(filedata, "A la dignité de grand\u2019croix",  i["grand_croix"])
    filedata = remplace(filedata, "A la dignité de grand'croix",       i["grand_croix"])

    return filedata


# ---------------------------------------------------------------------------
# Construction de l'index des personnes
# ---------------------------------------------------------------------------

def construction_index(filedata):
    """
    Dans le texte brut converti en HTML, les personnes commencent par :
    M. , Mme , Mlle
    """
    prefixes = [r"M\. ", "Mme ", "Mlle "]
    xxx = []
    for prefixe in prefixes:
        for m in re.finditer(prefixe, filedata):
            xxx.append(m.start())
    xxx.sort()
    xxx = check_retour_a_la_ligne(filedata, xxx)
    return xxx


def check_retour_a_la_ligne(filedata, xxx):
    valeurs_a_suppr = []
    for i in range(len(xxx) - 1):
        if debug: print(f"Vérification couple {i}/{i+1} : {xxx[i]}/{xxx[i+1]}")
        extrait = filedata[xxx[i]:xxx[i+1]]
        if max(extrait.find("<br>"), extrait.find("\n")) == -1:
            print(f"position {xxx[i+1]} supprimée de l'index car pas de retour à la ligne")
            valeurs_a_suppr.append(xxx[i+1])
    xxx = [v for v in xxx if v not in valeurs_a_suppr]
    print("==================================================")
    return xxx


# ---------------------------------------------------------------------------
# Extraction du nom / prénom
# ---------------------------------------------------------------------------

def get_nom(filedata, xxx, rang_personne, offset, ordre):
    ligne = filedata[xxx[rang_personne] + offset:
                     xxx[rang_personne] + offset + get_saut_suivant(filedata, xxx, rang_personne, offset)]
    if debug: print(f"ligne : {ligne}")
    print(f"{rang_personne} / {len(xxx)-1} : {ligne}")

    personne_listee = []

    # Longueur du titre de civilité
    longueur_titre = 0
    debut = filedata[xxx[rang_personne] + offset:xxx[rang_personne] + offset + 10]
    if debut.startswith("Mme "):      longueur_titre = 4
    elif debut.startswith("Mme\u00a0"): longueur_titre = 4
    elif debut.startswith("M. "):     longueur_titre = 3
    elif debut.startswith("Mlle "):   longueur_titre = 5

    ouverture_parenthese = filedata[xxx[rang_personne] + offset:xxx[rang_personne] + offset + 1000].find("(")
    fermeture_parenthese = filedata[xxx[rang_personne] + offset:xxx[rang_personne] + offset + 1000].find(")")

    if ouverture_parenthese == -1 or fermeture_parenthese == -1:
        # Pas de parenthèse : on prend le premier champ avant la virgule
        personne_listee.append(ligne[longueur_titre:].split(",")[0].strip())
        return personne_listee

    prenoms = filedata[xxx[rang_personne] + offset + ouverture_parenthese + 1:
                       xxx[rang_personne] + offset + fermeture_parenthese]
    if debug: print(f"prénoms = {prenoms}")

    prenom = prenoms.split(",")[0].strip() if "," in prenoms else prenoms.strip()
    if " dit "  in prenom: prenom = prenom[:prenom.find(" dit ")]
    if " dite " in prenom: prenom = prenom[:prenom.find(" dite ")]
    if debug: print(f"prenom = {prenom}")

    nom_complet = filedata[xxx[rang_personne] + offset + longueur_titre:
                           xxx[rang_personne] + offset + ouverture_parenthese - 1].strip()
    if debug: print(f"nom_complet = {nom_complet}")

    nom = nom_complet.split(",")[0].strip() if "," in nom_complet else nom_complet.strip()
    if debug: print(f"nom = {nom}")

    personne_listee.append(prenom + " " + nom)

    # Alias supplémentaires (nom de naissance, prénom d'usage)
    nom_de_naissance = ""
    for marqueur in [", né ", ", née "]:
        if marqueur in nom_complet:
            nom_de_naissance = nom_complet[nom_complet.find(marqueur) + len(marqueur):]
            personne_listee.append(prenom + " " + nom_de_naissance)
            break

    for marqueur_dit, longueur in [(" dit ", 5), (" dite ", 6)]:
        if marqueur_dit in prenoms:
            prenom_d_usage = prenoms[prenoms.find(marqueur_dit) + longueur:]
            prenom_d_usage = prenom_d_usage.split(",")[0].strip()
            personne_listee.append(prenom_d_usage + " " + nom)
            if nom_de_naissance:
                personne_listee.append(prenom_d_usage + " " + nom_de_naissance)
            break

    return personne_listee


# ---------------------------------------------------------------------------
# Wikidata
# ---------------------------------------------------------------------------

def get_id(data1, rang_personne_Q):
    try:
        return data1.json()["search"][rang_personne_Q]["id"]
    except (KeyError, IndexError):
        return "KO"


def get_label(data1, rang_personne_Q):
    try:
        return data1.json()["search"][rang_personne_Q]["label"]
    except (KeyError, IndexError):
        return ""


def get_description(data1, rang_personne_Q):
    try:
        return data1.json()["search"][rang_personne_Q]["description"]
    except (KeyError, IndexError):
        return ""


def filtre_description(description):
    if description in ("Wikimedia disambiguation page",
                       "page d'homonymie d'un projet Wikimédia"):
        description = f'<font color="red">{description}</font>'
    return description


def get_decorations(id):
    params2 = {
        "action": "wbgetclaims",
        "format": "json",
        "entity": id,
        "property": "P166"
    }
    data2 = requests.get(url, params=params2)
    try:
        award_received_total = len(data2.json()["claims"]["P166"])
    except KeyError:
        award_received_total = 0

    decoration_obtenue = [0] * decoration_total
    decoration_date    = [0] * decoration_total

    for award_received in range(award_received_total):
        for decoration in range(decoration_total):
            try:
                val = data2.json()["claims"]["P166"][award_received]["mainsnak"]["datavalue"]["value"]["id"]
            except KeyError:
                continue
            if val == decoration_Q[decoration]:
                decoration_obtenue[decoration] = 1
                try:
                    qualifiers = data2.json()["claims"]["P166"][award_received].get("qualifiers", {})
                    if "P585" in qualifiers:
                        decoration_date[decoration] = qualifiers["P585"][0]["datavalue"]["value"]["time"]
                except KeyError:
                    pass

    return decoration_obtenue, decoration_date


def get_date_naissance(id):
    params3 = {"action": "wbgetclaims", "format": "json", "entity": id, "property": "P569"}
    data3 = requests.get(url, params=params3)
    try:
        return data3.json()["claims"]["P569"][0]["mainsnak"]["datavalue"]["value"]["time"][1:5]
    except KeyError:
        return ""


def filtre_date_naissance(date_naissance, date_decret_ISO_wiki):
    if date_naissance == "": return ""
    annee_decret = int(date_decret_ISO_wiki[1:5])
    annee = int(date_naissance)
    if annee < annee_decret - 125: return f'<font color="red">{date_naissance}</font>'
    if annee > annee_decret - 18:  return f'<font color="red">{date_naissance}</font>'
    if annee > annee_decret - 28:  return f'<font color="orange">{date_naissance}</font>'
    return date_naissance


def get_date_deces(id):
    params4 = {"action": "wbgetclaims", "format": "json", "entity": id, "property": "P570"}
    data4 = requests.get(url, params=params4)
    try:
        return data4.json()["claims"]["P570"][0]["mainsnak"]["datavalue"]["value"]["time"][1:5]
    except KeyError:
        return ""


def filtre_date_deces(date_deces, date_decret_ISO_wiki):
    if date_deces == "": return ""
    annee_decret = int(date_decret_ISO_wiki[1:5])
    annee = int(date_deces)
    if annee < annee_decret - 2: return f'<font color="red">{date_deces}</font>'
    if annee < annee_decret:     return f'<font color="orange">{date_deces}</font>'
    return date_deces


# ---------------------------------------------------------------------------
# Navigation dans le texte
# ---------------------------------------------------------------------------

def get_saut_suivant(filedata, xxx, rang_personne, offset):
    zone = filedata[xxx[rang_personne] + offset:xxx[rang_personne] + offset + 5000]
    candidats = [zone.find("<br>"), zone.find("\n")]
    candidats = [c for c in candidats if c != -1]
    return min(candidats) if candidats else 5000


def get_grade_en_cours(texte, ordre):
    if ordre == "LH":
        rangs = {
            10: max(texte.rfind("A la dignité de grand\u2019croix"), texte.rfind("A la dignité de grand'croix")),
            9:  texte.rfind("A la dignité de grand officier"),
            8:  texte.rfind("Au grade de commandeur"),
            7:  max(texte.rfind("Au grade d\u2019officier"), texte.rfind("Au grade d'officier")),
            6:  texte.rfind("Au grade de chevalier"),
        }
    else:  # ONM
        rangs = {
            4: max(texte.rfind("A la dignité de grand\u2019croix"), texte.rfind("A la dignité de grand'croix")),
            3: texte.rfind("A la dignité de grand officier"),
            2: texte.rfind("Au grade de commandeur"),
            1: max(texte.rfind("Au grade d\u2019officier"), texte.rfind("Au grade d'officier")),
            0: texte.rfind("Au grade de chevalier"),
        }
    return max(rangs, key=rangs.get)


# ---------------------------------------------------------------------------
# Injection des infos Wikidata dans le fichier
# ---------------------------------------------------------------------------

def injection_personne(filedata, xxx, NOR, date_decret_ISO_wiki, ordre, boutons_simplifies,
                        rang_personne, rang_personne_Q, offset,
                        id, label, date_naissance, date_deces, description,
                        decoration_obtenue, decoration_date):

    saut_suivant = get_saut_suivant(filedata, xxx, rang_personne, offset)
    injection_index = xxx[rang_personne] + offset + saut_suivant

    injection_str = (
        '<style type="text/css"> form, table {display:inline;margin:0px;padding:0px;}</style>'
        "<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
        + str(rang_personne) + "/" + str(rang_personne_Q)
        + ' : <b><a href="https://www.wikidata.org/wiki/' + id + '" target="_blank">'
        + id + " : " + label
        + " (" + date_naissance + "-" + date_deces + "), "
        + description + "</b></a>"
    )

    grade_en_cours = get_grade_en_cours(filedata[0:injection_index], ordre)

    if boutons_simplifies:
        QS_range = [grade_en_cours]
    else:
        QS_range = [10, 9, 8, 7, 6] if ordre == "LH" else [4, 3, 2, 1, 0]

    for idx in QS_range:
        bold1 = "<b>" if idx == grade_en_cours else ""
        bold2 = "</b>" if idx == grade_en_cours else ""
        injection_str += (
            bold1
            + " <form onclick=\"QS_ajout_ligne('"
            + id + "|P166|" + decoration_Q[idx] + "|P585|" + date_decret_ISO_wiki
            + "|S464|','" + NOR + "','" + id + decoration_Q[idx] + "')\"><input type=\"button\" id=\""
            + id + decoration_Q[idx] + "\" value=\"" + decoration_nom[idx] + "\"></form>"
            + bold2
        )

    # Décorations existantes (LH et ONM uniquement)
    for k in [10, 9, 8, 7, 6, 11, 4, 3, 2, 1, 0, 5]:
        if decoration_obtenue[k] == 1:
            injection_str += (
                '<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<img src="' + decoration_img[k] + '" width="50"> &nbsp;'
                '<a href="https://www.wikidata.org/wiki/' + id + '#P166" target="_blank">'
                + decoration_nom[k] + "</a>"
            )
            if decoration_date[k] != 0:
                date_reformatee = decoration_date[k][1:11]  # +2008-09-12T... → 2008-09-12
                injection_str += " du " + date_reformatee

    filedata = filedata[:injection_index] + injection_str + filedata[injection_index:]
    offset += len(injection_str)
    return filedata, offset


# ---------------------------------------------------------------------------
# Traitement principal (boucle sur les personnes)
# ---------------------------------------------------------------------------

def traitement(filedata, NOR, date_decret_ISO_wiki, ordre, boutons_simplifies):
    xxx = construction_index(filedata)
    rang_personne = 0
    offset = 0

    while rang_personne < len(xxx):
        if debug: print(f"rang_personne = {rang_personne}")
        personne_listee = get_nom(filedata, xxx, rang_personne, offset, ordre)
        liste_des_id = []

        for alias in personne_listee:
            print(f"{rang_personne} / {len(xxx)-1} : *****{alias}*****")
            params1 = {
                "action": "wbsearchentities",
                "language": "fr",
                "format": "json",
                "search": alias
            }
            data1 = requests.get(url, params=params1)
            rang_personne_Q = 0
            id = ""
            while id != "KO":
                id = get_id(data1, rang_personne_Q)
                if id != "KO" and id not in liste_des_id:
                    label       = get_label(data1, rang_personne_Q)
                    description = filtre_description(get_description(data1, rang_personne_Q))
                    print(f"{rang_personne} / {len(xxx)-1} - {rang_personne_Q} : {id} : {label}, {description}")

                    decoration_obtenue, decoration_date = get_decorations(id)
                    date_naissance = filtre_date_naissance(get_date_naissance(id), date_decret_ISO_wiki)
                    date_deces     = filtre_date_deces(get_date_deces(id), date_decret_ISO_wiki)

                    filedata, offset = injection_personne(
                        filedata, xxx, NOR, date_decret_ISO_wiki, ordre, boutons_simplifies,
                        rang_personne, rang_personne_Q, offset,
                        id, label, date_naissance, date_deces, description,
                        decoration_obtenue, decoration_date
                    )
                    liste_des_id.append(id)
                rang_personne_Q += 1

        print("-------------------------------")
        rang_personne += 1

    return filedata


# ---------------------------------------------------------------------------
# Post-traitement du HTML
# ---------------------------------------------------------------------------

def suppression_p(filedata, ordre):
    """Retire les <p> parasites avant le 1er bouton de chaque grade."""
    xxxgrade = []
    for m in re.finditer("<b>Au grade d", filedata):
        xxxgrade.append(m.start())
    for m in re.finditer("<b>A la dignité de", filedata):
        xxxgrade.append(m.start())
    xxxgrade.sort()

    offset = 0
    for paragraphe in xxxgrade:
        emplacement_p = filedata[paragraphe - offset:].find("<p>")
        if emplacement_p == -1:
            continue
        emplacement_p = emplacement_p + paragraphe - offset
        filedata = filedata[:emplacement_p] + filedata[emplacement_p + 3:]
        offset += 3
    return filedata


def QS_ajout_script(filedata):
    script = """<script language="Javascript">
function QS_ajout_ligne(champ1, champ2, ID_bouton) {
  if (document.getElementById(ID_bouton).style.backgroundColor != "green") {
    var paragraph = document.getElementById("p");
    var text = document.createTextNode(champ1 + '"' + champ2 + '"');
    paragraph.appendChild(text);
    var br = document.createElement("br");
    paragraph.appendChild(br);
    document.getElementById(ID_bouton).style.color = "white";
    document.getElementById(ID_bouton).style.backgroundColor = "green";
  }
}
</script>
<p></p>
<b>Texte à utiliser dans <a href="https://quickstatements.toolforge.org/#/batch" target="_blank">QuickStatements</a> pour exporter les nouvelles décorations dans Wikidata :</b>
<p id="p"></p>
"""
    if filedata.find("</html>") != -1:
        filedata = filedata[:filedata.find("</html>")] + script + "</html>"
    else:
        filedata += script
    return filedata


# ---------------------------------------------------------------------------
# Point d'entrée
# ---------------------------------------------------------------------------

def main():
    print('OUVERTURE DU FICHIER "in.txt"...')
    try:
        with open("in.txt", "r", encoding="utf-8") as f:
            texte_brut = f.read()
    except IOError:
        raise SystemExit(
            'Erreur : collez le texte copié depuis Légifrance (bouton "Texte copié") '
            'dans un fichier nommé "in.txt" dans le dossier du programme.'
        )

    print("CONVERSION DU TEXTE BRUT EN HTML INTERNE...")
    filedata = txt_to_html(texte_brut)

    # Encapsuler dans un squelette HTML minimal
    filedata = (
        '<html><head><meta charset="utf-8">'
        '<link rel="stylesheet" href="style.css"></head><body>\n'
        + filedata
        + "\n</body></html>"
    )

    print("RECHERCHE DES INFOS DE BASE DU DECRET...")
    NOR                  = definition_NOR(filedata)
    date_decret_ISO_wiki = definition_date_decret_ISO_wiki(filedata)
    ordre                = definition_ordre(filedata)
    boutons_simplifies   = definition_boutons_simplifies()

    print("MISE EN FORME DES TITRES DU DECRET...")
    filedata = mise_en_forme_titres(filedata, ordre)

    print("RECUPERATION DES LIGNES ASSOCIEES A CHAQUE PERSONNE...")
    print("==================================================")
    filedata = traitement(filedata, NOR, date_decret_ISO_wiki, ordre, boutons_simplifies)

    print("NETTOYAGE...")
    filedata = suppression_p(filedata, ordre)

    print("AJOUT DU CHAMP QUICKSTATEMENTS A LA FIN DU FICHIER...")
    filedata = QS_ajout_script(filedata)

    print('ENREGISTREMENT DU FICHIER "out.html"...')
    with open("out.html", "w", encoding="utf-8") as f:
        f.write(filedata)

    print("==================================================")
    print('TRAITEMENT TERMINE. OUVREZ LE FICHIER "out.html".')


if __name__ == "__main__":
    main()