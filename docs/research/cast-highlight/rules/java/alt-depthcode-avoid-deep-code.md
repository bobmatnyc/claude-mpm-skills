---
title: Deep functions are a Production Risk in JavaScript
url: https://doc.casthighlight.com/alt_depthcode-avoid-deep-code/
slug: alt_depthcode-avoid-deep-code
content_type: rule
languages: [java, javascript]
has_code_examples: false
---

[Software Resiliency](http://casthighlight.wpengine.com/software-resiliency/)[Programming Best Practices](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# **Deep functions are a Production Risk in JavaScript**

This code insight counts one violation each time an artifact (global function or root code) has a too high depth code. Depth is evaluated throught imbrication of following structures :

if, do, for, while, case,

The depth threshold (max valid depth) is tuned to 5.

Example :  
function TooDeepFunction () {

while (toto) { // depth 1  
print ‘plouf’;  
for (;;) { // depth 2  
if (BOOL == 1) { // depth 3  
print ‘CAST’;  
}  
else if (name = ‘JOHN DOE’) { // else :depth 3, if: depth 4  
echo ‘CAST’;  
switch (INDEX) { // depth 5  
case 1 :  
if (BOOL >= 1) { // depth 6 ==> VIOLATION!  
print ‘example’;  
}  
default :  
return;  
}  
}  
}  
}  
}

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

## **Why you should care**

*Having deep functions in Javascript is considered bad practice*

## **Business Impacts**

*Combining multiple lines of code on one line is risky because it makes the code unreadable and less productive in the long run.*

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/innovation/)

### CAST recommendations

### References

https://softwareengineering.stackexchange.com/questions/104066/single-line-statements-good-practices

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
