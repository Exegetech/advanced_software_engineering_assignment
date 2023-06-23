# The Data Over Code Principle: Readings

## On the Criteria to be Used in Decomposing Systems Into Modules.
<Your answer goes here>

## The Secret History of Information Hiding.

We had an email analyzer that analyzes emails, save its data in a database. I maintained an app that serves as a GUI into these data. The previous engineer coded the app by taking the data in a database, in its raw form, deserialized, and use it directly. It has bunch of fields that are camel case, snake case, etc. Due to changes from the team that maintains the app, sometimes they changed the format of these fields, from snake case to camel case, rename it completely, or add another fields that contain additional data to explain existing fields. As a result, everytime they deploy a change, I had to go into my code base, do a grep and change the field name in more than one place. During that time we didn't use any typings, so the experience was a nightmare. The solution was to validate/clean the data at the app's boundary, so everytime we have struct field name changes, we can just change it in one place.

## Abstraction: Not What You Think It Is.

Concrete space: A car's gasoline tank volume.

Abstract space: Represented by 6 bars. Zero bar means the tank is empty, five bars means the tank is full.

Mapping between concrete to abstract. Imagine the tank volume is 30 gal.
- 0 - 4 gal maps to one bar
- 6 - 10 gal maps to two bars
- 11 - 15 gal maps to three bars
- 16 - 20 gal maps to four bars
- 21 - 25 gal maps to five bars
- 26 - 30 gal maps to six bars

```typescript
enum Bar {
  One,
  Two,
  Three,
  Four,
  Five,
  Six,
}

function calculateTankVolume(volSensor number) Bar {
}
```

## Research Corner: The Programmer's Apprentice.

Using the dataflow graph, we can trace the dependency data of `sum`. We see that `sum` requires `x`, then `x` requires `arr` and `i`. We can extract out the code into a separate function that takes these dependencies, that is, the `arr` and `i`. 

# KWIC Refactoring Drill

## Dataflow Patterns: 1.

On `alphabetize` line 45.

```python
shift_idx = (first_word_no + wordno) % len(lines[lno])
```

On `print_all_alph_cs_lines` line 79.

```python
return [lines[lno][(i+first_word_no) % wrd_cnt] for i in range(wrd_cnt)]
```

## Dataflow Patterns: 2.
<Your answer goes here>

## Dataflow Patterns: 3.

The code looks similar. That is, there is a modulo `%` operator. I know that modulo operator often is used to calculate circular algorithm. I would grep the codebase for this module operator. 

## Data-Centric Refactoring: 1.

It seems to me that these modules do not hide any secret. It still uses shared data structure, that is `line_storage`, `circ_index`, `alph_index`, which is, for now, a list. Changing the variables that point out to the data would require changing it in all of the modules.

Also, it seems that the `print_all_alph_cs_lines` need to know that `alphabetize` is actually using modulo operator. If we change the operator in `alphabetize`, then the `print_all_alph_cs_lines` would need to change too.

## Data-Centric Refactoring: 2.a.

The `put_file` function would need to change, taking filepath as argument to read the input data, and error handling that tells next functions whether the data is successfully read or not.

## Data-Centric Refactoring: 2.b.

The `alphabetize` and `print_all_alph_cs_lines` would need to change. Maybe the `print_all_alph_cs_line` would decide on when to call `alphabetize`, making `alphabetize` a subroutine of `print_all_alph_cs_line`.

## Data-Centric Refactoring: 2.c.

The `alphabetize` and `print_all_alph_cs_lines` would need to change because now they can no longer use simple array index access to get access to the items.

## Data-Centric Refactoring: 3.

```python
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
```

## Data-Centric Refactoring: 4.

```python
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
```

## Data-Centric Refactoring: 5.

Each of the following module:
- `IndexWordPair`, `IndexLinePair`

  Hides the fact that index and its associated word/line is a tuple. These are helper data structures for `Line` and `LineStorage`

- `IndexLinePair`

  Hides the fact that index and its associated line is a tuple

- `Line`

  Hides the underlying list storage, and the logic on shifting words.

- `LineStorage`

  Hides the underlying list storage of lines.

- `LineIdxWordIdxPair`



## Data-Centric Refactoring: 6.
<Your answer goes here>

# Case Study: Git

## Worktrees: 1.
<Your answer goes here>

## Worktrees: 2.
<Your answer goes here>

## Worktrees: 3.
<Your answer goes here>

## Submodules: 1.
<Your answer goes here>

## Submodules: 2.a.
<Your answer goes here>

## Submodules: 2.b.
<Your answer goes here>

## Submodules: 2.c.
<Your answer goes here>

## Submodules: 2.d.
<Your answer goes here>

## Submodules: 3.
<Your answer goes here>

## Freestyle: 1.
<Your answer goes here>

## Freestyle: 2.
<Your answer goes here>

## Freestyle: 3.
<Your answer goes here>
