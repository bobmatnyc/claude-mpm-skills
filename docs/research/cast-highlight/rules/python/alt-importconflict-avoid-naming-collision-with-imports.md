---
title: Importing naming collisions can cause risks
url: https://doc.casthighlight.com/alt_importconflict-avoid-naming-collision-with-imports/
slug: alt_importconflict-avoid-naming-collision-with-imports
content_type: rule
languages: [python]
has_code_examples: true
---

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/risk/)[Software Resiliency](http://casthighlight.wpengine.com/software-resiliency/)[Code Reliability](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# **Importing naming collisions can cause risks**

This code insight Counts one violation each time a name collision  is encountered:

pattern 1:  
from xxx import yyy  
from zzz import yyy

pattern 2:  
from xxx import yyy as zzz  
from aaa import bbb as zzz

pattern 3:  
import yyy as zzz  
import bbb as zzz

**bad**

```
from numpy import floor
from numpy import array
from math import floor
```

**good**

```
from numpy import floor as np_floor
from numpy import array as np_array
from math import floor
```

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

## **Why you should care**

As the last import will overload previous one’s, importing two objects with the same name can lead to unpredictable or even catastrophic results.

## **Business Impacts**

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/innovation/)

### CAST recommendations

### References

https://www.quantifiedcode.com/knowledge-base/correctness/Resolve%20import%20naming%20collision/kJ13jArn

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
