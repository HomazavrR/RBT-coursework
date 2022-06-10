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

    def get_from_db(self):
        """
        Возвращает значения из БД в переменной elems
        """
        sql = self.db.cursor()
        elems = [value for value in sql.execute(f"SELECT * FROM RB_tree")]
        if not elems:
            logging.log(logging.INFO, ' БД пуста')
        sql.close()
        return elems

    def del_all(self):
        """
        Удаляет все данные в базе данных.
        """
        cur = self.db.cursor()
        cur.execute("DELETE from RB_tree")
        self.db.commit()

    def db_insert(self, key):
        """
        Функция для вставки данных в базу данных
        """
        cur = self.db.cursor()
        cur.execute("INSERT INTO RB_tree VALUES (?)", (key))
        self.db.commit()
        cur.close()

    def save_tree(self, path):
        """
        Переписывает новые данные в БД поверх старых
        """
        self.del_all()
        for val in path:
            self.db_insert(val[0])