#!/usr/bin/env python3
# -*- coding: utf-8 -*-

ordres = {
    "ONM",
    "LH",
    "AL",
}

decorations = [
    {
        "nom": "Chevalier ONM",
        "grade": 5,
        "ordre": "ONM",
        "Q": "Q13422138",
        "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/92/Ordre_national_du_Merite_Chevalier_ribbon.svg/218px-Ordre_national_du_Merite_Chevalier_ribbon.svg.png",
    },
    {
        "nom": "Officier ONM",
        "grade": 4,
        "ordre": "ONM",
        "Q": "Q13422140",
        "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/52/Ordre_national_du_Merite_Officier_ribbon.svg/218px-Ordre_national_du_Merite_Officier_ribbon.svg.png",
    },
    {
        "nom": "Commandeur ONM",
        "grade": 3,
        "ordre": "ONM",
        "Q": "Q13422141",
        "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/82/Ordre_national_du_Merite_Commandeur_ribbon.svg/218px-Ordre_national_du_Merite_Commandeur_ribbon.svg.png",
    },
    {
        "nom": "Grand Officier ONM",
        "grade": 2,
        "ordre": "ONM",
        "Q": "Q13422142",
        "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b2/Ordre_national_du_Merite_GO_ribbon.svg/218px-Ordre_national_du_Merite_GO_ribbon.svg.png",
    },
    {
        "nom": "Grand'Croix ONM",
        "grade": 1,
        "ordre": "ONM",
        "Q": "Q13422143",
        "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/82/Ordre_national_du_Merite_GC_ribbon.svg/218px-Ordre_national_du_Merite_GC_ribbon.svg.png",
    },
    {
        "nom": "ONM", # sans plus de précision
        "grade": 6,
        "ordre": "ONM",
        "Q": "Q652962",
        "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cc/Ordre_national_du_merite_chevalier_FRANCE.jpg/86px-Ordre_national_du_merite_chevalier_FRANCE.jpg",
    },
    {
        "nom": "Chevalier LH",
        "grade": 5,
        "ordre": "LH",
        "Q": "Q10855271",
        "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e6/Legion_Honneur_Chevalier_ribbon.svg/218px-Legion_Honneur_Chevalier_ribbon.svg.png",
    },
    {
        "nom": "Officier LH",
        "grade": 4,
        "ordre": "LH",
        "Q": "Q10855195",
        "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Legion_Honneur_Officier_ribbon.svg/218px-Legion_Honneur_Officier_ribbon.svg.png",
    },
    {
        "nom": "Commandeur LH",
        "grade": 3,
        "ordre": "LH",
        "Q": "Q10855212",
        "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ef/Legion_Honneur_Commandeur_ribbon.svg/218px-Legion_Honneur_Commandeur_ribbon.svg.png",
    },
    {
        "nom": "Grand Officier LH",
        "grade": 2,
        "ordre": "LH",
        "Q": "Q10855216",
        "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/af/Legion_Honneur_GO_ribbon.svg/218px-Legion_Honneur_GO_ribbon.svg.png",
    },
    {
        "nom": "Grand'Croix LH",
        "grade": 1,
        "ordre": "LH",
        "Q": "Q10855226",
        "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/ba/Legion_Honneur_GC_ribbon.svg/218px-Legion_Honneur_GC_ribbon.svg.png",
    },
    {
        "nom": "LH", # sans plus de précision
        "grade": 6,
        "ordre": "LH",
        "Q": "Q163700",
        "img": "https://upload.wikimedia.org/wikipedia/commons/8/81/De_la_legion_d_honneur_Recto.png",
    },
    {
        "nom": "Chevalier AL",
        "grade": 3,
        "ordre": "AL",
        "Q": "Q13452528",
        "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6a/Ordre_des_Arts_et_des_Lettres_Chevalier_ribbon.svg/218px-Ordre_des_Arts_et_des_Lettres_Chevalier_ribbon.svg.png",
    },
    {
        "nom": "Officier AL",
        "grade": 2,
        "ordre": "AL",
        "Q": "Q13452524",
        "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2a/Ordre_des_Arts_et_des_Lettres_Officier_ribbon.svg/218px-Ordre_des_Arts_et_des_Lettres_Officier_ribbon.svg.png",
    },
    {
        "nom": "Commandeur AL",
        "grade": 1,
        "ordre": "AL",
        "Q": "Q13452531",
        "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ef/Ordre_des_Arts_et_des_Lettres_Commandeur_ribbon.svg/218px-Ordre_des_Arts_et_des_Lettres_Commandeur_ribbon.svg.png",
    },
    {
        "nom": "AL", # sans plus de précision
        "grade": 4,
        "ordre": "AL",
        "Q": "Q716909",
        "img": "https://upload.wikimedia.org/wikipedia/commons/9/9c/Chevalier_arts_et_lettres.jpg",
    },
]

def Q_par_grade_et_ordre(grade, ordre):
    for decoration in decorations:
        if decoration["grade"] == grade and decoration["ordre"] == ordre:
            return decoration["Q"]
    return None

def img_par_grade_et_ordre(grade, ordre):
    for decoration in decorations:
        if decoration["grade"] == grade and decoration["ordre"] == ordre:
            return decoration["img"]
    return None

def decorations_ordre(ordre):
    return [decoration for decoration in decorations if decoration["ordre"] == ordre]
