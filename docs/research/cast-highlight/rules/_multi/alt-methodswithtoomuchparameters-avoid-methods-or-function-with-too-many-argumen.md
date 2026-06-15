---
title: Methods with too many parameters can be complex
url: https://doc.casthighlight.com/alt_methodswithtoomuchparameters-avoid-methods-or-function-with-too-many-arguments/
slug: alt_methodswithtoomuchparameters-avoid-methods-or-function-with-too-many-arguments
content_type: rule
category: Transferability
has_code_examples: false
---

[Software Elegance](http://casthighlight.wpengine.com/software-elegance/)[Code Complexity](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-elegance/code-complexity/)

# **Why you should care**

For developers, it is important to consider that having too many arguments tends make the function excessively complex.  This increases development time as it becomes more difficult for others to use, and understand the offending sections of code.

# **Business Impacts**

Having too many parameters makes it difficult for developers to understand how to use a code base and collaborate on portions of code. This leads to high levels of backtracking and debugging, since developers have to remember and understand complex aspects while they are working. It is important to reduce this complexity to reduce needless expenditures of developer time and effort.

[Acceleration](http://casthighlight.wpengine.com/category/product/indicators-methodology/innovation/)

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

# **CAST Recommendations**

Implementing a style guide for all developers which outlines the maximum number of function arguments and places an emphasis on proper abstraction methodology for your application. Adding more layers of abstraction and further subdividing functions will reduce the complexity.

# **References**

<https://stackoverflow.com/questions/2244860/when-a-method-has-too-many-parameters>

[Style Guide](https://github.com/Kristories/awesome-guidelines)

# **How we detect**

This code insight counts one violation each time a function has more than X arguments where X is defined to 3.

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
