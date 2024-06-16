from Debug.ConsoleLogger import ConsoleLogger
from Enum.Color import Color
from Enum.LogType import LogType
from Form.MemberForm import MemberForm
from Models.Member import Member
from Repository.LogRepository import LogRepository
from Repository.MemberRepository import MemberRepository
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


class MemberController:

    @Auth.permission_required(Permission.MemberRead)
    def list_members(self, members: list[Member] = None):

        UserInterfaceFlow.quick_run_till_next(
            UserInterfaceAlert("Member overzicht aan het laden...", Color.HEADER)
        )

        LogRepository.log(LogType.MembersRead)

        if members is None:
            members = MemberRepository.find_all()

        rows = map(lambda m: [m.number, m.firstName, m.lastName, m.age, m.emailAddress,
                              m.streetName + " " + m.houseNumber], members)
        rows = list(rows)

        for index, row in enumerate(rows):
            row.insert(0, index + 1)

        rows = list(map(lambda m_row: UserInterfaceTableRow(m_row), rows))

        rows.insert(0, UserInterfaceTableRow(
            ["#", "Member nummer", "Voornaam", "Achternaam", "Leeftijd", "E-mailadres", "Adres"]))

        ui = UserInterfaceFlow()
        ui.add(UserInterfaceAlert("Member overzicht" if members is None else "Zoekresultaten", Color.HEADER))
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
            return self.search_members()

        if selected.isdigit() is False:
            UserInterfaceFlow.quick_run(
                UserInterfaceAlert("Ongeldige keuze", Color.FAIL),
                1
            )
            return self.list_members()

        member_index = int(selected) - 1

        self.show_member(members[member_index]) # TODO: Handle out of bounds

        return self.list_members()

    @Auth.permission_required(Permission.MemberRead)
    def search_members(self):

        LogRepository.log(LogType.MembersRead)

        query_ui = UserInterfaceFlow()
        query_ui.add(UserInterfacePrompt(
            prompt_text="Zoeken op naam, leeftijd, e-mailadres, adres of member nummer",
            memory_key="query",
            validations=[NoSpecialCharsValidation()]
        )
        )
        query = query_ui.run()['query']

        members = MemberRepository.find_by_query(query)

        if len(members) == 0:
            UserInterfaceFlow.quick_run(
                UserInterfaceAlert("Geen resultaten gevonden", Color.FAIL),
                2
            )
            return self.list_members()

        return self.list_members(members)

    @Auth.permission_required(Permission.MemberRead)
    def show_member(self, member: Member):

        LogRepository.log(LogType.MemberRead)

        rows = [
            UserInterfaceTableRow(["Nummer", member.number]),
            UserInterfaceTableRow(["Voornaam", member.firstName]),
            UserInterfaceTableRow(["Achternaam", member.lastName]),
            UserInterfaceTableRow(["Leeftijd", member.age]),
            UserInterfaceTableRow(["Gewicht", member.weight]),

            UserInterfaceTableRow(["Geslacht", member.gender.upper()]),
            UserInterfaceTableRow(["E-mailadres", member.emailAddress]),

            UserInterfaceTableRow(["Telefoonnummer", member.phoneNumber]),
            UserInterfaceTableRow(["Straatnaam", member.streetName]),
            UserInterfaceTableRow(["Huisnummer", member.houseNumber]),
            UserInterfaceTableRow(["Postcode", member.zipCode]),
            UserInterfaceTableRow(["Stad", member.city])
        ]

        ui = UserInterfaceFlow()
        ui.add(UserInterfaceAlert("Member " + member.firstName + " " + member.lastName, Color.HEADER))
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
            self.update_member(member)

        elif selected.upper() == "D":
            self.delete_member(member)

        self.list_members()

    @Auth.permission_required(Permission.MemberCreate)
    def add_member(self):

        ui = UserInterfaceFlow()
        ui.add(UserInterfaceAlert(text="Member toevoegen", color=Color.HEADER))

        ui = MemberForm.get_form(ui, None)

        fields = ui.run()

        member = Member()
        member.populate(list(fields.values()), list(fields.keys()))

        LogRepository.log(LogType.MemberCreated, f"id: {member.id} name: {member.firstName} {member.lastName}")

        MemberRepository.persist_member(member)

        IndexService.index_database()

        UserInterfaceFlow.quick_run(
            UserInterfaceAlert("Member toegevoegd", Color.OKGREEN),
            2
        )

    @Auth.permission_required(Permission.MemberUpdate)
    def update_member(self, member: Member):

        ui = UserInterfaceFlow()
        ui.add(UserInterfaceAlert(text="Member " + member.firstName + " " + member.lastName + " wijziging",
                                  color=Color.OKBLUE))
        ui.add(UserInterfaceAlert(text=f"Druk op enter om waarde niet te wijzigingen", color=Color.OKCYAN))

        ui = MemberForm.get_form(ui, member)

        fields = ui.run()

        member.populate(list(fields.values()), list(fields.keys()))

        MemberRepository.update_member(member)

        LogRepository.log(LogType.MemberUpdated, f"id: {member.id} name: {member.firstName} {member.lastName}")

        IndexService.index_database()

        UserInterfaceFlow.quick_run(
            UserInterfaceAlert("Member geüpdatet", Color.OKGREEN),
            2
        )

    @Auth.permission_required(Permission.MemberDelete)
    def delete_member(self, member: Member):

        MemberRepository.delete_member(member)

        LogRepository.log(LogType.MemberDeleted, f"name: {member.firstName} {member.lastName}")

        IndexService.index_database()

        UserInterfaceFlow.quick_run(
            UserInterfaceAlert("Member verwijderd", Color.OKGREEN),
            2
        )
