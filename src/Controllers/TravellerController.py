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
from View.Validations.NumberValidation import NumberValidation
from View.Validations.OnlyLetterValidation import OnlyLetterValidation


class TravellerController:

    @Auth.permission_required(Permission.TravellerRead)
    def list_travellers(self, travellers: list[Traveller] = None):

        UserInterfaceFlow.quick_run_till_next(
            UserInterfaceAlert("Traveller overzicht aan het laden...", Color.HEADER)
        )

        LogRepository.log(LogType.TravellersRead)

        if travellers is None:
            travellers = TravellerRepository.find_all()

        rows = map(lambda m: [m.number, m.first_name, m.last_name, m.driving_license_number, m.email_address,
                              m.street_name + " " + m.house_number], travellers)
        rows = list(rows)

        for index, row in enumerate(rows):
            row.insert(0, index + 1)

        rows = list(map(lambda m_row: UserInterfaceTableRow(m_row), rows))

        rows.insert(0, UserInterfaceTableRow(
            ["#", "Traveller nummer", "Voornaam", "Achternaam", "Rijbewijs nummer", "E-mailadres", "Adres"]))

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

        traveller_index = int(selected) - 1

        try:
            self.show_traveller(travellers[traveller_index])
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
            prompt_text="Zoeken op naam, leeftijd, e-mailadres, adres of traveller nummer",
            memory_key="query",
            validations=[NoSpecialCharsValidation()]
        )
        )
        query = query_ui.run()['query']

        travellers = TravellerRepository.find_by_query(query)

        if len(travellers) == 0:
            UserInterfaceFlow.quick_run(
                UserInterfaceAlert("Geen resultaten gevonden", Color.FAIL),
                2
            )
            return self.list_travellers()

        return self.list_travellers(travellers)

    @Auth.permission_required(Permission.TravellerRead)
    def show_traveller(self, traveller: Traveller):

        LogRepository.log(LogType.TravellerRead)

        rows = [
            UserInterfaceTableRow(["Nummer", traveller.number]),
            UserInterfaceTableRow(["Voornaam", traveller.first_name]),
            UserInterfaceTableRow(["Achternaam", traveller.last_name]),
            UserInterfaceTableRow(["Geboorte datum", traveller.dob]),

            UserInterfaceTableRow(["Geslacht", traveller.gender.upper()]),
            UserInterfaceTableRow(["E-mailadres", traveller.email_address]),
            UserInterfaceTableRow(["Rijbewijs nummer", traveller.driving_license_number]),

            UserInterfaceTableRow(["Telefoonnummer", traveller.phone_number]),
            UserInterfaceTableRow(["Straatnaam", traveller.street_name]),
            UserInterfaceTableRow(["Huisnummer", traveller.house_number]),
            UserInterfaceTableRow(["Postcode", traveller.zip_code]),
            UserInterfaceTableRow(["Stad", traveller.city])
        ]

        ui = UserInterfaceFlow()
        ui.add(UserInterfaceAlert("Traveller " + traveller.first_name + " " + traveller.last_name, Color.HEADER))
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
            self.update_traveller(traveller)

        elif selected.upper() == "D":
            self.delete_traveller(traveller)

        self.list_travellers()

    @Auth.permission_required(Permission.TravellerCreate)
    def add_traveller(self):

        ui = UserInterfaceFlow()
        ui.add(UserInterfaceAlert(text="Traveller toevoegen", color=Color.HEADER))

        ui = TravellerForm.get_form(ui, None)

        fields = ui.run()

        traveller = Traveller()
        traveller.populate(list(fields.values()), list(fields.keys()))

        LogRepository.log(LogType.TravellerCreated, f"id: {traveller.id} name: {traveller.first_name} {traveller.last_name}")

        TravellerRepository.persist_traveller(traveller)

        IndexService.index_database()

        UserInterfaceFlow.quick_run(
            UserInterfaceAlert("Traveller toegevoegd", Color.OKGREEN),
            2
        )

    @Auth.permission_required(Permission.TravellerUpdate)
    def update_traveller(self, traveller: Traveller):

        ui = UserInterfaceFlow()
        ui.add(UserInterfaceAlert(text="Traveller " + traveller.first_name + " " + traveller.last_name + " wijziging",
                                  color=Color.OKBLUE))
        ui.add(UserInterfaceAlert(text=f"Druk op enter om waarde niet te wijzigingen", color=Color.OKCYAN))

        ui = TravellerForm.get_form(ui, traveller)

        fields = ui.run()

        traveller.populate(list(fields.values()), list(fields.keys()))

        TravellerRepository.update_traveller(traveller)

        LogRepository.log(LogType.TravellerUpdated, f"id: {traveller.id} name: {traveller.first_name} {traveller.last_name}")

        IndexService.index_database()

        UserInterfaceFlow.quick_run(
            UserInterfaceAlert("Traveller geüpdatet", Color.OKGREEN),
            2
        )

    @Auth.permission_required(Permission.TravellerDelete)
    def delete_traveller(self, traveller: Traveller):

        TravellerRepository.delete_traveller(traveller)

        LogRepository.log(LogType.TravellerDeleted, f"name: {traveller.first_name} {traveller.last_name}")

        IndexService.index_database()

        UserInterfaceFlow.quick_run(
            UserInterfaceAlert("Traveller verwijderd", Color.OKGREEN),
            2
        )
