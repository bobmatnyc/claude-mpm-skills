---
title: "Prefer single quotes over double quotes for strings, in a consistent way"
url: https://doc.casthighlight.com/alt_string-avoid-mixed-style-for-string-quote/
slug: alt_string-avoid-mixed-style-for-string-quote
content_type: rule
languages: [python, java, javascript]
category: Changeability
has_code_examples: true
---

[Software Agility](http://casthighlight.wpengine.com/software-agility/)[Code Readability](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-agility/code-readability/)

# **Why you should care**

Be consistent with your choice of string quote character within a file. Pick ‘ or ” and stick with it. However, in a JavaScript context, the single quote will be preferred in order to have to escape single quotes in strings.

# **Business Impacts**

Consistency is key is keeping a maintainable codebase. While there is no practical difference using single or double quotes, is strongly advised to stick with one to avoid confusion and accidental bug creation among developers. A established style also will reduce conflict among the development team and wasted development time with maintenance.

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

# **CAST Recommendations**

Establish a clear and consistent style guide for your development team, which makes it clear what is the primary quote type to use, and when exactly it is acceptable to use the alternative. In a Javascript context, prioritize the use of single quotes over double quotes as JS usually has to manipulate/return HTML and JSON content where double quotes are the norm.

### References

<https://bytearcher.com/articles/single-or-double-quotes-strings-javascript/>  
<https://google.github.io/styleguide/jsguide.html#features-strings-use-single-quotes>

# **How we detect**

For Javascript, this code insight counts an occurrence each time a string is enclosed with double quotes, except if the string contains single quotes.

**Bad code sample**:

```
var foo = "it is a bad string";
var foo2 = "it is a \"bad\" string";
```

**Good code sample:**

```
var foo = "it's a good string";

var JSONObject='{
    "name":"John Johnson",
    "street":"Oslo West 555",
    "age":33,
    "phone":"555 1234567"}';
```

---

For other technologies, this code insight computes the number or string using ” and the number of string using ‘. The alert level defined in the model will be in relation with the ratio between them : a 50% ratio will be the worst possible result.

Also :

NSQ = Number of simple Quote  
NDQ = Number of Double Quote

***Nbr\_MixedStringsStyle = int ( 100 \* Min(NSQ, NDQ) / (NSQ + NDQ))***

**Bad code sample**

```
Python("Why are you hiding your eyes?")
Gollum('The lint. It burns. It burns us.')
Gollum("Always the great lint. Watching. Watching.")
```

**Good code sample**

```
Python('Why are you hiding your eyes?')
Gollum("I'm scared of lint errors.")
Narrator('"Good!" thought a happy Python reviewer.')
```

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)
