---
title: Having an assignment to “this” can be unproductive
url: https://doc.casthighlight.com/alt_object-avoid-having-the-assignment-to-this/
slug: alt_object-avoid-having-the-assignment-to-this
content_type: rule
languages: [php, sql]
category: Efficiency
has_code_examples: false
---

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/risk/)[Software Resiliency](http://casthighlight.wpengine.com/software-resiliency/)[Code Reliability](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# **Having an assignment to “this” can be unproductive**

This code insight counts a violation each time the PHP script has an assignment to “this”

“This report lists all the Classes containing assignements to ‘$this’.

It provides the following information:  
Class full name.”

Remedy –

Modify the source code and do not assign to ‘$this’.

” <?php  
class foo {

function foo(){  
// construct  
}

function bar(){  
$this = true;  
}  
}  
?>  
“

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

## **Why you should care**

In PHP the assignment to $this is used to unset the object, or it is a typographical error. Unsetting an object is not really necessary for performance reasons. Removing all variables that point to the object to be unset will have the same result. It is also important to remember to do so because the result will be a fatal error. As such, in PHP5 mode, this kind of practice could provoke a failure.

## **Business Impacts**

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/innovation/)

### CAST recommendations

### References

https://www.tutorialspoint.com/sql/sql-transactions.htm

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
