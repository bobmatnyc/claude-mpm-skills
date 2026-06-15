---
title: Long try blocks can cause risk in code
url: https://doc.casthighlight.com/alt_longtry-avoid-long-try-blocks/
slug: alt_longtry-avoid-long-try-blocks
content_type: rule
languages: [sql]
category: Robustness
has_code_examples: true
---

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/risk/)[Software Resiliency](http://casthighlight.wpengine.com/software-resiliency/)[Code Reliability](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# **Long try blocks can cause risk in code**

This code insight computes the integer part of the average size of all “try” block in number of lines of code.

For one “try” block, count the number of line of code between the “try” keyword and the first “except” keyword.

Example : in the following code, the “try” size is 4 lines:

```
try:
   # Yooo
   ordering = related_admin.get_ordering(request)
   # following line is empty

   # back to code
   if toto :
       print("toto")
       return
except toto: 
   titi()
```

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

## **Why you should care**

The larger the body of the try, the more likely that an exception will be raised by a line of code that you didn’t expect to raise an exception. In those cases, the try/except block hides a real error

## **Business Impacts**

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/innovation/)

### CAST recommendations

### References

https://www.tutorialspoint.com/sql/sql-transactions.htm

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
