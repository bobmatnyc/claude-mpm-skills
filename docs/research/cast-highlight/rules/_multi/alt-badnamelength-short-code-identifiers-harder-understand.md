---
title: Short code identifiers are harder to understand
url: https://doc.casthighlight.com/alt_badnamelength-short-code-identifiers-harder-understand/
slug: alt_badnamelength-short-code-identifiers-harder-understand
content_type: rule
has_code_examples: false
---

## **Short code identifiers are harder to understand**

[Software Agility](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-agility/)[Embedded Documentation](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-agility/embedded-documentation/)

This code insight counts the number of code identifiers (such as class, function, method, attribute names, etc.) whose length is lower than a predefined number of characters for each technology. Depending on the density of these short identifiers vs. all identifiers, Highlight counts penalty points for the given file.

### **Why you should care**

Have you ever attended a meeting where everybody continuously talks with acronyms and you don’t have a clue on what they’re referring to?  It’s very similar with short code identifiers. A method should textually indicate what it does (e.g. getLatestCustomerOrders instead of getLCO, deleteMyHardDrive instead of delete\_MHD) to help developers understand the code as they naturally think. Having a self-explanatory artifact name tends to reduce maintenance effort, and can help to avoid mistakes.

[How it works](http://casthighlight.wpengine.com/how-it-works/)[Features & Analytics](http://casthighlight.wpengine.com/outputs-analytics/)
