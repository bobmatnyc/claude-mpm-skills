---
title: The code contains too many lines containing several instructions
url: https://doc.casthighlight.com/alt_multinst-code-contains-many-lines-containing-several-instructions/
slug: alt_multinst-code-contains-many-lines-containing-several-instructions
content_type: rule
languages: [java]
category: Changeability
has_code_examples: false
---

## **The code contains too many lines containing several instructions**

[Software Agility](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-agility/)[Code Readability](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-agility/code-readability/)

This code insights verifies that the source code doesn’t contain multiple instructions in a single line. Depending on the density of cases of multiple instructions per line of code, and based on specific threshods, Highlight counts penalty points for the scanned file.

The following patterns are used to detect them:  
– more than one “;”  
– “{” … statement … “;”  
– statement … “; }”  
– “;” and one of the following keywords: while, for, foreach, if else, switch, try, catch, finally, do…  
– more than one keyword listed above, except for “else if”

### **Why you should care**

Having multiple instructions in one line of code remarkably decreases readability of your software. In addition to making source code harder to understand, developers may miss some important instructions – because they’re in the middle of others – that could impact the software execution (e.g. if(today == “Monday”) { echo “Have a good week”; formatUserDrive(); echo “and a great week-end too!”; }

References:  
<https://softwareengineering.stackexchange.com/questions/104066/single-line-statements-good-practices>  
<https://www.quora.com/When-is-it-appropriate-to-have-multiple-Java-statements-on-one-line>

### **CAST recommendations**

Although in some cases there may be a good reason to have more than one instruction per line (e.g. very simple code like “if(found) { break; }”), it is generally agreed by the developer community that each instruction should have its own code line.

[How it works](http://casthighlight.wpengine.com/how-it-works/)[Features & Analytics](http://casthighlight.wpengine.com/outputs-analytics/)
