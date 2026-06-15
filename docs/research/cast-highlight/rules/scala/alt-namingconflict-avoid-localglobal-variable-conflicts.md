---
title: Conflicts in Local / Global Variables can be Unproductive
url: https://doc.casthighlight.com/alt_namingconflict-avoid-localglobal-variable-conflicts/
slug: alt_namingconflict-avoid-localglobal-variable-conflicts
content_type: rule
languages: [scala, python]
has_code_examples: true
---

[Software Resiliency](http://casthighlight.wpengine.com/software-resiliency/)[Code Reliability](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# **Conflicts in Local / Global Variables can be Unproductive**

This code insight counts one violation each time a global variable is assigned in a function, because the variable has the same name.

In python, variables are created after receiving their first allocation, so with the following pattern :

<identifiers> =

**bad**

```
<xxx> = ..
...
def fct():
    ...
    <xxx> = ...
```

**good**

```
<xxx>
...
def fct():
    ...
    <yyy> = ...
```

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

## **Why you should care**

The following code below is considered to be a common error by developers in Python.

```
>>> x = 10
>>> def foo():
...     x += 1
...     print x
...
>>> foo()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "<stdin>", line 2, in foo
UnboundLocalError: local variable 'x' referenced before assignment
```

The above error occurs because, when *an assignment*is made to a variable in a scope, Python automatically considers that variable to be *local to that scope* and overlooks any similarly named variable in any outer scope.

This error is common because it is easy to confabulate assignments of functions to local and global variables in Python.  However, this should be avoided because this can immensely hamper productivity, wasting time and effort because of the confusion that can also arise within development.

It is important to avoid global variables since overusing them can be a symptom of poor design in object oriented programming as there is no separation of functionalities.  The very design of object-oriented programming is to isolate functionalities and responsibilities for better compartmentalization and optimization.  Not doing this can lead to spaghetti code which tends to be messy and inefficient.

## **Business Impacts**

*Conflicts that are created for local/global variables is to be taken seriously because it decreases code productivity which causes loss of time and maximizing effort in development.*

*Having an abundance of global variables in Python hurts Object-oriented programming which is a key component of development.  All of this would cause lack of productive output from the code which is not ideal from a business standpoint.*

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/innovation/)[Time / Effort](http://casthighlight.wpengine.com/category/product/indicators-methodology/innovation/)

### CAST recommendations

CAST recommends avoiding conflicts between local and global variables because of the lack of productivity that can occur in the code.  Local variables are automatically created in Python unless declared as global.

This is not recommended but a global variable can be created by declaring a function as global.  Here is some code below that demonstrates this.

```
globvar = 0

def set_globvar_to_one():
    global globvar    # Needed to modify global copy of globvar
    globvar = 1

def print_globvar():
    print(globvar)     # No need for global declaration to read value of globvar

set_globvar_to_one()
print_globvar()       # Prints 1
```

Although creating many global variables is not recommended, the code above is shown to distinguish global variables from local variables.  It is recommended to have more local variables and less global variables in the code.  All variables should be limited to local so that code can be easier to understand.

### References

https://www.toptal.com/python/top-10-mistakes-that-python-programmers-make#common-mistake-4–misunderstanding-python-scope-rules

https://stackoverflow.com/questions/13091357/python-global-local-variables

https://www.quora.com/How-can-I-avoid-using-global-variables-in-my-Python-code

https://stackoverflow.com/questions/423379/using-global-variables-in-a-function

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
