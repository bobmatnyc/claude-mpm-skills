---
title: Avoid classes overriding only equals() or only hashCode()
url: https://doc.casthighlight.com/alt_missinghashcode-avoid-classes-overriding-equals-hashcode/
slug: alt_missinghashcode-avoid-classes-overriding-equals-hashcode
content_type: rule
languages: [java, sql]
has_code_examples: false
---

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/risk/)[Software Resiliency](http://casthighlight.wpengine.com/software-resiliency/)[Programming Best Practices](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# **Avoid classes overriding only equals() or only hashCode()**

This code insight reports all classes that override only boolean equals(Object) or only int hashCode() .

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

## **Why you should care**

*Often classes are used in HashMap to provide an efficient storage and retrieval. The Java platform architects anticipated the importance of hash-based collection classes — such as Hashtable, HashMap, and HashSet — in typical Java applications, and comparing against many objects with equals() can be computationally expensive.*   
 *If your java class is used or can be used in a hash-based collection, override both of these methods to avoid any issues that can be painful to find when the issue appear in production because the error is not in the code that is present, but in the code that is absent.*

## **Business Impacts**

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/innovation/)

### CAST recommendations

### References

https://technet.microsoft.com/en-us/library/ms187009(v=sql.105).aspx

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
