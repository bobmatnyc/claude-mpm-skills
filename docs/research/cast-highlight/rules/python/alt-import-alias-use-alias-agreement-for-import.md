---
title: Alias agreement for imports can reduce costs
url: https://doc.casthighlight.com/alt_import_alias-use-alias-agreement-for-import/
slug: alt_import_alias-use-alias-agreement-for-import
content_type: rule
languages: [python]
category: Changeability
has_code_examples: true
---

[Cost](http://casthighlight.wpengine.com/category/product/indicators-methodology/cost/)[Software Agility](http://casthighlight.wpengine.com/software-resiliency/)[Code Readability](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# Alias agreement for imports can reduce costs

This code insight counts one violation each time a one of the following library is not imported with the conventionnal alias.

**Library -> Alias**  
numpy -> np  
scipy -> sp  
pandas -> pd  
matplotlib -> mpl  
matplotlib.pyplot -> plt  
seaborn -> sns  
datetime -> dt

**bad**

```

```

```
good
```

```
import numpy as np
```

```
import numpy
```

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

## **Why you should care**

Many well-known libraries have a conventions regarding which alias to use. Choosing a different one will not break the code but makes it less readable and harder to maintain for other developers.

## **Business Impacts**

*It is recommended to avoid these in order to ensure the code is more readable and cost effective.*

[Cost](http://casthighlight.wpengine.com/category/product/indicators-methodology/innovation/)

### CAST recommendations

### References

https://www.quantifiedcode.com/knowledge-base/readability/Consider%20using%20%27dt%27%20as%20alias%20for%20datetime%20imports/2c6u8cbQhttps://www.quantifiedcode.com/knowledge-base/readability/Use%20common%20abbreviations%20for%20libraries/7jRPIvMK

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)

c
