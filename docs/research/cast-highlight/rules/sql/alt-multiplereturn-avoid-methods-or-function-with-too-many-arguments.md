---
title: Multiple Significant Returns are risky for the code
url: https://doc.casthighlight.com/alt_multiplereturn-avoid-methods-or-function-with-too-many-arguments/
slug: alt_multiplereturn-avoid-methods-or-function-with-too-many-arguments
content_type: rule
languages: [sql]
category: Robustness
has_code_examples: false
---

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/risk/)[Software Resiliency](http://casthighlight.wpengine.com/software-resiliency/)[Code Reliability](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# **Multiple Significant Returns are risky for the code**

This code insight counts one violation each time a function has several meaningful return statements. Meaningful return statements are returning an expression different from **<nothing>**, **None** and **False**.

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

## **Why you should care**

When a function grows in complexity it is not uncommon to use multiple return statements inside the function’s body. However, in order to keep a clear intent and a sustainable readability level, it is preferable to avoid returning meaningful values from many output points in the body.

There are two main cases for returning values in a function: the result of the function return when it has been processed normally, and the error cases that indicate a wrong input parameter or any other reason for the function to not be able to complete its computation or task.

If you do not wish to raise exceptions for the second case, then returning a value, such as None or False, indicating that the function could not perform correctly might be needed. I**n this case, it is better to return as early as the incorrect context has been detected**. It will help to flatten the structure of the function: all the code after the return-because-of-error statement can assume the condition is met to further compute the function’s main result. Having multiple such return statements is often necessary.

## **Business Impacts**

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/innovation/)

### CAST recommendations

### References

https://www.tutorialspoint.com/sql/sql-transactions.htm

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
