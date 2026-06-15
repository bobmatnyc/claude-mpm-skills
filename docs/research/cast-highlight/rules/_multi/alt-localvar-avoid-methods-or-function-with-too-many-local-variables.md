---
title: Avoid methods or function with too many local variables
url: https://doc.casthighlight.com/alt_localvar-avoid-methods-or-function-with-too-many-local-variables/
slug: alt_localvar-avoid-methods-or-function-with-too-many-local-variables
content_type: rule
category: Transferability
has_code_examples: false
---

[SOFTWARE ELEGANCE](https://doc.casthighlight.com/category/product/indicators-methodology/software-elegance)

[CODE COMPLEXITY](https://doc.casthighlight.com/category/product/indicators-methodology/http://casthighlight.wpengine.com/category/product/indicators-methodology/software-elegance/code-complexity/)

This code insight counts one occurrence for each local variable in methods and functions found during the scan and shows up in CAST Highlight results when specific thresholds (ratio of local variables vs. total number of functions/methods) are reached for a given file, compared to the average ratio observed in other applications in the benchmark.

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

## **Why you should care**

Implementing too many local variables can make code more complex.

### CAST recommendations

Reduce the total number of parameters by subdividing your functions into more specialized and granular artifacts.

### References

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

[SEE FEATURES](https://doc.casthighlight.com/outputs-analytics/)

[HOW IT WORKS](https://doc.casthighlight.com/how-it-works/)
