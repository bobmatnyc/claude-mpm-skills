---
title: Lack of multiple-inclusion protection in header files
url: https://doc.casthighlight.com/alt_missingincludeprotections-lack-of-multiple-inclusion-protection-in-header-files/
slug: alt_missingincludeprotections-lack-of-multiple-inclusion-protection-in-header-files
content_type: rule
languages: [cpp]
has_code_examples: false
---

# Lack of multiple-inclusion protection in header files

##

[Software Resiliency](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/)[Programming Best Practices](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/programming-best-practices/)

This code insight verifies in C++ applications that header files (.h) are protected against multiple inclusion. If a header file is not using the appropriate syntax, Highlight counts an occurrence.

### **Why you should care**

The basic use of header files is to provide symbol declarations for functions and globals. Because multiple declarations of a given symbol in a single translation unit are a syntax error, you have to defensively structure your header files to not redefine anything in case they are included multiple times.

[How it works](http://casthighlight.wpengine.com/how-it-works/)[Features & Analytics](http://casthighlight.wpengine.com/outputs-analytics/)
