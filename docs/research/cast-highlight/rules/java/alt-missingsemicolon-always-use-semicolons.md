---
title: Missing Semicolons in JavaScript can be very unproductive
url: https://doc.casthighlight.com/alt_missingsemicolon-always-use-semicolons/
slug: alt_missingsemicolon-always-use-semicolons
content_type: rule
languages: [java, javascript]
has_code_examples: false
---

[Software Agility](http://casthighlight.wpengine.com/software-agility/)[Code Reliability](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# **Why you should care**

Relying on implicit insertion can cause subtle, hard to debug problems. Don’t do it.  There are a couple places where missing semicolons are particularly dangerous:

*MyClass.prototype.myMethod = function() {*  
*return 42;*  
*}  // No semicolon here.*

*(function() {*  
*// Some initialization code*  
*// wrapped in a function to*  
*// create a scope for locals.*  
*})();*

**==> The function returning 42 is called with the second function as a parameter, then the number 42 is “called” resulting in an error.**

*var x = {*  
*‘i’: 1,*  
*‘j’: 2*  
*}  // No semicolon here.*

*// Trying to do one thing on Internet Explorer and another on Firefox.*

*[ffVersion, ieVersion][isIE]();*

**==> You will most likely get a ‘no such property in undefined’ error at runtime as it tries to call x[ffVersion, ieVersion][isIE]().**

*var THINGS\_TO\_EAT = [apples, oysters, sprayOnCheese]  // No semicolon here.*

// conditional execution a la bash  
-1 == resultOfOperation() || die();

**==> die is always called since the array minus 1 is NaN which is never equal to anything (not even if resultOfOperation() returns NaN) and THINGS\_TO\_EAT gets assigned the result of die().**

*a = b*  
*/hi/g.exec(c).map(d);*

==> **the example is interpreted in the same way as:**  
 ***a = b / hi / g.exec(c).map(d);***

**Why?**

JavaScript requires statements to end with a semicolon, except when it thinks it can safely infer their existence. In each of these examples, a function declaration or object or array literal is used inside a statement. The closing brackets are not enough to signal the end of the statement. **JavaScript never ends a statement if the next token is an infix or bracket operator.**

This has really surprised people, so make sure your assignments end with semicolons.  Semicolons should be included at the end of function expressions, but not at the end of function declarations. The distinction is best illustrated with an example:

*var foo = function() {*

*return true;*

*};  // semicolon here.*

*function foo() {*

*return true;*

*}  // no semicolon here.*

# **Business Impacts**

Missing Semicolons in JavaScript would be very risky for the code and cause very minimal productivity because of potential bugs that lie in the code.

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/risk/)

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

# **CAST Recommendations**

# **References**

<https://en.wikipedia.org/wiki/Comment_(computer_programming)>

<https://www.cs.utah.edu/~germain/PPS/Topics/commenting.html>

[Style Guide](https://github.com/Kristories/awesome-guidelines)

# **How we detect**

This code insight counts a violation each time a semicolon is missing elsewhere.

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
