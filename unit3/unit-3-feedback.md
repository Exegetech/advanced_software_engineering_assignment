# Representable/Valid Principle: Readings Questions

## Applying the Linus Torvalds "Good Taste" coding requirement.

Good code can be more efficient because it could lead to less branching. By having less branching, the code performs less instructions to check the conditions in the branching, leading to more efficient code.

<------------------- Feedback ------------------->
Correct.
<------------------------------------------------>

## Bugs and Battleships.

I think the most obvious case is splitting test cases into happy paths and error paths. Error paths can especially be tricky since often times it is using a mechanism that breaks code flow. Often twe don't know at which layer of code an error is handled, or not at all. 

<------------------- Feedback ------------------->
This is on the right track, but needs to be more specific to mark correct. For example, are there any scenarios where two "happy paths" which produce the same set of representations should be equivalent (e.g. covered by the same test)? The official answer sheet has some discussion around this which may be helpful. 
<------------------------------------------------>

## The Most Dangerous Code in the World.

Looking at the options presented there, `CURLOPT_SSL_VERIFYHOST` and then `verify`, and then `CURLOPT_SSL_VERIFYPEER`. It looks quite confusing which settings override which. I think the libcurl developers need to just simplify it to just one option if possible, or at least, get rid of either the `CURLOPT_SSL_VERIFYHOST` or `verify`. The downside is less configuration for specific scenarios, and make debugging harder.

<------------------- Feedback ------------------->
There is no way to make this change in a backwards compatible manner. In fact, there isn't _anything_ that can be done without a breaking a change. 
<------------------------------------------------>

## Where to Draw the Boundary.

We need to limit the operations that can be done in that data structure. For example, when designing a circular array, we should not allow the user of the circular array code to access the underlying array but through public APIs.

<------------------- Feedback ------------------->
It seems there's some confusion about the concept of "carving reality at it's joints" and the representations of a given data structure and encapsulation. 

Encapsulation deals with information hiding within a module. "Carving reality at it's joints" is more about it's about modeling our software to accurately reflecting the true nature of things, rather than imposing arbitrary or superficial groupings.

The official solution contains some discussion which may help clear up this misunderstanding.
<------------------------------------------------>

# Restricting APIs

## 1.1.

Looking at the `run` signature, we can see how we can use this function the wrong way:
- put negative int in `time`
- put the wrong measurement in `time` (is it seconds? minutes? hours?)
- put negative int in `temperature`
- put the wrong measurement in `temperature` (is it celcius? fahrenheit? kelvin?)
- put any int in `mode` that has nothing to do with the laundry mode

We can create a `Time` and `Temperature` class that deals with the validations, and pass an instance of `time` and `temperature` to `run` function.

We can also create an enum for `Mode` that we can pass to `run` function.

<------------------- Feedback ------------------->
Correct. The explit types for `Time` and `Temperature` also fixes another problem, incorrect argument order.
<------------------------------------------------>

## 1.2.

The `LaundryDisplay` class should contains a reference to `Laundromat` class. `Laundromat` class should have a function to give information whether a laundry machine is on and `LaundryDisplay` should use that function.

<------------------- Feedback ------------------->
This solution would meet the requirement. That said, details about the `WashingMachine` leak in to the `Laundromat`. The official solution contains examples where the representation of a "Restricted" or "DisplayOnly" is kept local to `WashingMachine`.
<------------------------------------------------>

## 1.3.

`Laundromat` class could have a function

```java
public List<WashingMachine> getOnMachines()
```

that will be called by `LaundryDisplay` everytime `LaundryDisplay` needs to access whether a specific laundry machine is on or not.

<------------------- Feedback ------------------->
This is on the right track, but this solution could be improved. The official solution contains more information.
<------------------------------------------------>

## 2.1.

```typescript
enum Player {
 X,
 O,
}

type Board = [[Maybe<Player>, Maybe<Player>, Maybe<Player>],
              [Maybe<Player>, Maybe<Player>, Maybe<Player>],
              [Maybe<Player>, Maybe<Player>, Maybe<Player>]]

enum Position {
  TopLeft,
  TopMiddle,
  TopRight,
  MidLeft,
  MidMiddle,
  MidRight,
  BotLeft,
  BotMiddle,
  BotRight,
}

enum State {
  New,
  Running,
  Finished
}

type NewGame = {
  type: State.New;
  board: Board;
}

type RunningGame = {
  type: State.Running;
  board: Board;
  positions: {
    player: Player;
    position: Position;
  }[];
}

type FinishedGame = {
  type: State.Finished;
  board: Board;
}

type Game = NewGame | RunningGame | FinishedGame

enum FinishedState {
  AWinner
  Draw,
}

type AWinnerResult = {
  type: FinishedState.AWinner;
  player: Player;
}

type DrawResult = {
  type: FinishedState.Draw;
}

type Result = AWinnerResult | DrawResult

function move(game: NewGame | RunningGame, player: Player, pos: Position): Game
function takeMoveBack(game: RunningGame): NewGame | RunningGame
function whoWonOrDraw(game: FinishedGame): AWinnerResult
function isPositionOccupied(game: RunningGame | FinishedGame, pos: Position): boolean
```

<------------------- Feedback ------------------->
Excellent answer.
<------------------------------------------------>

## 2.2. Extra Challenge 1

```javascript
const Player = {
  X: 'X',
  Y: 'Y',
}

const Position = {
  TopLeft: 'TopLeft',
  TopMiddle: 'TopMiddle',
  TopRight: 'TopRight',
  MidLeft: 'MidLeft',
  MidMiddle: 'MidMiddle',
  MidRight: 'MidRight',
  BotLeft: 'BotLeft',
  BotMiddle: 'BotMiddle',
  BotRight: 'BotRight',
}

const State {
  New: 'New',
  Running: 'Running',
  Finished: 'Finished'
}

class Game {
  board
}

class NewGame extends Game {
  move(player)
}

class RunningGame extends Game {
  positions

  move(player)
  takeMoveBack()
  isPositionOccupied(position)
}

class FinishedGame extends Game {
  whoWonOrDraw()
  isPositionOccupied(position)
}

class Result
class AWinnerResult extends Result
class DrawResult extends Result
```

<------------------- Feedback ------------------->
Good answer.
<------------------------------------------------>

## 2.3. Extra challenge 2

To make it a compile error, I need to be able to encode all state of the squares, which will at most (3 x 3)! states. I am not sure how to do that without typing that much.

<------------------- Feedback ------------------->
This is on the right track. The official solution showcases how this might be done in a few different languages.
<------------------------------------------------>

# Simpler and More Correct

## 1.1.

```java
public enum CustomerType {
    STUDENT,
    EMPLOYEE,
    // Add more types as necessary
}

public class Discount {
    private CustomerType customerTypeDiscount;
    private String itemNameDiscount;
    private String dayOfWeekDiscount;
    private final double discountPercent;

    public boolean doesDiscountApply(Customer c, Item item) {
        if (customerTypeDiscount != null) {
            switch (customerTypeDiscount) {
                case STUDENT:
                    return c.isStudent();
                case EMPLOYEE:
                    return c.isEmployee();
                // Add more cases as necessary
                default:
                    return false;
            }
        }

        if (itemNameDiscount != null) {
            return item.getName().equals(itemNameDiscount);
        }

        if (dayOfWeekDiscount != null) {
            return DateUtils.getDayOfWeek().equals(dayOfWeekDiscount);
        }

        return false;
    }

    public double applyDiscount(double price) {
        return price * (1 - discountPercent);
    }
}
```

<------------------- Feedback ------------------->
Correct
<------------------------------------------------>

## 1.2.

```java
import java.time.DayOfWeek;

public enum CustomerType {
    STUDENT,
    EMPLOYEE
}

public class Discount {
    private CustomerType customerTypeDiscount;
    private String itemNameDiscount;
    private DayOfWeek dayOfWeekDiscount;
    private final double discountPercent;

    public boolean doesDiscountApply(Customer c, Item item, DayOfWeek currentDay) {
        if (customerTypeDiscount != null) {
            switch (customerTypeDiscount) {
                case STUDENT:
                    return c.isStudent();
                case EMPLOYEE:
                    return c.isEmployee();
                default:
                    return false;
            }
        }

        if (itemNameDiscount != null) {
            return item.getName().equals(itemNameDiscount);
        }

        if (dayOfWeekDiscount != null) {
            return currentDay.equals(dayOfWeekDiscount);
        }

        return false;
    }

    public double applyDiscount(double price) {
        return price * (1 - discountPercent);
    }
}
```
<------------------- Feedback ------------------->
Correct (assuming the omitted implementation of `DayOfWeek`  is valid).
<------------------------------------------------>

## 1.3.

We can use SKU or unique ID for item.

```java
import java.time.DayOfWeek;
import java.util.Objects;
import java.util.UUID;

public enum CustomerType {
    STUDENT,
    EMPLOYEE
    // Add more types as necessary
}

public class ItemId {
    private final UUID id;

    public ItemId(UUID id) {
        this.id = id;
    }
}

public class Discount {
    private CustomerType customerTypeDiscount;
    private ItemId itemIdDiscount;
    private DayOfWeek dayOfWeekDiscount;
    private final double discountPercent;

    public boolean doesDiscountApply(Customer c, Item item, DayOfWeek currentDay) {
        if (customerTypeDiscount != null) {
            switch (customerTypeDiscount) {
                case STUDENT:
                    return c.isStudent();
                case EMPLOYEE:
                    return c.isEmployee();
                // Add more cases as necessary
                default:
                    return false;
            }
        }
        if (itemIdDiscount != null) {
            return item.getId().equals(itemIdDiscount);
        }
        if (dayOfWeekDiscount != null) {
            return currentDay.equals(dayOfWeekDiscount);
        }
        return false;
    }

    public double applyDiscount(double price) {
        return price * (1 - discountPercent);
    }
}
```

<------------------- Feedback ------------------->
The goal here is to make sure that the discount is not applied when it shouldn't be. That could happen if someone called `applyDiscount` without ever calling `doesDiscountApply`. For example:

```java
Customer student_a;

Discount discount_student = new Discount(student_a, /*...*/);

// Apply a customer discount to an employee purchase:

double some_price_for_emp_purchase;

discount_student.applyDiscount(some_price_for_emp_purchase); // Wrong discount applied
```

One option is to make `applyDiscount` conditionally apply the discount by doing its own discount checking. Have a look at the official solution for another.
<------------------------------------------------>

## 1.4.

```java
import java.time.DayOfWeek;
import java.util.Objects;
import java.util.UUID;

public enum CustomerType {
    STUDENT,
    EMPLOYEE
    // Add more types as necessary
}

public class ItemId {
    private final UUID id;

    public ItemId(UUID id) {
        this.id = id;
    }
}

public abstract class Discount {
    protected final double discountPercent;

    public Discount(double discountPercent) {
        this.discountPercent = discountPercent;
    }

    public double applyDiscount(double price) {
        return price * (1 - discountPercent);
    }
}

public class CustomerTypeDiscount extends Discount {
    private final CustomerType customerType;

    public CustomerTypeDiscount(double discountPercent, CustomerType customerType) {
        super(discountPercent);
        this.customerType = customerType;
    }

    public boolean doesDiscountApply(Customer customer) {
        return customer.getType().equals(customerType);
    }
}

public class ItemDiscount extends Discount {
    private final ItemId itemId;

    public ItemDiscount(double discountPercent, ItemId itemId) {
        super(discountPercent);
        this.itemId = itemId;
    }

    public boolean doesDiscountApply(Item item) {
        return item.getId().equals(itemId);
    }
}

public class DayOfWeekDiscount extends Discount {
    private final DayOfWeek day;

    public DayOfWeekDiscount(double discountPercent, DayOfWeek day) {
        super(discountPercent);
        this.day = day;
    }

    public boolean doesDiscountApply(DayOfWeek currentDay) {
        return currentDay.equals(day);
    }
}
```

<------------------- Feedback ------------------->
Making the types of `Discount` correct by construction is on the right track.

The issue with this solution is that the refactoring moves the conditional from the `doesDiscountApply` method to all the call sites for `Discount.doesDiscountApply()`since the method signature is not consistent for `doesDiscountApply`, it's incumbent on the clients to cast `Discount` -> `{}Discount`.

The official solution avoids this.
<------------------------------------------------>

## 1.5. (Optional)

With the implementation above, we can input a mock `DayOfWeek day` variable for ease of testing.

<------------------- Feedback ------------------->
The issue with this approach (following on from the feedback for `1.4`) is that the `CustomerTypeDiscount` and `ItemNameDiscount` will do nothing with this additional parameter (assuming a consistent interface). An alternative approach (and the one taken in the official solution) is resolve the `DayOfWeek` property in the `DayOfWeekDiscount` via a Dependency Injection container.
<------------------------------------------------>

## 2.

We could have a separate table that contains the list of viewable photos of a user by another user. Something like this

```typescript
type ViewablePhoto = {
  photoUrl: string;
  viewingUser: User;
  owner: User;
}
```

<------------------- Feedback ------------------->
This answer is too ambiguious to mark correct. Would this check be restricted to the data layer? If so, then it's on the right track.

This is the core insight to get from this exercise. To put it more clearly, by moving all the privacy checks to the data layer the rest of the program doesn't have to concern itself with the privacy policy, and thus the likelihood of privacy leaks is reduced. This is the same reasoning that's needed to get the last round of the Todo exercise of Unit 2 right.

Note there is also a second part of how to get information about the viewer to the database layer so the query can be made. The way that Facebook did it was through the introduction of a ViewerContext parameter. So a rough draft of the solution after the refactor would look something along these lines:

```
// no need to check since getPhotos only returns photos viewable for the context.
def listPhotos(user, viewerContext):
  for photo is viewerContext.getPhotos(user, db):
    displayPhoto(photo)
```
<------------------------------------------------>
