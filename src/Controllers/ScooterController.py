from datetime import datetime

from Enum.Color import Color
from Enum.LogType import LogType

from Form.ScooterFormFull import ScooterFormFull
from Form.ScooterFormPartial import ScooterFormPartial
from Models.Scooter import Scooter
from Repository.LogRepository import LogRepository
from Repository.ScooterRepository import ScooterRepository
from Security.AuthorizationDecorator import Auth
from Security.AuthorizationService import AuthorizationService
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


class ScooterController:

    @Auth.permission_required(Permission.ScooterRead)
    def list_scooters(self, scooters: list[Scooter] = None):

        UserInterfaceFlow.quick_run_till_next(
            UserInterfaceAlert("Scooter overzicht aan het laden...", Color.HEADER)
        )

        LogRepository.log(LogType.ScooterRead)

        if scooters is None:
            scooters = ScooterRepository.find_all()

        rows = map(lambda s: [s.brand, s.model, s.serial_number, s.state_of_charge,
                              "Ja" if s.out_of_service_status == 'y' else "Nee"], scooters)
        rows = list(rows)

        for index, row in enumerate(rows):
            row.insert(0, index + 1)

        rows = list(map(lambda m_row: UserInterfaceTableRow(m_row), rows))

        rows.insert(0, UserInterfaceTableRow(
            ["#", "Merk", "Model", "Serienummer", "Batterij percentage", "In dienst"]))

        ui = UserInterfaceFlow()
        ui.add(UserInterfaceAlert("Scooter overzicht" if scooters is None else "Zoekresultaten", Color.HEADER))
        ui.add(UserInterfaceTable(rows=rows, has_header=True))
        ui.add(UserInterfacePrompt(
            prompt_text="Geef het nummer om te bekijken of druk op Z om te zoeken of druk op ENTER om terug te gaan",
            memory_key="action"
        )
        )
        selection = ui.run()

        selected = selection["action"]

        if selected == "":
            return None

        if selected.upper() == "Z":
            return self.search_scooters()

        if selected.isdigit() is False:
            UserInterfaceFlow.quick_run(
                UserInterfaceAlert("Ongeldige keuze", Color.FAIL),
                1
            )
            return self.list_scooters()

        index = int(selected) - 1

        try:
            self.show_scooter(scooters[index])
            return None
        except IndexError:
            UserInterfaceFlow.quick_run(
                UserInterfaceAlert("Ongeldige keuze", Color.FAIL),
                1
            )
            return None

    @Auth.permission_required(Permission.ScooterRead)
    def search_scooters(self):

        LogRepository.log(LogType.ScooterRead)

        query_ui = UserInterfaceFlow()
        query_ui.add(UserInterfacePrompt(
            prompt_text="Zoeken op merk, model, serienummer",
            memory_key="query",
            validations=[NoSpecialCharsValidation()]
        )
        )
        query = query_ui.run()['query']

        scooters = ScooterRepository.find_by_query(query)

        if len(scooters) == 0:
            UserInterfaceFlow.quick_run(
                UserInterfaceAlert("Geen resultaten gevonden", Color.FAIL),
                2
            )
            return self.list_scooters()

        return self.list_scooters(scooters)

    @Auth.permission_required(Permission.ScooterRead)
    def show_scooter(self, scooter: Scooter):

        LogRepository.log(LogType.ScooterRead)

        rows = [
            UserInterfaceTableRow(["Merk", scooter.brand]),
            UserInterfaceTableRow(["Model", scooter.model]),
            UserInterfaceTableRow(["Serienummer", scooter.serial_number]),
            UserInterfaceTableRow(["Maximale snelheid", scooter.top_speed]),
            UserInterfaceTableRow(["Batterij capaciteit (Wh)", scooter.battery_capacity]),
            UserInterfaceTableRow(["Huidige batterij percentage (0-100)", scooter.state_of_charge]),
            UserInterfaceTableRow(["Doel batterij percentage", scooter.target_range_soc_min + ' - ' + scooter.target_range_soc_max]),
            UserInterfaceTableRow(["Locatie", scooter.location_lat + ', ' + scooter.location_lng]),
            UserInterfaceTableRow(["In dienst", "Ja" if scooter.out_of_service_status == 'y' else "Nee"]),
            UserInterfaceTableRow(["Kilometerstand", scooter.mileage]),
            UserInterfaceTableRow(["Datum laatste onderhoud", scooter.last_maintenance]),
            UserInterfaceTableRow(["Datum in dienst", scooter.in_service_date]),
        ]

        ui = UserInterfaceFlow()
        ui.add(UserInterfaceAlert("Scooter " + scooter.brand + " " + scooter.model + scooter.serial_number, Color.HEADER))
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
            self.update_scooter(scooter)

        elif selected.upper() == "D":
            self.delete_scooter(scooter)

        self.list_scooters()

    @Auth.permission_required(Permission.ScooterCreate)
    def add_scooter(self):

        ui = UserInterfaceFlow()
        ui.add(UserInterfaceAlert(text="Scooter toevoegen", color=Color.HEADER))

        if AuthorizationService.current_user_has_permission(Permission.ScooterUpdateFull):
            ui = ScooterFormFull.get_form(ui, None)
        else:
            ui = ScooterFormPartial.get_form(ui, None)

        fields = ui.run()

        parts = fields['location'].split()
        lat = float(parts[0])
        lng = float(parts[1])

        fields['location_lat'] = str(lat)
        fields['location_lng'] = str(lng)
        fields['in_service_date'] = datetime.now().strftime("%d-%m-%Y")

        scooter = Scooter()
        scooter.populate(list(fields.values()), list(fields.keys()))

        LogRepository.log(LogType.ScooterCreated, f"{scooter.serial_number}")

        ScooterRepository.persist_scooter(scooter)

        IndexService.index_database()

        UserInterfaceFlow.quick_run(
            UserInterfaceAlert("Scooter toegevoegd", Color.OKGREEN),
            2
        )

    @Auth.permission_required(Permission.ScooterUpdate)
    def update_scooter(self, scooter: Scooter):

        ui = UserInterfaceFlow()
        ui.add(UserInterfaceAlert(text="Scooter " + scooter.brand + " " + scooter.model + scooter.serial_number + " wijziging",
                                  color=Color.OKBLUE))
        ui.add(UserInterfaceAlert(text=f"Druk op enter om waarde niet te wijzigingen", color=Color.OKCYAN))

        if AuthorizationService.current_user_has_permission(Permission.ScooterUpdateFull):
            ui = ScooterFormFull.get_form(ui, scooter)
        else:
            ui = ScooterFormPartial.get_form(ui, scooter)

        fields = ui.run()

        scooter.populate(list(fields.values()), list(fields.keys()))

        if AuthorizationService.current_user_has_permission(Permission.ScooterUpdateFull):
            ScooterRepository.update_scooter_full(scooter)
        else:
            ScooterRepository.update_scooter_partial(scooter)

        LogRepository.log(LogType.ScooterUpdated, f"id: {scooter.id}")

        IndexService.index_database()

        UserInterfaceFlow.quick_run(
            UserInterfaceAlert("Scooter geüpdatet", Color.OKGREEN),
            2
        )

    @Auth.permission_required(Permission.ScooterDelete)
    def delete_scooter(self, scooter: Scooter):

        ScooterRepository.delete_scooter(scooter)

        LogRepository.log(LogType.ScooterDeleted, f"id: {scooter.serial_number}")

        IndexService.index_database()

        UserInterfaceFlow.quick_run(
            UserInterfaceAlert("Scooter verwijderd", Color.OKGREEN),
            2
        )
