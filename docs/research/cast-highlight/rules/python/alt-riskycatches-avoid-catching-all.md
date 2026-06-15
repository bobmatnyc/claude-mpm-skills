---
title: Handling Exceptions should be explicit
url: https://doc.casthighlight.com/alt_riskycatches-avoid-catching-all/
slug: alt_riskycatches-avoid-catching-all
content_type: rule
languages: [python]
category: Robustness
has_code_examples: true
---

[Software Resiliency](http://casthighlight.wpengine.com/software-resiliency/)[Programming Best Practices](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# How we detect

This code insight counts one violation each time :

- an except instruction is immediately followed by a colon, i.e does not specify any exception class name (case of a bare except).
- an except instruction is catching the BaseException class
- an “except Exception:” is in first position or not in last position.

**bad**

```
def divide(a, b):
    try:
      result = a / b
    except:
      result = None

  return result
```

**good**

```
def divide(a, b):
    result = None

    try:
        result = a / b
    except ZeroDivisionError:
        print "Type error: division by 0."
    except TypeError:
        
        print "Type error: division by '{0}'.".format(b)
    except Exception as e:
        
        print "Error '{0}' occured. Arguments {1}.".format(e.message, e.args)
    else:
        
        print "No errors"
    finally:
        
        if result is None:
            result = 0

    return result
```

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

## **Why you should care**

Handling exceptions without specifying an exception type in your except-clause, and without performing any meaningful action in the exception handler, is not critical, but might hide actual programming errors. Hence, this is not considered `pythonic`. By not specifiycing an exception type, you might also loose information about the error itself.

A bare except: clause will catch SystemExit and KeyboardInterrupt exceptions, making it harder to interrupt a program with Control-C, and can disguise other problems. If you want to catch all exceptions that signal program errors, use except Exception: (bare except is equivalent to except BaseException:).

## **Business Impacts**

*It is advised to avoid risky catches because they can reduce the productivity of the application and waste plenty of team’s time and effort in the process.*

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/innovation/)[Time / Effort](http://casthighlight.wpengine.com/category/product/indicators-methodology/innovation/)

### CAST recommendations

Highlight considerations:

- If you really want to catch SystemExit or KeyboardInterrupt, do it explicitly, not with a bare except statement.
- generic catch “except Exception” will be tolerated by Highlight tool, only if it is preceded by at least one non-generic except statement, and is in last position.

### References

https://www.quantifiedcode.com/knowledge-base/correctness/Avoid%20untyped%20exception%20handlers/3JwOg9ad

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
