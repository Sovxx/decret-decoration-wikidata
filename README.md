# decret-decoration-wikidata
Tool to import from the official list of awarded French national decorations to Wikidata.

### Qu'est-ce que decret-decoration-wikidata ?
decret-decoration-wikidata est un outil d'importation qui facilite le renseignement des décorations françaises (Légion d'honneur et Ordre national du Mérite) sur Wikidata à partir du décret de nomination.

Il permet d'afficher sur une copie locale du décret :
* Les personnes existantes sur Wikidata qui sont susceptibles de correspondre aux personnes listées dans le décret.
* Des boutons pour ajouter sur Wikidata (via QuickStatement) la décoration attribuée par le décret.

<a href="doc/in.png"><img src="doc/in_400px.png"></a> &#10145; <a href="doc/out.png"><img src="doc/out_400px.png"></a>

---

### Utilisation
* Installez Python3 version 3.6 ou supérieure (gratuit).
* Installez le module ``requests`` (gratuit) pour Python3.
* Téléchargez decret-decoration-wikidata (bouton vert "Code" en haut à droite et "Download ZIP") et dézippez-le.
* Téléchargez la page du décret à traiter (Par exemple https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000043522969) et enregistrez cette page dans le même dossier que decret-decoration-wikidata en la renommant in.html.
* Ouvrez un terminal (invite de commande) dans le dossier (Par exemple ``cd C:/xxx/xxx``).
* Lancez le programme avec la commande ``python3 ./decret-decoration-wikidata.py`` (ou éventuellement ``py ./decret-decoration-wikidata.py``).
* Renseignez les quelques questions posées.
* Attendez... (Comptez ~20 minutes pour 1000 personnes).
* Ouvrez out.html : les personnes déjà listées sur Wikidata sont apparues.
* Si une décoration n'est pas encore renseignée sur Wikidata (<b>Attention aux homonymes ! Veillez à avoir un esprit critique</b>), cliquez sur le bouton correspondant. Note : Aucune donnée n'est envoyée à Wikidata.
* Allez tout en bas du fichier out.html pour récupérer le texte qui sera à importer dans QuickStatements (outil d'import rapide pour Wikidata).
---

### Bugs, suggestions
Vous pouvez signaler les bugs et suggestions dans l'onglet Issue ou me laisser un message sur ma page wikidata https://www.wikidata.org/wiki/User:Sovxx
