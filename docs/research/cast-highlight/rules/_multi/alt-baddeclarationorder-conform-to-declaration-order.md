---
title: Good declaration Order in JSP can reduce costs
url: https://doc.casthighlight.com/alt_baddeclarationorder-conform-to-declaration-order/
slug: alt_baddeclarationorder-conform-to-declaration-order
content_type: rule
category: Changeability
has_code_examples: false
---

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/risk/)[Software Resiliency](http://casthighlight.wpengine.com/software-resiliency/)[Programming Best Practices](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# Good declaration Order in JSP can reduce costs

This code insight counts a violation each time a page do not conform to the following declaration layout: a JSP file consists of the following sections in the order they are listed:

– Opening comments  
– JSP page directive(s)  
– Optional tag library directive(s)  
– Optional JSP declaration(s)  
– HTML and JSP code

Note : if several violation are encountered, only a global violation for the file is counted.

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

## **Why you should care**

Having a declaration order can improve Software Readability.

## **Business Impacts**

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/innovation/)

### CAST recommendations

### References

https://www.quantifiedcode.com/knowledge-base/correctness/%60else%60%20clause%20on%20a%20loop%20without%20a%20%60break%60%20statement/4aqWoDeY

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
