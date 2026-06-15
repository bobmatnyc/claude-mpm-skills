---
title: Too many “for in” loops is risky
url: https://doc.casthighlight.com/alt_forinloop-avoid-for-in-loop/
slug: alt_forinloop-avoid-for-in-loop
content_type: rule
has_code_examples: true
---

[Software Resiliency](http://casthighlight.wpengine.com/software-resiliency/)[Code Reliability](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-agility/code-reliability/)

# **Why you should care**

Since each iteration through the loop results in a property lookup either on the instance or on a prototype, the for-in loop has considerably more overhead per iteration and is therefore slower than the other loops. 

For the same number of loop iterations, a forin loop can end up as much as seven times slower than the other loop types. For this reason, it’s recommended to avoid the for-in loop unless your intent is to iterate over an unknown number of object properties.

Moreover when using with arrays, This is however very error prone because it does not loop from `0` to `length - 1` but over all the present keys in the object and its prototype chain. Here are a few cases where it fails:

function printArray(arr) {  
for (var key in arr) {  
print(arr[key]);  
}  
}  
printArray([0,1,2,3]); // This works.

var a = new Array(10);  
printArray(a); // This is wrong.

a = doc.getElementsByTagName(‘\*’); printArray(a); // This is wrong.

a = [0,1,2,3]; a.buhu = ‘wine’; printArray(a); // This is wrong again.

a = new Array; a[3] = 3;  
printArray(a); // This is wrong again

# **Business Impacts**

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/risk/)

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

# **CAST Recommendations**

# **References**

[Style Guide](https://github.com/Kristories/awesome-guidelines)

# **How we detect**

This code insight counts one violation each time a “**for (… in … )** ” loop is encountered

**bad:**

function printArray(arr) {  
**for** (var key **in** arr) {  
print(arr[key]);  
}  
}

**good :**

function printArray(arr) {  
var l = arr.length;  
**for** (var i = 0; i < l; i++) {  
print(arr[i]);  
}  
}

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
