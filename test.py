import argparse
import math



#  입력 값이 2의 거듭제곱이 아니거나 음수일 때 False를 리턴, 거듭제곱 꼴일 때만 True를 리턴
def is_power_of_two(self, n):
    # 정수가 아닐경우
    if not isinstance(n, int):
        return False

    # 비트 연산에서 거듭제곱은 비트 자리 중에 단 하나를 차지하는 성질을 이용하여 연산
    elif n > 0:
        return (n & (n - 1)) == 0

    # 음수일 경우 혹은 그 외의 경우
    else:
        return False

def main(self):
    parser = argparse.ArgumentParser(description='Associative Cache Simulator')
    # '-s: 세트 수, -n: 세트 당 블록 개수, -m: 워드 크기, -target: 파일이름'

    parser.add_argument('-s', type=int, required=True, help='number of sets. Must be power of two')
    parser.add_argument('-n', type=int, required=True, help='number of blocks per set. Must be power of two')
    parser.add_argument('-m', type=int, required=True, help="word size. Must be power of two")
    parser.add_argument('filename', default='test.in', help="file name containing address")

    args = parser.parse_args()

    if self.is_power_of_two(args.s) & self.is_power_of_two(args.n) & self.is_power_of_two(args.m) is True:
        self.s = int(math.log(args.s, 2))
        self.n = int(math.log(args.n, 2))
        self.m = int(math.log(args.m, 2))
        self.n_way = 2 ** (self.n - self.s)
        self.filename = args.filename
        return True

    else:
        print("모든 연산자는 2의 n승 꼴이어야 합니다.")
        return False

def read_memory(self, filename):
    file = open(filename, 'r')
    hex_address_list = []

    while True:
        line = file.readline()
        if line:
            line = line[2:10]
            hex_address_list.append(line)

        else:
            break

    file.close()
    return hex_address_list

def hex_to_binary(self, hex_address_list):
    bi_address_list = []
    for i in range(len(hex_address_list)):
        temp = bin(int(hex_address_list[i], 16))
        temp = temp[2:].zfill(32)
        bi_address_list.append(str(temp))

    return bi_address_list

def decompose_address(self, bi_address):
    word_address = bi_address[0:32 - 2]
    block_address = bi_address[0:32 - (self.m + 2)]
    tag = bi_address[0:32 - (self.s + self.m + 2)]
    set_idx = block_address[32 - (self.s + self.m + 2):]
    print('original: ', bi_address)
    print('word:     ', word_address)
    print('block:    ', block_address)
    print('tag add:  ', tag)
    print('setidx add', set_idx)
    print('')

def initialize_cache(self):
    cache = dict()
    for x in range(2 ** self.s):
        cache[x] =

def n_way_table(self):
    table = [[0 for x in range(2)] * self.n_way]
    return table


if __name__ == "__main__":
