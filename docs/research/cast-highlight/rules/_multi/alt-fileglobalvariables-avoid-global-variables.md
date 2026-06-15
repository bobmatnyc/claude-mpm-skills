---
title: Global Variables can easily change module behavior
url: https://doc.casthighlight.com/alt_fileglobalvariables-avoid-global-variables/
slug: alt_fileglobalvariables-avoid-global-variables
content_type: rule
category: Robustness
has_code_examples: true
---

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/risk/)[Software Resiliency](http://casthighlight.wpengine.com/software-resiliency/)[Code Reliability](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# Global Variables can easily change module behavior

This code insight counts one violation each time global variable is declared, unless its name is uppercase.

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

## **Why you should care**

Avoid global variables. Variables that are declared at the module level have the potential to change module behavior during the import, because assignments to module-level variables are done when the module is imported.

Avoid global variables in favor of class variables. Some exceptions are:

- Default options for scripts.
- Module-level constants. For example: `PI = 3.14159`. Constants should be named using all caps with underscores; see [Naming](https://google.github.io/styleguide/pyguide.html#Naming) below.
- It is sometimes useful for globals to cache values needed or returned by functions.
- If needed, globals should be made internal to the module and accessed through public module level functions; see [Naming](https://google.github.io/styleguide/pyguide.html#Naming) below.

## **Business Impacts**

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/innovation/)

### CAST recommendations

### References

https://google.github.io/styleguide/pyguide.html#Global\_variables

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
