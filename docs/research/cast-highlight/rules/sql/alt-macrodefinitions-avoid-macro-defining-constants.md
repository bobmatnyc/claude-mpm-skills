---
title: Macro definitions cause resiliency issues
url: https://doc.casthighlight.com/alt_macrodefinitions-avoid-macro-defining-constants/
slug: alt_macrodefinitions-avoid-macro-defining-constants
content_type: rule
languages: [sql]
has_code_examples: false
---

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/risk/)[Software Resiliency](http://casthighlight.wpengine.com/software-resiliency/)[Code Reliability](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# **Macro definitions cause resiliency issues**

This code insight counts one violation each time a macro without parameters defines a literal constant.

Literal constants are number, character or strings :  
– numbers, possibly preceded with **.** or **\**  
– characters enclosed with **‘**  
– strings, enclosed with ‘ or **“**

Exemple of violations : (**123**, **.25**, **\123**), un caractere (**‘…’**) ou une chaine (**“…”**)

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

## **Why you should care**

Code with macro definitions can cause resiliency issues.

## **Business Impacts**

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/innovation/)

### CAST recommendations

### References

https://www.tutorialspoint.com/sql/sql-transactions.htm

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
