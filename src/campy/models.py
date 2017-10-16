# coding: utf-8
from campy.utils import age
from collections import OrderedDict
from datetime import date
from datetime import datetime
from google.appengine.ext.ndb import BooleanProperty
from google.appengine.ext.ndb import DateProperty
from google.appengine.ext.ndb import DateTimeProperty
from google.appengine.ext.ndb import IntegerProperty
from google.appengine.ext.ndb import Model
from google.appengine.ext.ndb import StringProperty
from google.appengine.ext.ndb import StructuredProperty
from google.appengine.ext.ndb import TextProperty


NATIONALITIES = [
    u"DESCONOCIDA",
    u"Abjasia",
    u"Acrotiri y Dhekelia",
    u"Afganistán",
    u"Albania",
    u"Alemania",
    u"Andorra",
    u"Angola",
    u"Anguila",
    u"Antigua y Barbuda",
    u"Arabia Saudita",
    u"Argelia",
    u"Argentina",
    u"Armenia",
    u"Aruba",
    u"Australia",
    u"Austria",
    u"Azerbaiyán",
    u"Bahamas",
    u"Bangladés",
    u"Barbados",
    u"Baréin",
    u"Bélgica",
    u"Belice",
    u"Benín",
    u"Bermudas",
    u"Bielorrusia",
    u"Birmania",
    u"Bolivia",
    u"Bosnia y Herzegovina",
    u"Botsuana",
    u"Brasil",
    u"Brunéi",
    u"Bulgaria",
    u"Burkina Faso",
    u"Burundi",
    u"Bután",
    u"Cabo Verde",
    u"Camboya",
    u"Camerún",
    u"Canadá",
    u"Catar",
    u"Chad",
    u"Chile",
    u"China",
    u"Chipre",
    u"Chipre del Norte",
    u"Ciudad del Vaticano",
    u"Colombia",
    u"Comoras",
    u"Corea del Norte",
    u"Corea del Sur",
    u"Costa de Marfil",
    u"Costa Rica",
    u"Croacia",
    u"Cuba",
    u"Curazao",
    u"Dinamarca",
    u"Dominica",
    u"Ecuador",
    u"Egipto",
    u"El Salvador",
    u"Emiratos Árabes Unidos",
    u"Eritrea",
    u"Eslovaquia",
    u"Eslovenia",
    u"España",
    u"Estados Unidos",
    u"Estonia",
    u"Etiopía",
    u"Filipinas",
    u"Finlandia",
    u"Fiyi",
    u"Francia",
    u"Gabón",
    u"Gambia",
    u"Georgia",
    u"Ghana",
    u"Gibraltar",
    u"Granada",
    u"Grecia",
    u"Groenlandia",
    u"Guam",
    u"Guatemala",
    u"Guernsey",
    u"Guinea",
    u"Guinea Ecuatorial",
    u"Guinea-Bisáu",
    u"Guyana",
    u"Haití",
    u"Honduras",
    u"Hong Kong",
    u"Hungría",
    u"India",
    u"Indonesia",
    u"Irak",
    u"Irán",
    u"Irlanda",
    u"Isla de Man",
    u"Isla de Navidad",
    u"Isla Norfolk",
    u"Islandia",
    u"Islas Caimán",
    u"Islas Cocos",
    u"Islas Cook",
    u"Islas Feroe",
    u"Islas Marianas del Norte",
    u"Islas Marshall",
    u"Islas Pitcairn",
    u"Islas Salomón",
    u"Islas Turcas y Caicos",
    u"Islas Vírgenes Británicas",
    u"Islas Vírgenes de los Estados Unidos",
    u"Israel",
    u"Italia",
    u"Jamaica",
    u"Japón",
    u"Jersey",
    u"Jordania",
    u"Kazajistán",
    u"Kenia",
    u"Kirguistán",
    u"Kiribati",
    u"Kosovo",
    u"Kuwait",
    u"Laos",
    u"Lesoto",
    u"Letonia",
    u"Líbano",
    u"Liberia",
    u"Libia",
    u"Liechtenstein",
    u"Lituania",
    u"Luxemburgo",
    u"Macao",
    u"Macedonia",
    u"Madagascar",
    u"Malasia",
    u"Malaui",
    u"Maldivas",
    u"Malí",
    u"Malta",
    u"Marruecos",
    u"Mauricio",
    u"Mauritania",
    u"México",
    u"Micronesia",
    u"Moldavia",
    u"Mónaco",
    u"Mongolia",
    u"Montenegro",
    u"Montserrat",
    u"Mozambique",
    u"Nagorno Karabaj",
    u"Namibia",
    u"Nauru",
    u"Nepal",
    u"Nicaragua",
    u"Níger",
    u"Nigeria",
    u"Niue",
    u"Noruega",
    u"Nueva Caledonia",
    u"Nueva Rusia",
    u"Nueva Zelanda",
    u"Omán",
    u"Osetia del Sur",
    u"Países Bajos",
    u"Pakistán",
    u"Palaos",
    u"Palestina",
    u"Panamá",
    u"Papúa Nueva Guinea",
    u"Paraguay",
    u"Perú",
    u"Polinesia Francesa",
    u"Polonia",
    u"Portugal",
    u"Puerto Rico",
    u"Reino Unido",
    u"República Centroafricana",
    u"República Checa",
    u"República del Congo",
    u"República Democrática del Congo",
    u"República Dominicana",
    u"Ruanda",
    u"Rumania",
    u"Rusia",
    u"Sahara Occidental",
    u"Samoa",
    u"Samoa Americana",
    u"San Bartolomé",
    u"San Cristóbal y Nieves",
    u"San Marino",
    u"San Martín",
    u"San Pedro y Miquelón",
    u"San Vicente y las Granadinas",
    u"Santa Elena, Ascensión y Tristán de Acuña",
    u"Santa Lucía",
    u"Santo Tomé y Príncipe",
    u"Senegal",
    u"Serbia",
    u"Seychelles",
    u"Sierra Leona",
    u"Singapur",
    u"Sint Maarten",
    u"Siria",
    u"Somalia",
    u"Somalilandia",
    u"Sri Lanka",
    u"Suazilandia",
    u"Sudáfrica",
    u"Sudán",
    u"Sudán del Sur",
    u"Suecia",
    u"Suiza",
    u"Surinam",
    u"Svalbard",
    u"Tailandia",
    u"Taiwán",
    u"Tanzania",
    u"Tayikistán",
    u"Timor Oriental",
    u"Togo",
    u"Tokelau",
    u"Tonga",
    u"Transnistria",
    u"Trinidad y Tobago",
    u"Túnez",
    u"Turkmenistán",
    u"Turquía",
    u"Tuvalu",
    u"Ucrania",
    u"Uganda",
    u"Uruguay",
    u"Uzbekistán",
    u"Vanuatu",
    u"Venezuela",
    u"Vietnam",
    u"Wallis y Futuna",
    u"Yemen",
    u"Yibuti",
    u"Zambia",
    u"Zimbabue",
    u"OTRA"
]


PROVINCES = [
    u"Buenos Aires",
    u"Catamarca",
    u"Chaco",
    u"Chubut",
    u"Ciudad Autónoma de Bs. As.",
    u"Córdoba",
    u"Corrientes",
    u"Entre Ríos",
    u"Formosa",
    u"Jujuy",
    u"La Pampa",
    u"La Rioja",
    u"Mendoza",
    u"Misiones",
    u"Neuquén",
    u"Río Negro",
    u"Salta",
    u"San Juan",
    u"San Luis",
    u"Santa Cruz",
    u"Santa Fe",
    u"Santiago del Estero",
    u"Tierra del Fuego",
    u"Tucumán"
]


class _Roles(object):
    SYSTEM_ADMINISTRATOR = "system administrator"
    SECRETARY = "secretary"
    ADVISOR = "advisor"
roles = _Roles


class SerializableModel(Model):
    @staticmethod
    def _should_serialize(key, include, exclude):
        return not ((exclude and key in exclude) or (include and key not in include))

    def json(self, include=None, exclude=None):
        d = super(SerializableModel, self).to_dict(include=include, exclude=exclude)
        for k, v in d.iteritems():
            if isinstance(v, datetime):
                d[k] = v.strftime("%Y-%m-%dT%H:%M:%SZ")
            elif isinstance(v, date):
                d[k] = v.strftime("%Y-%m-%d")
        return d


class BaseModel(SerializableModel):
    def id(self):
        return self.key and self.key.id()

    def json(self, include=None, exclude=None):
        d = super(BaseModel, self).json(include, exclude)
        if self._should_serialize("id", include, exclude):
            d["id"] = self.id()
        return d


class Branch(BaseModel):
    name = StringProperty(required=True)


class User(BaseModel):
    name = StringProperty(required=True)
    email = StringProperty(required=True)
    roles = StringProperty(repeated=True)

    def __init__(self, **kwargs):
        kwargs["id"] = kwargs.get("email")
        super(User, self).__init__(**kwargs)


class Advisor(SerializableModel):
    """Used only as StructuredProperty for Patient."""
    id = StringProperty(required=True)
    name = StringProperty(required=True)


class Child(SerializableModel):
    """Used only as StructuredProperty for Patient."""
    modifiedon = DateTimeProperty(required=True)
    name = StringProperty(required=True)
    birthdate = DateProperty()
    known_age = IntegerProperty()

    def age(self):
        if self.birthdate:
            return age(self.birthdate)
        if self.known_age is not None:
            return age(self.modifiedon) + self.known_age
        return None

    def json(self, include=None, exclude=None):
        d = super(Child, self).json(include, exclude)
        if self._should_serialize("age", include, exclude):
            d["age"] = self.age()
        return d


class Patient(BaseModel):
    createdon = DateTimeProperty(required=True, auto_now_add=True)
    modifiedon = DateTimeProperty(required=True, auto_now=True)
    record = IntegerProperty(required=True)
    firstname = StringProperty(required=True)
    middlename = StringProperty()
    surname = StringProperty()
    birthdate = DateProperty(required=True)
    nationality = StringProperty(required=True, choices=NATIONALITIES)
    occupation = StringProperty(required=True)
    children = StructuredProperty(Child, repeated=True)
    cellphone = StringProperty()
    cellphone2 = StringProperty()
    telephone = StringProperty()
    email = StringProperty()
    province = StringProperty(choices=PROVINCES)
    city = StringProperty()
    district = StringProperty()
    advisor = StructuredProperty(Advisor)
    coadvisors = StructuredProperty(Advisor, repeated=True)
    relative_firstname = StringProperty()
    relative_middlename = StringProperty()
    relative_surname = StringProperty()
    relative_relationship = StringProperty()
    relative_cellphone = StringProperty()
    relative_province = StringProperty(choices=PROVINCES)
    relative_city = StringProperty()
    relative_district = StringProperty()
    notes = TextProperty()

    def age(self):
        return age(self.birthdate) if self.birthdate else None

    def has_advisor(self, user):
        uid = user.id()
        return (self.advisor and self.advisor.id == uid) or\
               (self.coadvisors and uid in map(lambda a: a.id, self.coadvisors))

    def json(self, include=None, exclude=None):
        d = super(Patient, self).json(include, ["children", "advisor", "coadvisors"] + (exclude or []))
        if self._should_serialize("children", include, exclude):
            d["children"] = [c.json(include, exclude) for c in self.children] if self.children else []
        if self._should_serialize("advisor", include, exclude):
            d["advisor"] = self.advisor.json(include, exclude) if self.advisor else None
        if self._should_serialize("coadvisors", include, exclude):
            d["coadvisors"] = [c.json(include, exclude) for c in self.coadvisors] if self.coadvisors else []
        if self._should_serialize("age", include, exclude):
            d["age"] = self.age()
        return d


class Observation(BaseModel):
    TYPES = OrderedDict([
        ("VISIT", u"Entrevista presencial"),
        ("TELEPHONE", u"Seguimiento telefónico")
    ])
    DURATIONS = OrderedDict([
        (5, "5 min"),
        (10, "10 min"),
        (15, "15 min"),
        (30, "30 min"),
        (45, "45 min"),
        (60, "1 h"),
        (75, "1 h 15 min"),
        (90, "1 h 30 min"),
        (105, "1 h 45 min"),
        (120, "2 h"),
        (150, "2 h 30 min"),
        (180, "3 h")
    ])
    CHANNELS = OrderedDict([
        ("GOOGLE", u"Anuncio en Internet"),
        ("STREET", u"Publicidad callejera"),
        ("COMMENT", u"Recomendación de otra persona"),
        ("OTHER", u"Otro")
    ])
    PREGNANCY_CONFIRMATION_METHODS = [
        u"Análisis de sangre",
        u"Ecografía",
        u"Síntomas",
        u"Test de orina"
    ]
    ABORTION_TYPES = [
        u"Espontáneo",
        u"Provocado"
    ]
    ABORTION_METHODS = [
        u"Intervención médica",
        u"Píldora abortiva",
        u"OTRO"
    ]
    ABORTION_PILLS = [
        u"Misoprostol",
        u"Pastilla del día después",
        u"OTRO"
    ]
    SMOKER_TYPE = [
        u"No fumadora",
        u"Fumadora ocasional",
        u"Fumadora diaria"
    ]
    type = StringProperty(required=True, choices=TYPES.keys())
    date = DateProperty(required=True)
    companion_relationship = StringProperty()
    relative_firstname = StringProperty()
    relative_surname = StringProperty()
    learned_about_center = StringProperty()
    detail = StringProperty()
    pregnancy_confirmed = BooleanProperty()
    pregnancy_length_weeks = IntegerProperty()
