---
title: The code contains use of getClass().getName()
url: https://doc.casthighlight.com/alt_classescomparisons-code-contains-use-getclass-getname/
slug: alt_classescomparisons-code-contains-use-getclass-getname
content_type: rule
languages: [java]
category: Efficiency
has_code_examples: true
---

[SOFTWARE RESILIENCY](https://doc.casthighlight.com/software-resiliency/)

[BEST PRACTICES](https://doc.casthighlight.com/category/product/indicators-methodology/code-insights/software-resiliency/best-practices/)

# **Why you should care**

In a Java Virtual Machine (JVM), “Two classes are the same class (and consequently the same type) if they are loaded by the same class loader and they have the same fully qualified name” [JVMSpec 1999]. Two classes with the same name but different package names are distinct, as are two classes with the same fully qualified name loaded by different class loaders.

It could be necessary to check whether a given object has a specific class type or whether two objects have the same class type associated with them, for example, when implementing the equals() method. If the comparison is performed incorrectly, the code could assume that the two objects are of the same class when they are not. As a result, class names must not be compared.

Depending on the function that the insecure code performs, it could be vulnerable to a mix-and-match attack. An attacker could supply a malicious class with the same fully qualified name as the target class. If access to a protected resource is granted based on the comparison of class names alone, the unprivileged class could gain unwarranted access to the resource.

Conversely, the assumption that two classes deriving from the same codebase are the same is error prone. Although this assumption is commonly observed to be true in desktop applications, it is typically not the case with J2EE servlet containers. The containers can use different class loader instances to deploy and recall applications at runtime without having to restart the JVM. In such situations, two objects whose classes come from the same codebase could appear to the JVM to be two different classes. Also note that the equals() method might not return true when comparing objects originating from the same codebase.

# **How we detect**

This Code Insight counts one occurrence each time the following pattern is detected in the source code:

```
getClass().getName()
```

# **References**

<https://wiki.sei.cmu.edu/confluence/display/java/OBJ09-J.+Compare+classes+and+not+class+names>

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

[SEE FEATURES](https://www.castsoftware.com/products/highlight/outputs-analytics)

[HOW IT WORKS](https://www.castsoftware.com/products/highlight/how-it-works)
