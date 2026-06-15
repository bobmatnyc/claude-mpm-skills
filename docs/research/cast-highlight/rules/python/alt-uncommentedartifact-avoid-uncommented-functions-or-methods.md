---
title: Uncommented functions or methods increase costs
url: https://doc.casthighlight.com/alt_uncommentedartifact-avoid-uncommented-functions-or-methods/
slug: alt_uncommentedartifact-avoid-uncommented-functions-or-methods
content_type: rule
languages: [python]
category: Transferability
has_code_examples: true
---

[Cost](http://casthighlight.wpengine.com/category/product/indicators-methodology/cost/)[Software Agility](http://casthighlight.wpengine.com/software-resiliency/)[Embedded Documentation](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# Uncommented functions or methods increase costs

Count one violation each time a function or method do not have a docstring as first instruction:

**bad** :

```
                def area
                (width, height)
                : 
    return width * height
```

**good**:

```
                def area
                (width, height)
                :
    """ Returns the area of a rectangle. """
    return width * height
```

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

## **Why you should care**

Docstrings help you remember the intention of a function or method. This is especially important as your codebase grows and it becomes harder to remember the implementation details of each object.

## **Business Impacts**

*It is recommended to avoid these in order to ensure the code is more readable and cost effective.*

[Cost](http://casthighlight.wpengine.com/category/product/indicators-methodology/innovation/)

### CAST recommendations

### References

https://www.quantifiedcode.com/knowledge-base/maintainability/Consider%20documenting%20your%20class%28es%29/5ZdRTEsh

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
