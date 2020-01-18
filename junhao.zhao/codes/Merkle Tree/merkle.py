from hashlib import sha256


class MerkleNode:
    def __init__(self, hash_val: str):
        self.hash_val = hash_val
        self.leaf_idx = None
        self.lchild = None
        self.rchild = None


class BinaryMerkleTree:
    def __init__(self, data: list):
        '''
        :param data: requires a LIST.
        '''
        self.origin_data = data
        self.merkle_root = self.__build()

    def check_data(self, checked: list) -> tuple:
        '''
        :param checked: another data to be checked.
        :return tuple: (True, None) if the same, or (False, [index]) if corrupted.
        '''
        self.new_root = self.__build(checked)
        # self.print_all_hash(self.new_root)
        if self.merkle_root.hash_val == self.new_root.hash_val:
            return True, None
        ori, new = [self.merkle_root], [self.new_root]
        while True:
            if ori[0].lchild is ori[0].rchild: break
            next1, next2 = [], []
            for d1, d2 in zip(ori, new):
                if d1.hash_val != d2.hash_val:
                    next1.extend((d1.lchild, d1.rchild))
                    next2.extend((d2.lchild, d2.rchild))
            ori, new = next1, next2
        corrupted = []
        for i in range(len(ori)):
            if ori[i].hash_val != new[i].hash_val:
                corrupted.append(new[i].leaf_idx)
        return False, corrupted

    def print_all_hash(self, root: MerkleNode = None) -> None:
        '''Level Order Traverse.'''
        st = [root if root else self.merkle_root]
        node = level = 0
        while st:
            level += 1
            print('\nlevel', level)
            for _ in range(len(st)):
                node += 1
                cur = st.pop(0)
                print('node', node, ':', cur.hash_val)
                if cur.lchild: st.append(cur.lchild)
                if cur.rchild: st.append(cur.rchild)

    def __build(self, data: list = None) -> MerkleNode:
        '''Build a merkle tree with given data.'''
        if data is None: data = self.origin_data
        # transform
        nodes = []
        for i, d in enumerate(data):
            new_node = MerkleNode(sha256(str(d).encode('utf-8')).hexdigest())
            new_node.leaf_idx = i
            nodes.append(new_node)
        # combine
        while len(nodes) > 1:
            if len(nodes) & 1: nodes.append(MerkleNode(''))
            it, tmp = iter(nodes), []
            for cur in it:
                sibling = next(it)
                new_node = MerkleNode(sha256((cur.hash_val + sibling.hash_val).encode('utf-8')).hexdigest())
                new_node.lchild = cur
                new_node.rchild = sibling
                tmp.append(new_node)
            nodes = tmp
        return nodes[0] if nodes else None
