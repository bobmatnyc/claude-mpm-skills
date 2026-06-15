---
title: Inconsistencies in @throws tags can increase costs
url: https://doc.casthighlight.com/alt_unusedthrowstags-avoid-function-throwing-exceptions-and-not-having-a-throws-tag-php/
slug: alt_unusedthrowstags-avoid-function-throwing-exceptions-and-not-having-a-throws-tag-php
content_type: rule
languages: [php]
category: Changeability
has_code_examples: false
---

[Cost](http://casthighlight.wpengine.com/category/product/indicators-methodology/cost/)[Software Agility](http://casthighlight.wpengine.com/software-resiliency/)[Code Readability](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# Inconsistencies in @throws tags can increase costs

This code insight searches all the function that throws functions without having a @throws tag.

Verifies :  
1 – that a @throws tag exists for a function that throws exceptions.  
2 – the number of @throw tags and the number of throw tokens matches.  
3 – the exception type.

algo :  
Search all @throw tags in the documental comment of a function.  
Search all throw instruction in the function code.  
Checks that all exceptions thrown in the code whose type is known have a corresponding @throw tag. Once this check is done, those tags are removed from the list. Remaining tags are related to throw instructions on unknow type exception.  
For this remaining list of tags, check that there is at least one tag if it exists at least one throw instruction on an unknow type exception, and that there is not more tags than such throw instruction.

Examples :  
**throw new PHP\_Exception1(‘Error’);** throws a exception whose type is “PHP\_Exception1”

**throw $this->callSomeFunction();** throws a exception whose type is unknown (due to  analyzer limitation).

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

## **Why you should care**

Every function that throw exceptions must have a throw tag.  Try to reduce the number of function that throws exceptions without having a @throws tag.

## **Business Impacts**

*It is recommended to avoid these in order to ensure the code is more readable and cost effective.*

[Cost](http://casthighlight.wpengine.com/category/product/indicators-methodology/innovation/)

### CAST recommendations

### References

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)

c
