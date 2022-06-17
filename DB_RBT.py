import sqlite3
import logging
logging.basicConfig(level=logging.INFO)

class DataBase:
    """
    Класс с функциями для взаимодействий с БД
    """
    def __init__(self, name):
        """
        Создает базу данных

        """
        self.db = sqlite3.connect(f"{name}")
        sql = self.db.cursor()
        sql.execute("""CREATE TABLE IF NOT EXISTS RB_tree ( 
            key integer
        )""")
        self.db.commit()
        sql.close()

    def get_keys_db(self):
        """
        Возвращает значения из БД в переменной keys
        """
        sql = self.db.cursor()
        keys = [value for value in sql.execute(f"SELECT * FROM RB_tree")]
        if not keys:
            logging.log(logging.INFO, ' БД пуста')
        sql.close()
        return keys

    def clear_bd(self):
        """
        Удаляет все данные в БД
        """
        cur = self.db.cursor()
        cur.execute("DELETE from RB_tree")
        self.db.commit()

    def ins_db(self, key):
        """
        Функция для вставки данных в БД
        """
        cur = self.db.cursor()
        cur.execute("INSERT INTO RB_tree VALUES (?)", (key))
        self.db.commit()
        cur.close()

    def save_tree(self, path):
        """
        Переписывает новые данные в БД поверх старых
        """
        self.clear_bd()
        for val in path:
            self.ins_db(val[0])