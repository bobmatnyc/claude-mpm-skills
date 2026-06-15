---
title: Avoid structures initializations with unamed fields
url: https://doc.casthighlight.com/alt_unnameddata-avoid-structures-initializations-unamed-fields/
slug: alt_unnameddata-avoid-structures-initializations-unamed-fields
content_type: rule
has_code_examples: true
---

[SOFTWARE RESILIENCY](https://doc.casthighlight.com/software-resiliency/)

[BEST PRACTICES](https://doc.casthighlight.com/category/product/indicators-methodology/code-insights/software-resiliency/best-practices/)

# **Why you should care**

You should almost always specify field names when initializing structs. This is now enforced by [go vet](https://pkg.go.dev/cmd/vet).

# **How we detect**

CAST Highlight counts one occurrence each time a struct field has no name, except when init concerns an array.

```
// bad
func foo {
     // local var
     k := User{"John", "Doe", true}
}
my_function(User{"Joe", "Bidon", true})
 
//good
func bar {
    k := User{
        FirstName: "John",
        LastName: "Doe",
        Admin: true,
    }
}
 
func toto() {
     sig = append(sig, common.LeftPadBytes([]byte{64}, 32)...)
     tab = []String{“s1”, “s2”, “s3}
}
```

# **References**

<https://github.com/uber-go/guide/blob/master/style.md#use-field-names-to-initialize-structs>

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

[SEE FEATURES](https://www.castsoftware.com/products/highlight/outputs-analytics)

[HOW IT WORKS](https://www.castsoftware.com/products/highlight/how-it-works)
