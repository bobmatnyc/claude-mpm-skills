---
title: Code should be stripped out of suspicious comments
url: https://doc.casthighlight.com/alt_suspiciouscomments-code-stripped-suspicious-comments/
slug: alt_suspiciouscomments-code-stripped-suspicious-comments
content_type: rule
category: Changeability
has_code_examples: false
---

## **Code should be stripped out of suspicious comments (e.g. todo, tbd, tbc, etc.)**

[Software Agility](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-agility/)[Embedded Documentation](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-agility/embedded-documentation/)

This code insight counts the number of occurences where suspicious keywords are found in comments. Based on the number of cases and associated with specific thresholds CAST has defined, Highlight counts penalty points to the scanned file.

Keywords that are taken into account by this code insight:  
 – two or more successive ! and/or ? (e.g. what is this code doing???!!!)  
 – todo, fixme, tdc (to be confirmed), tbd (to be defined), attention

### **Why you should care**

Sometimes, comments that are left by developers translate their doubts, questions or emotions about the code they’re working on. Having some suspicious comments, especially in production code, could indicate a component is not totally finalized, not really mature yet or -more worrying – that may contain a bug. There’s nothing worse than a bug that pops up in production and when the team investigates it they find a comment saying “todo”.

References:  
<https://cwe.mitre.org/data/definitions/546.html>

### **CAST recommendations**

As recommended by MITRE (CWE-546), a potential mitigation would be to remove comments that suggest the presence of bugs, incomplete functionality, or weaknesses, before deploying the application.

[How it works](http://casthighlight.wpengine.com/how-it-works/)[Features & Analytics](http://casthighlight.wpengine.com/outputs-analytics/)
