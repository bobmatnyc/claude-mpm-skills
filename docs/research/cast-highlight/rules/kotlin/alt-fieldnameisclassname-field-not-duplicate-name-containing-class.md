---
title: A field should not duplicate the name of its containing class
url: https://doc.casthighlight.com/alt_fieldnameisclassname-field-not-duplicate-name-containing-class/
slug: alt_fieldnameisclassname-field-not-duplicate-name-containing-class
content_type: rule
languages: [kotlin]
category: Changeability
has_code_examples: true
---

[SOFTWARE AGILITY](https://doc.casthighlight.com/software-agility/)

[CODE READABILITY](https://doc.casthighlight.com/category/product/indicators-methodology/code-insights/software-agility/code-readability/)

# **Why you should care**

It can be confusing to have a class member with the same name (case differences aside) as its enclosing class, especialy when considering the common practice of naming a class instance for the class itself.

Best practice dictates that any field or member with the same name as the enclosing class be renamed to be more descriptive of the particular aspect of the class it represents or holds.

# **How we detect**

CAST Highlight counts one occurrence each time a field has the same name than its class or struct.

**Bad Code**

```
public class Foo {
  private var foo : String // NonCompliant
 
  public func getFoo() -> String {
     return foo
  }
}
struct SuperHero {
    var superhero : String  // NonCompliant
    var power: String
    
    func whoIsIt() {
        print("Name: " + self.nom + ", Power: " + self.power)
    }
}
var foo = Foo()
foo.getFoo() // what does this return?
```

**Good Code**

```
public class Foo {
  private var name : String
  public func getName() -> String {
      return name
  }
}
 
var foo = Foo();
foo.getName()
```

# **References**

<https://kotlinlang.org/docs/coding-conventions.html>  
[https://riptutorial.com/kotlin/example/30735/elvis-operator—–](https://riptutorial.com/kotlin/example/30735/elvis-operator-----)  
<https://github.com/Kotlin/kotlin-style-guide/issues/18>

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

[SEE FEATURES](https://www.castsoftware.com/products/highlight/outputs-analytics)

[HOW IT WORKS](https://www.castsoftware.com/products/highlight/how-it-works)
