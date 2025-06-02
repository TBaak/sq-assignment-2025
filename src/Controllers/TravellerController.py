from Debug.ConsoleLogger import ConsoleLogger
from Enum.Color import Color
from Enum.LogType import LogType
from Form.TravellerForm import TravellerForm
from Models.Traveller import Traveller
from Repository.LogRepository import LogRepository
from Repository.TravellerRepository import TravellerRepository
from Security.AuthorizationDecorator import Auth
from Security.Enum.Permission import Permission
from Service.IndexService import IndexService
from View.UserInterfaceAlert import UserInterfaceAlert
from View.UserInterfaceFlow import UserInterfaceFlow
from View.UserInterfacePrompt import UserInterfacePrompt
from View.UserInterfaceTable import UserInterfaceTable
from View.UserInterfaceTableRow import UserInterfaceTableRow
from View.Validations.NoSpecialCharsValidation import NoSpecialCharsValidation
from View.Validations.NumberValdation import NumberValidation
from View.Validations.OnlyLetterValdation import OnlyLetterValidation


class TravellerController:

    @Auth.permission_required(Permission.TravellerRead)
    def list_travellers(self, travellers: list[Traveller] = None):

        UserInterfaceFlow.quick_run_till_next(
            UserInterfaceAlert("Traveller overzicht aan het laden...", Color.HEADER)
        )

        LogRepository.log(LogType.TravellersRead)

        if travellers is None:
            travellers = TravellerRepository.find_all()

        rows = map(lambda m: [m.number, m.first_name, m.last_name, m.age, m.email,
                              m.street_name + " " + m.house_number], travellers)
        rows = list(rows)

        for index, row in enumerate(rows):
            row.insert(0, index + 1)

        rows = list(map(lambda m_row: UserInterfaceTableRow(m_row), rows))

        rows.insert(0, UserInterfaceTableRow(
            ["#", "Traveller nummer", "Voornaam", "Achternaam", "Leeftijd", "E-mailadres", "Adres"]))

        ui = UserInterfaceFlow()
        ui.add(UserInterfaceAlert("Traveller overzicht" if travellers is None else "Zoekresultaten", Color.HEADER))
        ui.add(UserInterfaceTable(rows=rows, has_header=True))
        ui.add(UserInterfacePrompt(
            prompt_text="Geef het nummer om te bekijken of druk op Z om te zoeken of druk op ENTER om terug te gaan",
            memory_key="action"
        )
        )
        selection = ui.run()

        selected = selection["action"]

        if selected == "":
            return

        if selected.upper() == "Z":
            return self.search_travellers()

        if selected.isdigit() is False:
            UserInterfaceFlow.quick_run(
                UserInterfaceAlert("Ongeldige keuze", Color.FAIL),
                1
            )
            return self.list_travellers()

        member_index = int(selected) - 1

        try:
            self.show_traveller(travellers[member_index])
        except IndexError:
            UserInterfaceFlow.quick_run(
                UserInterfaceAlert("Ongeldige keuze", Color.FAIL),
                1
            )

    @Auth.permission_required(Permission.TravellerRead)
    def search_travellers(self):

        LogRepository.log(LogType.TravellersRead)

        query_ui = UserInterfaceFlow()
        query_ui.add(UserInterfacePrompt(
            prompt_text="Zoeken op naam, leeftijd, e-mailadres, adres of member nummer",
            memory_key="query",
            validations=[NoSpecialCharsValidation()]
        )
        )
        query = query_ui.run()['query']

        members = TravellerRepository.find_by_query(query)

        if len(members) == 0:
            UserInterfaceFlow.quick_run(
                UserInterfaceAlert("Geen resultaten gevonden", Color.FAIL),
                2
            )
            return self.list_travellers()

        return self.list_travellers(members)

    @Auth.permission_required(Permission.TravellerRead)
    def show_traveller(self, member: Traveller):

        LogRepository.log(LogType.TravellerRead)

        rows = [
            UserInterfaceTableRow(["Nummer", member.number]),
            UserInterfaceTableRow(["Voornaam", member.first_name]),
            UserInterfaceTableRow(["Achternaam", member.last_name]),
            UserInterfaceTableRow(["Leeftijd", member.age]),
            UserInterfaceTableRow(["Gewicht", member.weight]),

            UserInterfaceTableRow(["Geslacht", member.gender.upper()]),
            UserInterfaceTableRow(["E-mailadres", member.email]),

            UserInterfaceTableRow(["Telefoonnummer", member.phone]),
            UserInterfaceTableRow(["Straatnaam", member.street_name]),
            UserInterfaceTableRow(["Huisnummer", member.house_number]),
            UserInterfaceTableRow(["Postcode", member.zip_code]),
            UserInterfaceTableRow(["Stad", member.city])
        ]

        ui = UserInterfaceFlow()
        ui.add(UserInterfaceAlert("Member " + member.first_name + " " + member.last_name, Color.HEADER))
        ui.add(UserInterfaceTable(rows))
        ui.add(UserInterfacePrompt(
            prompt_text="Druk op W om te wijzigingen of druk D om te verwijderen of druk op enter om terug te gaan",
            memory_key="action",
            validations=[OnlyLetterValidation()]
        )
        )

        selection = ui.run()

        selected = selection["action"]

        if selected == "":
            return

        if selected.upper() == "W":
            self.update_traveller(member)

        elif selected.upper() == "D":
            self.delete_traveller(member)

        self.list_travellers()

    @Auth.permission_required(Permission.TravellerCreate)
    def add_traveller(self):

        ui = UserInterfaceFlow()
        ui.add(UserInterfaceAlert(text="Member toevoegen", color=Color.HEADER))

        ui = TravellerForm.get_form(ui, None)

        fields = ui.run()

        member = Traveller()
        member.populate(list(fields.values()), list(fields.keys()))

        LogRepository.log(LogType.TravellerCreated, f"id: {member.id} name: {member.first_name} {member.last_name}")

        TravellerRepository.persist_traveller(member)

        IndexService.index_database()

        UserInterfaceFlow.quick_run(
            UserInterfaceAlert("Member toegevoegd", Color.OKGREEN),
            2
        )

    @Auth.permission_required(Permission.TravellerUpdate)
    def update_traveller(self, member: Traveller):

        ui = UserInterfaceFlow()
        ui.add(UserInterfaceAlert(text="Member " + member.first_name + " " + member.last_name + " wijziging",
                                  color=Color.OKBLUE))
        ui.add(UserInterfaceAlert(text=f"Druk op enter om waarde niet te wijzigingen", color=Color.OKCYAN))

        ui = TravellerForm.get_form(ui, member)

        fields = ui.run()

        member.populate(list(fields.values()), list(fields.keys()))

        TravellerRepository.update_traveller(member)

        LogRepository.log(LogType.TravellerUpdated, f"id: {member.id} name: {member.first_name} {member.last_name}")

        IndexService.index_database()

        UserInterfaceFlow.quick_run(
            UserInterfaceAlert("Member geüpdatet", Color.OKGREEN),
            2
        )

    @Auth.permission_required(Permission.TravellerDelete)
    def delete_traveller(self, member: Traveller):

        TravellerRepository.delete_traveller(member)

        LogRepository.log(LogType.TravellerDeleted, f"name: {member.first_name} {member.last_name}")

        IndexService.index_database()

        UserInterfaceFlow.quick_run(
            UserInterfaceAlert("Member verwijderd", Color.OKGREEN),
            2
        )
