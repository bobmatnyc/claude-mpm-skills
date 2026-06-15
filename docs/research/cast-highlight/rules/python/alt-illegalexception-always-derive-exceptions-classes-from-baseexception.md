---
title: Illegal exceptions can cause Production Risks
url: https://doc.casthighlight.com/alt_illegalexception-always-derive-exceptions-classes-from-baseexception/
slug: alt_illegalexception-always-derive-exceptions-classes-from-baseexception
content_type: rule
languages: [python]
category: Robustness
has_code_examples: true
---

[Software Resiliency](http://casthighlight.wpengine.com/software-resiliency/)[Code Resiliency](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# Risky catches increase production risks

This code insight counts one violation each time a class whose name is ending with **Exception** or **Error** is not derived from another class whose name is ending with Exception or Error, excluding BaseException.

**bad**

```
class MyException(object):
    def __init__(self, code, message):
        self.code = code
        self.message = message

try:
    if 1 != 0:
        raise MyException(42, "1 != 0 Exception")
except MyException as e:
    print(e.message)
```

**good**

```
lass MyException(Exception):
    def __init__(self, code, message):
        self.code = code
        self.message = message

try:
    if 1 != 0:
        raise MyException(1244, "1 != 0 Exception")
except MyException as e:
    print(e.message)
```

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

## **Why you should care**

Classes used for handling and representing exceptions must always inherit from `BaseException` at the lowest level. User-defined exception classes should actually inherit from `Exception`; they shouldn’t directly inherit from `BaseException`. Python requires all exception classes to inherit from a base exception superclass to ensure that they all meet the minimum required interface needed to be useful.

Highlight will consider that each classes whose name ends with “Exception” or “Error” is an exception class. This will be statically right, and is acceptable because Highlight is a statistical tool.

Through this rule, Highlight will check that all exceptions classes are derived from the builtin BaseException (but never directly !).

## **Business Impacts**

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/innovation/)

### CAST recommendations

### References

https://www.quantifiedcode.com/knowledge-base/correctness/Inherit%20from%20%60BaseException%60%20for%20all%20custom%20exceptions/72tTnTsJ

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
