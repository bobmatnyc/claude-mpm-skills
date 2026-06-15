---
title: CDATA is an XML construct which can only be read by JSP
url: https://doc.casthighlight.com/alt_xmlformat-use-cdata-for-jsp-documents/
slug: alt_xmlformat-use-cdata-for-jsp-documents
content_type: rule
languages: [java, javascript]
has_code_examples: false
---

[Software Resiliency](http://casthighlight.wpengine.com/software-resiliency/)[Programming Best Practices](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/programming-best-practices/)

# **Why you should care**

CDATA stands for character Data and is an XML construct. It lies in between these strings which include data that could mistakenly be interpreted as XML markup. It has no meaning in HTML as it is ignored by the parser. However, it is not ignored by Javascript making CDATA markers useful around the text of inline and elements of XHTML documents.

# **Business Impacts**

CDATA can be read by JSP scripts but it cannot be read by HTML which can make it a Production risk if used improperly. However it improves productivity when utilized correctly.

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/risk/)

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

# **CAST Recommendations**

# **References**

https://docs.oracle.com/cd/E19159-01/819-3669/bnalq/index.html

[Style Guide](https://github.com/Kristories/awesome-guidelines)

# **How we detect**

This code insight shows that, for JSP documents (using XML syntax), a CDATA element should be used only when necessary to ensure your code does not break the document structure. This occurs when writing Java code inside declarations, scriptlets, and expressions.

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
