---
title: Explicit comparison to singleton can be unreadable
url: https://doc.casthighlight.com/alt_comparisontosingleton-avoid-explicit-comparison-to-singleton/
slug: alt_comparisontosingleton-avoid-explicit-comparison-to-singleton
content_type: rule
languages: [python]
category: Changeability
has_code_examples: true
---

[Cost](http://casthighlight.wpengine.com/category/product/indicators-methodology/cost/)[Software Agility](http://casthighlight.wpengine.com/software-resiliency/)[Code Readability](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# Explicit comparison to singleton can be unreadable

This code insight count one violation each time a condition use an explicit comparison to “**none**“, “**false**” or “**true**” (using operators == or !=).

**Bad**:

if number == None: print(“This works, but is not the preferred PEP 8 pattern”)

if number ! = None : print(“This works, but is not the preferred PEP 8 pattern”)

if otherNumber == false  
print(“yooo !”)

if otherNumber != false  
print(“yooo !”)

if T\_flag == True :  
 print ( “This works, but is not the preferred PEP 8 pattern” )

if F\_flag ! = True :  
 print ( “This works, but is not the preferred PEP 8 pattern” )

**good**:

if number is None : print ( “This works, but is not the preferred PEP 8 pattern” )

if  **not** otherNumber  
  print ( “yooo !” )

# or better :  
if **not** otherNumber **and otherNumber is not None**

print ( “yooo !” )

if  **not** otherNumber  
  print ( “yooo !” )

if  T\_ flag :

print  ( “PEP 8 Style Guide prefers this pattern” )

# or moire restrictive check (exclude assimiled True values like non nul or non empty values)

if  T\_ flag  **is True**   :

print  ( “PEP 8 Style Guide prefers this pattern” )

if   **not** F\_ flag :

print  ( “PEP 8 Style Guide prefers this pattern” )

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

## **Why you should care**

Per the PEP 8 Style Guide, the preferred way to compare something to   `None`   is the pattern   `if Cond is None`  . This is only a guideline. It can be ignored if needed. But the purpose of the PEP 8 style guidelines is to improve the readability of code.

Python evaluates certain values as `false` when in a boolean context. A quick “rule of thumb” is that all “empty” values are considered `false` so `0, None, [], {}, ''` all evaluate as `false` in a boolean context. So comparing to “false” may be confusing.

Moreover, conditions using Python booleans are easier to read and less error-prone. In most cases, they’re also faster

Per the PEP 8 Style Guide, the preferred ways to compare something to   `True`   are the patterns   `if cond is True:`   or  `if cond:`  . This is only a guideline. It can be ignored if needed. But the purpose of the PEP 8 Style Guide is to improve the readability of code.

## **Business Impacts**

*It is recommended to avoid these in order to ensure the code is more readable and cost effective.*

[Cost](http://casthighlight.wpengine.com/category/product/indicators-methodology/innovation/)

### CAST recommendations

### References

http://docs.quantifiedcode.com/python-code-patterns/readability/comparison\_to\_none.html

https://google.github.io/styleguide/pyguide.html#Conditional\_Expressions

http://docs.quantifiedcode.com/python-code-patterns/readability/comparison\_to\_true.html

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)

c
