import logging

from DB_RBT import DataBase

from rbtree import RBTree, TreeDrawer


class Facade:
    """
    Класс шаблона проектирования
    """
    def __init__(self, name='DB_RBT.db'):
        """
        создание БД, запись в БД, запись элементов из БД в структуру дерева
        """
        self.data_wait_for_save = False
        self.rbmodel = RBTree()
        self.DB = DataBase(name)
        self.drawer = TreeDrawer()

    def save_data(self):
        path = [str(x.key) for x in self.drawer._preorder(self.drawer.tree)]
        if path != None:
            self.DB.save_tree(float(path))
            logging.log(logging.INFO, ' данные добавлены в бд')
        else:
            logging.log(logging.INFO, ' нет несохраненных данных')

    def get_tree_from_db(self):
        """
        Запись элементов из БД в структуру дерева
        """
        keys = self.DB.get_keys_db()
        if keys != []:
            for a in keys:
                self.drawer.insert(int(a[0]))