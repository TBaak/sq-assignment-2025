from Enum.Color import Color
from Form.MemberForm import MemberForm
from Helpers.UserHelper import UserHelper
from Models.Member import Member
from Repository.MemberRepository import MemberRepository
from Service.IndexService import IndexService
from View.UserInterfaceAlert import UserInterfaceAlert
from View.UserInterfaceFlow import UserInterfaceFlow
from View.UserInterfacePrompt import UserInterfacePrompt
from View.UserInterfaceTable import UserInterfaceTable
from View.UserInterfaceTableRow import UserInterfaceTableRow
from View.Validations.EmailValdation import EmailValidation
from View.Validations.GenderValidation import GenderValidation
from View.Validations.LengthValdation import LengthValidation
from View.Validations.NotBlankValdation import NotBlankValidation
from View.Validations.NumberValdation import NumberValidation
from View.Validations.OnlyLetterValdation import OnlyLetterValidation
from View.Validations.OnlyNumberValdation import OnlyNumberValidation
from View.Validations.ZipcodeValdation import ZipcodeValidation


class MemberController:

    def list_members(self):
        members = MemberRepository.find_all()

        rows = map(lambda m: [m.firstName, m.lastName, m.age, m.emailAddress,
                              m.streetName + " " + m.houseNumber], members)
        rows = list(rows)

        for index, row in enumerate(rows):
            row.insert(0, index + 1)

        rows = list(map(lambda m_row: UserInterfaceTableRow(m_row), rows))

        rows.insert(0, UserInterfaceTableRow(
            ["#", "Voornaam", "Achternaam", "Leeftijd", "E-mailadres", "Adres"]))

        ui = UserInterfaceFlow()
        ui.add(UserInterfaceAlert("Member overzicht", Color.HEADER))
        ui.add(UserInterfaceTable(rows=rows, has_header=True))
        ui.add(UserInterfacePrompt(
            prompt_text="Geef het nummer om te bekijken of druk op ENTER om terug te gaan",
            memory_key="action",
            validations=[NumberValidation()]
        )
        )
        selection = ui.run()

        selected = selection["action"]

        if selected == "":
            return

        member_index = int(selected) - 1

        self.show_member(members[member_index])

        return self.list_members()

    def show_member(self, member: Member):

        rows = [
            UserInterfaceTableRow(["ID", member.id]),
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

    def add_member(self):
        UserHelper.has_permission(None)  # TODO: Implement this

        ui = UserInterfaceFlow()
        ui.add(UserInterfaceAlert(text="Member toevoegen", color=Color.OKBLUE))

        ui = MemberForm.get_form(ui, None)

        fields = ui.run()

        member = Member()
        member.populate(list(fields.values()), list(fields.keys()))

        MemberRepository.persist_member(member)

        IndexService.index_database()

        UserInterfaceFlow.quick_run(
            UserInterfaceAlert("Member toegevoegd", Color.OKGREEN),
            2
        )

    def update_member(self, member: Member):
        UserHelper.has_permission(None)  # TODO: Implement this

        ui = UserInterfaceFlow()
        ui.add(UserInterfaceAlert(text="Member " + member.firstName + " " + member.lastName + " wijziging", color=Color.OKBLUE))

        ui = MemberForm.get_form(ui, member)

        fields = ui.run()

        member.populate(list(fields.values()), list(fields.keys()))

        MemberRepository.update_member(member)

        IndexService.index_database()

        UserInterfaceFlow.quick_run(
            UserInterfaceAlert("Member geüpdatet", Color.OKGREEN),
            2
        )

    def delete_member(self, member: Member):
        UserHelper.has_permission(None)  # TODO: Implement this

        MemberRepository.delete_member(member)

        IndexService.index_database()

        UserInterfaceFlow.quick_run(
            UserInterfaceAlert("Member verwijderd", Color.OKGREEN),
            2
        )

