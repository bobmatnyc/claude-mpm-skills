---
title: Exceptions shouldn’t be caught with system exception classes
url: https://doc.casthighlight.com/alt_riskycatches-exceptions-shouldnt-catched-system-exception-classes/
slug: alt_riskycatches-exceptions-shouldnt-catched-system-exception-classes
content_type: rule
category: Robustness
has_code_examples: false
---

## **Exceptions shouldn’t be caught with system exception classes**

[Software Resiliency](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/)[Programming Best Practices](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/programming-best-practices/)

This code insight detects and counts the usage of generic exception catches like catch(…), Exception, Throwable, SystemException, RuntimeException, Error. Based on frequency thresholds CAST has determined by analyzing source code over the last 25 years, Highlight determines whether the usage ratio of these generic catches is abornmally high or not, and counts penalty points for the scanned source file accordingly.

### **Why you should care**

When an error occurs in your software, it is always better to know where it came from –  in order to inform the user and log the error with the appropriate message for further investigation by the development team. If such an exception is handled in a generic way, one won’t be able to know whether it came from the system supporting the application or from the application itself. If this code insight shows up in your application, you may want to ensure that exceptions are not systematically handled by the system instead of being managed by your application. Managing errors within your application can dramatically reduce the time to fix a bug, because of the explicit and intelligible error message.

References:  
<https://stackoverflow.com/questions/21938/is-it-really-that-bad-to-catch-a-general-exception>

### **CAST recommendations**

Whenever possible (and when your development think it is relevant), exceptions that come from your software should be handled by a dedicated custom class of your application.

[How it works](http://casthighlight.wpengine.com/how-it-works/)[Features & Analytics](http://casthighlight.wpengine.com/outputs-analytics/)
