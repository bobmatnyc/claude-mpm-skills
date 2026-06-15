---
title: Avoid classes using incorrect dynamic allocation
url: https://doc.casthighlight.com/alt_baddynamicclassdefinitions-avoid-classes-using-incorrect-dynamic-allocation/
slug: alt_baddynamicclassdefinitions-avoid-classes-using-incorrect-dynamic-allocation
content_type: rule
has_code_examples: false
---

# Avoid classes using incorrect dynamic allocation

[Software Resiliency](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/)[Programming Best Practices](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/programming-best-practices/)

This code insights verifies classes that don’t use dynamic allocation correctly, i.e. without constructors by copy or without allocation operator. Depending on the density of occurrences and specific thresholds, Highlight counts penalty points to the scanned file.

### **Why you should care**

Classes with incorrect dynamic allocation can lead to unexpected behaviors.

[How it works](http://casthighlight.wpengine.com/how-it-works/)[Features & Analytics](http://casthighlight.wpengine.com/outputs-analytics/)
