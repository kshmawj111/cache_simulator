import argparse
import math


class CacheSimulator:

    # 변수 설정
    # 세트의 갯수, 블록 사이즈, 워드 사이즈
    s, n, m = 0, 0, 0
    filename = ''

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
            self.n = args.n
            self.m = int(math.log(args.m, 2))
            self.filename = args.filename
            return True

        else:
            print("모든 연산자는 2의 n승 꼴이어야 합니다.")
            return False


    def read_memory(self):
        file = open(self.filename, 'r')
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


    def hex_to_binary(self):
        bi_address_list = []
        hex_address_list = self.read_memory()
        for i in range(len(hex_address_list)):
            temp = bin(int(hex_address_list[i], 16))
            temp = temp[2:].zfill(32)
            bi_address_list.append(str(temp))

        return bi_address_list

    # 한 개의 binary memory address를 인자로 받아 입력 받은 s, n, m 값을 바탕으로 분해하고
    # 나온 결과 값을 decomposed란 list 형태로 return
    def decompose_address(self, bi_address):
        block_address = bi_address[0:32-(self.m + 2)]
        tag = bi_address[0:32-(self.s + self.m + 2)]
        set_idx = int(block_address, 2) % (2**self.s)
        decomposed = [set_idx, tag]
        return decomposed

        '''set_idx = block_address[32-(self.s + self.m + 2):]
               print('original: ', bi_address)
               print('word:     ', word_address)
               print('block:    ',block_address)
               print('tag add:  ',tag)
               print('setidx add', set_idx)
               print('')'''

    # bi_address_list로부터 받은 모든 address를 decompose 하여 새로운 decomposed_list로 저장
    def set_decomposed_list(self):
        bi_address_list = self.hex_to_binary()
        decomposed_list = []

        for address in bi_address_list:
            temp = self.decompose_address(address)
            decomposed_list.append(temp)


        return decomposed_list

    # Key = set_idx, Value = [valid bit = 0, tag = 0bXXXXXXXXXXXX]로 이루어진 dict를 생성
    # 입력받은 s값 만큼 key value를 생성하고 그에 대응하여 value를 match
    def initialize_cache(self):
        cache = dict()
        for x in range(2**self.s):

            cache[x] = self.n_way_table()

        return cache

    # [valid bit, tag, LRU count]로 이루어진 set index당 매칭될 list 생성
    def n_way_table(self):
        base = [0 for x in range(3)]
        table = []

        for i in range(self.n):
            table.append(base)

        return table

    def set_cache_data(self):
        output_list = []
        hit = 0
        miss = 0
        sum_valid_bit = 0

        input_address = self.set_decomposed_list()
        cache_table = self.initialize_cache()

        for address in range(len(input_address)):
            incoming_idx = input_address[address][0]
            cache_table_value = cache_table[incoming_idx]

            for way in range(self.n):
                hit_flag = 0
                #      cache tag                      input address tag               cache valid bit
                if (cache_table_value[way][1] == input_address[address][1]) & (cache_table_value[way][0] == 1):
                    hit_flag += 1

                else:
                    hit_flag += 0


            if hit_flag == 1:
                output_list.append('hit')
                hit += 1

            elif hit_flag == 0:
                output_list.append('miss')
                miss += 1

            for way in range(self.n):

                sum_valid_bit += cache_table_value[way][0]

            if sum_valid_bit == self.n:
                pass # way의 요소가 꽉 찼을 때

            else:
                for way in range(self.n):
                    cache_table_value[way][0] = 1
                    cache_table_value[way][1] = input_address[address][0]




















if __name__ == "__main__":
    a = CacheSimulator()
    if a.main() is True:
        # print(a.decompose_address('00000000000011000001010010111000'))
        pass



