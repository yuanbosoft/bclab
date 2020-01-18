from merkle import BinaryMerkleTree

if __name__ == '__main__':
    origin_data = ['a', 'bb', 'ccc', 123, 456, 789, (1, 'b', 3), ['a', 2, 'c']]
    downloaded1 = ['a', 'bb', 'ccc', 123, 456, 789, (1, 'b', 3), ['a', 2, 'c']]
    downloaded2 = ['a', 'bb', 'ccd', 123, 456, 789, (1, 'e', 3), ['a', 2, 'c']]
    mt = BinaryMerkleTree(origin_data)
    # mt.print_all_hash()
    print(mt.check_data(downloaded1))
    print(mt.check_data(downloaded2))
