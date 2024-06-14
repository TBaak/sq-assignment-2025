import random
from datetime import datetime

from Debug.ConsoleLogger import ConsoleLogger
from Models.Member import Member
from Repository.BaseClasses.DBRepository import DBRepository
from Service.IndexService import IndexService


class MemberRepository:

    @staticmethod
    def find_all(ids: list[int] = None) -> list[Member]:
        db = DBRepository.create_connection()
        cursor = db.cursor()

        if ids is not None:
            cursor.execute('SELECT * FROM member WHERE id IN (%s)' % ','.join('?' * len(ids)), ids)
        else:
            cursor.execute("SELECT * FROM member")

        result = cursor.fetchall()

        cursor.close()
        db.close()

        members = []

        for memberData in result:
            member = Member(is_encrypted=True)
            member.populate(memberData, ['id', 'firstName', 'lastName', 'age', 'weight', 'gender', 'streetName',
                                         'houseNumber', 'city', 'zipCode', 'emailAddress', 'phoneNumber', 'number'])
            member.decrypt()
            members.append(member)

        return members

    @staticmethod
    def find_by_query(query: str):
        if query == "":
            return MemberRepository.find_all()

        member_ids = IndexService.find_member_by_query(query)

        if len(member_ids) == 0:
            return []

        return MemberRepository.find_all(member_ids)



    @staticmethod
    def persist_member(member: Member):
        db = DBRepository.create_connection()
        cursor = db.cursor()

        member.number = MemberRepository.generate_member_number()

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
            "phoneNumber,"
            "number"
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
            ":phoneNumber,"
            ":number"
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

    @staticmethod
    def generate_member_number():
        year_last_two_digits = str(datetime.now().year)[2:]

        random_number = str(random.randint(1000000, 9999999))

        numbers = (year_last_two_digits + random_number)

        check_digit = sum(map(lambda x: int(x), [*numbers])) % 10

        return numbers + str(check_digit)