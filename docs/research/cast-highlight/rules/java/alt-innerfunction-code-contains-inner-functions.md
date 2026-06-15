---
title: The code contains inner functions
url: https://doc.casthighlight.com/alt_innerfunction-code-contains-inner-functions/
slug: alt_innerfunction-code-contains-inner-functions
content_type: rule
languages: [java, javascript]
has_code_examples: true
---

[SOFTWARE RESILIENCY](https://doc.casthighlight.com/software-resiliency/)

[BEST PRACTICES](https://doc.casthighlight.com/category/product/indicators-methodology/code-insights/software-resiliency/best-practices/)

# **Why you should care**

While most script engines support Function Declarations within blocks it is not part of ECMAScript (see ECMA-262, clause 13 and 14). Worse implementations are inconsistent with each other and with future EcmaScript proposals. ECMAScript only allows for Function Declarations in the root statement list of a script or function. Instead use a variable initialized with a Function Expression to define a function within a block.

# **How we detect**

This Code Insight counts one occurrence each time a function is declared in a block:

**Bad Code**

```
if (x) {
function foo() {}
}
```

**Good Code**

```
function bar() {
  function inner() {return i;}
  if (x) {
     var foo = function() {}; 
   }
}
```

# **References**

<https://stackoverflow.com/questions/15663098/function-declarations-should-not-be-placed-in-blocks>  
<https://rules.sonarsource.com/javascript/RSPEC-1530>

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

[SEE FEATURES](https://www.castsoftware.com/products/highlight/outputs-analytics)

[HOW IT WORKS](https://www.castsoftware.com/products/highlight/how-it-works)
