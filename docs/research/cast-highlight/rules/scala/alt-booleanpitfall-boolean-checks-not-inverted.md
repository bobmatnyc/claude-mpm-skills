---
title: Boolean checks should not be inverted
url: https://doc.casthighlight.com/alt_booleanpitfall-boolean-checks-not-inverted/
slug: alt_booleanpitfall-boolean-checks-not-inverted
content_type: rule
languages: [scala, kotlin]
category: Transferability
has_code_examples: true
---

[SOFTWARE ELEGANCE](https://doc.casthighlight.com/software-elegance/)

[CODE COMPLEXITY](https://doc.casthighlight.com/category/product/indicators-methodology/code-insights/software-elegance/code-complexity/)

# **Why you should care**

It is needlessly complex to invert the result of a boolean comparison. The opposite comparison should be made instead. This is furthermore the case in compound conditions.

# **How we detect**

CAST Highlight counts one occurrence each time a conditions begins with an unjustified negation.  
The negation is justified if it provides more benefits than disadvantages.  
To evaluate the needing of using a negation, check how many “!” operators appear or disappear if we take the opposite conditional expression. Count one violation if the resulting number of ‘!’ is less or equal than is the original expression.  
Consider conditions expressions that comply with the following patterns :

- if (!( ….. ))
- while (!( ….. ))
- return !( … )
- … = !( … )

```
fun toto () {
    if (!(a == 2)) { b++ }  // Not compliant, prefer (a != 2)
    val b = !(i < 10)  // Not compliant, prefer (i >= 10)
    
    if (!((a>b) && titi() || !(a==1) && b==6)) { b++ }
    // not compliant, prefer (((a<b) || !titi()) && ((a==1) || b!==6))
        
    return !(!entityOptions.containerType.isFragment || !(entityOptions.cache ?: getGlobalCacheImpl(currentClass)).hasCache)
    // not compliant, prefer (entityOptions.containerType.isFragment && (entityOptions.cache ?: getGlobalCacheImpl(currentClass)).hasCache)        
 
    a = !(b && c && d) // OK, because (!b || !c || !d) is not more readable.
        
    if (!(a is FunctionDescriptor || a is PropertyDescriptor || a is PackageFragmentDescriptor)) {return}
    // not compliant, prefer (a !is FunctionDescriptor && a !is PropertyDescriptor && a !is PackageFragmentDescriptor)
}
```

# **References**

<https://rules.sonarsource.com/kotlin/RSPEC-1940>

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

[SEE FEATURES](https://www.castsoftware.com/products/highlight/outputs-analytics)

[HOW IT WORKS](https://www.castsoftware.com/products/highlight/how-it-works)
