---
title: TLD Headers can reduce Production Risks
url: https://doc.casthighlight.com/alt_taglibrarydescriptor-use-significant-tld-header/
slug: alt_taglibrarydescriptor-use-significant-tld-header
content_type: rule
has_code_examples: false
---

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/risk/)[Software Resiliency](http://casthighlight.wpengine.com/software-resiliency/)[Programming Best Practices](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# TLD Headers can reduce Production Risks

This code insight counts one violation each time a TLD header do not contains:

- the xml version,
- the xml encoding
- the DOCTYPE statement

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

## **Why you should care**

A tag library descriptor (TLD) file must have a header section including the definition of the XML version and the encoding format along with the appropriate DOCTYPE statement identifying the governing DTD.

For example, a JSP 1.2 TLD file must begin with:

<?xml version=”1.0″ encoding=”ISO-8859-1″ ?>  
<!DOCTYPE taglib  
PUBLIC “-//Sun Microsystems, Inc.//DTD JSP Tag Library 1.2//EN”  
“<http://bit.ly/10lWUaT>“>

## **Business Impacts**

*Having more tag libraries than necessary is risky for the code.  It is best to only have tag libraries that are used so that the code can be more productive.*

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/innovation/)

### CAST recommendations

### References

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
