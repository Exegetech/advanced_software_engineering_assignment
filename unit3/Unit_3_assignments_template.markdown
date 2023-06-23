# Representable/Valid Principle: Readings Questions

## Applying the Linus Torvalds "Good Taste" coding requirement.

Good code can be more efficient because it could lead to less branching. By having less branching, the code performs less instructions to check the conditions in the branching, leading to more efficient code.

## Bugs and Battleships.

I think the most obvious case is splitting test cases into happy paths and error paths. Error paths can especially be tricky since often times it is using a mechanism that breaks code flow. Often twe don't know at which layer of code an error is handled, or not at all. 

## The Most Dangerous Code in the World.

Looking at the options presented there, `CURLOPT_SSL_VERIFYHOST` and then `verify`, and then `CURLOPT_SSL_VERIFYPEER`. It looks quite confusing which settings override which. I think the libcurl developers need to just simplify it to just one option if possible, or at least, get rid of either the `CURLOPT_SSL_VERIFYHOST` or `verify`. The downside is less configuration for specific scenarios, and make debugging harder.

## Where to Draw the Boundary.

We need to limit the operations that can be done in that data structure. For example, when designing a circular array, we should not allow the user of the circular array code to access the underlying array but through public APIs.

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

## 1.2.

The `LaundryDisplay` class should contains a reference to `Laundromat` class. `Laundromat` class should have a function to give information whether a laundry machine is on and `LaundryDisplay` should use that function.

## 1.3.

`Laundromat` class could have a function

```java
public List<WashingMachine> getOnMachines()
```

that will be called by `LaundryDisplay` everytime `LaundryDisplay` needs to access whether a specific laundry machine is on or not.

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

## 2.3. Extra challenge 2

To make it a compile error, I need to be able to encode all state of the squares, which will at most (3 x 3)! states. I am not sure how to do that without typing that much.

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

## 1.5. (Optional)

With the implementation above, we can input a mock `DayOfWeek day` variable for ease of testing.

## 2.

We could have a separate table that contains the list of viewable photos of a user by another user. Something like this

```typescript
type ViewablePhoto = {
  photoUrl: string;
  viewingUser: User;
  owner: User;
}
```
