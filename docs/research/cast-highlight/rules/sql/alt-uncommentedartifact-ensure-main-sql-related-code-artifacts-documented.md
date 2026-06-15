---
title: Ensure that your main SQL-related code artifacts are documented
url: https://doc.casthighlight.com/alt_uncommentedartifact-ensure-main-sql-related-code-artifacts-documented/
slug: alt_uncommentedartifact-ensure-main-sql-related-code-artifacts-documented
content_type: rule
languages: [sql]
category: Changeability
has_code_examples: false
---

## **Ensure that your main SQL-related code artifacts are documented**

[Software Agility](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-agility/)[Embedded Documentation](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-agility/embedded-documentation/)

This code insight counts the number of SQL-related code artifacts (functions, procedures, triggers and view declarations) that are not preceded with a block of comments, and compares that number to the total number of artifacts. Depending on this ratio and based on thresholds CAST has defined, Highlight counts penalty points to the scanned file.

### **Why you should care**

On average, a developer can write approximately 10 lines of code per day. The rest of the time he/she is trying to understand the existing code (and probably attends boring meeting too). That’s even more true when database functions, procedures and other SQL-related code artifacts are shared across different components. Adding a comment that explains how a piece of code is supposed to work is a great help for development teams. A well-documented application generally means lower maintenance cost and tends to be less error-prone when modifications need to be made in the software.

### **CAST recommendations**

If this code insight regularly shows up in your software, you may want to tell your development team to ensure the main SQL-related code artifacts of your application are regularly enriched with a useful block of comment to quickly understand the logic behind the code.

[How it works](http://casthighlight.wpengine.com/how-it-works/)[Features & Analytics](http://casthighlight.wpengine.com/outputs-analytics/)
