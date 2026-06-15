---
title: Conditional expressions should not be too complex
url: https://doc.casthighlight.com/alt_complexconditions-the-code-contains-too-many-complex-conditions-conditionals-expressions-with-at-least-and-logical-operator-and-composed-with-too-many-simple-contitions-comparisons-expres/
slug: alt_complexconditions-the-code-contains-too-many-complex-conditions-conditionals-expressions-with-at-least-and-logical-operator-and-composed-with-too-many-simple-contitions-comparisons-expres
content_type: rule
category: Transferability
has_code_examples: false
---

[Software Elegance](http://casthighlight.wpengine.com/category/product/indicators-methodology/software-elegance)[Code Complexity](http://casthighlight.wpengine.com/category/product/indicators-methodology/software-elegance/code-complexity/)

# **Why you should care**

Having complex conditional expressions in your software might slow down your development team to quickly evaluate if and how the code will be run within these conditions. In addition, if conditions are misunderstood because there are too complex (especially when additional native functions like “!empty” or “!isset” makes the whole condition even more complex) , it might create unexpected behaviors during the QA phase or, more badly, in production if the logic path that verifies a condition hasn’t been followed by testers.

# **Business Impacts**

Complex conditional operations can cause loss of time in an attempt to understand the code. It also decreases the innovation capabilities of the code. These factors can make the code unsuitable for clients.

[Acceleration](http://casthighlight.wpengine.com/category/product/indicators-methodology/acceleration/)

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

# **CAST Recommendations**

# **References**

[Style Guide](https://github.com/Kristories/awesome-guidelines)

# **How we detect**

This code insight verifies that source code doesn’t frequenlty contain too complex logical conditions, by looking at their number of distinct operators (mainly AND and OR). Based on specific thresholds to define whether a condition is complex or not, and depending on the frequency of occurences found in the code, Highlight counts penalty points to the scanned file.

Example of a simple conditional expression:  
(a && b && c && d && e && f) is not complex, because there is no distinct operators.

Example of a complex conditional expression:  
((a && b && c) || (d && e || f)) is complex.

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
