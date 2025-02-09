# Application de gestion des élèves et des professeurs

Cette application permet une gestion complète des élèves et des professeurs dans un lycée, en facilitant la modification des choix Parcoursup des élèves tout en permettant aux professeurs de gérer les informations des élèves. 

## Fonctionnalités à implémenter

### 1. **Websocket pour l'actualisation du dashboard**
   - Utiliser le WebSocket pour actualiser en temps réel les informations affichées sur le dashboard, telles que les cartes indiquant les noms des élèves connectés, etc.

### 2. **Menu Paramètres**
   - Ajouter un menu de paramètres permettant d'activer ou de désactiver plusieurs options pour personnaliser l'application.

### 3. **Confirmation définitive des vœux**
   - Ajouter un bouton permettant à l'élève de confirmer définitivement ses vœux. 
     - Lors de la confirmation, l'application doit demander à l'utilisateur s'il est vraiment sûr de valider ses choix.
     - Une fois la confirmation effectuée, l'élève ne pourra plus modifier l'ordre des vœux. Il faudra prendre des mesures pour empêcher toute modification via le code JavaScript.
     - Après confirmation, la valeur dédiée dans la base SQL passe à `True`, ce qui marque la validation définitive des choix.
     - Lors de la mise à jour des valeurs dans le fichier `/routes/update_data.py`, il est nécessaire de vérifier si la valeur dédiée dans la base SQL est bien à `False` avant d'apporter des modifications.

### 4. **Page d'identifiants perdus**
   - Créer une page permettant aux utilisateurs de signaler la perte de leurs identifiants.
   - Lorsqu'un utilisateur demande un nouvel identifiant, une ligne est ajoutée dans le tableau `identifiants_perdus` de la base SQL, avec toutes les informations nécessaires (voir la classe dans le fichier `SQLClassSQL.py` pour plus de détails).

### 5. **Page Professeurs**
   - Permettre aux professeurs de lier une classe à son professeur principal (PP).
   - Afficher sur le dashboard des professeurs la liste des élèves ayant fait une demande d'identifiants perdus.
   - Fournir une fonctionnalité permettant aux professeurs de consulter les statistiques des élèves sous leur responsabilité.

### 6. **Page et compte Super Administrateur**
   - Prévoir un compte "Super Administrateur" pour gérer les professeurs et les comptes des élèves sur le site.
   - Le super administrateur aura des droits complets sur l'ensemble de l'application, y compris la gestion des comptes des professeurs et des élèves.


