from Models.Member import Member
from Repository.MemberRepository import MemberRepository


class CreateMemberTest:

    @staticmethod
    def run():
        member = Member()
        member.firstName = "John"
        member.lastName = "Doe"
        member.age = "25"
        member.weight = "75"
        member.phoneNumber = "0612345678"
        member.emailAddress = "tom@qbana.nl"
        member.streetName = "Kerkstraat"
        member.houseNumber = "1"
        member.city = "Amsterdam"
        member.zipCode = "1234AB"
        member.gender = "m"

        MemberRepository.persist_member(member)