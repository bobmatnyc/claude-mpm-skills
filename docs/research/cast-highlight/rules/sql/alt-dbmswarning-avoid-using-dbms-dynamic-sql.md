---
title: Native Dynamic SQL is easier to use than DBMS SQL.
url: https://doc.casthighlight.com/alt_dbmswarning-avoid-using-dbms-dynamic-sql/
slug: alt_dbmswarning-avoid-using-dbms-dynamic-sql
content_type: rule
languages: [sql]
has_code_examples: false
---

## **Native Dynamic SQL is easier to use than DBMS SQL**.

[Software Resiliency](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/)[Programming Best Practices](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/programming-best-practices/)

This code insight shows that PL/SQL provides two ways to write dynamic SQL:

- Native dynamic SQL, a PL/SQL language (that is, native) feature for building and executing dynamic SQL statements  
  DBMS\_SQL package, an API for building, executing, and describing dynamic SQL statements
- Native dynamic SQL code is easier to read and write than equivalent code that uses the DBMS\_SQL package, and runs noticeably faster (especially when it can be optimized by the compiler).

However, to write native dynamic SQL code, you must know at compile time the number and data types of the input and output variables of the dynamic SQL statement. If you do not know this information at compile time, you must use the DBMS\_SQL package.

### **Why you should care**

DBMS – Database Management System is a computer software application that interacts with other applications, and the database to capture and analyze data.  SQL is a base that is used with most Database systems like Oracle, Microsoft SQL server and so forth.

Dynamic SQL is a technique to build SQL statements dynamically at runtime.  Running Native Dynamic SQL over the DBMS SQL is much easier as Native Dynamic SQL is integrated with SQL and can be used similarly to static SQL.  DBMS dynamic SQL is not as easy as many procedures have to be used in a strict sequence and require a lot of code which can be time consuming and prone to errors.

References:  
<https://docs.oracle.com/cd/A87860_01/doc/appdev.817/a76939/adg09dyn.htm>

[How it works](http://casthighlight.wpengine.com/how-it-works/)[Features & Analytics](http://casthighlight.wpengine.com/outputs-analytics/)
