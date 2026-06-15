---
title: Unused variables can cause risks in code
url: https://doc.casthighlight.com/alt_unusedvar-avoid-unused-variable/
slug: alt_unusedvar-avoid-unused-variable
content_type: rule
languages: [python]
has_code_examples: true
---

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/risk/)[Software Resiliency](http://casthighlight.wpengine.com/software-resiliency/)[Code Reliability](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# **This code insight shows that Unused variables can cause risks in code**

Counts one violation each time local variable is initialized but never used.

**bad**

```
def area(width, height):
    a = width * height
    
    return width * height
```

**good**

```
def area(width, height):
    return width * height
```

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

## **Why you should care**

A local variable in your function is not being used. This is usually caused when someone starts implementing a function but never finishes it, or someone has refactored a function but forgot to remove old parts of the function that are no longer used. Therefore you should go back and review the function to make sure it has no problems.

## **Business Impacts**

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/innovation/)

### CAST recommendations

### References

https://www.quantifiedcode.com/knowledge-base/correctness/Local%20variable%20assigned%20but%20never%20used/5GJ6uvk0

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
