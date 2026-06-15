---
title: Short functions and identifiers increase costs
url: https://doc.casthighlight.com/alt_badnamelength-avoid-short-function-or-methods-name/
slug: alt_badnamelength-avoid-short-function-or-methods-name
content_type: rule
languages: [java, javascript]
category: Changeability
has_code_examples: false
---

[Software Agility](http://casthighlight.wpengine.com/software-agility/)[Embedded Documentation](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-agility/embedded-documentation/)

# **Why you should care**

Developers tend to shorten the text required for writing code to save time and get it running. However, using short, nondescript function/variable names increases the need for excessive commenting and makes it more difficult for developers to collaborate and understand each other’s code. It also can be a source of inter-team conflict about naming conventions.

# **Business Impacts**

Having shortened methods and identifiers makes it difficult to developers to understand what different sections of code do — this can cause an increase in collaborative development time, which in turn, leads to excess cost. Disagreements in naming convention can also be a source of conflict between team members, which impacts team effectiveness.

“Well-chosen identifiers make it significantly easier for developers and analysts to understand what the system is doing and how to fix or extend the source code to apply for new needs.”

[Cost](http://casthighlight.wpengine.com/category/product/indicators-methodology/innovation/)

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

# **CAST Recommendations**

A unified naming convention should also be established for each programming language used, with and exact style and methodology to name variables and functions. (See reference on “Naming Convention”). This will lead to the use of more verbose and descriptive function and identifier names, which in turn will increase code readability and allow portions of code easily “self-document”. This will also reduce the effort needed for other team members to read and understand the source code.

# **References**

<https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Functions>

<https://www.w3schools.com/js/js_syntax.asp>

<https://en.wikipedia.org/wiki/Naming_convention_(programming)>

<https://en.wikipedia.org/wiki/Self-documenting_code>

[Style Guide](https://github.com/Kristories/awesome-guidelines)

# **How we detect**

This code insight computes the average length of functions and identifiers encountered in the script and determines if the length is understandable.

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
