---
title: The code contains classes that overload equals(Object)
url: https://doc.casthighlight.com/alt_overloadequals_code-contains-classes-overload-equalsobject/
slug: alt_overloadequals_code-contains-classes-overload-equalsobject
content_type: rule
languages: [java]
has_code_examples: true
---

[SOFTWARE RESILIENCY](https://doc.casthighlight.com/software-resiliency/)

[BEST PRACTICES](https://doc.casthighlight.com/category/product/indicators-methodology/code-insights/software-resiliency/best-practices/)

# **Why you should care**

“equals” as a method name should be used exclusively to override Object.equals(Object) to prevent any confusion. It is tempting to overload the method to take a specific class instead of Object as parameter, to save the class comparison check. However, this will not work as expected when that is the only override.

In addition, issues with Overloaded Equals:

- All the Collections provided by Java ie; Set, List, Map use the overridden method for comparing two objects.  
  So **even if you overload the equals method**, **it doesn’t solve** the purpose of comparing two objects.  
  Also, if you just overload and implement the hashcode method, it would result in erroneous behavior
- If you have **both overloaded and overridden** equals methods and exposing both these methods **you are going to confuse** the client side developers.  
  It is by convention people believe that you are overriding the Object class

# **How we detect**

CAST Highlight counts one occurrence each time an equals method is overloaded, i.e. has parameters with type other than Object.

**Bad Code**

```
class MyClass {
private int foo = 1;

public boolean equals(MyClass o) { // Noncompliant; does not override Object.equals(Object)
return o != null && o.foo == this.foo;
}

public static void main(String[] args) {
MyClass o1 = new MyClass();
Object o2 = new MyClass();
System.out.println(o1.equals(o2)); // Prints "false" because o2 an Object not a MyClass
}
}

class MyClass2 {
public boolean equals(MyClass2 o) { // Ignored; `boolean equals(Object)` also present
//..
}

public boolean equals(Object o) {
//...
}
}
```

**Good Code**

```
class MyClass {
private int foo = 1;

@Override
public boolean equals(Object o) {
if (this == o) \{
return true;
}
if (o == null || getClass() != o.getClass()) {
return false;
}

MyClass other = (MyClass)o;
return this.foo == other.foo;
}

/* ... */
}

class MyClass2 {
public boolean equals(MyClass2 o) {
//..
}

public boolean equals(Object o) {
//...
}
}
```

# **References**

<https://stackoverflow.com/questions/2910520/is-overloading-equals-worthwhile>  
<https://rules.sonarsource.com/java/RSPEC-1210>

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

[SEE FEATURES](https://www.castsoftware.com/products/highlight/outputs-analytics)

[HOW IT WORKS](https://www.castsoftware.com/products/highlight/how-it-works)
