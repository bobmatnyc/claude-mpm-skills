---
title: Too much commented out code can be counter-productive
url: https://doc.casthighlight.com/alt_commentedoutcode-much-commented-code-can-counter-productive/
slug: alt_commentedoutcode-much-commented-code-can-counter-productive
content_type: rule
category: Changeability
has_code_examples: false
---

## **Too much commented out code can be counter-productive**

[Software Agility](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-agility/)[Embedded Documentation](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-agility/embedded-documentation/)

This code insight counts the number of comment lines that starts with keywords such as if, else, while, foreach, switch, etc. and ends with “;”, “{” or “}”. Depending on the density of commented out lines compared to total lines of code, Highlight counts penalty points for the scanned source file.

### **Why you should care**

Commented out code – some old code instructions that are left in comments – is one of the most wide-spread issues in source code. It could remain in your software forever, as a developer’s legacy to humanity or just in case it could be reused.  But when found in high density, it can distract the developer on what’s important (the really useful code that will be executed in production), and most of the time this commented out code is quickly obsolete and couldn’t work properly if it was uncommented.

References:  
<https://kentcdodds.com/blog/please-dont-commit-commented-out-code>

[How it works](http://casthighlight.wpengine.com/how-it-works/)[Features & Analytics](http://casthighlight.wpengine.com/outputs-analytics/)
