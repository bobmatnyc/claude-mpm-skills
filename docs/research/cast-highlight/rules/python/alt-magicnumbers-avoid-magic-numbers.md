---
title: Magic Numbers are a Production Risk
url: https://doc.casthighlight.com/alt_magicnumbers-avoid-magic-numbers/
slug: alt_magicnumbers-avoid-magic-numbers
content_type: rule
languages: [python]
category: Robustness
has_code_examples: true
---

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/risk/)[Software Resiliency](http://casthighlight.wpengine.com/software-resiliency/)[Programming Best Practices](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# Magic Numbers are a Production Risk

This code insight counts one violation each time a litteral numeric constant is encountered, that is not assigned to a constant.

- ```
  interger : (0|0[xX])?[0123456789ABCDEF]+([lL]?
  ```
- ```
  decimal : ([0-9]*\.[0-9]+|[0-9]+\.)
  ```
- real : [0-9]+[eE][+-]?[0-9]+

**exception**

- one digit integer
- 0.0, .0, 0.
- 1.0

Note : a constant is a variable assigned only one time in its scope.

example:

```
PI = 3.14          # not a violation because assigned to a constant
CONST = 123 * 456  # 2 violations : the assignation is an expression (containing 2 Magics)
a = 12             # violation because assigned to a variable
if (b):
    a = b
```

`)`

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

## **Why you should care**

It is recommended to use constants as default values for arguments in a function or method. This is cleaner, easier to read and there’s only one place to modify. Make sure, you document your constant, to explain where the value comes from.

**Highlight :**

Avoid litteral numeric constants.

## **Business Impacts**

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/innovation/)

### CAST recommendations

### References

https://www.quantifiedcode.com/knowledge-base/maintainability/Use%20constants%20as%20default%20values%20for%20arguments/24kTDwfL

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
