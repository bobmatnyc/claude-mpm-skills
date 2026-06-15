---
title: Empty and Implicit Returns cause resiliency issues.
url: https://doc.casthighlight.com/alt_unsignificantreturn-avoid-empty-and-implicit-return/
slug: alt_unsignificantreturn-avoid-empty-and-implicit-return
content_type: rule
has_code_examples: false
---

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/risk/)[Software Resiliency](http://casthighlight.wpengine.com/software-resiliency/)[Code Reliability](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# **Empty and Implicit Returns cause resiliency issues.**

This code insight

Counts one violation each time a function has **at least one significant return** (expression different from *nothing*, *none* or *false*) and in the same time :

- at least one **empty return**  
  OR
- an **implicit return** in place of the last statement.

bad

def foo(x):  
if x >= 0:  
return math.sqrt(x)  
# <— implicit return here

def bar(x):  
if x < 0:  
return # <—- empty return here  
return math.sqrt(x)

good

def foo(x):  
if x >= 0:  
return math.sqrt(x)  
else:  
return Nonedef bar(x):  
if x < 0:  
return None  
return math.sqrt(x)

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

## **Why you should care**

Be consistent in return statements. Either all return statements in a function should return an expression, or none of them should. If any return statement returns an expression, any return statements where no value is returned should explicitly state this as return None , and an explicit return statement should be present at the end of the function (if reachable).

## **Business Impacts**

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/innovation/)

### CAST recommendations

### References

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
