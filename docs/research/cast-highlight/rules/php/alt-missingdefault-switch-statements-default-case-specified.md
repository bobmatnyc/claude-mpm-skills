---
title: Switch statements should have a default case specified
url: https://doc.casthighlight.com/alt_missingdefault-switch-statements-default-case-specified/
slug: alt_missingdefault-switch-statements-default-case-specified
content_type: rule
languages: [php]
category: Security
has_code_examples: false
---

## Switch statements should have a default case specified

[Software Resiliency](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/)[Programming Best Practices](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/programming-best-practices/)

This code insight verifies the ratio between the number of switch statements with missing default cases specified and the total number of switch statements found in the source code. Depending on this ratio and thresholds CAST has defined, Highlight counts penalty points for the scanned file.

Example in PHP:  
switch($foo) {  
    case 0:  
       // do something  
       break;  
    case 1:  
       // do something else  
       break;  
 }

### **Why you should care**

As MITRE perfectly explains, this flaw represents a common problem in software development, in which not all possible values for a variable are considered or handled by a given process. Because of this, further decisions are made based on poor information, and cascading failure results. This cascading failure may result in any number of security issues, and constitutes a significant failure in the system.

References:  
<https://cwe.mitre.org/data/definitions/478.html>

### **CAST recommendations**

CAST recommends that users follow MITRE’s proposed mitigation: In the case of switch style statements, the very simple act of creating a default case can mitigate this situation, if done correctly. Often however, the default case is used simply to represent an assumed option, as opposed to working as a check for invalid input. This is poor practice and in some cases is as bad as omitting a default case entirely.

Example in PHP:  
switch($foo) {  
    case 0:  
       // do something  
       break;  
    case 1:  
       // do something else  
       break;  
    default:  
       // do something if not case 0 nor case 1  
 }

[How it works](http://casthighlight.wpengine.com/how-it-works/)[Features & Analytics](http://casthighlight.wpengine.com/outputs-analytics/)
