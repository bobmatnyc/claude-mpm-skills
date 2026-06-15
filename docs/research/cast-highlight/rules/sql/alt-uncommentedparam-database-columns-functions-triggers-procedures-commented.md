---
title: "Database columns, functions, triggers and procedures should be commented"
url: https://doc.casthighlight.com/alt_uncommentedparam-database-columns-functions-triggers-procedures-commented/
slug: alt_uncommentedparam-database-columns-functions-triggers-procedures-commented
content_type: rule
languages: [sql]
category: Changeability
has_code_examples: false
---

## **Database columns, functions, triggers and procedures should be commented**

[Software Agility](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-agility/)[Embedded Documentation](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-agility/embedded-documentation/)

This code insight counts the number of function parameters, triggers, procedures and database columns (on CREATE TABLE) that are not commented. Based on specific thresholds CAST has defined, Highlight counts penalty points to the scanned file.

### **Why you should care**

Making sure your code artifacts are well documented is key to allowing development teams to maintain applications faster and more confidently. This is particularly true for this code insight that concerns database-related artifacts such as stored procedures, functions, triggers and more generally source code that can impact data.

References:  
<https://sqlwithmanoj.com/2012/02/26/best-practices-while-creating-stored-procedures/>  
<https://www.mssqltips.com/sqlservertutorial/167/using-comments-in-a-sql-server-stored-procedure/>

### **CAST recommendations**

Code artifacts should be documented as often as you can to ensure that a developer who doesn’t know the application can quickly understand what the code is doing, in order to modify it (bug fix or functional evolutions) while decreasing the risk of introducing new bugs.

[How it works](http://casthighlight.wpengine.com/how-it-works/)[Features & Analytics](http://casthighlight.wpengine.com/outputs-analytics/)
