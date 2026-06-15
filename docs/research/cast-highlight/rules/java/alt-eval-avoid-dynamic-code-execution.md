---
title: eval() evaluates statements
url: https://doc.casthighlight.com/alt_eval-avoid-dynamic-code-execution/
slug: alt_eval-avoid-dynamic-code-execution
content_type: rule
languages: [java, javascript]
has_code_examples: false
---

[Software Resiliency](http://casthighlight.wpengine.com/software-resiliency/)[Code Reliability](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# **Why you should care**

Eval() is a function property of the global object. The argument of the of the eval() function is a string. If the string represents an expression, eval() evaluates the expression. If the argument represents one or more JavaScript statements, eval() evaluates the statements. Do not use eval() to evaluate an arithmetic expression as JavaScript automatically evaluates arithmetic expressions.

# **Business Impacts**

eval() can be a double-edged sword if used improperly which tends to be unproductive. One the one hand, eval() can successfully evaluate statements when strings are included. However, it cannot be used to evaluate anything else as that would result in a loss of time.

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/risk/)

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

# **CAST Recommendations**

# **References**

<https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/eval>

[Style Guide](https://github.com/Kristories/awesome-guidelines)

# **How we detect**

This code insight focuses on how an eval() works.This function takes an arbitrary string and executes it as JavaScript code. When the code in question is known beforehand (not determined at runtime), there’s no reason to use eval(). If the code is dynamically generated at runtime, there’s often a better way to achieve the goal without eval() :  
using square bracket notation to access dynamic properties is better and simpler  
using browsers’ built-in methods (JSON.parse, when dealing with a JSON response from an Ajax request)  
It’s also important to remember that passing strings to setInterval(), setTimeout(), and the Function() constructor is, for the most part, similar to using eval() and therefore should be avoided. Behind the scenes, JavaScript still has to evaluate and execute the string you pass as programming code.

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
