---
title: Avoid ‘if … else if’ constructs with missing final ‘else’ clauses
url: https://doc.casthighlight.com/alt_missingfinalelse-avoid-else-constructs-missing-final-else-clauses/
slug: alt_missingfinalelse-avoid-else-constructs-missing-final-else-clauses
content_type: rule
languages: [java]
category: Changeability
has_code_examples: true
---

[SOFTWARE RESILIENCY](https://doc.casthighlight.com/software-resiliency/)

[CODE RELIABILITY](https://doc.casthighlight.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# **Why you should care**

This rule applies whenever an if statement is followed by one or more else if statements; the final else if should be followed by an else statement.

The requirement for a final else statement is defensive programming.

The else statement should either take appropriate action or contain a suitable comment as to why no action is taken. This is consistent with the requirement to have a final default clause in a switch statement.

# **How we detect**

CAST Highlight counts one occurrence each time if-else if statements are not ended by else clause, except when all branches of an if-else if end with return, the code that comes after the if implicitly behaves as if it was in an else clause.

Bad Code

```
if x == 0 {
	doSomething()
} else if x == 1 {
	doSomethingElse()
}
```

Good Code

```
if x == 0 {
	doSomething()
} else if x == 1 {
	doSomethingElse()
} else {
	return errors.New("unsupported int")
}
 
if x == 0 {
	doSomething()
	return 1
} else if x == 1 {
	return 2
} else if {
	return errors.New("unsupported int")
}
```

# **References**

<https://stackoverflow.com/questions/35053371/what-is-the-benefit-of-terminating-if-else-if-constructs-with-an-else-clause>  
<https://rules.sonarsource.com/java/RSPEC-126>  
<https://wiki.sei.cmu.edu/confluence/display/java/MSC57-J.+Strive+for+logical+completeness>

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

[SEE FEATURES](https://www.castsoftware.com/products/highlight/outputs-analytics)

[HOW IT WORKS](https://www.castsoftware.com/products/highlight/how-it-works)
