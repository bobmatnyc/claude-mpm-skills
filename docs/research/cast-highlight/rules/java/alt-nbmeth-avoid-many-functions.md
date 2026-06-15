---
title: Declaring too many functions can make Javascript code complex
url: https://doc.casthighlight.com/alt_nbmeth-avoid-many-functions/
slug: alt_nbmeth-avoid-many-functions
content_type: rule
languages: [java, javascript]
category: Efficiency
has_code_examples: false
---

[Software Elegance](http://casthighlight.wpengine.com/category/product/indicators-methodology/software-elegance)[Code Complexity](http://casthighlight.wpengine.com/category/product/indicators-methodology/software-elegance/code-complexity/)

# **Why you should care**

A JavaScript file should not declare an excessive number of functionssince a higher number of functionalities declared in a module increase the complexity of this module and slows down the effectiveness of the code.

Too many functions can also lead to bigger file sizes which leads to reduced compactness of the code.

# **Business Impacts**

Further increasing the complexity of the code can harm the business-applications of the code in terms of overall productivity and it’s speed.  Code that is incredibly complex might not grow and evolve.

[Acceleration](http://casthighlight.wpengine.com/category/product/indicators-methodology/innovation/)

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

# **CAST Recommendations**

CAST recommends limiting the number of literal functions assigned to global variables as well as lowering the amount of declaring global functions.  It is fine to incorporate inner functions and literal functions without assigning them to global variables to ensure the code can provide accelerated progress for the portfolio.

# **References**

https://www.quora.com/Will-too-many-JavaScript-functions-negatively-impact-performance-How-about-if-there-are-several-AJAX-calls-to-render-the-template

[Style Guide](https://github.com/Kristories/awesome-guidelines)

# **How we detect**

This code insight is defined in the alarm model of the javascript langiuage, but following items should be counted :

- global functions declarations
- literal functions assigned to global var.

Are not concerned :

- inner functions
- literal functions (if assigned to local var)
- anonymous functions (if assigned to local var)

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
