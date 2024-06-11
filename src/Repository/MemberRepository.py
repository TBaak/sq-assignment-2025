from Models.Member import Member
from Repository.Repository import Repository


class MemberRepository:

    @staticmethod
    def persist_member(member: Member):
        db = Repository.create_connection()
        cursor = db.cursor()

        member.encrypt()

        cursor.execute(
            "INSERT INTO member ("
            "firstName,"
            "lastName,"
            "age,"
            "weight,"
            "gender,"
            "streetName,"
            "houseNumber,"
            "city,"
            "zipCode,"
            "emailAddress,"
            "phoneNumber"
            ") VALUES ("
            ":firstName,"
            ":lastName,"
            ":age,"
            ":weight,"
            ":gender,"
            ":streetName,"
            ":houseNumber,"
            ":city,"
            ":zipCode,"
            ":emailAddress,"
            ":phoneNumber"
            ")",
            member.serialize()
        )

        db.commit()

        cursor.close()
        db.close()
