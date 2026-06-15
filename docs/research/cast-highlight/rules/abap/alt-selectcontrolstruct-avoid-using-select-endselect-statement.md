---
title: Avoid using SELECT … ENDSELECT statement
url: https://doc.casthighlight.com/alt_selectcontrolstruct-avoid-using-select-endselect-statement/
slug: alt_selectcontrolstruct-avoid-using-select-endselect-statement
content_type: rule
languages: [abap, sql]
has_code_examples: false
---

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/risk/)[Software Resiliency](http://casthighlight.wpengine.com/software-resiliency/)[Programming Best Practices](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# Avoid using SELECT … ENDSELECT statement

#

This code insight shows that The SELECT … ENDSELECT works as a loop fetching single record for every loop pause. Basically, it works like a client cursor which will generate too much traffic on the network and communications between the application server and the database server.

This report lists all ABAP Artifacts using SELECT … ENDSELECT statement on tables and views.  
It provides the following information:  
ABAP Artifacts full name, number of violations

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

## **Why you should care**

## **Business Impacts**

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/innovation/)

### CAST recommendations

### References

https://technet.microsoft.com/en-us/library/ms187009(v=sql.105).aspx

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
