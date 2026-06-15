---
title: Multiple packages in the same file have multiple references can cause agility issues
url: https://doc.casthighlight.com/alt_basex_package-avoid-several-packages-in-the-same-file/
slug: alt_basex_package-avoid-several-packages-in-the-same-file
content_type: rule
languages: [sql]
category: Robustness
has_code_examples: false
---

[Software Agility](http://casthighlight.wpengine.com/software-agility/)[Code Readability](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-agility/Code-Readability/)

# **Why you should care**

A package is a schema object that groups logically related PL/SQL types, variables, and subprograms. They usually have a specification (spec) and a body. The spec is the package’s interface which declares the types, variables, constants, exceptions, cursors, and subprograms which are referenced from outside the package. Although the body tends to be unnecessary it defines queries for the cursors and code for the subprograms. Their advantages lie in Modularity, Easier application design, Information hiding, Added functionality, and better performance.

Avoid several packages in the same file because it requires Oracle to recompile every stored program that references the packages. As a result, multiple packages are referenced causing agility issues and possible bug entry.

# **Business Impacts**

Adding several packages in the same file can be seen as efficient but is actually a costly endevour that can hamper the code’s agility.

[Cost](http://casthighlight.wpengine.com/category/product/indicators-methodology/cost/)

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

# **CAST Recommendations**

# **References**

https://docs.oracle.com/cd/B19306\_01/appdev.102/b14261/packages.htm

[Style Guide](https://github.com/Kristories/awesome-guidelines)

# **How we detect**

This code insights shows that several packages should be avoided in the same file.

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
