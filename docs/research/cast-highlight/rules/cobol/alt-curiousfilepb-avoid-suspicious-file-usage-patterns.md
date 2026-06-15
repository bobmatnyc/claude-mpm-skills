---
title: Suspicious File Usage patterns can be risky
url: https://doc.casthighlight.com/alt_curiousfilepb-avoid-suspicious-file-usage-patterns/
slug: alt_curiousfilepb-avoid-suspicious-file-usage-patterns
content_type: rule
languages: [cobol]
category: Robustness
has_code_examples: false
---

[Software Resiliency](http://casthighlight.wpengine.com/software-resiliency/)[Code Reliability](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# Risky catches increase production risks

This code insight counts a violation each time in a single cobol source file :

- a sorted file (SD) is never sorted : an instruction  
  **SD  *<SORT-FILE>*.**  
  is found in DATA DIVISION, but not corresponding  
  **SORT *<SORT-FILE>* …….**  
  is found in PROCEDURE DIVISION.
- a file (only FD) declared in data division is never open nor closed in the procedure division
- a file (only FD)declared in data division is open or close more than once, and the number of open is different from the number of closed.
- a file (FD or SD ) is open more than once.
- a file (FD or SD ) is closed more than once.

*Note : only files that are declared in the same file with a SELECT instruction in the FILE CONTROL paragraph of the INPUT-OUTPUT SECTION of the ENVIRONMENT DIVISION, are taken into account for this diag.*

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

## **Why you should care**

A file is not used properly or in compliance with its declaration.

## **Business Impacts**

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/innovation/)

### CAST recommendations

### References

https://www.quantifiedcode.com/knowledge-base/correctness/Inherit%20from%20%60BaseException%60%20for%20all%20custom%20exceptions/72tTnTsJ

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
