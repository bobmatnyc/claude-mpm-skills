---
title: Bad variable names can increase costs
url: https://doc.casthighlight.com/alt_badnaming-avoid-bad-variable-name/
slug: alt_badnaming-avoid-bad-variable-name
content_type: rule
languages: [scala, python]
category: Transferability
has_code_examples: true
---

[Cost](http://casthighlight.wpengine.com/category/product/indicators-methodology/cost/)[Software Agility](http://casthighlight.wpengine.com/software-resiliency/)[Embedded Documentation](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# Bad variable names can increase costs

This code insight counts one violation each time the name do not complies with:

***Constants***

**(([A-Z\_][A-Z0-9\_]\*)|(\_\_.\*\_\_))**

- underscore allowed
- upercase
- anything delimited with double underscore

Note : a constant is an identifier that is assigned at only one time in a function, method or global scope, with a literal value (number, string or list)

***Variables***

**[a-z\_][a-z0-9\_]**

- underscore allowed
- lowercase

Note : a variable is an identifier that is assigned at least one time in a function, method or global scope.

**Examples**

```
PI = 3.14                   # (constant because assigned only one time in root scope)
CONST1 = [item1, item2]     # (constant because initialized with a literal list
CONST2 = "this is a string" # (constant because initialized with a literal string
my_var = 10                 # (variable because assigned later in same scope)
```

```
class toto:
   def meth() :
       CONST3 = 100    # (constant because assigned only one time in meth() scope)
       var = 10        # (variable because assigned later)
       print 'yo'
       var = 5
       my_var2 = var   # (variable because not initialized with a literal
       PI=5            # (variable because assigned two times in "meth()" scope)
       print(PI)
       PI = PI_0
```

```
my_var = 5
```

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

## **Why you should care**

The name of the variable or constant does match the naming convention. This error is a stylistic warning. The code will execute. But you can improve the readability of the code by renaming the variable or constant to match the following regular expression:

- Variables: `[a-z_][a-z0-9_]$`
- Constants: `(([A-Z_][A-Z0-9_]*)|(__.*__))$`

## **Business Impacts**

[Cost](http://casthighlight.wpengine.com/category/product/indicators-methodology/innovation/)

### CAST recommendations

### References

https://www.quantifiedcode.com/knowledge-base/maintainability/Avoid%20using%20%22non-Pythonic%22%20variable%20names/4m6i5Dpz

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
