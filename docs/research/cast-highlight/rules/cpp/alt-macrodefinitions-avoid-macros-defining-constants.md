---
title: Avoid macros defining constants
url: https://doc.casthighlight.com/alt_macrodefinitions-avoid-macros-defining-constants/
slug: alt_macrodefinitions-avoid-macros-defining-constants
content_type: rule
languages: [cpp]
has_code_examples: false
---

# Avoid macros defining constants

[Software Resiliency](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/)[Code Reliability](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

This code insight verifies in C++ applications when macros without parameters define a literal constant. Depending on the density of occurrences and the thresholds set for this code insight, Highlight counts penalty points for the scanned file.

Literal constants are numbers, characters or strings (numbers, possibly preceded with . or \, characters enclosed with ‘, strings, enclosed with ‘ or “).

### **Why you should care**

As macros do not obey the C++ scope and type rules, this often leads to subtle and not-so-subtle problems, causing unexpected behaviors or compilation issues.

[How it works](http://casthighlight.wpengine.com/how-it-works/)[Features & Analytics](http://casthighlight.wpengine.com/outputs-analytics/)
