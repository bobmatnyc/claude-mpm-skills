---
title: Automatic numbering increases costs
url: https://doc.casthighlight.com/alt_automaticnumbering-automatic-numbering-increases-costs/
slug: alt_automaticnumbering-automatic-numbering-increases-costs
content_type: rule
languages: [python]
category: Transferability
has_code_examples: false
---

[Cost](http://casthighlight.wpengine.com/category/product/indicators-methodology/cost/)[Software Agility](http://casthighlight.wpengine.com/software-resiliency/)[Code Readability](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# **Automatic numbering increases costs**

This code insight counts one violation each a string contains empty format replacement fields.

bad

print “{} is {}”.format(“life”,”hard”)

good

print “{0} is {1}”.format(“life”,”hard”)

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

## **Why you should care**

If you are not numbering your replacement fields {} in your format string, Python auto-numbers them. For example, using “{} {}” is interpreted as {0} {1}. This is correct code, but is hard to read if you use a large number of parameters. If a format string is particularly long, it is difficult to tell which replacement fields relate to which argument of your format string. Especially if code is refactored, unnumbered replacement fields are often not in sync with the arguments of the format string.

## **Business Impacts**

*It is recommended to avoid these in order to ensure the code is more readable and cost effective.*

[Cost](http://casthighlight.wpengine.com/category/product/indicators-methodology/innovation/)

### CAST recommendations

### References

https://www.quantifiedcode.com/knowledge-base/maintainability/Explicitly%20number%20replacement%20fields%20in%20a%20format%20string/3aSZNLMu

.

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
