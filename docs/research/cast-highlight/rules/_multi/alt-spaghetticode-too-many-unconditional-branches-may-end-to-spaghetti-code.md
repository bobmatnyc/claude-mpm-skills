---
title: Too many unconditional branches may end to Spaghetti Code
url: https://doc.casthighlight.com/alt_spaghetticode-too-many-unconditional-branches-may-end-to-spaghetti-code/
slug: alt_spaghetticode-too-many-unconditional-branches-may-end-to-spaghetti-code
content_type: rule
has_code_examples: false
---

## Too many unconditional branches may end to Spaghetti Code

[Software Resiliency](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/)[Programming Best Practices](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/programming-best-practices/)

This code insight counts the number of unconditional branches (e.g. GOTO, continue, break except if it is at end of a ‘case statement’…). Highlight counts penalty points contributing to the Software Resiliency health factor, depending on the density of this pattern you should ideally have in the scanned source file.

### **Why you should care**

Using on a too frequent basis the statements GOTO, continue or break implies a cerebral gymnastic to follow how the program executes, while a good code should be read easily. Having multiple unconditional branches into a single file, when combined with a high amount of code, increases the chances for a develop to introduce new bugs.

[How it works](http://casthighlight.wpengine.com/how-it-works/)[Features & Analytics](http://casthighlight.wpengine.com/outputs-analytics/)
