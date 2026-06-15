---
title: Avoid using dynamic queries
url: https://doc.casthighlight.com/alt_dynamicqueries-avoid-using-dynamic-queries/
slug: alt_dynamicqueries-avoid-using-dynamic-queries
content_type: rule
category: Security
has_code_examples: false
---

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/risk/)[Software Resiliency](http://casthighlight.wpengine.com/software-resiliency/)[Programming Best Practices](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# Avoid using dynamic queries

#

This code insight shows that dynamic queries are difficult to test and can decrease the code understanding. Moreover, include dynamic coding in UI components can generate security issues if the content of the dynamic clauses is not filtered properly.

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

## **Why you should care**

Avoid using dynamic coding as much as possible and check if dynamic content is filtered properly.

## **Business Impacts**

*Having the RETURN statement in the middle of the command makes rest of the code unproductive.  Lack of a RETURN statement would cause the code to function improperly and result in a loss of time.*

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/innovation/)

### CAST recommendations

### References

http://help.sap.com/saphelp\_nw2004s/helpdata/en/8f/35de1718944eb8a1462cf6362cc8b8/frameset.htm

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
