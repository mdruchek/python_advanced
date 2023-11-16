from typing import Union, List

Number = Union[int, float, complex]


def find_insert_position(array: List[Number], number: Number, position=0) -> int:
    if not array:
        return 0
    if number <= array[0]:
        return position
    if number > array[-1]:
        return position + len(array)
    half_len = len(array) // 2
    subarray1 = array[:half_len]
    subarray2 = array[half_len:]
    if subarray1[-1] < number <= subarray2[0]:
        return position + 1
    for num, subarray in enumerate((subarray1, subarray2)):
        if subarray[0] < number <= subarray[-1]:
            if num == 1:
                position += len(subarray1)
            position = find_insert_position(subarray, number, position)
            return position


if __name__ == '__main__':
    A: List[Number] = [1, 2, 3, 3, 3, 5]
    x: Number = 4
    insert_position: int = find_insert_position(A, x)
    assert insert_position == 5

    A: List[Number] = [1, 2, 3, 3, 3, 5]
    x: Number = 4
    A.insert(insert_position, x)
    assert A == sorted(A)
