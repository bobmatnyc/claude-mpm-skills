---
title: "Too many controversial, unsafe or deprecated keywords in procedure divisions"
url: https://doc.casthighlight.com/alt_prohibitedkeyword-many-controversial-unsafe-deprecated-keywords-procedure-divisions/
slug: alt_prohibitedkeyword-many-controversial-unsafe-deprecated-keywords-procedure-divisions
content_type: rule
languages: [cobol]
category: Changeability
has_code_examples: false
---

## **Too many controversial, unsafe or deprecated keywords in procedure divisions**

[Software Resiliency](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/)[Code Reliability](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

This code insights looks in COBOL procedure divisions for a list of possible deprecated or controversial keywords and verifies if their usage frequency is abnormaly high.

Possible deprecated or controversial keywords Highlight looks at: SELECT, ACCEPT (if not followed by FROM DAY, FROMTIME or FROM DATE), CORRESPONDING or CORR, NOTE, ENTRY, NEXT SENTENCE, DISPLAY … UPON CONSOLE, INITIALIZE, MERGE.

### **Why you should care**

Over decades, COBOL systems have been proved to be robust and resilient. However, some instructions or keywords can still have negative and unexpected impacts on your applications, or are just known as deprecated since … 1974! Below are a few examples and possible consequences it may have when used too frequently;

Avoid the keyword input instruction ACCEPT because it can lead to a treatment interruption.

Avoid using CORRESPONDING clause because this requires some homonymous variable declarations that are more ambiguous to use for other instructions. While it was usefull when punching physical cards many decades ago, it could save a lot of time/typos.

Avoid using NOTE  because it introduces a comment for the whole paragraph if it is the first instruction, or until the next dot. The instruction is deprecated since COBOL 74.

Avoid using ENTRY because it introduces an alternative entry point in the program.

Avoid using NEXT SENTENCE statements because it transfers control to the next COBOL sentence – that is, following the next dot. It does not transfer control to the logically next COBOL verb as occurs with the CONTINUE verb.

### **CAST recommendations**

Static code analysis tools can help your development teams identify this code insight, while peer code review is useful to educate junior teams on all the subtleties of an older language.

[How it works](http://casthighlight.wpengine.com/how-it-works/)[Features & Analytics](http://casthighlight.wpengine.com/outputs-analytics/)
