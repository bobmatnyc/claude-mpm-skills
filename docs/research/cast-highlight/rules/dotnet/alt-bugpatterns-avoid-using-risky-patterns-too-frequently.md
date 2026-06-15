---
title: Avoid using risky patterns too frequently
url: https://doc.casthighlight.com/alt_bugpatterns-avoid-using-risky-patterns-too-frequently/
slug: alt_bugpatterns-avoid-using-risky-patterns-too-frequently
content_type: rule
languages: [dotnet, java, cpp]
category: Robustness
has_code_examples: false
---

[Software Resiliency](http://casthighlight.wpengine.com/software-resiliency/)[Programming Best Practices](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/programming-best-practices/)

# **Why you should care**

Some specific code syntaxes, even if they compile and don’t make a software crash directly, are not recommended mainly for two reasons:

- They’re often obscure and/or implicit and could definitely lead to misinterpretations by junior developers, which frequently means unexpected bugs when the code is modified

- When located around these blurry syntaxes (coding gurus will qualify them as “art”), real bugs are much harder to catch, especially because the syntax doesn’t bestially describe what it does and needs advanced interpretations

To illustrate the confusion these risky patterns could generate, take a look at [this real-life example below found on GitHub](https://github.com/BinomialLLC/crunch/blob/master/crnlib/crn_tree_clusterizer.h) (line #421 and #424):

> left\_child = new\_left\_child;  
>  left\_weight = left\_weight;  
> right\_child = new\_right\_child;  
>  right\_weight = right\_weight;

And most importantly, look at the issue and doubts this variable self-assignment has raised within the development team:

# **Business Impacts**

Using risky syntax can lead to increased bugs in an application, since it makes troubleshooting and expansion of existing code needlessly complicated. This, in turn, will increase the time and effort that developers have to spend maintaining and updating a given codebase.

[Cost](http://casthighlight.wpengine.com/category/product/indicators-methodology/innovation/)

![7633](https://doc.casthighlight.com/wp-content/uploads/2017/09/Example-RiskyPatterns-1.png)![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

# **CAST Recommendations**

When possible, software should use the most simple and explicit code syntax to perform actions. While some development gurus say they can do more with less code, it generally means spending more time for small bugs.

# **References**

https://stackoverflow.com/questions/11008030/a-for-loop-without-any

[Style Guide](https://github.com/Kristories/awesome-guidelines)

# **How we detect**

This code insight verifies that the source code doesn’t contain technology-specific patterns that tend to generate unexpected bugs. Below are listed some examples for the technologies Highlight supports. Based on specific thresholds CAST has defined over time, Highlight counts penalty points for the scanned file.

##### C/C++ and Objective-C

while(…);  
for(…);  
if(…);  
a = a;  
a == b;  
\* expr ; with expr containing no function call nor assignment operator.

##### VB/VB.Net

**:**<end of line>  
<begin of line> **:****::  
=** …….. **=** (no colon or coma between the peer of equals)

##### C#

while(…);  
for(…);  
foreach(…);  
if(…);  
a = a ;  
a == b ;

##### Java and JSP

while(…);  
for(…);  
if(…);  
a = a ;  
a == b ;

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
