from __future__ import annotations
import copy
import functools

class IndexWordPair:
    def __init__(self, index: int, word: str):
        self.index = index
        self.word = word
    

class Line:
    def __init__(self, words: list[str]):
        self.storage = words

    def __iter__(self) -> Line:
        self.index = 0
        return self

    def __next__(self) -> IndexWordPair:
        index = self.index
        word = self.storage[index]
        self.index += 1
        return IndexWordPair(index, word)


class IndexLinePair:
    def __init__(self, index: int, line: Line):
        self.index = index
        self.line = line


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
        index = self.index
        line = self.storage[index]
        self.index += 1
        return IndexLinePair(index, line)

    
line_storage = None
def putfile(linelist):
    global line_storage
    line_storage = copy.copy(linelist)

circ_index = None


def cs_setup():
    global circ_index, line_storage
    
    circ_index = []
    for lineno in range(len(line_storage)):
        line = line_storage[lineno]
        for wordno in range(len(line)):
            circ_index.append( (lineno, wordno) )
            
######################################################################
## ALPHABETIZING MODULE

alph_index = None

def alphabetize():
    global alph_index, line_storage, circ_index
    def cmp_csline(shift1, shift2):
      def csword(shift, wordno, lines):
        (lno, first_word_no) = shift
        shift_idx = (first_word_no + wordno) % len(lines[lno])
        return lines[lno][shift_idx]
    
      def cswords(shift, lines):
        return len(lines[shift[0]])
    
      def cmp(num1, num2):
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
    
######################################################################
## OUTPUT MODULE

def print_all_alph_cs_lines():
    global alph_index, line_storage
    def csline(shift, lines):
        (lno, first_word_no) = shift
        wrd_cnt = len(lines[lno])
        return [lines[lno][(i+first_word_no) % wrd_cnt] for i in range(wrd_cnt)]
    
    for shift in alph_index:
        print (csline(shift, line_storage))

        
## MASTER CONTROL
putfile([["a", "b", "c", "d"],
         ["one"],
         ["hey", "this", "is", "different"],
         ["a", "b", "c", "d"]])
cs_setup()
alphabetize()
print_all_alph_cs_lines()
