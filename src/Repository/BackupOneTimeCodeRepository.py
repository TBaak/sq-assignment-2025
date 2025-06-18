from typing import Optional

from Enum.LoginError import LoginError
from Models.BackupOneTimeCode import BackupOneTimeCode
from Models.User import User
from Repository.BaseClasses.DBRepository import DBRepository
from Security.SecurityHelper import SecurityHelper
from Service.IndexService import IndexService


class BackupOneTimeCodeRepository:

    @staticmethod
    def find_by_code(code: str) -> (Optional[User], Optional[LoginError]):
        db = DBRepository.create_connection()
        cursor = db.cursor()

        code_id = IndexService.find_otc_by_code(code)

        if code_id is None:
            return None, LoginError.NotFound

        otc = SecurityHelper.get_logged_in_user()

        found_otc = cursor.execute(
            "SELECT id, one_time_code, backup_name, user_id "
            "FROM backup_one_time_codes "
            "WHERE id = :code_id AND user_id = :user_id "
            "LIMIT 1",
            {"code_id": code_id, "user_id": otc.id}
        )

        values = found_otc.fetchone()

        otc = BackupOneTimeCode(is_encrypted=True)
        otc.populate(values, ['id', 'one_time_code', 'backup_name', 'user_id'])
        otc.decrypt()

        return otc, None

    @staticmethod
    def find_all():
        db = DBRepository.create_connection()
        cursor = db.cursor()

        cursor.execute("SELECT id, one_time_code, backup_name, user_id FROM backup_one_time_codes")
        result = cursor.fetchall()

        cursor.close()
        db.close()

        otcs = []

        for otcData in result:
            otc = BackupOneTimeCode(is_encrypted=True)
            otc.populate(otcData, ['id', 'one_time_code', 'backup_name', 'user_id'])
            otc.decrypt()
            otcs.append(otc)

        return otcs

    @staticmethod
    def persist_otc(otc: BackupOneTimeCode):
        db = DBRepository.create_connection()
        cursor = db.cursor()

        otc.encrypt()

        cursor.execute(
            "INSERT INTO backup_one_time_codes (one_time_code, backup_name, user_id) "
            "VALUES (:one_time_code, :backup_name, :user_id)",
            otc.serialize()
        )

        db.commit()

        cursor.close()
        db.close()

    @staticmethod
    def delete_otc(otc: BackupOneTimeCode):
        db = DBRepository.create_connection()
        cursor = db.cursor()

        cursor.execute(
            "DELETE FROM backup_one_time_codes WHERE id = :id",
            otc.serialize()
        )

        db.commit()

        cursor.close()
        db.close()
