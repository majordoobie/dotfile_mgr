# int s=0;
#
#                        for(int i=first; i<= last;i++)
#
#                                    s=s+array[i];
#
#                        return s;

from typing import List

def sum_rec(array: List[int], first: int, last: int) -> int:
    if first == last:
        return array[first]
    mid = int((first + last) / 2)
    return sum_rec(array, first, mid) + sum_rec(array, mid + 1, last)

def sum_iter(array: List[int], first: int, last: int) -> int:
    _sum = 0
    for index in range(first, last + 1):
        _sum = _sum + array[index] 
    return _sum

def main() -> None:
    array = [2] * 8
    array[1] = 8

    print(sum_rec(array, 0, 7))
    print(sum_iter(array, 0, 7))

if __name__ == "__main__":
    main()
