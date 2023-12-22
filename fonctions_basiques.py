#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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

def trim_string(texte="", texte_debut="", texte_fin=""):
    position_debut = texte.find(texte_debut)
    if position_debut == -1: return -1
    position_fin = texte[position_debut+len(texte_debut)+1:].find(texte_fin)
    if position_fin == -1 or position_fin == 0:
        position_fin = len(texte)
    else:
        position_fin = position_debut+len(texte_debut)+1 + position_fin
    return texte[position_debut:position_fin]

def get_majuscules(texte=""):
    # retourne les mots précédents le 1er double espace, MAJmin, né ou dit
    if texte == "": return -1
    debutMAJmin = 0
    while not (texte[debutMAJmin:debutMAJmin+1].isupper() and texte[debutMAJmin+1:debutMAJmin+2].islower()):
        debutMAJmin += 1
        if debutMAJmin == len(texte) - 1:
            debutMAJmin = -1
            break
    if debutMAJmin == 0: return -1
    if debutMAJmin == -1: debutMAJmin = 0 #pour faire -1 ci-dessous
    fins = [texte.find("  "), debutMAJmin-1, texte.find(" né"), texte.find(" dit")]
    fins = [fin for fin in fins if fin != -1] #list comprehension
    if fins == []: return texte
    return texte[:min(fins)]

def get_position_fin_majuscules(texte=""):
    # retourne la position juste après la fin du dernier mot tout en majuscules
    if len(texte) < 2: return -1
    fins = [position for position in range(1,len(texte)) if (texte[position].isupper() and texte[position-1].isupper())] #list comprehension
    if len(fins) == 0: return -1
    return max(fins)+1

def get_minuscules(texte=""):
    # retourne les mots à partir du 1er mot avec 1 majuscule puis une minuscule
    if texte == "": return -1
    debutMAJmin = 0
    while not (texte[debutMAJmin:debutMAJmin+1].isupper() and texte[debutMAJmin+1:debutMAJmin+2].islower()):
        debutMAJmin += 1
        if debutMAJmin == len(texte) - 1: return -1
    return texte[debutMAJmin:]

def clean_espaces(texte=""):
    #retire les espaces éventuels au début
    if type(texte) != str : return -1
    if texte == "" : return ""
    fin_espace = 0
    while texte[fin_espace:fin_espace+1] == " ":
        fin_espace += 1
        if fin_espace == len(texte) + 1: return ""
    return texte[fin_espace:]

def clean_dit_ne(texte=""):
    #retire les dit ou né et ce qui suit
    if type(texte) != str : return -1
    if texte.find(" dit") != -1:
        texte = texte[:texte.find(" dit")]
    if texte.find(" né") != -1:
        texte = texte[:texte.find(" né")]
    return texte