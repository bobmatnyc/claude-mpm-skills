---
title: A line of code shouldn’t be too long (to help readability)
url: https://doc.casthighlight.com/alt_longlines-a-line-of-code-shouldnt-be-too-long-to-help-readability/
slug: alt_longlines-a-line-of-code-shouldnt-be-too-long-to-help-readability
content_type: rule
category: Changeability
has_code_examples: false
---

[Software Agility](http://casthighlight.wpengine.com/software-agility/)[Code Readability](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-agility/code-readability/)

# **Why you should care**

A piece of source code in your software could be compared to a page of a book.  In a book, a human can’t easily read and understand a very long line – it’s all about eye comfort. That’s even more true when reading code, since each keyword could be translated into many words (e.g. “!=” means “is different than”).  In addition to negatively affecting readability, having very long lines can destroy the positive impact of code indentation, which makes the code even harder to understand and maintain (because of chaotic line returns).  Having shorter lines of code in your application can help developers more quickly understand how the code works.  It also tends to reduce semantic misinterpretations that could drive to unexpected behaviors (i.e. bugs).

# **Business Impacts**

[Cost](http://casthighlight.wpengine.com/category/product/indicators-methodology/cost/)

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

# **CAST Recommendations**

Static code analysis tools can help your development teams identify this code insight, while peer code review is useful to educate the long-line addicts. Ideally, one line of code is a unit element that means or performs something specific – a part of a sentence if you will.

It is generally agreed that the ideal length for a line of code is from 80 to 100 characters.

# **References**

<https://stackoverflow.com/questions/9765942/space-after-function-name-is-wrong>

[Style Guide](https://github.com/Kristories/awesome-guidelines)

# **How we detect**

This code insight counts the number of characters for each line of code and verifies that an application doesn’t globally contain too many long lines. Depending on thresholds defined by CAST based on its expertise and experience in measuring software, Highlight counts penalty points contributing to the Software Agility health factor.

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
