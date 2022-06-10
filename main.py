import sys
import time
from facade import Facade
from PyQt5 import QtWidgets




class Window(QtWidgets.QDialog):
    """
    Этот класс создает главное окно
    """
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self._init_tree_drawer()
        self._init_ui(self.tree_drawer.canvas)
        self.facade = facade

    def _center(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def _init_ui(self, canvas):
        self.setWindowTitle('Красно-черное дерево поиска | Терещенко Карина, ИСП-31-19')
        # Управление деревом
        tree_mng_groupbox = QtWidgets.QGroupBox("Управление")
        tree_mng_layout = QtWidgets.QHBoxLayout()

        key_label = QtWidgets.QLabel('Key:')
        self.key_input = QtWidgets.QLineEdit()
        self.add_btn = QtWidgets.QPushButton('Добавить')
        self.remove_btn = QtWidgets.QPushButton('Удалить')
        self.search_btn = QtWidgets.QPushButton('Поиск')
        self.timer_label = QtWidgets.QLabel('Время поиска: XXX sec')

        self.add_btn.clicked.connect(self._add_btn_handler)
        self.remove_btn.clicked.connect(self._remove_btn_handler)
        self.search_btn.clicked.connect(self._search_btn_handler)

        tree_mng_layout.addWidget(key_label)
        tree_mng_layout.addWidget(self.key_input)
        tree_mng_layout.addWidget(self.add_btn)
        tree_mng_layout.addWidget(self.remove_btn)
        tree_mng_layout.addWidget(self.search_btn)
        tree_mng_layout.addWidget(self.timer_label)

        tree_mng_groupbox.setLayout(tree_mng_layout)

        io_groupbox = QtWidgets.QGroupBox("Взаимодействие с базой данных")
        io_layout = QtWidgets.QHBoxLayout()

        self.export_btn = QtWidgets.QPushButton('Сохранить')
        self.import_btn = QtWidgets.QPushButton('Загрузить')

        io_layout.addWidget(self.export_btn)
        io_layout.addWidget(self.import_btn)

        self.import_btn.clicked.connect(lambda:self.facade.get_tree_from_db())
        self.export_btn.clicked.connect(lambda:self.facade.save_data())

        io_groupbox.setLayout(io_layout)

        # Устанавливаю главный лейаут
        layout = QtWidgets.QVBoxLayout()

        layout.addWidget(canvas)
        controls_layout = QtWidgets.QHBoxLayout()
        controls_layout.addWidget(tree_mng_groupbox)
        controls_layout.addWidget(io_groupbox)
        layout.addLayout(controls_layout)
        self.setLayout(layout)
        self._center()

    def _init_tree_drawer(self):
        self.tree_drawer = facade.drawer

    def _add_btn_handler(self):
        if len(self.key_input.text()) == 0:
            return
        try:
            key = int(self.key_input.text())
            self.tree_drawer.insert(key)
            self.key_input.clear()
        except ValueError:
            self._show_error('Неверный тип данных', 'Введите натуральное число!')

    def _remove_btn_handler(self):
        if len(self.key_input.text()) == 0:
            return
        try:
            key = int(self.key_input.text())
            self.tree_drawer.remove(key)
            self.key_input.clear()
        except ValueError:
            self._show_error('Неверный тип данных', 'Введите натуральное число!')

    def _search_btn_handler(self):
        if len(self.key_input.text()) == 0:
            return

        key = None
        try:
            key = int(self.key_input.text())
            start_time = time.time()
            self.tree_drawer.search(key)
            exec_time = time.time() - start_time
            self.key_input.clear()
            self.timer_label.setText('Время поиска: %f sec' % exec_time)
        except ValueError:
            self._show_error('Неверный тип данных', 'Введите натуральное число!')

    def _export_btn_handler(self):
        fname = QtWidgets.QFileDialog.getSaveFileName(self, 'Export RBTree', 'mytree.rbtree',
                                                      'Red-Black Tree files (*.rbtree)')[0]
        if fname:
            with open(fname, 'wb') as f:
                pickle.dump(self.tree_drawer.tree, f)

    def _import_btn_handler(self):
        fname = QtWidgets.QFileDialog.getOpenFileName(self, 'Import RBTree', '',
                                                      'Red-Black Tree files (*.rbtree)')[0]
        if fname:
            with open(fname, 'rb') as f:
                self.tree_drawer.tree = pickle.load(f)
            self.tree_drawer.plot()

    def _show_error(self, title, message):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg.exec_()
        self.key_input.clear()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    facade = Facade()
    main = Window()
    main.show()

    sys.exit(app.exec_())