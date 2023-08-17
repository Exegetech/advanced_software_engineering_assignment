# The Embedded Design Principle: Readings

## Dark Knowledge and Graph Grammars.

A derivation is an example of dark knowledge because the information on how to get from the original to the derived is not apparent anywhere.

Can you really capture it? Maybe we can capture the decision that we choose as much as possible in the design of our program. But can we really capture the decision that we don't choose?

I usually try to capture it as much as possible using comments and unit tests.

<------------------- Feedback ------------------->
The following statement is accurate:

> A derivation is an example of dark knowledge because the information on how to get from the original to the derived is not apparent anywhere.

What's important here is that the design is representented in the software, to put it another way: the design is _recoverable_ from the software. From this direction, the decisions/paths not chosen aren't relevent as the design is reachable without them. 
<------------------------------------------------>

## My favorite principle for code quality.

I would try to abstract out common logic. 

```java
public interface Stat {
    int count();
    String message(int count);
}

class DisplayStat {
  public Map<Stat, int> lastStatCachedTime;

  public void display(Stat stat) {
    int lastCachedTime = this.lastCachedTime.get(stat);
    if (lastCachedTime <= lastMidnight()) {
        int count = stat.count();
        this.lastCachedTime.set(Time.now());
        print(stat.message(count));
    } else {
        print(stat.message(count));
    }
  }
}

class UserStat implements Stat {}
class ArticleStat implements Stat {}
class WordStat implements Stat {}

Displayer displayer = new Displayer()

Stat userStat = new UserStat()
Stat articleStat = new ArticleStat()
Stat wordStat = new WordStat()

displayer.display(userStat)
displayer.display(articleStat)
displayer.display(wordStat)
```

<------------------- Feedback ------------------->
Good answer. The notion of a `Stat` has been unified along with other design details like the caching policy.
<------------------------------------------------>

# Design Exercise: Todo List.

Located in this gist https://gist.github.com/Exegetech/6c54748c0969743aa2a4518447192d57

<------------------- Feedback ------------------->
#### Revision 0

The `enum` representing an `Task`'s status is spot-on. The usage of a special type alias for the notion of `{Task|User}Id`s is also well-done. That being said, the `number` type admits many more operations than the the design of `Id` requires (see: the Representation/Valid principle from Unit 3). A further refined special ID type is preferred. 

Another critique to add is the presence of methods for creating/updating a todo item on the `Engine` type.  Firstly, it creates a design dependency from these methods to the internal representation of the `Task`. For example, if the choices about what data is needed to create/update a todo item change, so will these methods.
Secondly, it further pressures code that creates a todo item to depend on the `Engine` interface. In Unit 6, the course will discuss how this is a violation of the Parnas subset criteria (from the Unit 6 reading, “Designing Software for Ease of Extension and Contraction”): it is sensible to have a component that creates/edits a todo item with no reference to `Engine`.

Finally, By having the operations to manipulate `Task`s be in a single interface(`Engine`), instead of being in the `Task` and `TaskList` classes, the design assumes that there's a global storage for `Task`. It's better if to create a model that is agnostic of this aspect. Read this for more information:
https://mailchi.mp/1777c3addec0/mistake-of-the-month-a-serialization-format-is-not-a-programming-model?e=bd41c1fb2b. Also take a look at the official solution to see how the programming model would look like.

#### Revision 1

Good choice with the priority representation; Representing priority as integer or floats either makes it harder to add new priorities in between old priorities or harder to reorder priorities.

The use of a `Filter` type to represent the filtering requirement could be improved by using a lambda. Lambdas are open and can therefore meet any future change. The official solution contains some information why this pattern is optimal. Once you've completed the Week 5 exercises, you should know how to transform these into the equivalent Command -> List function (where Command is some sum), and then refunctionalize into the general form (`Task-> Boolean) -> TaskList`.


#### Revision 2

The representation of `privacy` could be improved: Having `isPrivate` as a boolean is not open to being extended to allow for more advanced access control.

The `void` return types on the `Engine.*Task` methods do not make it clear that a restricted list is returned. The official solution contains an additional concept, `TodoListView`, which represents the notion of a "viewer context". Returning this representation from methods like `GetItems` is preferable because it clearly delineates a generic "TodoList" from something more specific -- that is one which is being "viewed" by a non-owner. The utility of this is shown in the solution for Revision 3.

#### Revision 3

The utilization of `renderTaskList` (which accounts for the viewer) to handle counts makes sense as privacy controls are implemented there. Additionally, `renderTaskList` has the possibility of a bug if it calls `.length` on a pre-filtered task. The storage of revisions on the `Task` is on the right track, but more information about how this mechanism works is needed to mark this correct. The official solution contains a few different approaches to this.

<------------------------------------------------>

# Django Email.

## 1.

The hidden coupling here is the fact that `send_messages` of the `console.py` depend on its own `write_message` that has its stream written decoded data (UTF-8 or any other encoding), while the `send_messages` of `filebased.py` just writes binary.  So depending on which implementation, the `send_messages` will send either a decoded data or binary data. I see that `send_message` is generic enough to not care about what type of encoding the underlying stream should be, but I don't know if other requirements may arise in the future that requires changing the `send_message` method.

<------------------- Feedback ------------------->
The `('-' \* 79)` separator is shared between them. To put it more generally: both methods rely on the notion of an common "email format". If one implementation changes, the other must as well to satisfy the same design. The official answer sheet contains some possible improvements to embed this idea.
<------------------------------------------------>

I would refactor such that the code that does the decoding of the data does not live in `write_message` but somewhere else. Maybe a separate function, or maybe in `send_message`. I also would make sure that all the underlying class that implements `write_message` also implements `send_message` because there is a hidden coupling between these two methods.

## 2.a.

If we obfuscate the identifiers, I would look for this piece of code

```python
except ...:
    if ...:
        raise
    return ...
```

I would know that there is an exception handling that propagates that exception or not propagating that exception depending on some condition.

<------------------- Feedback ------------------->
Correct.
<------------------------------------------------>

## 2.b.

I am actually not really sure how to answer this. I understand that the `smtp.py` only fail silently when there is an SMTP exception, but the `console.py` fail silently for all exception. But that's as far as I understand it.

<------------------- Feedback ------------------->
In this case, there are exactly two policies (`fail_silently: bool`): 

1. Abort the process when the error occurs, report the error
2. Ignore all errors, continue processing, suppress the error(s)

Note that these polices could be represented in code any number of ways, but share a similiar "form". The official solution contains other examples.
<------------------------------------------------>

## 2.c.

See 2.b.

## 3.a.

The restrictions it is placing on file paths:
- must be provided either in function argument or in settings
- must be a string
- must be a directory
- must be writable

The restrictions make sense, since we want to write a file in a path that's not used yet and has write permission.

<------------------- Feedback ------------------->
The restictions are correct, but there is a subtle error in how this solution refers to the `file_path`.

It is correct to say: _"the `file_path` is a valid directory path that exists and can be written to"_, but it's not correct to say _"the `file_path` is writable"_.

The `file_path` is a string so while it does _represent_ a existing writeable directory, the string itself cannot be written to.
<------------------------------------------------>

## 3.b.

Depending on where this `_init_` function is called, I think this is misplaced. I can think of 2 instances on when this `_init_` function is called:
- At the starting of this app, when all classes are initialized
- At the moment we want to write email content to a file

Looking at the `file_path` argument passed on `_init_` though, it seems to me that the latter is the case. But the location of this code is still confusing, since we don't know how much time has elapsed between instantiating this class and executing `write_message` and `send_message`. Between those, the file path might not be valid anymore.

I think it is better to separate the content of the function `_init_` like in 3.c.

<------------------- Feedback ------------------->
The answer here follows from the analysis done in `3.a`. How can we embed those restrictions listed in such a way to make the design apparent? The official solution contains some examples.
<------------------------------------------------>

## 3.c.

```python
def __init__(self, *args, file_path=None, **kwargs):
    self._fname = None
    if file_path is not None:
        self.file_path = file_path
    else:
        self.file_path = getattr(settings, 'EMAIL_FILE_PATH', None)

    # Make sure self.file_path is a string.
    if not isinstance(self.file_path, str):
        raise ImproperlyConfigured('Path for saving emails is invalid: %r' % self.file_path)
    self.file_path = os.path.abspath(self.file_path)


    kwargs['stream'] = None
    super().__init__(*args, **kwargs)


def validate_path(self):
    # Make sure that self.file_path is a directory if it exists.
    if os.path.exists(self.file_path) and not os.path.isdir(self.file_path):
        raise ImproperlyConfigured(
            'Path for saving email messages exists, but is not a directory: %s' % self.file_path
        )
    # Try to create it, if it not exists.
    elif not os.path.exists(self.file_path):
        try:
            os.makedirs(self.file_path)
        except OSError as err:
            raise ImproperlyConfigured(
                'Could not create directory for saving email messages: %s (%s)' % (self.file_path, err)
            )
    # Make sure that self.file_path is writable.
    if not os.access(self.file_path, os.W_OK):
        raise ImproperlyConfigured('Could not write to directory: %s' % self.file_path)
```

Later on, in `filebased.py` implementation of `send_messages`, we can use `validate_path` before writing to the file stream.

<------------------- Feedback ------------------->
The goal here is to follow the reasoning done in `3.a-c` to embed the design intention of the `file_path` parameter (which is implicit given the signature). This solution just moves that implict/dark knowledge to `send_messages`. The official solution should clear things up.
<------------------------------------------------>

## 4.a.

`subject`, `date` and `Message-ID` headers have default value and of type string.

<------------------- Feedback ------------------->
Correct.
<------------------------------------------------>

## 4.b.

We have `to`, `cc`, and `reply-to` being treated the same. They are handled like this:
- In `_init_`, there is an assertion to check if the argument is a list or tuple. However, the check is to verify that the type is not a `str`. This code assumes that `to`, `cc` and `reply-to` is being passed as `str`.

- In `set_list_header_if_not_empty`, check the value from `extra_headers` and if exists there, assign it to message headers, else (by virtue of exception), get it from arguments, join them together as comma separated values stringified.

<------------------- Feedback ------------------->
This solution is correct. Note that `cc` and `reply-to` have additional behavior that is inplicitly stated: they have to be a list or tuple, _otherwise an exception will be raised_.
<------------------------------------------------>

## 4.c.i.

Some kind of cache, can be in memory, can be in a file, to store the list of all email-addresses that had been messaged that day. We could add it in `send` function on `mail/message.py`.

```python
def send(self, fail_silently=False):
    """Send the email message."""
    recipients = self.recipients()
    if not recipients:
        # Don't bother creating the network connection if there's nobody to
        # send to.
        return 0

    self.collect_recipients.add(recipients)
    return self.get_connection(fail_silently).send_messages([self])
```

<------------------- Feedback ------------------->
Correct.
<------------------------------------------------>

## 4.c.ii.

We could have a validate function on the `__init__` of `core/mail/message.py`

```python
def __init__(self, subject='', body='', from_email=None, to=None, bcc=None,
                   connection=None, attachments=None, headers=None, cc=None,
                   reply_to=None):
    """
    Initialize a single email message (which can be sent to multiple recipients).
    """
    self.validate_headers(headers)
```
<------------------- Feedback ------------------->
Correct. Note that other explicit fields like `to` and `bcc` will also need to be checked as they are also represented in the `headers` argument.
<------------------------------------------------>

## 4.c.iii.

If SMTP spec was written to include integer and string, then the method `isinstance(to, str)` and its siblings would've been written differently. Probably the programmer would realize that it is better to separate the email validation code in a separate function that can be changed whenever the spec changes. 

```python
def __init__(self, subject='', body='', from_email=None, to=None, bcc=None,
                   connection=None, attachments=None, headers=None, cc=None,
                   reply_to=None):
    """
    Initialize a single email message (which can be sent to multiple recipients).
    """
    self.validate_email_address(to)
    self.validate_email_address(bcc)
    self.validate_email_address(cc)
    self.validate_email_address(reply_to)
```

<------------------- Feedback ------------------->
Correct.
<------------------------------------------------>

## 4.d.

Headers are just extra data for an email. I would suggest the person who've never worked with email headers to just read some articles online. I can encode headers in types, i.e,

```typescript
type HeaderWithEmailValueType =
    | 'From'
    | 'To'
    | 'Reply-To'

type RequiredHeaderType =
    | HeaderWithEmailValueTYpe
    | ...

type AdditionalHeaderType =
    | ... 

type HeaderType = RequiredHeaderType | AdditionalHeaderType

type Headers = Record<HeaderType, string>
```

I think this makes the code clearer, with the bonus of having compiler guides us through type checking.

<---------------------- Feedback --------------------->
This proposed solution is an improvement and takes the code one step along the embedded design principle. The official solution includes a method which eliminates the need for guards checking if the the headers are valid (as required in the solution in `4.e`), for example. The official answer sheet contains a fleshed out implementation which displays this. 
<----------------------------------------------------->

## 4.e.

```typescript
class EmailMessage {
    constructor(
        subject: string,
        body: string,
        headers: Headers
    ) {
        this.validateHeaders(headers);
        this.headers = headers;
    }
}
```

<------------------- Feedback ------------------->
See the feedback for `4.d`.
<------------------------------------------------>

## 4.f.

```typescript
class EmailMessage {
    constructor(
        subject: string,
        body: string,
        headers: Headers
    ) {
        this.assertHeaders(headers);
        this.headers = headers;
    }

    private validateRequiredHeaders = (headers: Headers): void => {
        this.validateHeadersWithEmailValue(headers)
        this.validateOtherRequiredHeaders(headers)
    }

    private assertHeaders = (headers: Headers): void => {
        this.validateRequiredHeaders(headers)
        this.validateAdditionalHeaders(headers)
    }

    private send = (): void => {
        const recipients = this.recipients(this.headers);
        this.collectRecipients(recipients);

        // send
    }
}
```

<------------------- Feedback ------------------->
See the feedback for `4.d`.
<------------------------------------------------>

## 5.

In this `open` method https://github.com/django/django/blob/f0d6f01fbe171f4599fd13e34ccff0a5af653e90/django/core/mail/backends/smtp.py#L42

We see this description

```
"""
Ensure an open connection to the email server. Return whether or not a
new connection was required (True or False) or None if an exception
passed silently.
"""
```

This is prone to boolean blindness. Not only boolean, in fact, there are another possible returned value here, that is `None`, which is redundant with `False`. It is better to redesign this API such that it returns enums with 2 values instead.

```typescript
enum OpenResultType {
    NewConnectionRequired,
    NewConnectionNotRequired,
}

```

<------------------- Feedback ------------------->
Great example.
<------------------------------------------------>

## 6.

<Your answer goes here>


## Follow-up question.

Not a primarily an OOP programmer, I would refactor this code to be functional first, and have no inheritance. However, I probably would get tripped on the same hidden coupling in this code regardless.

I personally wouldn't see that big of a problem in this code (written by someone else), as long as the testing works fine. I do have friction in reading it though, and I can see myself having harder time if I have to work on this code and extend it, since there are so many assumptions hidden inside, and the design is not clear, so I can't see the big picture. In reality, the testing usually is even worse, so I don't think I would gain much value in reading the tests. 

<------------------- Feedback ------------------->
The official answer sheet contains some examples. Note the correspondence between the unit tests required and the number of representable states.
<------------------------------------------------>
