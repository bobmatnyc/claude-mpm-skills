---
title: Variable declaration creates an instance in the class
url: https://doc.casthighlight.com/alt_vardecl-always-declare-variables/
slug: alt_vardecl-always-declare-variables
content_type: rule
languages: [java]
has_code_examples: true
---

[Software Resiliency](http://casthighlight.wpengine.com/software-resiliency/)[Programming Best Practices](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/programming-best-practices/)

# **Why you should care**

It is important to remember that KSH uses variables and parameters to store values.  It also supports data types and arrays.  The four data types KSH supports include *string, integer, float*and *array*.  If a data type is not defined then KSH assumes the variable is a string.

Usually KSH variables can be declared as a local variable because these variables will be considered as global in scope otherwise.  Having too many global variables can cause unspecified functions which leads to spaghetti code that ends up being hard to manage and collaborate with.  This in turn leads to a buggy and unproductive code.

# **Business Impacts**

Declaring variables is advised because it is considered to be good programming practice but it also allows the code to be more resilient.  Preventing spaghetti code is absolutely key to progress, otherwise it can lead to confusion and frustration in the development teams.

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/innovation/)[Spaghetti Code](https://en.wikipedia.org/wiki/Spaghetti_code)

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

# **CAST Recommendations**

CAST recommends having declared variables as local variables because it allows for code to have specified functionalities and to prevent spaghetti code from occurring.

Here are a few examples below of how to declare variables –

variable= – declares variable and set it to null

```
$ typeset —i NUM=1 
   $ print $NUM 
   1
```

NUM is set to an integer=type variable and assigned a value.

Whenever spaghetti code arises, it is important for the development team to take a few steps back, re-evaluate the project’s functions and goals.  Usually the company has a style guide but it may not be followed because it does not have the necessary guidelines that can used for current projects.  In such cases, the guides should be updated to meet the needs of developers and newer projects.

# **References**

https://docs.oracle.com/javase/tutorial/java/javaOO/variables.html

www.informit.com/articles/article.aspx?p=99035

https://www.acrolinx.com/blog/companys-style-guide-measure/

[Style Guide](https://github.com/Kristories/awesome-guidelines)

# **How we detect**

This code insight showcases a non-existing variable is implicitly declared when assigned.  It is considered good practice to declare the variable before proceeding any further.

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
