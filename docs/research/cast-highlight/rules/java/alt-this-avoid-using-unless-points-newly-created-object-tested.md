---
title: Avoid using “this” unless it points to a newly created object (and tested)
url: https://doc.casthighlight.com/alt_this-avoid-using-unless-points-newly-created-object-tested/
slug: alt_this-avoid-using-unless-points-newly-created-object-tested
content_type: rule
languages: [java, javascript]
category: Transferability
has_code_examples: true
---

[Software Resiliency](http://casthighlight.wpengine.com/software-resiliency/)[Code Reliability](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# **Why you should care**

In some contexts, using the keyword “this” could impact software reliability and lead to unexpected behaviors. More specifically, in a constructor, this is a reference on a new object just created by the new keyword when invoking a constructor. But, if the constructor is not invoked with new (that is just like a simple function), no error will be raised. This will simply reference the global object (window in a browser) and all members accessed with “this.xxxx” will be treated as global variables – that is certainly not the expected behavior.

# **Business Impacts**

Using the “this” variable leads to ambiguity, complexity and confusion within the code. It can cause unexpected application behavior and require more developer time/effort to understand and maintain. Especially when multiple team members need to be able to understand what “this” refers to within a given context.

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/)[Time / Effort](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/)

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

### **CAST recommendations**

Because “this” is often too ambiguous, which makes source code harder to understand, you’d need to check how the method is invoked to understand what value this holds.

Bad pattern example:

```
function Waffle() {
    this.tastes = "yummy";                   // what’s the value of “this” ??
    this.getTastes = function() {          // what’s the value of “this” ??
         return this.tastes;                       // should rather use a closure on "this"
    }
 }
```

Good pattern example:

```
function Waffle() {
     // check that the constructor Waffle
     //has been invoked with new.
     if (!(this instanceof Waffle)) {
         return new Waffle();         /* Waffle has not been invoked with new, so do it and ensure the value of this… */
     }
     this.tastes = "yummy";          /* According to previous test, we know that “this” references the right object. */
     var _this = this;
     this.getTastes= function() { 
         return _this.tastes;            // OK, no ambiguity with the closure !
     }
 }
```

**References**

<http://blog.millermedeiros.com/avoiding-the-this-keyword-on-jquery/>  
Javascript Patterns, by Stoyan Stefanov (O’Reilly, page 45)  
<https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/this>

<http://javascriptissexy.com/understand-javascripts-this-with-clarity-and-master-it/>

<https://stackoverflow.com/questions/48780927/javascript-when-and-when-not-to-use-this>

<https://luizfar.wordpress.com/2012/04/28/dont-use-this-in-javascript/>

[Style Guide](https://github.com/Kristories/awesome-guidelines)

# **How we detect**

This code insight identifies and counts the number of cases where the keyword “this” may be used outside one of the authorized usage patterns, in functions body:

```
var xxx = this
```

Pattern accepted because it reveals that the coder will save the value of “this” to use it in a closure for inner functions. This is a good practice.

```
$(this) or jQuery(this)
```

Pattern accepted because it is a common and practiced way to write callbacks working on DOM elements.

In presence of “this instanceof”  
 Pattern accepted because it reveals that the coder ensures that “this” has the right value. In this case, all usage of “this” are allowed in the function.

Depending on the density of “this” incorrect usage, and based on thresholds CAST has defined by analyzing thousands of applications and billions lines of code, Highlight counts penalty points within the scanned source files.

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See Features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
