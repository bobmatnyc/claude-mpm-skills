---
title: Multiple imports on the same line can increase costs
url: https://doc.casthighlight.com/alt_multipleimports-avoid-imports-on-the-same-line/
slug: alt_multipleimports-avoid-imports-on-the-same-line
content_type: rule
languages: [python]
category: Changeability
has_code_examples: true
---

[Cost](http://casthighlight.wpengine.com/category/product/indicators-methodology/cost/)[Software Agility](http://casthighlight.wpengine.com/software-resiliency/)[Code Readability](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# Multiple imports on the same line can increase costs

This code insight counts one violation if an “import” not preceded by a “from” contains several arguments.

**bad**

import os, sys

**good**

import os  
import sys  
from xxx import a, b

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

## **Why you should care**

Imports should usually be on separate lines, e.g.:

```
Yes: import os
     import sys

No:  import sys, os
```

It’s okay to say this though:

```
from subprocess import Popen, PIPE
```

## **Business Impacts**

*It is recommended to avoid these in order to ensure the code is more readable and cost effective.*

[Cost](http://casthighlight.wpengine.com/category/product/indicators-methodology/innovation/)

### CAST recommendations

### References

https://www.python.org/dev/peps/pep-0008/#imports

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)

c
