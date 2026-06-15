---
title: Uncommented Classes increase costs
url: https://doc.casthighlight.com/alt_uncommentedartifact-avoid-uncommented-classes/
slug: alt_uncommentedartifact-avoid-uncommented-classes
content_type: rule
languages: [python]
category: Robustness
has_code_examples: true
---

[Cost](http://casthighlight.wpengine.com/category/product/indicators-methodology/cost/)[Software Agility](http://casthighlight.wpengine.com/software-resiliency/)[Embedded Documentation](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# Uncommented Classes increase costs

Count one violation each time a class do not have a docstring as first instruction:

**bad** :

```
                class CustomException
                (Exception)
                :
    def __init__
                (self, msg, code)
                :
        self.msg = msg
        self.code = code
```

**good**:

```
                class CustomException
                (Exception)
                :
    """Raise when some custom event did not occur."""
    def __init__
                (self, msg, code)
                :
        self.msg = msg
        self.code = code
```

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

## **Why you should care**

Docstrings help you remember the intention of a class. This is especially important as your codebase grows and it becomes harder to remember the implementation details of each object. Other developers will also have it easier to understand your code.

## **Business Impacts**

*It is recommended to avoid these in order to ensure the code is more readable and cost effective.*

[Cost](http://casthighlight.wpengine.com/category/product/indicators-methodology/innovation/)

### CAST recommendations

### References

https://www.quantifiedcode.com/knowledge-base/maintainability/Consider%20documenting%20your%20class%28es%29/5ZdRTEsh

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
