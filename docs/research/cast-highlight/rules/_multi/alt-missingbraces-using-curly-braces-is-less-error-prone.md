---
title: "Using {curly braces} is less error-prone"
url: https://doc.casthighlight.com/alt_missingbraces-using-curly-braces-is-less-error-prone/
slug: alt_missingbraces-using-curly-braces-is-less-error-prone
content_type: rule
category: Security
has_code_examples: false
---

## **Using {curly braces} is less error-prone**

[Software Resiliency](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/)[Programming Best Practices](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/programming-best-practices/)

This code insight counts the number of missing curly braces in constructs such as functions, loops (while, do, for…) or conditional statements (if, else), except for “else” used within an “else if” statement. Highlight counts penalty points contributing to the Software Resiliency health factor, depending on the density of missing braces compared to the total braces you should ideally have in the scanned source file.

### **Why you should care**

Using curly braces – even if for some programming languages missing braces won’t block the application compilation/execution – helps developers visually identify where a code instruction or condition starts and where it stops. The absence of braces could lead to unexpected behaviors or possible security flaws, if for instance a developer mistakenly adds sensitive information or instructions inside or outside { } he/she couldn’t see because they were missing. This is especially true when the code is complex and contains a lot of logical conditions.

[How it works](http://casthighlight.wpengine.com/how-it-works/)[Features & Analytics](http://casthighlight.wpengine.com/outputs-analytics/)
