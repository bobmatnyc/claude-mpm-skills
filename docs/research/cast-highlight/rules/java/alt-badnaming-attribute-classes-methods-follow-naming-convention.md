---
title: "Attribute, classes and methods should follow a naming convention"
url: https://doc.casthighlight.com/alt_badnaming-attribute-classes-methods-follow-naming-convention/
slug: alt_badnaming-attribute-classes-methods-follow-naming-convention
content_type: rule
languages: [java]
category: Changeability
has_code_examples: false
---

[Software Agility](http://casthighlight.wpengine.com/software-agility/)[Code Readability](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-agility/code-readability/)

# **Why you should care**

You may think naming conventions are purely cosmetic, and you’re not completely wrong. However, this is a signature of a mature development team who writes good software. If theses simple rules are not applied, what about the rest? Like in English where a sentence starts with a capital letter and ends with a full stop, naming conventions help developers read code easier and faster.

# **Business Impacts**

[Cost](http://casthighlight.wpengine.com/category/product/indicators-methodology/cost/)

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

# **CAST Recommendations**

Static code analysis tools can help your development teams identify this code insight, while modern IDEs propose to automatically rename identifiers across a software project.

# **References**

<https://www.thoughtco.com/using-java-naming-conventions-2034199>  
<https://google.github.io/styleguide/javaguide.html#s5.1-identifier-names>

[Style Guide](https://github.com/Kristories/awesome-guidelines)

# **How we detect**

This code insight verifies the ratio between cases where naming conventions for attributes, classes and methods are not applied to the total number of identifiers of this kind. Based on thresholds CAST has defined by analyzing software over the last 25 years, Highlight counts penalty points to the source file.

**Examples for Java:**  
– Classes should be in CamelCase: start with an uppercase, first letter of each next word starting with an uppercase  
– Methods should be in mixed case: start with lowercase, first letter of each next word starting with an uppercase

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
