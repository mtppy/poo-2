Les patrons de conception réutilisable
======================================

Python est un langage à typage dynamique de ce fait beaucoup 
de design pattern utiliser dans les autres langage ne nécessite 
pas la création d'objet intermédiaire


1 Createur
----------

Fabrique
~~~~~~~~

La fabrique permet d'instantier un objet dont la classe sera connue que pendant
l'exécution du programme.

En python, pour faire une fabrique, on peut utiliser un simple dictionnaire pour
stocker les classes::

    class Paginable:
        ...

    class Livre(Paginable):
        ...

    class BD(Paginable):
        ...

    class Manga(Paginable):
        ...

    paginables = {
        'livre': Livre,
        'bd': BD,
        'manga': Manga
    }


    paginables['bd']()

exercice
~~~~~~~~

Créer un fichier vehi.py et copier dedans le code ci-dessous::

    import json

    json_content = """
        [
            {
                "type": "velo",
                "conducteur": "Tom-Tom",
                "id": 1
            },
            {
                "type": "velo",
                "conducteur": "Nana",
                "id": 2
            },
            {
                "type": "rosalie",
                "conducteur": "Croquignol",
                "id": 3,
                "passagers": [
                    "Filochard",
                    "Ribouldingue"
                ]
            },
            {
                "type": "tandem",
                "conducteur": "Olga",
                "id": 4,
                "passagers": [
                    "Bronsky"
                ]
            }
        ]     
    """

    class Vehicule:
        def __init__(self, id_, conducteur):
            self.id = id_
            self.conducteur = conducteur

        def __repr__(self):
            return "<{cls.__name__} {obj.id}" \
                   " conduit par {obj.conducteur}>".format(cls=type(self), obj=self)


    class PassagerMixin:
        """
        Mixin Pour fournir la méthode `add_passager`. 
        """
        max_passagers = 1

        def add_passager(self, nom):
            if not hasattr(self, '_passagers'):
                self._passagers = []

            if len(self._passagers) == self.max_passagers:
                raise ValueError('Nombre max de passagers atteint')
            self._passagers.append(nom)

        @property
        def passagers(self):
            return tuple(getattr(self, '_passagers', ()))

        def __repr__(self):
            representation = super().__repr__()
            return '<{} avec: {}>'.format(representation, self.passagers)


    class Velo(Vehicule):
        pass

    class Tandem(PassagerMixin, Vehicule):
        pass

    class Rosalie(PassagerMixin, Vehicule):
        max_passagers = 3


    def charger_vehicules(vehicules):
        vehicules_objets = []
        for vehicule in vehicules:
            if vehicule['type'] == 'velo':
                obj = Velo(vehicule['id'], vehicule['conducteur'])
                vehicules_objets.append(obj)

            elif vehicule['type'] == 'rosalie':
                obj = Rosalie(vehicule['id'], vehicule['conducteur'])
                vehicules_objets.append(obj)

            elif vehicule['type'] == 'tandem':
                obj = Tandem(vehicule['id'], vehicule['conducteur'])
                vehicules_objets.append(obj)
            else:
                raise ValueError('type {} non supporté'.format(vehicule['type']))

            if isinstance(obj, PassagerMixin):
                for passager in vehicule['passagers']:
                    obj.add_passager(passager)

        return vehicules_objets


    def main():
        vehicules = charger_vehicules(json.loads(json_content))

        for vehicule in vehicules:
            print(vehicule)

    main()


Exécuter le fichier en utilisant la commande **python3 vehi.py**


Transforme le code ci-dessous en utilisant une fabrique pour remplacer 
les *if-else* dans la fonction **charger_vehicules()**.

Remplacer l'instruction **if isinstance(obj, PassagerMixin)** par l'instruction
**if hasattr(obj, 'add_passager')** dans la fonction **charger_vehicules()**.
Cette modification permet l'utilisation de ce que l'on appelle le duck-typing, 
Donner votre avis sur les avantages et les inconvénients.


Borg
~~~~

Toutes les instances partagent le même état::

    class Borg:

        _shared_state = {}

        def __init__(self):
            self.__dict__ = self._shared_state


2 Les structuraux
-----------------

Adaptateur 
~~~~~~~~~~

Faire passer un objet pour un autre objet en l'encapsulant. C'est utile lorsque l'on souhaite utiliser
une bibliothèque, mais qu'elle manipule des objets différents des nôtres

Par exemple imaginons que l'on souhaite utiliser cette fonction dans notre programme::  

    def uzine(robot):
        while robot.get_etat() == 'OK':    
            robot.faire_un_travail_repetitif()
        print("L'etat du robot est {}".format(robot.get_etat()))

Cette fonction appelle la méthode **faire_un_travail_repetitif** tant que la méthode 
**get_etat()** retourne 'OK'


Notre programme n'a pas de robot mais des objets de type humains::

    class Humain:
        def __init__(self):
            self.sante = 10

        def faire_un_travail_repetitif(self):
            self.sante -= 1
            print('soupire')

La classe **Humain** ne peut pas être utilisé dans la fonction **uzine()** car
elle n'a pas de méthode **get_etat()**. On va donc encapsuler les objets
humains dans un objet qui définira cette méthode.

::

    class RobotAdapteur:
        def __init__(self, humain):
            self._humain = humain

        def get_etat(self):
            if self._humain.sante > 5:
                return 'OK'
            return 'HS'

        def __getattr__(self, attr_name):
            return getattr(self._humain, attr_name)

    cyborg = RobotAdapteur(Humain())
    uzine(cyborg)  
    print(cyborg.sante)


En python, la méthode **__getattr__** est appelée quand un attribut n'est pas trouvé dans un objet::

    class Foo:
        def __init__(self):
            self.a  = 'exist'
        def __getattr__(self, attr_name):    
            return "Jocker"

    foo = Foo()
    print(foo.a) # 'exist'
    print(foo.b) # 'Jocker'


exercice
~~~~~~~~

Créer un fichier **tarificateur.py** et copier dedans la fonction ci-dessous::

    def prix_voyageur(vehicules, prix):
        return {
             vehicule.identifiant: len(vehicule.voyageurs) * prix
             for vehicule
             in vehicules
        }

On souhaite utiliser la fonction prix_voyageur sur nos véhicules

Dans votre programme importer la fonction **prix_voyageur()**::

    from tarificateur import prix_voyageur


Modifier la fonction **main()** comme ci-dessous et compléter la classe **Adaptateur**::

    class Adaptateur:
        """
        Encapsule un objet Vehicule.
        - L'attribut `identifiant` est lié à l'attribut `id` de l'objet
          encapsulé.
        - L'attribut `voyageurs` est lié à l'attribut `passagers` de l'objet
          encapsulé.

        Si l'objet encapsulé n'a pas d'attribut `passagers` l'attribut 
        `voyageurs` retourne () 
        """

    def main():
        vehicules = charger_vehicules(json.loads(json_content))

        vehicules = [Adaptateur(vehicule) for vehicule in vehicules]  
        
        for vehicule in vehicules:
            print(vehicule)

        print(prix_voyageur(vehicules))


3 Les Comportementaux
---------------------

Stratégie
~~~~~~~~~

Avec le typage dynamique, une simple fonction peut suffire::

    def fr_formater(personne):
        return '{personne.prenom} {personne.nom}'.format(personne=personne)


    def en_formater(personne):
        return '{personne.nom} {personne.prenom}'.format(personne=personne)


    class Personne:
        def __init__(self, prenom, nom, formater=fr_formater):
            self.nom = nom 
            self.prenom = prenom
            self.formater = formater
        def __str__(self):
            return self.formater(self)

    personne = Personne('Elie', 'Copter')
    print(personne)
    personne.formater = en_formater
    print(personne)


exercice
~~~~~~~~

Faire des startegie pour trier la liste de véhicules:
- trier_par_id(vehicules)
- trier_par_conducteur(vehicules)

La fonction **main** prendra en paramètre une stratégie comme ceci::

    def main(trier_par):
        vehicules = charger_vehicules(json.loads(json_content))
        vehicules = [Adaptateur(vehicule) for vehicule in vehicules]  
        
        trier_par(vehicules)

        for vehicule in vehicules:
            print(vehicule)

        print(prix_voyageur(vehicules))

    main(trier_par_conducteur)


Astuce: Pour trier une liste sur l'attribut x::

    vehicules.sort(key=lambda vehicule: vehicule.x)
     

Modifier l'appel de la fonction main comme-ceci::  

    main(functions_de_trie[sys.argv[1]])


Créer le dictionnaire **functions_de_trie** pour stoquer les stratégies de trie.
On pourra alors changer passer l'ordre de trie en paramètre du programme::
    
    python3 vehi.py id
    python3 vehi.py conducteur

