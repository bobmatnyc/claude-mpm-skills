---
title: Truncate tables compromise backups
url: https://doc.casthighlight.com/alt_truncate-truncate-tables-compromise-backups/
slug: alt_truncate-truncate-tables-compromise-backups
content_type: rule
category: Efficiency
has_code_examples: false
---

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/risk/)[Software Resiliency](http://casthighlight.wpengine.com/software-resiliency/)[Code Reliability](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# **Truncate tables compromise backups**

This code insight detects the total number of database objects containing code: SP, Functions, and Triggers.

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

## **Why you should care**

*Although “truncate table” statement can be desirable under some circumstances from a performance point of view it is problematic because deletion are not logged. Thus the log backups become useless.*

## **Business Impacts**

*Truncate tables increase risks from a productivity standpoint because it eliminates backups in code which can greatly setback projects.*

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/innovation/)

### CAST recommendations

### References

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
