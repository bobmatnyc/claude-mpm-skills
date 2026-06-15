---
title: Method parameters should have their description tag
url: https://doc.casthighlight.com/alt_missingautomateddoc2-method-parameters-should-have-their-description-tag/
slug: alt_missingautomateddoc2-method-parameters-should-have-their-description-tag
content_type: rule
languages: [dotnet, java]
has_code_examples: false
---

[Software Agility](http://casthighlight.wpengine.com/software-agility/)[Embedded Documentation](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-agility/embedded-documentation/)

# **Why you should care**

Ensuring your application source code is well-documented is a no brainer and an undisputed good programming practice. And since applications are now more and more exposed to a technical audience through APIs, the level and quality of the technical documentation is a key differentiator that could make your software adopted (or not) by a user community. The Java-native javadoc (XMLDOC for C#) feature is one of the greatest ways to automatically build your API/technical documentation (see tools like Swagger, SpringDoc, NDoc or Sandcastle) and to ensure it is synced with your code.

# **Business Impacts**

When proper documentation is attached to an application via documentation generators, the source code becomes much easier to understand and maintain for internal developers.

Without this addition, it may be harder for developers to collaborate on a codebase AND if the application is ever opened for external use, it may be perceived as undesirable, since it would be difficult to work with missing pieces of documentation.

[Cost](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/)

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

# **CAST recommendations**

Static code analysis tools can help your development teams identify where description tags are missing.  A small effort today quickly turns into big quality tomorrow, especially if you plan to expose your application through an API.

# **References**

<http://www.oracle.com/technetwork/java/javase/documentation/index-137868.html>

[Style Guide](https://github.com/Kristories/awesome-guidelines)

# **How we detect**

This code insight verifies the ratio between the number of method parameters which have an associated [javadoc](https://en.wikipedia.org/wiki/Javadoc) (or XMLDOC for C#) tag (e.g. @param name description) and the total number of method parameters.

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See Features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
