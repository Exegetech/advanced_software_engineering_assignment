from __future__ import annotations
import copy
import functools

class IndexWordPair:
    def __init__(self, index: int, word: str):
        self.index = index
        self.word = word

    def get_index(self) -> int:
        return self.index
    
    def get_word(self) -> str:
        return self.word


class Line:
    def __init__(self, words: list[str]):
        self.storage = words

    def __iter__(self) -> Line:
        self.index = 0
        return self

    def __next__(self) -> IndexWordPair:
        if self.index < len(self.storage):
            index = self.index
            word = self.storage[index]
            self.index += 1
            return IndexWordPair(index, word)
        else:
            raise StopIteration

    def get_size(self) -> int:
        return len(self.storage)

    def get_word(self, index: int) -> str:
        return self.storage[index]

    def get_shifted_word(self, first_word_index: int, index: int) -> str:
        line_size = len(self.storage)
        shift_index = ((first_word_index + index) % line_size)
        return self.storage[shift_index]


class IndexLinePair:
    def __init__(self, index: int, line: Line):
        self.index = index
        self.line = line

    def get_index(self) -> int:
        return self.index
    
    def get_line(self) -> Line:
        return self.line


class LineStorage:
    def __init__(self):
        self.storage = []

    def add_lines(self, lines: list[list[str]]) -> None:
        for line in lines:
            line_obj = Line(line)
            self.storage.append(line_obj)

    def __iter__(self) -> LineStorage:
        self.index = 0
        return self

    def __next__(self) -> IndexLinePair:
        if self.index < len(self.storage):
            index = self.index
            line = self.storage[index]
            self.index += 1
            return IndexLinePair(index, line)
        else:
            raise StopIteration

    def get_line(self, index: int) -> Line:
        return self.storage[index]


class LineIdxWordIdxPair:
    def __init__(self, line_idx: int, word_idx: int):
        self.line_idx = line_idx
        self.word_idx = word_idx

    def get_line_idx(self) -> int:
        return self.line_idx

    def get_word_idx(self) -> int:
        return self.word_idx

class Index:
    def __init__(self):
        self.storage = []

    def add(self, line_idx: int, word_idx: int):
        pair = LineIdxWordIdxPair(line_idx, word_idx)
        self.storage.append(pair)

    def __iter__(self) -> Index:
        self.index = 0
        return self

    def __next__(self) -> LineIdxWordIdxPair:
        if self.index < len(self.storage):
            index = self.index
            pair = self.storage[index]
            self.index += 1
            return pair
        else:
            raise StopIteration

    
line_storage = LineStorage()


def putfile(linelist: list[str]) -> None:
    global line_storage
    line_storage.add_lines(linelist)


circ_index = Index()


def cs_setup() -> None:
    global circ_index, line_storage
    
    for idx_line_pair in line_storage:
        line_idx = idx_line_pair.get_index()
        line_obj = idx_line_pair.get_line()

        for idx_word_pair in line_obj:
            word_idx = idx_word_pair.get_index()
            circ_index.add(line_idx, word_idx)

            
alph_index = None


def alphabetize() -> None:
    global alph_index, line_storage, circ_index

    def cmp_csline(shift1: LineIdxWordIdxPair, shift2: LineIdxWordIdxPair) -> bool:
      def csword(shift: LineIdxWordIdxPair, word_idx: int, lines: LineStorage) -> str:
        line_idx = shift.get_line_idx()
        first_word_idx = shift.get_word_idx()

        line = lines.get_line(line_idx)
        return line.get_shifted_word(first_word_idx, word_idx)
    
      def cswords(shift: LineIdxWordIdxPair, lines: LineStorage) -> int:
        line_idx = shift.get_line_idx()
        line = lines.get_line(line_idx)
        return line.get_size()
    
      def cmp(num1: int, num2: int) -> bool:
        return (num1 > num2) - (num1 < num2)
    
      lines = line_storage
          
      nwords1 = cswords(shift1, lines)
      nwords2 = cswords(shift2, lines)
      lasti = min(nwords1, nwords2)
          
      for i in range(lasti + 1):
        cword1 = csword(shift1, i, lines)
        cword2 = csword(shift2, i, lines)
          
        if cword1 != cword2:
          return cmp(cword1, cword2)
          
      return cmp(nwords1, nwords2)
  
    alph_index = sorted(circ_index, key=functools.cmp_to_key(cmp_csline))

    
def print_all_alph_cs_lines() -> None:
    global alph_index, line_storage

    def csline(shift: LineIdxWordIdxPair, lines: LineStorage) -> list[str]:
        line_idx = shift.get_line_idx()
        first_word_idx = shift.get_word_idx()

        line = lines.get_line(line_idx)
        line_size = line.get_size()

        return [line.get_shifted_word(first_word_idx, i) for i in range(line_size)]
    
    for shift in alph_index:
        print(csline(shift, line_storage))

        
putfile([["a", "b", "c", "d"],
         ["one"],
         ["hey", "this", "is", "different"],
         ["a", "b", "c", "d"]])
cs_setup()
alphabetize()
print_all_alph_cs_lines()
