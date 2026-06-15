---
title: Avoid using functions before their declaration
url: https://doc.casthighlight.com/alt_baddeclarationorder-avoid-using-functions-declaration/
slug: alt_baddeclarationorder-avoid-using-functions-declaration
content_type: rule
languages: [java, javascript]
category: Changeability
has_code_examples: false
---

## **Avoid using functions before their declaration**

[Software Agility](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-agility/)[Code Readability](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-agility/code-readability/)

This code insight counts the number of cases when functions are called prior to their definition in the source code. Based on the density of this bad practice and on specific thresholds CAST has defined, Highlight counts penalty points for the scanned file.

Pattern example (here, in Javascript):

var foo = myFunction(10);  
 // eventually some stuff…

function myFunction(param) {  
    // your function definition  
}

### **Why you should care**

Have you ever tried to watch a movie by starting in the middle of the story? It is hard to really understand who’s who since you may have missed some important details that were explained in the first scenes. Most (approx. 99.9%) developers read their source code by scrolling down, hence function definitions should be placed before (above) they’re used in the application, in order to know the different parameters of a function they’re about to modify.

References:  
<http://eslint.org/docs/rules/no-use-before-define>  
<http://javascript.crockford.com/code.html>

### **CAST recommendations**

For readability purpose, it is better to define a function before using it, as follows:

function myFunction(param) {  
    // your function definition  
 }

// eventually some stuff…

var foo = myFunction(10);

[How it works](http://casthighlight.wpengine.com/how-it-works/)[Features & Analytics](http://casthighlight.wpengine.com/outputs-analytics/)
