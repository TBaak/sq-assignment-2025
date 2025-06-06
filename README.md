# URBAN MOBILITY backend system
_ANALYSIS 8: SOFTWARE QUALITY_

## Prerequisites

- Python 3.13
- Python libraries:
  - `pip install -r requirements.txt`

## TODO

> ✅ = Afgerond 
>
> 🔄 = In progress

- ✅ CRUD Traveller
- ✅ CRUD Scooters
- ✅ CRUD Users
- ✅ Symmetrische database encryptie
- ✅ Password hashing
- ✅ Invoer validatie met domein logica
- ✅ Logging van acties
- 🔄 Database backups
- 🔄 Systeem beheerder rol
- 🔄 Service engineer rol

## Structuur

De basis opzet voor de applicatie is een MVC structuur, waarbij de applicatie is opgebouwd uit verschillende lagen:
- **Model**: De laag die de data en de logica van de applicatie beheert.
- **View**: De laag die de presentatie van de data verzorgt.
- **Controller**: De laag die de interactie tussen de model en view beheert, zoals het verwerken van gebruikersinvoer en het aanroepen van de juiste methoden in het model.

### Model

Alle data is opgedeeld in verschillende modellen. Bewaard in de `Models` map. De modellen hebben een respectievelijke tabel
in de database en een repository klasse die de database interactie verzorgt. De repository klasse is verantwoordelijk voor het ophalen, toevoegen, bijwerken en verwijderen van data in de database.
De repository klasses worden bewaard in de `Repositories` map.

### View

De views kunnen gezien worden aan een aaneenschakeling van console stappen. Elke stap is een aparte view die de gebruiker begeleidt door het proces. De views zijn te vinden in de `Views` map.
Om een complete view op te zetten worden eerst de stappen gedefinieerd en hierna worden deze stappen getoond aan de gebruiker.

#### Validatie

De validatie op de `UserInterfacePrompt` invoer wordt gedaan via validatie klassen in de `Validations` map. Deze klassen 
zijn verantwoordelijk voor het valideren van de invoer van de gebruiker en het geven van feedback als de invoer niet geldig is. 
De validatie klassen worden bij het definiëren van de view ingevoerd en automatisch aangeroepen bij het verwerken van de invoer van de gebruiker.

#### Formulieren

De formulieren zijn vooraf samengestelde stappen die de gebruiker de juiste invoer laten doen voor een model.
De formulieren worden bewaard in de `Forms` map.

### Controllers

De controllers zijn verantwoordelijk voor het aanroepen van de juiste methoden in de modellen en het tonen van de juiste views.
Elke route/actie heeft een eigen methode in de controller. De controllers zijn te vinden in de `Controllers` map.

#### Security

Per methode in de controller is er een beveiliging die controleert of de gebruiker geautoriseerd is om de actie uit te voeren.
Dit gaat met behulp van de `Auth` decorator. Deze decorator controleert of de gebruiker is ingelogd en of de gebruiker d
e juiste rechten heeft om de actie uit te voeren.

#### Services

De services zijn verantwoordelijk voor de logica van de applicatie.
Ze worden gebruikt als ondersteuning laag voor de controller functionaliteit en zijn te vinden in de `Services` map.

## Indexering

Omdat de database geëncrypt is, wordt bij het starten van de applicatie de database geïndexeerd.
De index wordt bewaard in de `IndexService` en wordt gebruikt om te zoeken in de database.

## Database seeder

In het project is een database seeder aanwezig die de database vult met testdata. Deze seeder kan gedraaid worden via 
jet `um_database_seeder.py` script.

> Geadviseerd wordt om de database te verwijderen voordat de seeder wordt gedraaid, om te voorkomen dat er dubbele data in de database komt.