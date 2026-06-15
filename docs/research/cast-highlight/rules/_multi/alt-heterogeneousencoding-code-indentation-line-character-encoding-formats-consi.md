---
title: "Code indentation, line, and character encoding formats should be consistent"
url: https://doc.casthighlight.com/alt_heterogeneousencoding-code-indentation-line-character-encoding-formats-consistent/
slug: alt_heterogeneousencoding-code-indentation-line-character-encoding-formats-consistent
content_type: rule
category: Changeability
has_code_examples: false
---

## **Code indentation, line, and character encoding formats should be consistent**

[Software Agility](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-agility/)[Code Readability](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-agility/code-readability/)

This code insights detects when different code formatting styles are heterogeneous (CRLF, CR or LF for new line formatting, full spaces, tab spaces … for identations, UTF8, Windows-1252 … for character encoding). Depending on the number of different styles used within a given scanned source file, Highlight counts penalty points accordingly.

### **Why you should care**

Considering if a coding style (e.g. double space or tab to indent a line) is better than another is an opinion and disputable. However, the formatting style should be consistent across a code base. It makes the source code much easier to read, thus more comfortable to work with.

References:  
[https://code.tutsplus.com/tutorials/top-15-best-practices-for-writing-super-readable-code–net-8118](https://code.tutsplus.com/tutorials/top-15-best-practices-for-writing-super-readable-code--net-8118)

### **CAST recommendations**

Static code analysis tools can automate this code insight verification. Ideally, a unique code formatting style should be adopted technology wide, at least within a given application.

[How it works](http://casthighlight.wpengine.com/how-it-works/)[Features & Analytics](http://casthighlight.wpengine.com/outputs-analytics/)
