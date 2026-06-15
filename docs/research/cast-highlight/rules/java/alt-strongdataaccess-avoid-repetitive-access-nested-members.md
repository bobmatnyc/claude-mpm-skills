---
title: Avoid repetitive access to nested members
url: https://doc.casthighlight.com/alt_strongdataaccess-avoid-repetitive-access-nested-members/
slug: alt_strongdataaccess-avoid-repetitive-access-nested-members
content_type: rule
languages: [java, javascript]
category: Efficiency
has_code_examples: false
---

[Software Resiliency](http://casthighlight.wpengine.com/software-resiliency/)[Programming Best Practices](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/programming-best-practices/)

# **Why you should care**

As explained by W3C: “Accessing the DOM in browsers is an expensive thing to do. The DOM is a very complex API and rendering in browsers can take up a lot of time. You can see this when running complex web applications when your computer is already maxed out with other work — changes take longer or get shown half way through and so on”.

Remediating this code pattern can take back up to 50% of the time consumed by a function.

Since object members may contain other members, it’s not uncommon to see patterns such as window.location.href in JavaScript code. These nested members cause the JavaScript engine to go through the object member resolution process each time a dot is encountered, while storing properties in local variables will dramatically increase execution speed in some cases.

# **Business Impacts**

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/risk/)

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

# **CAST Recommendations**

Generally speaking, if you’re going to read an object property more than one time in a function, it’s best to store that property value in a local variable. The local variable can then be used in place of the property to avoid the performance overhead of another property lookup. This is especially important when dealing with nested object members that have a more dramatic effect on execution speed.

**Bad pattern:**  
function toggle(element){  
if (YAHOO.util.Dom.hasClass(  
element, “selected”)){  
YAHOO.util.Dom.removeClass(  
element, “selected”);  
return false;  
} else {  
YAHOO.util.Dom.addClass(  
element, “selected”);  
return true;  
}  
}

**Good pattern:**  
function toggle(element) {  
var Dom = YAHOO.util.Dom;  
if (Dom.hasClass(element, “selected”)){  
Dom.removeClass(element, “selected”);  
return false;  
} else {  
Dom.addClass(element, “selected”);  
return true;  
}  
}

# **References**

<https://www.w3.org/wiki/JavaScript_best_practices#Keep_DOM_access_to_a_minimum>

[Style Guide](https://github.com/Kristories/awesome-guidelines)

# **How we detect**

This code insight counts the number of cases when an object member (e.g. Acme.util.Dom.hasClass) goes through more than two nesting levels (i.e. it has at least three dots to access the object member). Depending on the number of cases identified in the code, Highlight counts penalty points to the scanned file.

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
