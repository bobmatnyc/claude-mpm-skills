---
title: ‘Not…is’ syntax can be unreadable
url: https://doc.casthighlight.com/alt_conditionreadability-avoid-not-is-syntax/
slug: alt_conditionreadability-avoid-not-is-syntax
content_type: rule
languages: [python]
category: Changeability
has_code_examples: false
---

[Cost](http://casthighlight.wpengine.com/category/product/indicators-methodology/cost/)[Software Agility](http://casthighlight.wpengine.com/software-resiliency/)[Code Readability](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# ‘Not…is’ syntax can be unreadable

Count one violation each time the **not … is** syntax is encountered.

**bad**

some\_list = None  
if not some\_list is None:  
do\_something()

**good**

some\_list = None  
if some\_list is not None:  
do\_something()

**Note**: there is no violation if the operators “and”, “or”, && or ||  
are between “not” and “is” because that means that “not” and “is ”  
are in different elementary conditions:

if not toto and titi is tata:  
do\_anything()

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

## **Why you should care**

In Python readability counts. That is why if-checks should be written with the reader in mind. Therefore it is generally better to write a condition just like one would write prose.

## **Business Impacts**

*It is recommended to avoid these in order to ensure the code is more readable and cost effective.*

[Cost](http://casthighlight.wpengine.com/category/product/indicators-methodology/innovation/)

### CAST recommendations

### References

https://www.quantifiedcode.com/knowledge-base/readability/%60not%20…%20is%60%20used%20instead%20of%20%60is%20not%60/4ORGpHyx

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)

c
