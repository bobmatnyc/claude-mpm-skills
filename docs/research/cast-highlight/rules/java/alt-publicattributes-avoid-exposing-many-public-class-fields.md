---
title: Avoid exposing too many attributes
url: https://doc.casthighlight.com/alt_publicattributes-avoid-exposing-many-public-class-fields/
slug: alt_publicattributes-avoid-exposing-many-public-class-fields
content_type: rule
languages: [java]
category: Security
has_code_examples: false
---

## Avoid exposing too many public class fields

[Software Resiliency](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/)[Programming Best Practices](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/programming-best-practices/)

This code insight counts the number of cases when an attribute is directly exposed outside a class (more explicitly when the keyword “public” is associated with a data field of the class). Based on the density and on specific thresholds CAST has defined, Highlight counts penalty points for the scanned file.

### **Why you should care**

This code insight is all about how your software manages data access across code artifacts. While the principle says that data should be private as often as possible and should not be accessible by other objects which don’t own or can’t manipulate it, it looks like this is not systematically the case in the code you scanned. It might be a software design as well as a security concern.

From a software engineering standpoint, having too many public fields when they should be private or protected tend to break data encapsulation, which is a primary concept of object-oriented programming. Encapsulation binds together the data and functions that manipulate the data, and that keeps both safe from outside interference and misuse.

References:  
 <http://blog.everymansoftware.com/2012/03/getset-methods-vs-public-properties.html>  
 <https://softwareengineering.stackexchange.com/questions/176876/why-shouldnt-i-be-using-public-variables-in-my-java-class>  
 <https://en.wikipedia.org/wiki/Object-oriented_programming#Encapsulation>

### **CAST recommendations**

If your application implements OO programming, the code should apply Object-Oriented principles such as Inheritance, Abstraction, Polymorphism, etc. Encapsulation is one of them. CAST recommends keeping data members private as much as possible and control access outside of a class through Getter() and Setter() methods.

[How it works](http://casthighlight.wpengine.com/how-it-works/)[Features & Analytics](http://casthighlight.wpengine.com/outputs-analytics/)
