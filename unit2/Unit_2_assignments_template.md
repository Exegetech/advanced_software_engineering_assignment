# The Embedded Design Principle: Readings

## Dark Knowledge and Graph Grammars.

A derivation is an example of dark knowledge because the information on how to get from the original to the derived is not apparent anywhere.

Can you really capture it? Maybe we can capture the decision that we choose as much as possible in the design of our program. But can we really capture the decision that we don't choose?

I usually try to capture it as much as possible using comments and unit tests.

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

# Design Exercise: Todo List.

Located in this gist https://gist.github.com/Exegetech/6c54748c0969743aa2a4518447192d57

# Django Email.

## 1.

The hidden coupling here is the fact that `send_messages` of the `console.py` depend on its own `write_message` that has its stream written decoded data (UTF-8 or any other encoding), while the `send_messages` of `filebased.py` just writes binary.  So depending on which implementation, the `send_messages` will send either a decoded data or binary data. I see that `send_message` is generic enough to not care about what type of encoding the underlying stream should be, but I don't know if other requirements may arise in the future that requires changing the `send_message` method.

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

## 2.b.

I am actually not really sure how to answer this. I understand that the `smtp.py` only fail silently when there is an SMTP exception, but the `console.py` fail silently for all exception. But that's as far as I understand it.

## 2.c.

See 2.b.

## 3.a.

The restrictions it is placing on file paths:
- must be provided either in function argument or in settings
- must be a string
- must be a directory
- must be writable

The restrictions make sense, since we want to write a file in a path that's not used yet and has write permission.

## 3.b.

Depending on where this `_init_` function is called, I think this is misplaced. I can think of 2 instances on when this `_init_` function is called:
- At the starting of this app, when all classes are initialized
- At the moment we want to write email content to a file

Looking at the `file_path` argument passed on `_init_` though, it seems to me that the latter is the case. But the location of this code is still confusing, since we don't know how much time has elapsed between instantiating this class and executing `write_message` and `send_message`. Between those, the file path might not be valid anymore.

I think it is better to separate the content of the function `_init_` like in 3.c.

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

## 4.a.

`subject`, `date` and `Message-ID` headers have default value and of type string.

## 4.b.

We have `to`, `cc`, and `reply-to` being treated the same. They are handled like this:
- In `_init_`, there is an assertion to check if the argument is a list or tuple. However, the check is to verify that the type is not a `str`. This code assumes that `to`, `cc` and `reply-to` is being passed as `str`.

- In `set_list_header_if_not_empty`, check the value from `extra_headers` and if exists there, assign it to message headers, else (by virtue of exception), get it from arguments, join them together as comma separated values stringified.

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

## 6.

<Your answer goes here>


## Follow-up question.

Not a primarily an OOP programmer, I would refactor this code to be functional first, and have no inheritance. However, I probably would get tripped on the same hidden coupling in this code regardless.

I personally wouldn't see that big of a problem in this code (written by someone else), as long as the testing works fine. I do have friction in reading it though, and I can see myself having harder time if I have to work on this code and extend it, since there are so many assumptions hidden inside, and the design is not clear, so I can't see the big picture. In reality, the testing usually is even worse, so I don't think I would gain much value in reading the tests. 
