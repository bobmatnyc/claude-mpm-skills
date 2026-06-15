---
title: Constructors with a return value can be unproductive in PHP
url: https://doc.casthighlight.com/alt_constructorreturn-avoid-having-constructors-with-a-return-value/
slug: alt_constructorreturn-avoid-having-constructors-with-a-return-value
content_type: rule
languages: [php, sql]
category: Robustness
has_code_examples: false
---

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/risk/)[Software Resiliency](http://casthighlight.wpengine.com/software-resiliency/)[Code Reliability](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# **Constructors with a return value can be unproductive in PHP**

This code insight counts a violation each time the script has a constructor with a return value

” <?php  
class foo {

function foo(){  
$error = ”; // is set when something goes wrong  
// things that can go wrong  
return $error;  
}  
}

$foo = new foo();

?>”

Remedy –

“Review the source code and if the issue is related to the management of the errors you can always adopt the approach below:  
If something goes wrong in the constructor you can either:  
– Throw an exception (PHP5 only)  
– Put this functionality in a separate function and call it. This function can then either return the object or an error.”

” <?php  
class foo {

function foo(){  
// things that can not go wrong  
}

function createFoo(){  
// is set to something else  
// when something goes wrong  
$error = new foo();

// things that can go wrong

return $error;  
}  
}

$foo = foo::createFoo();

?>”

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

## **Why you should care**

In PHP a constructor is the function that is called when an object is created and can be used to initialize object-variables. Using a return-value in a constructor is probably used to generate an error when something goes wrong during initialization. The return value from an object will be ignored and the result will always be the object itself. In this situation, the returned value of the constructor is a corrupt object which will be re-used in the source code and which could produce unexpected results.

## **Business Impacts**

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/innovation/)

### CAST recommendations

### References

https://www.tutorialspoint.com/sql/sql-transactions.htm

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
