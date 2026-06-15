---
title: Avoid Implied Typecasting
url: https://doc.casthighlight.com/alt_missingidentical-avoid-implied-typecasting/
slug: alt_missingidentical-avoid-implied-typecasting
content_type: rule
languages: [java, javascript]
category: Security
has_code_examples: false
---

[Software Resiliency](http://casthighlight.wpengine.com/software-resiliency/)[Code Reliability](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# **Why you should care**

Software development is an exact science and software doesn’t really like having doubts. Some programming languages have different ways to evaluate and compare manipulated information.  In the case of this code insight, a syntax confusion due to an implicit interpretation (e.g. using “==” instead of “===” in Javascript) may lead to bad data manipulation in production and possibly generates unwanted bugs and security flaws (by allowing the software to execute portions of code you wasn’t expecting).  An example to illustrate: it’s not because you say “true” (will be interpreted by the software as a string) that it really is (interpreted by the software as a state TRUE).

# **Business Impacts**

Implied Typecasting is not extremely harmful to code but it is a sign of bad practice being displayed in development teams which can indicate symptoms of productivity issues.  It is helpful to prevent these issues by employing standard company policies which discourage such practices. Otherwise it can hamper the agile environment set by the company.

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/innovation/)

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

# **CAST Recommendations**

The good practice is to systematically use braces. Modern development environments can automatically add them when writing new code. Ideally, from a pure maintainability standpoint, the braces should also have a dedicated line for even greater readability.

# **References**

JavaScript Patterns: Build Better Applications with Coding and Design Patterns, by Stoyan Stefanov (O’Reilly)  
[https://code.tutsplus.com/tutorials/the-essentials-of-writing-high-quality-javascript–net-15145](https://code.tutsplus.com/tutorials/the-essentials-of-writing-high-quality-javascript--net-15145)

[Style Guide](https://github.com/Kristories/awesome-guidelines)

# **How we detect**

This code insight counts the number of cases where a “falsy“ literal operand (false, 0, [], undefined, “”) is compared by using “==” or “!=”, or when a variable is implicitly verified (true or false) without using a comparison or logical operator (e.g. if(data) { … }). Depending on the usage density of this pattern, Highlight counts penalty points contributing to the Software Resiliency health factor for the scanned source file.

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
