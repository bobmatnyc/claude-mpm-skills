---
title: Operators and operands should use appropriate spacing to help readability
url: https://doc.casthighlight.com/alt_badspacing-operators-operands-use-appropriate-spacing-help-readability/
slug: alt_badspacing-operators-operands-use-appropriate-spacing-help-readability
content_type: rule
languages: [php]
category: Changeability
has_code_examples: false
---

## **Operators and operands should use appropriate spacing to help readability**

[Software Agility](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-agility/)[Code Readability](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-agility/code-readability/)

This code insights verifies that operators and operands are generally surrounded with spaces for better readability. Depending on thresholds CAST has defined, Highlight counts penalty points for the scanned file if missing spaces are too frequent.

### **Why you should care**

Itishardertoquicklyunderstandwordsthatarenotseparatedwithspaces, don’t you think? This is the same for code, especially when defining logical conditions or loops with operators (e.g. &&, ||, >=, etc.) and operands. Adding spaces before and after operators and operands will makes software easier to read.

References:  
<https://msu.edu/~hanson54/cse232/coding-style.html#ws>  
<http://syque.com/cstyle/ch6.2.htm>

### **CAST recommendations**

Ideally, spaces should be added before and after each operator and operand, as shown in the example below.

**Very packed IF condition (PHP):**

if((!empty($foo)&&$foo>=$number)||($number<=(10\*10))) { …

**Same IF condition with some spaces:**

if((!empty($foo) && $foo >= $number) || ($number <= (10 \* 10))) { …

[How it works](http://casthighlight.wpengine.com/how-it-works/)[Features & Analytics](http://casthighlight.wpengine.com/outputs-analytics/)
