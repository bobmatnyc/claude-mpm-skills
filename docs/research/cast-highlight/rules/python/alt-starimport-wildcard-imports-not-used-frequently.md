---
title: Wildcard imports should not be used too frequently
url: https://doc.casthighlight.com/alt_starimport-wildcard-imports-not-used-frequently/
slug: alt_starimport-wildcard-imports-not-used-frequently
content_type: rule
languages: [python, java]
category: Transferability
has_code_examples: false
---

## **Wildcard imports should not be used too frequently**

[Software Agility](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-agility/)[Code Readability](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-agility/code-readability/)

This code insight detects and counts the number of import statements with a wildcard (e.g. “import java.awt.\*”) and compares with the number of total import occurences found in the code.

### **Why you should care**

Like in database queries, importing software libraries or packages using wildcards could be an indication of a lazy attitude – those who don’t want to spend any of their time to import a specific component (e.g. import java.awt.Event) to be used their application.  Too many wildcard imports may lead to possible conflicts when compiling your programs. in addition, because using wildwards implicitly include all other components that are not required by your application, source code tends to be less readable (what is the exact list of components the application is working with?).

References:  
<https://www.quantifiedcode.com/knowledge-base/maintainability/Avoid%20using%20wildcard%20%28%2A%29%20imports/3Q3eTYIU>  
<https://pythonconquerstheuniverse.wordpress.com/2011/03/28/why-import-star-is-a-bad-idea/>

### **CAST recommendations**

Ensure imports in your software are as specific as possible. Ideally, you should import only the components that your application needs.

[How it works](http://casthighlight.wpengine.com/how-it-works/)[Features & Analytics](http://casthighlight.wpengine.com/outputs-analytics/)
