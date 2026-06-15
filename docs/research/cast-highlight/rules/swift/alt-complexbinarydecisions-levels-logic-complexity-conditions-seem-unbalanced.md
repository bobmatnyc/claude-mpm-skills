---
title: Levels of logic complexity and conditions seem to be unbalanced
url: https://doc.casthighlight.com/alt_complexbinarydecisions-levels-logic-complexity-conditions-seem-unbalanced/
slug: alt_complexbinarydecisions-levels-logic-complexity-conditions-seem-unbalanced
content_type: rule
languages: [swift]
category: Transferability
has_code_examples: false
---

[Software Elegance](http://casthighlight.wpengine.com/software-elegance/)[Code Complexity](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-elegance/code-complexity/)

# **Why you should care**

Managing software complexity is an art of balancing the different natures of complexity that code can exhibit. Ensuring that logical operators are not too frequently complex within logical conditions is one way to help developers spend more time adding new features instead of trying to figure out how to interpret when a condition is applicable. Ideally, simple combinations of logical operators makes the code easier to understand, adapt and fix, even if the source file is complex overall.

# **Business Impacts**

[Acceleration](http://casthighlight.wpengine.com/category/product/indicators-methodology/acceleration/)

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

# **CAST Recommendations**

In the context of this code insight, some IFs could be added in order to reduce the abnormally high ratio between logical operators and conditions.  Associated with another code insight that exclusively focuses on conditions complexity (Cyclomatic Complexity), these two complexity insights will help you find a good compromise between operators’ complexity and conditional complexity.

# **References**

<https://dzone.com/articles/code-complexity-is-killing-us>

[Style Guide](https://github.com/Kristories/awesome-guidelines)

# **How we detect**

This code insight counts the number of logical operators (AND and OR) and compares it to the number of condition expressions (IF, WHILE, FOR). Based on ratios and thresholds CAST has determined by thousands of complex software, Highlight counts penalty points for the scanned source file.

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
