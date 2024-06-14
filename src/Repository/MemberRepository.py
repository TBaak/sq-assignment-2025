from Debug.ConsoleLogger import ConsoleLogger
from Models.Member import Member
from Repository.BaseClasses.DBRepository import DBRepository


class MemberRepository:

    @staticmethod
    def find_all() -> list[Member]:
        db = DBRepository.create_connection()
        cursor = db.cursor()

        cursor.execute("SELECT * FROM member")
        result = cursor.fetchall()

        cursor.close()
        db.close()

        members = []

        for memberData in result:
            member = Member(is_encrypted=True)
            member.populate(memberData, ['id', 'firstName', 'lastName', 'age', 'weight', 'gender', 'streetName',
                                         'houseNumber', 'city', 'zipCode', 'emailAddress', 'phoneNumber'])
            member.decrypt()
            members.append(member)

        return members

    @staticmethod
    def persist_member(member: Member):
        db = DBRepository.create_connection()
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
            ");",
            member.serialize()
        )

        ConsoleLogger.vv("Created member: " + str(member.serialize()))

        db.commit()

        cursor.close()
        db.close()

    @staticmethod
    def update_member(member):
        db = DBRepository.create_connection()
        cursor = db.cursor()

        member.encrypt()

        cursor.execute(
            "UPDATE member SET "
            "firstName = :firstName,"
            "lastName = :lastName,"
            "age = :age,"
            "weight = :weight,"
            "gender = :gender,"
            "streetName = :streetName,"
            "houseNumber = :houseNumber,"
            "city = :city,"
            "zipCode = :zipCode,"
            "emailAddress = :emailAddress,"
            "phoneNumber = :phoneNumber "
            "WHERE id = :id",
            member.serialize()
        )

        ConsoleLogger.vv("Updated member: " + str(member.serialize()))

        db.commit()

        cursor.close()
        db.close()

    @staticmethod
    def delete_member(member):
        db = DBRepository.create_connection()
        cursor = db.cursor()

        member.encrypt()

        cursor.execute(
            "DELETE FROM member WHERE id = :id",
            member.serialize()
        )

        ConsoleLogger.vv("Deleted member: " + str(member.id))

        db.commit()

        cursor.close()
        db.close()
