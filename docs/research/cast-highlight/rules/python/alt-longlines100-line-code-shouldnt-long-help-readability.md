---
title: A line of code shouldn’t be too long (to help readability)
url: https://doc.casthighlight.com/alt_longlines100-line-code-shouldnt-long-help-readability/
slug: alt_longlines100-line-code-shouldnt-long-help-readability
content_type: rule
languages: [python]
category: Changeability
has_code_examples: false
---

## **A line of code shouldn’t be too long (to help readability)**

[Software Agility](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-agility/)[Code Readability](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-agility/code-readability/)

This code insight counts the number of characters for each line of code and verifies that an application doesn’t globally contain too many long lines. Depending on thresholds defined by CAST based on its expertise and experience in measuring software, Highlight counts penalty points contributing to the Software Agility health factor.

### **Why you should care**

A piece of source code in your software could be compared to a page of a book.  In a book, a human can’t easily read and understand a very long line – it’s all about eye comfort. That’s even more true when reading code, since each keyword could be translated into many words (e.g. “!=” means “is different than”).  In addition to negatively affecting readability, having very long lines can destroy the positive impact of code indentation, which makes the code even harder to understand and maintain (because of chaotic line returns).  Having shorter lines of code in your application can help developers more quickly understand how the code works.  It also tends to reduce semantic misinterpretations that could drive to unexpected behaviors (i.e. bugs).

References:  
<http://legacy.python.org/dev/peps/pep-0008/#maximum-line-length>

[How it works](http://casthighlight.wpengine.com/how-it-works/)[Features & Analytics](http://casthighlight.wpengine.com/outputs-analytics/)
