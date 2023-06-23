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
class Line:
  def __init__(self):
    # code

  def add(self, line_item):
    # code

  def __iter__(self):
    # code

  def __next__(self):
    # code

  def get(self, shift_idx):
    # code


class LineStorage:
  def __init__(self):
    # code

  def add_item(self, line):
    # code

  def add_items(self, lines):
    # code

  def __iter__(self):
    # code

  def __next__(self):
    # code

  def get(self, line_no, shift_idx = None):
    # code


class Index:
  def __init__(self):
    # code

  def add(self, line_no, word_no):
    # code
 
  def __iter__(self):
    # code

  def __next__(self):
    # code


def sort_alphabetically(index):
  # code
```

## Data-Centric Refactoring: 4.
<Your answer goes here>

## Data-Centric Refactoring: 5.
<Your answer goes here>

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
