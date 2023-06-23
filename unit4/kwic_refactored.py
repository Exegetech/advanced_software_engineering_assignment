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

    
line_storage = LineStorage()


def putfile(linelist: list[str]) -> None:
    global line_storage
    line_storage.add_lines(linelist)


circ_index = None


def cs_setup() -> None:
    global circ_index, line_storage
    
    circ_index = []
    for idx_line_pair in line_storage:
        line_idx = idx_line_pair.get_index()
        line_obj = idx_line_pair.get_line()

        for idx_word_pair in line_obj:
            word_idx = idx_word_pair.get_index()
            circ_index.append((line_idx, word_idx))

            
alph_index = None


def alphabetize() -> None:
    global alph_index, line_storage, circ_index

    def cmp_csline(shift1, shift2) -> bool:
      def csword(shift, wordno: int, lines: LineStorage) -> str:
        (lno, first_word_no) = shift
        line = lines.get_line(lno)
        line_size = line.get_size()
        shift_idx = ((first_word_no + wordno) % line_size)
        return line.get_word(shift_idx)
    
      def cswords(shift, lines: LineStorage) -> int:
        line_idx = shift[0]
        line = lines.get_line(line_idx)
        return line.get_size()
    
      def cmp(num1: int, num2: int) -> bool:
        return (num1>num2)-(num1<num2)
    
      lines = line_storage
          
      nwords1 = cswords(shift1, lines)
      nwords2 = cswords(shift2, lines)
      lasti = min(nwords1, nwords2)
          
      for i in range(lasti+1):
        cword1 = csword(shift1, i, lines)
        cword2 = csword(shift2, i, lines)
          
        if cword1 != cword2:
          return cmp(cword1, cword2)
          
      return cmp(nwords1, nwords2)
  
    alph_index = sorted(circ_index, key=functools.cmp_to_key(cmp_csline))
    
def print_all_alph_cs_lines() -> None:
    global alph_index, line_storage

    def csline(shift, lines) -> list[str]:
        (lno, first_word_no) = shift
        line = lines.get_line(lno)
        wrd_cnt = line.get_size()
        return [line.get_word((i+first_word_no) % wrd_cnt) for i in range(wrd_cnt)]
    
    for shift in alph_index:
        print(csline(shift, line_storage))

        
putfile([["a", "b", "c", "d"],
         ["one"],
         ["hey", "this", "is", "different"],
         ["a", "b", "c", "d"]])
cs_setup()
alphabetize()
print_all_alph_cs_lines()
