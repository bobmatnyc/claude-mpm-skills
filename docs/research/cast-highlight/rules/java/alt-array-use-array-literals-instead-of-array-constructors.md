---
title: Array literals are less risky than Array constructors in JavaScript
url: https://doc.casthighlight.com/alt_array-use-array-literals-instead-of-array-constructors/
slug: alt_array-use-array-literals-instead-of-array-constructors
content_type: rule
languages: [java, javascript, sql]
has_code_examples: false
---

[Software Resiliency](http://casthighlight.wpengine.com/software-resiliency/)[Code Reliability](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# **Array literals are less risky than Array constructors in JavaScript**

This code insight counts one violation each time “**new array(…)**” is encountered.

**bad** *:*

Length is **3** :  
*var a1 = new Array(x1, 1.2, “string”);*

Length is **2** :  
*var a2 = new Array(x1, x2);*

*Length is **x1** or **error** if not an integer :  
*var a3 = new Array(x1);**

**Length is **0**.  
*var a4 = new Array();***

**good*:***

Length is **3** : *var a = [1.5, x2, “string”];*

Length is **2** :  
*var a2 = [x1, x2];*

Length is **1** :  
*var a3 = [x1]; *var a3 = [“string”];**

Length is **0** :  
*var a4 = [];*

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

## **Why you should care**

The array literal syntax is simple, straightforward, and elegant. After all, an array is just a zero-indexed list of values. There’s no need to complicate things (and write more code) by including a constructor and using the new operator.

One more reason to stay away from new Array() is to avoid a possible trap that this constructor has in store for you.

When you pass a single number to the Array() constructor, it doesn’t become the value of the first array element. It sets the length of the array instead. This means that new

Array(3) creates an array with length of 3, but no actual elements.

Although this behavior might be a little unexpected, it gets worse when you pass a floating point number to new Array() as opposed to an integer. This results in an error because the floating point is not a valid value for the array’s length

Length is **3** :  
*var a1 = new Array(x1, x2, x3);*

Length is **2** :  
*var a2 = new Array(x1, x2);*

*Length is **x1** :  
*var a3 = new Array(x1);**

**Length is **0**.  
*var a4 = new Array();***

## **Business Impacts**

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/innovation/)

### CAST recommendations

### References

https://www.tutorialspoint.com/sql/sql-transactions.htm

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
