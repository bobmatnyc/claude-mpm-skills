---
title: Backslash line continuation makes code less readable
url: https://doc.casthighlight.com/alt_multilineinstruction-backslash-line-continuation-makes-code-less-readable/
slug: alt_multilineinstruction-backslash-line-continuation-makes-code-less-readable
content_type: rule
languages: [python, java]
category: Changeability
has_code_examples: false
---

[Cost](http://casthighlight.wpengine.com/category/product/indicators-methodology/cost/)[Software Agility](http://casthighlight.wpengine.com/software-resiliency/)[Code Readability](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# **Backslash line continuation makes code less readable**

This code insight shows that each time a backslash is the last non blank character of a line.

Bad

my\_very\_big\_string = “”””””For a long time I used to go to bed early. Sometimes, \  
when I had put out my candle, my eyes would close so quickly that I had not even \  
time to say “I’m going to sleep.”””””””

from some.deep.module.inside.a.module import a\_nice\_function, another\_nice\_function, \  
yet\_another\_nice\_function

Good

my\_very\_big\_string = (  
“”For a long time I used to go to bed early. Sometimes, “”  
“”when I had put out my candle, my eyes would close so quickly “”  
“”that I had not even time to say “I’m going to sleep.”””  
)

from some.deep.module.inside.a.module import (  
a\_nice\_function, another\_nice\_function, yet\_another\_nice\_function)

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

## **Why you should care**

*When a logical line of code is longer than the accepted limit, you need to split it over multiple physical lines. The Python interpreter will join consecutive lines if the last character of the line is a backslash. This is helpful in some cases, but should usually be avoided because of its fragility: a white space added to the end of the line, after the backslash, will break the code and may have unexpected results.*

*A better solution is to use parentheses around your elements. Left with an unclosed parenthesis on an end-of-line the Python interpreter will join the next line until the parentheses are closed. The same behavior holds for curly and square braces.*

## **Business Impacts**

*It is recommended to avoid these in order to ensure the code is more readable and cost effective.*

[Cost](http://casthighlight.wpengine.com/category/product/indicators-methodology/innovation/)

### CAST recommendations

### References

http://support.objectivity.com/sites/default/files/docs/objy/R11\_0\_0/html/java/guide/jgdObjectQualification.html

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
