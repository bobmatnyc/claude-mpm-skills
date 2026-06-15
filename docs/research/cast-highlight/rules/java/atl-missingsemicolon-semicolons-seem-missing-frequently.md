---
title: Semicolons seem to be missing too frequently
url: https://doc.casthighlight.com/atl_missingsemicolon-semicolons-seem-missing-frequently/
slug: atl_missingsemicolon-semicolons-seem-missing-frequently
content_type: rule
languages: [java, javascript]
category: Robustness
has_code_examples: false
---

## **Semicolons seem to be missing too frequently**

[Software Resiliency](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/)[Code Reliability](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

This code insight verifies that semicolons are not missing too frequently. Depending on the calculated density and based on thresholds CAST has defined by analyzing hundreds of Javascript projects, Highlight counts penalty points to the scanned file.

### **Why you should care**

Although Javascript provides more flexibility in the syntax compared to other more “rigid” programming languages (that’s typically the case for semicolons which are not always necessary for the code to be properly interpeted), it might cause unexpected behaviors in some specific circumstances. More precisely, if your application Javascript files are generally minified (spaces and line breaks are stripped out in order to reduce the file size) and semicolons are missing, your script just could crash or not return the expected value as shown in the code example below.

Code without optional semicolons, with a line break:

return  
 a + b;

Javascript will automatically deal with missing semicolons and will unexpectedly interpret the code this way:

return;  
 a + b;

This script will return nothing, then will add a + b, while the expected behavior is to return the result of a + b.

Also, from a readability standpoint, it is always better to adopt a unique coding style.

References:  
<http://cjihrig.com/blog/the-dangers-of-javascripts-automatic-semicolon-insertion/>  
<http://inimino.org/~inimino/blog/javascript_semicolons>

### **CAST recommendations**

Since using semicolons where mandatory is the majority of cases, they should also be used when optional.

[How it works](http://casthighlight.wpengine.com/how-it-works/)[Features & Analytics](http://casthighlight.wpengine.com/outputs-analytics/)
