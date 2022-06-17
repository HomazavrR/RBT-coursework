import collections
import networkx as nx

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class Node:
    """Узел красно-чёрного дерева"""

    def __init__(self, key):
        self.left = None
        self.right = None
        self.parent = None
        self.key = key
        self.color = 'r'


class RBTree:
    """Красно-черное дерево"""

    def __init__(self, *args):
        self.root = None

        if len(args) == 1:
            if isinstance(args[0], collections.Iterable):
                for x in args[0]:
                    self.insert(x)
            else:
                raise TypeError(str(args[0]) + " is not iterable")

    def get_node(self, key, *args):
        """Возвращает узел по ключу."""

        if len(args) == 0:
            start = self.root
        else:
            start = args[0]

        if not start:
            return None
        if key == start.key:
            return start
        elif key > start.key:
            return self.get_node(key, start.right)
        else:
            return self.get_node(key, start.left)

    def get_path(self, node):
        """Обходит дерево"""

        curr = node
        lst = [curr.key]
        while curr.parent is not None:
            curr = curr.parent
            lst.append(curr.key)

        return reversed(lst)

    def insert(self, key, *args):
        """Вставка узла"""
        if not isinstance(key, int):
            raise TypeError(str(key) + " is not an int")
        else:
            if not self.root:
                self.root = Node(key)
                self.root.color = 'k'
            elif len(args) == 0:
                if not self.get_node(key):
                    self.insert(key, self.root)
            else:
                child = Node(key)
                parent = args[0]
                if child.key > parent.key:
                    if not parent.right:
                        parent.right = child
                        child.parent = parent
                        if parent.color == 'r':
                            self._insert_case_one(child)
                    else:
                        self.insert(key, parent.right)
                else:
                    if not parent.left:
                        parent.left = child
                        child.parent = parent
                        if parent.color == 'r':
                            self._insert_case_one(child)
                    else:
                        self.insert(key, parent.left)

    def _insert_case_one(self, child):
        if not child.parent:
            self.root.color = 'k'
        else:
            self._insert_case_two(child)

    def _insert_case_two(self, child):
        if child.parent.color == 'r':
            self._insert_case_three(child)

    def _insert_case_three(self, child):
        parent = child.parent
        grand_node = parent.parent

        if grand_node.left == parent:
            uncle = grand_node.right
        else:
            uncle = grand_node.left

        if uncle and uncle.color == 'r':
            grand_node.color = 'r'
            parent.color = 'k'
            uncle.color = 'k'
            self._insert_case_one(grand_node)
        else:
            self._insert_case_four(child)

    def _insert_case_four(self, child):
        parent = child.parent
        grand_node = parent.parent
        if grand_node.left == parent:
            uncle = grand_node.right
        else:
            uncle = grand_node.left

        if grand_node.left == parent and parent.right == child:
            self._rotate_left(parent)
            child = child.left
        elif grand_node.right == parent and parent.left == child:
            self._rotate_right(parent)
            child = child.right

        self._insert_case_five(child)

    def _insert_case_five(self, child):
        parent = child.parent
        grand_node = parent.parent
        if grand_node.left == parent:
            uncle = grand_node.right
        else:
            uncle = grand_node.left

        if parent.left == child:
            grand_node.color = 'r'
            parent.color = 'k'
            self._rotate_right(grand_node)
        elif parent.right == child:
            grand_node.color = 'r'
            parent.color = 'k'
            self._rotate_left(grand_node)

    def _rotate_left(self, pivot):
        old_root = pivot
        parent = old_root.parent

        new_root = old_root.right
        temp = new_root.right
        old_root.right = new_root.left

        if old_root.right:
            old_root.right.parent = old_root
        new_root.left = old_root
        old_root.parent = new_root

        if parent is None:
            self.root = new_root
            self.root.parent = None
        else:
            if parent.right and parent.right.key == old_root.key:
                parent.right = new_root
                new_root.parent = parent
            elif parent.left and parent.left.key == old_root.key:
                parent.left = new_root
                new_root.parent = parent

    def _rotate_right(self, pivot):
        if not pivot.left:
            pass
        else:
            old_root = pivot
            parent = old_root.parent

            new_root = old_root.left
            temp = new_root.left
            old_root.left = new_root.right

            if (old_root.left):
                old_root.left.parent = old_root

            new_root.right = old_root
            old_root.parent = new_root

            if parent is None:
                self.root = new_root
                self.root.parent = None
            else:
                if parent.right and parent.right.key == old_root.key:
                    parent.right = new_root
                    new_root.parent = parent
                elif parent.left and parent.left.key == old_root.key:
                    parent.left = new_root
                    new_root.parent = parent

    def delete(self, key):
        """Удаление ключа"""
        node = self.get_node(key, self.root)
        if node:
            if node == self.root:
                self.root = None
            elif not (node.left or node.right):
                if node.parent:
                    self._delete_leaf(node)

            elif not (node.left and node.right):
                self._delete_leaf_parent(node)

            else:
                self._delete_node(node)

    def _delete_node(self, node):
        """Удаление узла"""
        if self.get_height(node.left) > self.get_height(node.right):
            to_switch = self.get_max(node.left)
            self._switch_nodes(node, to_switch)

            if not (to_switch.right or to_switch.left):
                to_delete = self.get_max(node.left)
                self._delete_leaf(to_delete)
            else:
                to_delete = self.get_max(node.left)
                self._delete_leaf_parent(to_delete)
        else:
            to_switch = self.get_min(node.right)
            self._switch_nodes(node, to_switch)

            if not (to_switch.right or to_switch.left):
                to_delete = self.get_min(node.right)
                self._delete_leaf(to_delete)
            else:
                to_delete = self.get_min(node.right)
                self._delete_leaf_parent(to_delete)

    def get_height(self, *args):
        """Плолучаем высоту дерева"""
        if len(args) == 0:
            node = self.root
        else:
            node = args[0]

        if not node or (not node.left and not node.right):
            return 0
        else:
            return 1 + max(self.get_height(node.left), self.get_height(node.right))

    def get_max(self, *args):
        """Получаем узел с максимальным значением"""
        if len(args) == 0:
            node = self.root
        else:
            node = args[0]

        if not node.right:
            return node
        else:
            return self.get_max(node.right)

    def get_min(self, *args):
        """Получаем узел с минимальным значением"""
        if len(args) == 0:
            node = self.root
        else:
            node = args[0]

        if not node.left:
            return node
        else:
            return self.get_min(node.left)

    def _switch_nodes(self, node1, node2):
        switch1 = node1
        switch2 = node2
        temp_key = switch1.key

        if switch1.key == self.root.key:
            self.root.key = node2.key
            switch2.key = temp_key

        elif switch2.key == self.root.key:
            switch1.key = self.root.key
            self.root.key = temp_key
        else:
            switch1.key = node2.key
            switch2.key = temp_key

    def _delete_leaf_parent(self, node):
        par_node = node.parent
        node_color = node.color
        if node.left:
            child_color = node.left.color
        else:
            child_color = node.right.color

        if node.key == self.root.key:
            if node.right:
                self.root = node.right
                self.root.color = 'k'
                node.right = None
                new_node = node.right
            else:
                self.root = node.left
                self.root.color = 'k'
                node.left = None
                new_node = node.left

        else:
            if par_node.right == node:
                if node.right:
                    par_node.right = node.right
                    par_node.right.parent = par_node
                    node.right = None
                    if node_color == 'k' and child_color == 'r':
                        par_node.right.color = 'k'

                else:
                    par_node.right = node.left
                    par_node.right.parent = par_node
                    node.left = None
                    if node_color == 'k' and child_color == 'r':
                        par_node.right.color = 'k'

                new_node = par_node.right

            else:

                if node.right:
                    par_node.left = node.right
                    par_node.left.parent = par_node
                    node.right = None
                    if node_color == 'k' and child_color == 'r':
                        par_node.left.color = 'k'
                else:
                    par_node.left = node.left
                    par_node.left.parent = par_node
                    node.left = None
                    if node_color == 'k' and child_color == 'r':
                        par_node.left.color = 'k'

                new_node = par_node.left

        del node

        if node_color == 'k' and child_color == 'k':
            self._delete_case_one(new_node, par_node)

    def _delete_leaf(self, node):
        par_node = node.parent
        node_color = node.color
        new_node = None

        if par_node:
            if par_node.left == node:
                par_node.left = None
                new_node = None
            else:
                par_node.right = None
                new_node = None

            del node

        new_parent = par_node

        if node_color == 'k':
            self._delete_case_one(new_node, new_parent)

    def _delete_case_one(self, child, parent):
        if parent:
            self._delete_case_two(child, parent)

    def _delete_case_two(self, child, parent):
        node = child
        par_node = parent
        sib_node = None

        if par_node.left == node:
            sib_node = par_node.right
        elif par_node.right == node:
            sib_node = par_node.left

        if sib_node and sib_node.color == 'r':
            sib_node.color = 'k'
            par_node.color = 'r'
            if par_node.left == node:
                self._rotate_left(par_node)
            else:
                self._rotate_right(par_node)

        self._delete_case_three(node, par_node)

    def _delete_case_three(self, child, parent):
        node = child
        par_node = parent
        sib_node = None

        if par_node.left == node:
            sib_node = par_node.right
        elif par_node.right == node:
            sib_node = par_node.left

        if (sib_node and sib_node.color == 'k') or (not sib_node):
            sib_color = 'k'
        else:
            sib_color = 'r'

        if (sib_node and sib_node.left and sib_node.left.color == 'k') or (not sib_node or not sib_node.left):
            sib_left_color = 'k'
        else:
            sib_left_color = 'r'

        if (sib_node and sib_node.right and sib_node.right.color == 'k') or (not sib_node or not sib_node.right):
            sib_right_color = 'k'
        else:
            sib_right_color = 'r'

        if par_node.color == 'k' and sib_color == 'k' and sib_left_color == 'k' and sib_right_color == 'k':
            if sib_node:
                sib_node.color = 'r'
            self._delete_case_one(par_node, par_node.parent if par_node.parent else None)
        else:
            self._delete_case_four(node, par_node)

    def _delete_case_four(self, child, parent):
        node = child
        par_node = parent
        sib_node = None

        if par_node.left == node:
            sib_node = par_node.right
        elif par_node.right == node:
            sib_node = par_node.left

        if (sib_node and sib_node.color == 'k') or (not sib_node):
            sib_color = 'k'
        else:
            sib_color = 'r'

        if (sib_node and sib_node.left and sib_node.left.color == 'k') or (not sib_node or not sib_node.left):
            sib_left_color = 'k'
        else:
            sib_left_color = 'r'

        if ((sib_node and sib_node.right and sib_node.right.color == 'k') or (not sib_node or not sib_node.right)):
            sib_right_color = 'k'
        else:
            sib_right_color = 'r'

        if par_node.color == 'r' and sib_color == 'k' and sib_left_color == 'k' and sib_right_color == 'k':
            sib_node.color = 'r'
            par_node.color = 'k'
        else:
            self._delete_case_five(node, par_node)

    def _delete_case_five(self, child, parent):
        node = child
        par_node = parent
        sib_node = None

        if par_node.left == node:
            sib_node = par_node.right
        elif par_node.right == node:
            sib_node = par_node.left

        if (sib_node and sib_node.color == 'k') or (not sib_node):
            sib_color = 'k'
        else:
            sib_color = 'r'

        if (sib_node and sib_node.left and sib_node.left.color == 'k') or (not sib_node or not sib_node.left):
            sib_left_color = 'k'
        else:
            sib_left_color = 'r'

        if (sib_node and sib_node.right and sib_node.right.color == 'k') or (not sib_node or not sib_node.right):
            sib_right_color = 'k'
        else:
            sib_right_color = 'r'

        if sib_color == 'k':

            if par_node.left == node and sib_right_color == 'k' and sib_left_color == 'r':
                sib_node.color = 'r'
                sib_node.left.color = 'k'
                self._rotate_right(sib_node)
            elif par_node.right == node and sib_left_color == 'k' and sib_right_color == 'r':
                sib_node.color = 'r'
                sib_node.right.color = 'k'
                self._rotate_left(sib_node)

        self._delete_case_six(node, par_node)

    def _delete_case_six(self, child, parent):
        node = child
        par_node = parent
        sib_node = None

        if par_node.left == node:
            sib_node = par_node.right
        elif par_node.right == node:
            sib_node = par_node.left

        if (sib_node and sib_node.color == 'k') or (not sib_node):
            sib_color = 'k'
        else:
            sib_color = 'r'

        if (sib_node and sib_node.left and sib_node.left.color == 'k') or (not sib_node or not sib_node.left):
            sib_left_color = 'k'
        else:
            sib_left_color = 'r'

        if (sib_node and sib_node.right and sib_node.right.color == 'k') or (not sib_node or not sib_node.right):
            sib_right_color = 'k'
        else:
            sib_right_color = 'r'

        if par_node.left == node and sib_color == 'k' and sib_right_color == 'r':
            sib_node.color = par_node.color
            par_node.color = 'k'
            sib_node.right.color = 'k'
            self._rotate_left(par_node)
        elif par_node.right == node and sib_color == 'k' and sib_left_color == 'r':
            sib_node.color = par_node.color
            par_node.color = 'k'
            sib_node.left.color = 'k'
            self._rotate_right(par_node)

class TreeDrawer:
    """
    Класс создающий и расчитывающий красно-черное дерево
    """
    def __init__(self):
        self.tree = RBTree()
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

        pass

    def insert(self, key):
        """Вставка узла в главное окно"""
        self.tree.insert(key)
        self.plot()

    def remove(self, key):
        """Удаление узла из главного окна"""
        self.tree.delete(key)
        self.plot()

    def search(self, key):
        """Поиск узла"""
        node = self.tree.get_node(key)
        if node:
            node_path = self.tree.get_path(node)
            self.plot(self._color_search_path(node_path))

    def plot(self, search_colors=None):
        """Расчет отрисовки дерева"""
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.clear()

        if self.tree.root:

            g = nx.Graph()

            pos = self._get_pos_list(self.tree)
            nodes = [x.key for x in self._preorder(self.tree)]
            edges = self._get_edge_list(self.tree)
            labels = {x: x for x in nodes}
            if search_colors is None:
                colors = []
                try:
                    colors = self._get_color_list(self.tree)
                except AttributeError:
                    pass
            else:
                colors = search_colors

            g.add_nodes_from(nodes)
            g.add_edges_from(edges)

            max_len = len(str(self.tree.get_max().key))
            size = max_len * 200
            if len(colors) > 0:
                nx.draw_networkx_nodes(g, pos, node_size=size, node_color=colors, ax=ax)
                nx.draw_networkx_edges(g, pos, ax=ax)
                nx.draw_networkx_labels(g, pos, labels, font_color='w', ax=ax,font_size=8)
            else:
                nx.draw_networkx_nodes(g, pos, node_size=size, node_color='r', ax=ax)
                nx.draw_networkx_edges(g, pos, ax=ax)
                nx.draw_networkx_labels(g, pos, labels, ax=ax,font_size=8)

        ax.axis('off')

        self.canvas.draw()

    def _color_search_path(self, path):
        """Отрисовка пути поиска"""
        nodes = [x.key for x in self._preorder(self.tree)]
        colors = self._get_color_list(self.tree)
        for p in path:
            try:
                pos = nodes.index(p)
                colors[pos] = 'g'
            except ValueError:
                pass
        return colors

    def _get_pos_list(self, tree):
        return self._get_pos_list_from(tree, tree.root, {}, (0, 0), 1.0)

    def _get_pos_list_from(self, tree, node, poslst, coords, gap):
        positions = poslst

        if node and node.key == tree.root.key:
            positions[node.key] = (0, 0)
            positions = self._get_pos_list_from(tree, tree.root.left, positions, (0, 0), gap)
            positions = self._get_pos_list_from(tree, tree.root.right, positions, (0, 0), gap)
            return positions
        elif node:
            if node.parent.right and node.parent.right.key == node.key:
                new_coords = (coords[0] + gap, coords[1] - 1)
                positions[node.key] = new_coords
            else:
                new_coords = (coords[0] - gap, coords[1] - 1)
                positions[node.key] = new_coords

            positions = self._get_pos_list_from(tree, node.left, positions, new_coords, gap / 2)
            positions = self._get_pos_list_from(tree, node.right, positions, new_coords, gap / 2)
            return positions
        else:
            return positions

    def _get_edge_list(self, tree):
        return self._get_edge_list_from(tree, tree.root, [])

    def _get_edge_list_from(self, tree, node, edgelst):
        edges = edgelst

        if node and node.key == tree.root.key:
            if node.left:
                edges.append((node.key, node.left.key))
                edges = self._get_edge_list_from(tree, node.left, edges)
            if node.right:
                edges.append((node.key, node.right.key))
                edges = self._get_edge_list_from(tree, node.right, edges)

            return edges

        elif node:
            if node.left:
                edges.append((node.key, node.left.key))
            if node.right:
                edges.append((node.key, node.right.key))

            edges = self._get_edge_list_from(tree, node.left, edges)
            edges = self._get_edge_list_from(tree, node.right, edges)
            return edges

        else:
            return edges

    def _preorder(self, tree, *args):
        if len(args) == 0:
            elements = []
            node = tree.root
        else:
            node = tree
            elements = args[0]

        elements.append(node)

        if node.left:
            self._preorder(node.left, elements)
        if node.right:
            self._preorder(node.right, elements)

        return elements

    def _get_color_list(self, tree):
        nodelist = self._preorder(tree)
        colorlist = []
        for node in nodelist:
            if node.color:
                colorlist.append(node.color)

        return colorlist
