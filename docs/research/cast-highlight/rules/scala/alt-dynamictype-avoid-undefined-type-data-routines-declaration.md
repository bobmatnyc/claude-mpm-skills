---
title: Avoid undefined type on data or routines declaration
url: https://doc.casthighlight.com/alt_dynamictype-avoid-undefined-type-data-routines-declaration/
slug: alt_dynamictype-avoid-undefined-type-data-routines-declaration
content_type: rule
languages: [scala]
has_code_examples: true
---

[SOFTWARE RESILIENCY](https://doc.casthighlight.com/software-resiliency/)

[BEST PRACTICES](https://doc.casthighlight.com/category/product/indicators-methodology/code-insights/software-resiliency/best-practices/)

# **Why you should care**

Groovy support dynamic types, that is declarations where the type is *def* or *unspecified*.

# **How we detect**

CAST Highlight counts one occurrence each time a function, method, field member, variable or parameter has no explicit type defined. def is not an explicit type.

```
    void functionWithDynamicParameter(def parameter) {              // violation
    }
 
    void functionWithParameterWithoutTypeDeclaration(parameter, def param2) {   // + 2 violations
    }
 
    void functionWithObjectParameter(Object parameter)              // OK
 
    def functionWithDynamicReturnType() {                         // + 1 VIOLATION
    }
 
   def variableWithDynamicType = "yoooo"                       // +1 VIOLATION
 
    class toto {
              def fieldWithDynamicType = 0       // +1 VIOLATION
 
              def int fieldWithExplicitType        // OK
 
              def void methodWithExplicitReturnType() {   // OK
              }
 
              def methodWithDynamicType() {              // +1 VIOLATION
                       def localVarWithDynamicType = 0   // +1 VIOLATION
              }
 
    }
```

# **References**

<https://codenarc.org/codenarc-rules-convention.html> (FieldTypeRequired, MethodParameterTypeRequired, MethodReturnTypeRequired, VariableTypeRequired)

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

[SEE FEATURES](https://www.castsoftware.com/products/highlight/outputs-analytics)

[HOW IT WORKS](https://www.castsoftware.com/products/highlight/how-it-works)
