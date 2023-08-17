# Algebraic Refactoring: Readings 

## The Algebra of Algebraic Datatypes, Part 1.

```typescript
enum TemperatureType {
  Celcius,
  Fahrenheit,
  Kelvin
}

interface Temperature {
  type: TemperatureType;
  value: number;
}

type GetTemperature = () => Temperature 
```

## Program Derivation for Functional Programs. (Optional)

You can derive programs from mathematical proof, the end result would look like functional code instead of imperative code.

# Equational Reasoning Drill

## Changing a function call.

```
((x, y) -> x + y + 1)(a + 1, b) === ((x, y) -> x + y + 1)(a, b + 1)

Left side
[a + 1 / x, b / y](x + y + 1)
a + 1 + b + 1
a + b + 2

Right side
[a / x, b + 1 / y](x + y + 1)
a + b + 1 + 1
a + b + 2
```

## Swapping an if-statement.

```
if (x) a else b === if (!x) b else a

Case: x = true
Left side
if (true) a else b
a

Right side
if (!true) b else a
if (false) b else a
a

Case: x = false
Left side
if (false) a else b
b

Right side
if (!false) b else a
if (true) b else a
b
```

## Un-nesting an if-statement.

```
if (x) { if (y) a else b } else b === if (x && y) a else b

Case: x = true, y = true
Left side
if (true) { if (true) a else b } else b
if (true) a else b
a

Right side
if (true && true) a else b
if (true) a else b
a

Case: x = true, y = false
Left side
if (true) { if (false) a else b } else b
if (false) a else b
b

Right side
if (true && false) a else b
if (false) a else b
b

Case: x = false, y = true
Left side
if (false) { if (true) a else b } else b
b

Right side
if (false && true) a else b
if (false) a else b
b

Case: x = false, y = false
Left side
if (false) { if (false) a else b } else b
if (false) a else b
b

Right side
if (false && false) a else b
if (false) a else b
b
```

```
if (x) a else { if (y) a else b === if (x || y) a else b

Case: x = true, y = true
Left side
if (true) a else { if (true) a else b }
a

Right side
if (true || true) a else b
if (true) a else b
a

Case: x = true, y = false
Left side
if (true) a else { if (false) a else b }
if (true) a else b
a

Right side
if (true || false) a else b
if (true) a else b
a

Case: x = false, y = true
Left side
if (false) a else { if (true) a else b }
if (true) a else b
a

Right side
if (false || true) a else b
if (false) a else b
a

Case: x = false, y = false
Left side
if (false) a else { if (false) a else b }
if (false) a else b
b

Right side
if (false || false) a else b
if (false) a else b
b
```

## Conditional-to-function.

```
if (A) o.foo() else o.bar()
      ===
f = if (A) (() -> o.foo()) else (() -> o.bar());
f()

Case A: true
Left side
if (true) o.foo() else o.bar()
o.foo()

Right side
f = if (true) (() -> o.foo()) else (() -> o.bar()); f ()
f = (() -> o.foo()); f()
f = o.foo()

Case A: false
Left side
if (false) o.foo() else o.bar()
o.bar()

Right side
f = if (false) (() -> o.foo()) else (() -> o.bar()); f ()
f = (() -> o.bar()); f()
f = o.bar()
```

## Functoriality of map.

```
map(f, map(g, l)) = map((x) -> f(g(x)), l)

Case l: Nil
Left side
map(f, map(g, Nil))
map(f, Nil)
Nil

Right side
map((x) -> f(g(x)), Nil)
Nil

Case l: Cons n r
Left side
map(f, map(g, Cons n r))
map(f, Cons g(n) map(g, r))
Cons f(g(n)) map(f, map(g, r))
       
Right side
map((x) -> f(g(x)), Cons n r)
(Cons ((x) -> f(g(x)))(n)) map((x) -> (f(g(x))), r)
Cons f(g(n)) map((x) -> f(g(x)), r)

We see that in both left and right side, Cons f(g(n)) is true
and by inductive reasoning

map(f, map(g, r)) = map((x) -> f(g(x)), r)

QED
```

# Mechanical Refactoring

## Algebraically Refactoring a Weak API: 1.

The program will set the wrong field in the TodoItem class

## Algebraically Refactoring a Weak API: 2.

As of now, it is not possible, because we need to know the `status` field of a `TodoItem`. We also don't know the type of `status`. If it is a `string` type, then this can violate the representable/valid principle because it is possible to to have an invalid `status`. Other examples that can be invalid are `dueDate` and `colour`.

## Algebraically Refactoring a Weak API: 3.

```python
from enum import Enum

class Status(Enum):
  PENDING = 'pending'
  FINISHED = 'finished'

class Colour(Enum):
  RED = 'red'

def updateStatus(self, status: Status):
  setattr(self, 'status', status)

def updateColour(self, colour: Colour):
  setattr(self, 'colour', colour)

def updateIsPublic(self, isPublic: boolean):
  setattr(self, 'isPublic', isPublic)
```

## Mechanically Refactoring a Weak API: 1.
<Your answer goes here>

## Mechanically Refactoring a Weak API: 2.

They would think that they can pass any string to `mode`.

## Mechanically Refactoring a Weak API: 3.
<Your answer goes here>

## Mechanically Refactoring a Weak API: 4.
<Your answer goes here>

# Hidden Coupling Drill

## Example 1: 1.

Foo calls bar.

## Example 1: 2.

Visible.

## Example 1: 3.

The coupling is visible.

## Example 2: 1.

Malloc needs `8` but without direct reference to `*str`

## Example 2: 2.

Hidden.

## Example 2: 3.

I am not a C developer, but we probably could replace `8` to `strlen(&str)`.

## Example 3: 1.

There are 2 players and loop of 2 times.

## Example 3: 2.

Hidden.

## Example 3: 3.

There should be a field that says `numOfPlayers` and the array and loop can use it.

## Example 4: 1.

There are 90 days of history by default.

## Example 4: 2.

Visible.

## Example 4: 3.

The coupling is visible.

## Example 5: 1.

There is no coupling.

## Example 5: 2.

There is no coupling.

## Example 5: 3.

There is no coupling.

## Example 6: 1.

The function `handleRequest` must know that the request object has `"username"` and `"password"` field set by the HTML element.

## Example 6: 2.

Hidden

## Example 6: 3.

There should be variables that keep the field names of `"username"` and `"password"`. These variables should be used by the function that created this HTML string and by the `handleRequest`.

## Example 7: 1.

The file string path is hardcoded.

## Example 7: 2.

Hidden.

## Example 7: 3.

There should be variables that store the paths to these images. The function `openFile` should be passed these variables.

## Example 8: 1.

The for loops reference Rectangle and Circle

## Example 8: 2.

Visible.

## Example 8: 3.

The coupling is visible.

## Example 9: 1.

Most likely there is a correction between `recipeNames` in `recipeTypes`

## Example 9: 2.

Hidden.

## Example 9: 3.

We could have tuple/struct that associates between `recipeNames` and `recipeTypes`. These 2 data should always go hand in hand.

## Mini-Case Study: The X Macro Trick. (optional)
<Your answer goes here>

# Case Study: A Tale of Two Parsers

## Data Modeling: 1.

```typescript
enum PrimitiveType {
  Boolean,
  Byte,
  Char,
  Double,
  Float,
  Int,
  Long,
  Short,
}
```

## Data Modeling: 2.

```typescript
type Primitive =
  | {
    type: PrimitiveType.Boolean;
    value: any;
  }
  | {
    type: PrimitiveType.Byte;
    value: any;
  }
  | {
    type: PrimitiveType.Char;
    value: any; 
  }
  | {
    type: PrimitiveType.Double;
    value: any;
  } 
  | {
    type: PrimitiveType.Float;
    value: any;
  } 
  | {
    type: PrimitiveType.Int;
    value: any;
  } 
  | {
    type: PrimitiveType.Long;
    value: any;
  } 
  | {
    type: PrimitiveType.Short;
    value: any;
  } 
```

## Data Modeling: 3.

```typescript
enum PrimitiveType {
  Boolean,
  Byte,
  Char,
  Double,
  Float,
  Int,
  Long,
  Short,
  Void,
}
```

There is an addition of `void` in this version.

## Data Modeling: 4.
<Your answer goes here>

## Data Modeling: 5.
<Your answer goes here>

## Data Modeling: 6.
<Your answer goes here>

## Data Modeling: 7.
<Your answer goes here>

## Code Follows Data: 1.
<Your answer goes here>

## Code Follows Data: 2.
<Your answer goes here>

## Code Follows Data: 3.
<Your answer goes here>

## Code Follows Data: 4.
<Your answer goes here>
