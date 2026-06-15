---
title: Too many global variables can be unproductive
url: https://doc.casthighlight.com/alt_applicationglobalvariables-the-code-contains-too-many-implied-global-variables-to-prevent-conflicts-in-global-scope-all-variables-should-be-explicitely-declared-and-if-possible-not-in-global-sco/
slug: alt_applicationglobalvariables-the-code-contains-too-many-implied-global-variables-to-prevent-conflicts-in-global-scope-all-variables-should-be-explicitely-declared-and-if-possible-not-in-global-sco
content_type: rule
has_code_examples: false
---

[Software Resiliency](http://casthighlight.wpengine.com/software-resiliency/)[Code Reliability](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# **Why you should care**

Global variables should be encapsulated in a class and doing so can make code more productive.

# **Business Impacts**

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/risk/)

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

# **CAST Recommendations**

# **References**

<https://stackoverflow.com/questions/9765942/space-after-function-name-is-wrong>

[Style Guide](https://github.com/Kristories/awesome-guidelines)

# **How we detect**

This code insight counts a violation each time there are too many global variables

int m\_iGlobal = 0;

void m()  
{  
m\_iGlobal = 1; // VIOLATION  
}

Remedy

Create a static data member in the appropriate class to replace the global variable.

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
