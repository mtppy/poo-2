
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
