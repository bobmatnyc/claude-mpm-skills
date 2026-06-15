---
title: Avoid classes with missing destructor declarations in header files
url: https://doc.casthighlight.com/alt_missingclassdestructor-avoid-classes-with-missing-destructor-declarations-in-header-files/
slug: alt_missingclassdestructor-avoid-classes-with-missing-destructor-declarations-in-header-files
content_type: rule
languages: [cpp]
category: Robustness
has_code_examples: false
---

# Avoid classes with missing destructor declarations in header files

[Software Resiliency](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/)[Programming Best Practices](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/programming-best-practices/)

This code insight verifies in C++ applications if classes in header files (.h) haven’t declared destructors. Highlight counts one occurrence for each missing class destructor found in a header file.

### **Why you should care**

In some cases, missing class destructors can lead to memory leaks, causing software unstability.

[How it works](http://casthighlight.wpengine.com/how-it-works/)[Features & Analytics](http://casthighlight.wpengine.com/outputs-analytics/)
