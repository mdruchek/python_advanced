"""
Помимо того чтобы логи писать, нужно их ещё и уметь читать,
иначе мы будем как в известном анекдоте, писателями, а не читателями.

Для вас мы написали простую функцию обхода binary tree по уровням.
Также в репозитории есть файл с логами, написанными этой программой.

Напишите функцию restore_tree, которая принимает на вход путь до файла с логами
    и восстанавливать исходное BinaryTree.

Функция должна возвращать корень восстановленного дерева

def restore_tree(path_to_log_file: str) -> BinaryTreeNode:
    pass

Примечание: гарантируется, что все значения, хранящиеся в бинарном дереве уникальны
"""
import itertools
import logging
import random
import re
from collections import deque
from dataclasses import dataclass
from typing import Optional, Dict

logger = logging.getLogger("tree_walk")


@dataclass
class BinaryTreeNode:
    val: int
    left: Optional["BinaryTreeNode"] = None
    right: Optional["BinaryTreeNode"] = None

    def __repr__(self):
        return f"<BinaryTreeNode[{self.val}]>"


def walk(root: BinaryTreeNode):
    queue = deque([root])

    while queue:
        node = queue.popleft()

        logger.info(f"Visiting {node!r}")

        if node.left:
            logger.debug(
                f"{node!r} left is not empty. Adding {node.left!r} to the queue"
            )
            queue.append(node.left)

        if node.right:
            logger.debug(
                f"{node!r} right is not empty. Adding {node.right!r} to the queue"
            )
            queue.append(node.right)


counter = itertools.count(random.randint(1, 10 ** 6))


def get_tree(max_depth: int, level: int = 1) -> Optional[BinaryTreeNode]:
    if max_depth == 0:
        return None

    node_left = get_tree(max_depth - 1, level=level + 1)
    node_right = get_tree(max_depth - 1, level=level + 1)
    node = BinaryTreeNode(val=next(counter), left=node_left, right=node_right)

    return node


def restore_tree(path_to_log_file: str) -> BinaryTreeNode:
    tree: Dict[int, BinaryTreeNode] = {}
    with open(path_to_log_file, "r") as file:
        for line in file.readlines():
            val_node = list(map(int, re.findall(r"\d+", line)))
            if "INFO" in line and val_node[0] not in tree:
                if not tree:
                    val_root = val_node[0]
                tree[val_node[0]] = BinaryTreeNode(val=val_node[0])
            elif "left" in line:
                left = BinaryTreeNode(val_node[1])
                tree[val_node[1]] = left
                tree[val_node[0]].left = tree[val_node[1]]
            elif "right" in line:
                right = BinaryTreeNode(val_node[1])
                tree[val_node[1]] = right
                tree[val_node[0]].right = tree[val_node[1]]
    return tree[val_root]


if __name__ == "__main__":
    log_file = "walk_log.txt"
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(levelname)s:%(message)s",
        filename=log_file,
        filemode="w"
    )

    root = get_tree(7)
    walk(root)
    restore_tree(log_file)
