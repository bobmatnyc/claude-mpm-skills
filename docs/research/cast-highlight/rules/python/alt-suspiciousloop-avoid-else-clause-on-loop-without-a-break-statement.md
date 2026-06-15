---
title: Break Statements helps reduce production risk
url: https://doc.casthighlight.com/alt_suspiciousloop-avoid-else-clause-on-loop-without-a-break-statement/
slug: alt_suspiciousloop-avoid-else-clause-on-loop-without-a-break-statement
content_type: rule
languages: [python]
has_code_examples: true
---

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/risk/)[Software Resiliency](http://casthighlight.wpengine.com/software-resiliency/)[Programming Best Practices](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# Break Statements helps reduce Production Risk

This code insight counts one violation each time a loop with a else clause do not contains any break or return statement.

**bad**

```
def contains_magic_number(list, magic_number):
    for i in list:
        if i == magic_number:
            print "This list contains the magic number."
    else:
        print "This list does NOT contain the magic number."
```

**good**

```
def contains_magic_number(list, magic_number):
    for i in list:
        if i == magic_number:
            print "This list contains the magic number."
            break  # added break statement here
    else:
        print "This list does NOT contain the magic number."
```

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

## **Why you should care**

The `else` clause of a loop is executed when the loop sequence is empty. When a loop specifies no `break` statement, the `else`clause will always execute, because the loop sequence will eventually always become empty. Sometimes this is the intended behavior, in which case you can ignore this error. But most times this is not the intended behavior, and you should therefore review the code in question.

## **Business Impacts**

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/innovation/)

### CAST recommendations

### References

https://www.quantifiedcode.com/knowledge-base/correctness/%60else%60%20clause%20on%20a%20loop%20without%20a%20%60break%60%20statement/4aqWoDeY

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
