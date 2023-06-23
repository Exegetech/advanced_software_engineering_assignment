# Hidden Layer of Logic: Readings

## The Three Levels of Software.

One example of a function that I can think of, is any function that deals with date and time. JavaScript's `Date` object actually parses a date string as UTC, but gives the string back as local time. This has given me surprises several times in the past. I couldn't remember the actual functions that I wrote, but I thought I'd give a simple well known example.

For example, we have an function that gets a date string from a user, and save it in a Date representation.

```typescript
function getDateObj(date: string): Date {
  return new Date(date);
}

function displayDateObj(date: Date): string {
  return date.toDateString();
}
```

Then we write a test to make sure this code works.

```typescript
it('must give the correct date string', () => {
  const newYear = '2019-01-01';

  // Sometimes it breaks because the result can be 'Mon Dec 31 2018'
  expect(displayDateObj(getDateObj(newYear))).toEqual('Tue Jan 01 2019');
});
```

This test code will pass in some CI machines and will not pass in other CI machines. It depends on the time zone of the CI machine that runs this test. Of course, this code will also break depending on the location of the user's browser.

The reason is because `Date` constructor, given a single `string` argument, will parse that `string` as UTC (with added default milisecond, minutes, hours, if not in the `string`), and store it as UTC. However, when we convert it back to `string`, by using `toDateString()` function, it will actually localizes the `string`.

There are a several ways that we can fix this. We can either add a time zone parameter to the `getDateObj` function, or we can assume that the users always want to input date in their local time zone, and counter that. Lets say we assume that the users always want to input date in their local time zone.

```typescript
function getDateObj(date: string): Date {
  const dateObj = new Date();
  dateObj.setMinutes(dateObj.getMinutes() + dateObj.getTimezoneOffset());
  
  return dateObj;
}
```

Source https://www.youtube.com/watch?v=oKFb2Us9kmg

```
<----------------   Feedback   ------------------->
The JavaScript `Date` specification states that the string returned is in the local time zone. An error of modular reasoning is one where it is not possible to tell if the code works by just reading it or the specification and interfaces of it's dependecies. The answer sheet contains some examples.
<------------------------------------------------->
```

## The Design of Software is a Thing Apart.

I maintain an application that sends orders to exchanges. We call this list of orders a `Basket`. We can wave a `Basket`, making it live. We call the instance of a live `Basket` a `Wave`. This application has four windows, that is `BasketManager`, `BasketOrderManager`, `WaveManager`, and `WaveOrderManager`. In each of those windows, a trader can see list of orders and their completion progress and several other calculations. The calculations are very similar for a `Basket` and a `Wave`. We can get completion progress from the orders. So `Basket` needs `BasketOrder` data, and `Wave` needs `WaveOrder` data to calculate completion progress. As you have guessed it, `WaveOrder` is just an instance of `BasketOrder`.

Since the calculation is similar, we can have one function that calculates the progress of a `Basket` or a `Wave`.

```typescript
interface Shared {
  // contain properties that are similar
  // between BasketOrder and WaveOrder that matters in calculation
}

interface BasketOrder extends Shared { ... }
interface WaveOrder extends Shared { ... }

function calculate(orders: Shared[]): number { ... }

// calculate basket
const basketOrders: BasketOrder[] = [ ... ] 
const basket = calculate(basketOrders)

// calculate basket
const waveOrders: WasketOrder[] = [ ... ] 
const wave = calculate(waveOrders)
```

However, there is one difference between `Basket` and `Wave`. A `Basket`'s completion progress depends on all of its `Wave`s. For the majority of a time, a `Basket` only has one `Wave` instance. Sometimes though, a `Basket` can have multiple `Wave`s. Probably a trader decides to wave in parts. Probably a trader decides to cancel a `Wave` and redo. The calculation that happens inside `Basket` needs to take into account of this scenario.

So it is better to separate the `calculate` function.

```typescript
interface BasketOrder {}

function calculateBasket(orders: BasketOrder[], waveOrders: WaveOrder[]): number { ... }

interface WaveOrder {}

function calculateWave(orders: WaveOrder[]): number { ... }
```

Later on, traders would most likely start asking new or modification of features that diverge between `Basket` and `Wave` as time goes on. To make this software more modular, it is better to separate these two functions.

```
<----------------   Feedback   ------------------->
This is a good answer. There are two specifications here -- one for `basket` another for `wave` -- sharing the same calculation implementation.
<------------------------------------------------->
```

## Painless Functional Specifications Part 1.

The artifacts that depend on the design spec are the are the other derived specs. As Spolsky said, by writing a design spec, we only have to communicate how the program is supposed to work once. The QA, marketing, business development, technical writers, managers, and developers can derive their own specifications from the design spec.

```
<----------------   Feedback   ------------------->
Correct.
<------------------------------------------------->
```

## Modules Matters Most.

We can have small interface that deals with a specific functionality.

```typescript
interface Gunner {
  shoot(): void;
}

interface Warrior {
  slash(): void;
}

class A implements Gunner, Warrior { }
```


```
<----------------   Feedback   ------------------->
Correct.
<------------------------------------------------->
```

# Hoare Logic

## 1.

I can make `x = 2` and `y = 2`

```
{ true }
x = 2; 
{ x > 1 }
y = 2;
{ x > 1, y > 1 }
z = x + y;
{ z > 1 }
```

By forgetting assertions, we worry less about what sort of inputs that our code needs to worry. We make the precondition of our code weaker, so that strongest postcondition of the code before our code can be stronger.


```
<----------------   Feedback   ------------------->
We can change it to anything such that `z > 1`, so the values in the solution are correct. The solution correctly identifies that weakening ("forgetting") assertions means that they describe a larger space of behaviors ("the sort of inputs that our code needs to worry"). More generally though, the outcome is that there are more ways for the program to change and still have that assertion hold.  The strength of the upstream post-conditions is just one outcome.
<------------------------------------------------->
```

## 2.

By going backwards:

- Line 5, 6, 7 

  ```
  { }
  d := c + 1
  { d = 5 }
  ```

  Using assignment rule

```
  { [ c + 1 / d ] d = 5 }
  d := c + 1
  { d = 5 }

  { c + 1 = 5 }
  d := c + 1
  { d = 5 }

  { c = 4 }
  d := c + 1
  { d = 5 }
```

- Line 3, 4, 5

  ```
  { }
  c := b * 2
  { c = 4 }
  ```

  Using assignment rule

  ```
  { [ b * 2 / c ] c = 4}
  c := b * 2
  { c = 4 }

  { b * 2 = 4}
  c := b * 2
  { c = 4 }

  { b = 2}
  c := b * 2
  { c = 4 }
  ```

- Line 1, 2, 3

  ```
  { }
  b := 2 - a
  { b = 2 }
  ```

  Using assignment rule
  
  ```
  { [ 2 - a / b ] b = 2 }
  b := 2 - a
  { b = 2 }

  { 2 - a = 2 }
  b := 2 - a
  { b = 2 }

  { a = 0 }
  b := 2 - a
  { b = 2 }
  ```

All asssertions

```
{ a = 0 }
b := 2 - a
{ b = 2 }
c := b * 2
{ c = 4 }
d := c + 1
{ d = 5 }
```

<----------------   Feedback   ------------------->
Correct.  A goal of these exercises is to apply the rules mechanically, that is, apply rule after rule and follow the rules exactly. This solution displays that clearly. Well done.
<------------------------------------------------->

## 3.

- Line 5, 6, 7

  ```
  { }
  a := z * 5 + (1 - z) * 12
  {
    ((x is odd) => (a = 5)) &&
    ((x is even) => (a = 12))
  }
  ```

  Using assignment rule

  ```
  { 
    [ z * 5 + (1 - z) * 12 / a ]
    ((x is odd) => (a = 5)) &&
    ((x is even) => (a = 12)) 
  }
  a := z * 5 + (1 - z) * 12
  {
    ((x is odd) => (a = 5)) &&
    ((x is even) => (a = 12))
  }

  { 
    ((x is odd) => (z * 5 + (1 - z) * 12 = 5)) &&
    ((x is even) => (z * 5 + (1 - z) * 12 = 12)) 
  }
  a := z * 5 + (1 - z) * 12
  {
    ((x is odd) => (a = 5)) &&
    ((x is even) => (a = 12))
  }

  { 
    ((x is odd) => (z * 5 + 12 - 12 * z = 5)) &&
    ((x is even) => (z * 5 + 12 - 12 * z = 12)) 
  }
  a := z * 5 + (1 - z) * 12
  {
    ((x is odd) => (a = 5)) &&
    ((x is even) => (a = 12))
  }

  { 
    ((x is odd) => (z = 1)) &&
    ((x is even) => (z = 0)) 
  }
  a := z * 5 + (1 - z) * 12
  {
    ((x is odd) => (a = 5)) &&
    ((x is even) => (a = 12))
  }
  ```

- Line 3, 4, 5

  ```
  { }
  z := x - y
  { 
    ((x is odd) => (z = 1)) &&
    ((x is even) => (z = 0)) 
  }
  ```

  Using assignment rule

  ```
  {
    [ x - y / z ]
    ((x is odd) => (z = 1)) &&
    ((x is even) => (z = 0)) 
  }
  z := x - y
  { 
    ((x is odd) => (z = 1)) &&
    ((x is even) => (z = 0)) 
  }

  {
    ((x is odd) => (x - y = 1)) &&
    ((x is even) => (x - y = 0)) 
  }
  z := x - y
  { 
    ((x is odd) => (z = 1)) &&
    ((x is even) => (z = 0)) 
  }

  {
    ((x is odd) => (x = y + 1)) &&
    ((x is even) => (x = y)) 
  }
  z := x - y
  { 
    ((x is odd) => (z = 1)) &&
    ((x is even) => (z = 0)) 
  }
  ```

- Line 1, 2, 3

  ```
  { x > 0 }
  y := (x / 2) * 2
  {
    ((x is odd) => (x = y + 1)) &&
    ((x is even) => (x = y)) 
  }
  ```

  Taking into account that this is an integer division. `x` is odd will give different result than `x` is even. 

  If `x` is an odd number, then the computation `y := (x / 2) * 2` will result in:
  
  ```
  x = 1 => y = 0
  x = 3 => y = 2
  x = 5 => y = 4
  ```

  If `x` is an even number, then the computation `y := (x / 2) * 2` will result in:
  
  ```
  x = 2 => y = 2
  x = 4 => y = 4
  x = 6 => y = 6
  ```

All assertions

```
{ x > 0 }
y := (x / 2) * 2
{
  ((x is odd) => (x = y + 1)) &&
  ((x is even) => (x = y)) 
}
z := x - y
{
  ((x is odd) => (z = 1)) &&
  ((x is even) => (z = 0))
}
a := z * 5 + (1 - z) * 12
{
  ((x is odd) => (a = 5)) &&
  ((x is even) => (a = 12))
}
```

<----------------   Feedback   ------------------->
This solution is correct. The official solution includes an example applying the Assigment rule to first post-condition (the first missing one in the assignment) to show that the assertions result in a tautology ({x = x}) and therefore the assertion {x < 0} is stronger than necessary.
<------------------------------------------------->

## 4.1.

By going backwards:

- Line 11, 12, 23

  ```
  { }
  x := x + 1
  {
    ((a <= 0) => (x = 8 * b + 1)) &&
    ((a > 0) => (x = 12 * b + 1))
  }
  ```

  Using assignment rule

  ```
  {
    [ x + 1 / x ] 
    ((a <= 0) => (x = 8 * b + 1)) &&
    ((a > 0) => (x = 12 * b + 1))
  }
  x := x + 1
  {
    ((a <= 0) => (x = 8 * b + 1)) &&
    ((a > 0) => (x = 12 * b + 1))
  }

  {
    ((a <= 0) => (x + 1 = 8 * b + 1)) &&
    ((a > 0) => (x + 1 = 12 * b + 1))
  }
  x := x + 1
  {
    ((a <= 0) => (x = 8 * b + 1)) &&
    ((a > 0) => (x = 12 * b + 1)),
  }

  {
    ((a <= 0) => (x = 8 * b + 1 - 1)) &&
    ((a > 0) => (x = 12 * b + 1 - 1))
  }
  x := x + 1
  {
    ((a <= 0) => (x = 8 * b + 1)) &&
    ((a > 0) => (x = 12 * b + 1))
  }

  {
    ((a <= 0) => (x = 8 * b)) &&
    ((a > 0) => (x = 12 * b))
  }
  x := x + 1
  {
    ((a <= 0) => (x = 8 * b + 1)) /\
    ((a > 0) => (x = 12 * b + 1)),
  }
  ```

- Line 9, 10, 11

  ```
  { }
  x := m * x
  {
    ((a <= 0) => (x = 8 * b)) &&
    ((a > 0) => (x = 12 * b))
  }
  ```

  Using assignment rule

  ```
  {
    [ m * x / x ]
    ((a <= 0) => (x = 8 * b)) &&
    ((a > 0) => (x = 12 * b))
  }
  x := m * x
  {
    ((a <= 0) => (x = 8 * b)) &&
    ((a > 0) => (x = 12 * b))
  }

  {
    ((a <= 0) => (m * x = 8 * b)) &&
    ((a > 0) => (m * x = 12 * b))
  }
  x := m * x
  {
    ((a <= 0) => (x = 8 * b)) &&
    ((a > 0) => (x = 12 * b))
  }

  {
    ((a <= 0) => (x = 8 * b / m)) &&
    ((a > 0) => (x = 12 * b / m))
  }
  x := m * x
  {
    ((a <= 0) => (x = 8 * b)) &&
    ((a > 0) => (x = 12 * b))
  }
  ```

- Line 7, 8, 9

  ```
  { }
  x := x * 2
  {
    ((a <= 0) => (x = 8 * b / m)) &&
    ((a > 0) => (x = 12 * b / m))
  }
  ```

  Using assignment rule

  ```
  {
    [ x * 2 / x ] 
    ((a <= 0) => (x = 8 * b / m)) &&
    ((a > 0) => (x = 12 * b / m))
  }
  x := x * 2
  {
    ((a <= 0) => (x = 8 * b / m)) &&
    ((a > 0) => (x = 12 * b / m))
  }

  {
    ((a <= 0) => (x * 2 = 8 * b / m)) &&
    ((a > 0) => (x * 2 = 12 * b / m))
  }
  x := x * 2
  {
    ((a <= 0) => (x = 8 * b / m)) &&
    ((a > 0) => (x = 12 * b / m))
  }

  {
    ((a <= 0) => (x = (8 * b / m) / 2)) &&
    ((a > 0) => (x = (12 * b / m) / 2))
  }
  x := x * 2
  {
    ((a <= 0) => (x = 8 * b / m)) &&
    ((a > 0) => (x = 12 * b / m))
  }

  {
    ((a <= 0) => (x = 4 * b / m)) &&
    ((a > 0) => (x = 6 * b / m))
  }
  x := x * 2
  {
    ((a <= 0) => (x = 8 * b / m)) &&
    ((a > 0) => (x = 12 * b / m))
  }
  ```

- Line 5, 6, 7

  ```
  { }
  x := b * 2
  {
    ((a <= 0) => (x = 4 * b / m)) &&
    ((a > 0) => (x = 6 * b / m))
  }
  ```

  Using assignment rule

  ```
  {
    [ b * 2 / x ] 
    ((a <= 0) => (x = 4 * b / m)) &&
    ((a > 0) => (x = 6 * b / m))
  }
  x := b * 2
  {
    ((a <= 0) => (x = 4 * b / m)) &&
    ((a > 0) => (x = 6 * b / m))
  }

  {
    ((a <= 0) => (b * 2 = 4 * b / m)) &&
    ((a > 0) => (b * 2 = 6 * b / m))
  }
  x := b * 2
  {
    ((a <= 0) => (x = 4 * b / m)) &&
    ((a > 0) => (x = 6 * b / m))
  }

  {
    ((a <= 0) => (2 = 4 / m)) &&
    ((a > 0) => (2 = 6 / m))
  }
  x := b * 2
  {
    ((a <= 0) => (x = 4 * b / m)) &&
    ((a > 0) => (x = 6 * b / m))
  }

  {
    ((a <= 0) => (m = 4 / 2)) &&
    ((a > 0) => (m = 6 / 2))
  }
  x := b * 2
  {
    ((a <= 0) => (x = 4 * b / m)) &&
    ((a > 0) => (x = 6 * b / m))
  }

  {
    ((a <= 0) => (m = 2)) &&
    ((a > 0) => (m = 3))
  }
  x := b * 2
  {
    ((a <= 0) => (x = 4 * b / m)) &&
    ((a > 0) => (x = 6 * b / m))
  }
  ```

- Line 3, 4, 5

  ```
  { }
  m := d * 2 + (1 - d) * 3
  {
    ((a <= 0) => (m = 2)) &&
    ((a > 0) => (m = 3)),
  }
  ```

  Using assignment rule

  ```
  {
    [ d * 2 + (1 - d) * 3 / m ]
    ((a <= 0) => (m = 2)) &&
    ((a > 0) => (m = 3))
  }
  m := d * 2 + (1 - d) * 3
  {
    ((a <= 0) => (m = 2)) &&
    ((a > 0) => (m = 3))
  }

  {
    ((a <= 0) => (d * 2 + (1 - d) * 3 = 2)) &&
    ((a > 0) => (d * 2 + (1 - d) * 3 = 3))
  }
  m := d * 2 + (1 - d) * 3
  {
    ((a <= 0) => (m = 2)) &&
    ((a > 0) => (m = 3))
  }

  {
    ((a <= 0) => (d * 2 + 3 - d * 3 = 2)) &&
    ((a > 0) => (d * 2 + 3 - d * 3 = 3))
  }
  m := d * 2 + (1 - d) * 3
  {
    ((a <= 0) => (m = 2)) &&
    ((a > 0) => (m = 3))
  }

  {
    ((a <= 0) => (3 - d = 2)) &&
    ((a > 0) => (3 - d = 3))
  }
  m := d * 2 + (1 - d) * 3
  {
    ((a <= 0) => (m = 2)) &&
    ((a > 0) => (m = 3))
  }

  {
    ((a <= 0) => (d = 1)) &&
    ((a > 0) => (d = 0))
  }
  m := d * 2 + (1 - d) * 3
  {
    ((a <= 0) => (m = 2)) &&
    ((a > 0) => (m = 3))
  }
  ```

- Line 1, 2, 3

  ```
  { true }
  d := (2 - (a + 1) / a) / 2
  {
    ((a <= 0) => (d = 1)) &&
    ((a > 0) => (d = 0))
  }
  ```

  If `a <= 0`, then the computation `d := (2 - (a + 1) / a) / 2` will result in:

  ```
  a = -3 => d = 1
  a = -2 => d = 1
  a = -1 => d = 1
  a = 0 => d = 1
  ```

  If `a > 0`, then the computation `d := (2 - (a + 1) / a) / 2` will result in:

  ```
  a = 1 => d = 0
  a = 2 => d = 0
  a = 3 => d = 0
  ```

All assertions

```
{ true }
d := (2 - (a + 1) / a) / 2
{
  ((a <= 0) => (d = 1)) &&
  ((a > 0) => (d = 0))
}
m := d * 2 + (1 - d) * 3
{
  ((a <= 0) => (m = 2)) &&
  ((a > 0) => (m = 3))
}
x := b * 2
{
  ((a <= 0) => (x = 4 * b / m)) &&
  ((a > 0) => (x = 6 * b / m))
}
x := x * 2
{
  ((a <= 0) => (x = 8 * b / m)) &&
  ((a > 0) => (x = 12 * b / m))
} 
x := m * x
{
  ((a <= 0) => (x = 8 * b)) &&
  ((a > 0) => (x = 12 * b))
}
x := x + 1
{
  ((a <= 0) => (x = 8 * b + 1)) &&
  ((a > 0) => (x = 12 * b + 1))
}
```

<----------------   Feedback   ------------------->
In general, division over the integers behaves less nicely than division over the real numbers. Going from `m*x=8*b` to `x=8*b/m` is not valid without more information. First, viewing this part of the program in isolation, there is nothing disproving the possibility `m = 0`. Second, consider the state `{m=1, b=9, x=0}`; then `x=8*b/m` is true, but `m*x=8*b` is false. So they are not equivalent in the general case.

Further, the equality “(a / b) / n = (a / n) / b” only holds when “a”  is known to be perfectly divisible by “b.” The application here is invalid.  For example, the assignment “x = 0, b = 1, m = 5” satisfies “x = (4 * b) / m”, but, after running “x := x * 2,” it does not satisfy “x = (8 * b) / m”.
<------------------------------------------------->


## 4.2.

This code contains conditional because `x` depends on `a` implicitly. `d` introduced conditional.

<----------------   Feedback   ------------------->
Correct! The official solution contains a detailed explanation for exactly why
this is.
<------------------------------------------------->

## 5.

Since `d` introduced conditional, then we can move `d` (and its dependency, `m`) down, right before we use it.

We can order such that the statement about `d` and `m` comes later, right before we need to use it (that is, before `x := m + x`. The whole precondition and postcondition is unchanged.

```
1  { true }
2  x := b * 2
3  { }
4  x := x * 2
5  { }
6  d := (2 - (a + 1) / a) / 2
7  { }
8  m := d * 2 + (1 - d) * 3
9  { }
10 x := m * x
11 { }
12 x := x + 1
13 {
     ((a <= 0) => (x = 8b + 1)) &&
     ((a > 0) => (x = 12b + 1))
   }
```

We can prove it backward

- Line 11, 12, 13

  ```
  { }
  x := x + 1
  {
    ((a <= 0) => (x = 8b + 1)) &&
    ((a > 0) => (x = 12b + 1))
  }
  ```

  Using assignment rule

  ```
  {
    [ x + 1 / x ] 
  }
  x := x + 1
  {
    ((a <= 0) => (x = 8b + 1)) &&
    ((a > 0) => (x = 12b + 1))
  }

  {
    [ x + 1 / x ] 
    ((a <= 0) => (x = 8b + 1)) &&
    ((a > 0) => (x = 12b + 1))
  }
  x := x + 1
  {
    ((a <= 0) => (x = 8b + 1)) &&
    ((a > 0) => (x = 12b + 1))
  }

  {
    ((a <= 0) => (x + 1 = 8b + 1)) &&
    ((a > 0) => (x + 1 = 12b + 1))
  }
  x := x + 1
  {
    ((a <= 0) => (x = 8b + 1)) &&
    ((a > 0) => (x = 12b + 1))
  }

  {
    ((a <= 0) => (x = 8b)) &&
    ((a > 0) => (x = 12b))
  }
  x := x + 1
  {
    ((a <= 0) => (x = 8b + 1)) &&
    ((a > 0) => (x = 12b + 1))
  }
  ```

- Line 9, 10, 11

  ```
  { }
  x := m * x
  {
    ((a <= 0) => (x = 8b)) &&
    ((a > 0) => (x = 12b))
  }
  ```

  Using assignment rule

  ```
  {
    [ m * x / x ]
    ((a <= 0) => (x = 8b)) &&
    ((a > 0) => (x = 12b))
  }
  x := m * x
  {
    ((a <= 0) => (x = 8b)) &&
    ((a > 0) => (x = 12b))
  }

  {
    ((a <= 0) => (m * x = 8b)) &&
    ((a > 0) => (m * x = 12b))
  }
  x := m * x
  {
    ((a <= 0) => (x = 8b)) &&
    ((a > 0) => (x = 12b))
  }
  ```

- Line 7, 8, 9

  ```
  { }
  m := d * 2 + (1 - d) * 3
  {
    ((a <= 0) => (m * x = 8b)) &&
    ((a > 0) => (m * x = 12b))
  }
  ```

  Using assignment rule

  ```
  {
    [ d * 2 + (1 - d) * 3 / m ]
    ((a <= 0) => (m * x = 8b)) &&
    ((a > 0) => (m * x = 12b))
  }
  m := d * 2 + (1 - d) * 3
  {
    ((a <= 0) => (m * x = 8b)) &&
    ((a > 0) => (m * x = 12b))
  }

  {
    ((a <= 0) => (((d * 2) + (1 - d) * 3) * x = 8b)) &&
    ((a > 0) => (((d * 2) + (1 - d) * 3) * x = 12b))
  }
  m := d * 2 + (1 - d) * 3
  {
    ((a <= 0) => (m * x = 8b)) &&
    ((a > 0) => (m * x = 12b))
  }

  {
    ((a <= 0) => ((3 - d) * x = 8b)) &&
    ((a > 0) => ((3 - d) * x = 12b))
  }
  m := d * 2 + (1 - d) * 3
  {
    ((a <= 0) => (m * x = 8b)) &&
    ((a > 0) => (m * x = 12b))
  }
  ```

- Line 5, 6, 7

  ```
  { }
  d := (2 - (a + 1) / a) / 2
  {
    ((a <= 0) => ((3 - d) * x = 8b)) &&
    ((a > 0) => ((3 - d) * x = 12b))
  }
  ```

  Using assignment rule

  ```
  { 
    [ (2 - (a + 1) / a) / 2 / d ]
    ((a <= 0) => ((3 - d) * x = 8b)) &&
    ((a > 0) => ((3 - d) * x = 12b))
  }
  d := (2 - (a + 1) / a) / 2
  {
    ((a <= 0) => ((3 - d) * x = 8b)) &&
    ((a > 0) => ((3 - d) * x = 12b))
  }

  { 
    ((a <= 0) => ((3 - ((2 - (a + 1) / a) / 2)) * x = 8b)) &&
    ((a > 0) => ((3 - ((2 - (a + 1) / a) / 2)) * x = 12b))
  }
  d := (2 - (a + 1) / a) / 2
  {
    ((a <= 0) => ((3 - d) * x = 8b)) &&
    ((a > 0) => ((3 - d) * x = 12b))
  }
  ```

- Line 3, 4, 5

  ```
  { }
  x := x * 2
  { 
    ((a <= 0) => ((3 - ((2 - (a + 1) / a) / 2)) * x = 8b)) &&
    ((a > 0) => ((3 - ((2 - (a + 1) / a) / 2)) * x = 12b))
  }
  ```

  ```
  {
    [ x * 2 / x]
    ((a <= 0) => ((3 - ((2 - (a + 1) / a) / 2)) * x = 8b)) &&
    ((a > 0) => ((3 - ((2 - (a + 1) / a) / 2)) * x = 12b))
  }
  x := x * 2
  { 
    ((a <= 0) => ((3 - ((2 - (a + 1) / a) / 2)) * x = 8b)) &&
    ((a > 0) => ((3 - ((2 - (a + 1) / a) / 2)) * x = 12b))
  }

  {
    ((a <= 0) => ((3 - ((2 - (a + 1) / a) / 2)) * (x * 2) = 8b)) &&
    ((a > 0) => ((3 - ((2 - (a + 1) / a) / 2)) * (x * 2) = 12b))
  }
  x := x * 2
  { 
    ((a <= 0) => ((3 - ((2 - (a + 1) / a) / 2)) * x = 8b)) &&
    ((a > 0) => ((3 - ((2 - (a + 1) / a) / 2)) * x = 12b))
  }
  ```

- Line 1,2, 3


  ```
  { true }
  x := b * 2
  {
    ((a <= 0) => ((3 - ((2 - (a + 1) / a) / 2)) * (x * 2) = 8b)) &&
    ((a > 0) => ((3 - ((2 - (a + 1) / a) / 2)) * (x * 2) = 12b))
  }
  ```

<----------------   Feedback   ------------------->
The reordering is correct.  Lines 3 and 5 can be made simpler using the consequence rule.
The official solution shows how.
<------------------------------------------------->

## 6.

```
{ true }
i := 0
{
  i = 0 &&
  for all i, arr[0..i] does not contain val
}
while i < n && arr[i] != val do
  { }
  i := i + 1
  { }
end
{ arr[i] == val || (forall j, (j >= 0 && j < n) => arr[j] != val) }
```

1. Proof

Using, using indexes


2. Loop invariant statement

`for all i, arr[0..i] does not contain val`

At the start of iteration `i`, `arr[i]` should not be `val`. Notation

```
arr[i] != val /\ n = len(arr)
```

We need to see if it satisfies these three properties:
- `{ P && b } S { P }`

  ```
  { for all i, arr[0..i] does not contain val && i < n && arr[i] != val }
  i := i + 1
  { for all i, arr[0..i] does not contain val }
  ```

- `Pre -> P`

  ```
  i = 0 /\ n = len(arr) -> arr[i] != val /\ n = len(arr)
  ```

- `P /\ -b -> Post`

   ```
   -> { arr[i] == val \/ (forall j, (j >= 0 && j < n) => arr[j] != val) }
   ```

<----------------   Feedback   ------------------->
Great answer!
<------------------------------------------------->
