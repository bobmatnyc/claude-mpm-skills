---
title: Avoid ‘switch’ with too many ‘case’ statements
url: https://doc.casthighlight.com/alt_largeswitchcase-avoid-switch-many-case-statements/
slug: alt_largeswitchcase-avoid-switch-many-case-statements
content_type: rule
category: Changeability
has_code_examples: true
---

[SOFTWARE AGILITY](https://doc.casthighlight.com/software-agility/)

[CODE READABILITY](https://doc.casthighlight.com/category/product/indicators-methodology/code-insights/software-agility/code-readability/)

# **Why you should care**

When switch statements have large sets of case clauses, it is usually an attempt to map two sets of data. A real map structure would be more readable and maintainable, and should be used instead.

# **How we detect**

CAST Highlight triggers this code insight when the average number of cases for switches found into a source file exceeds 3.

```
func main() {
i := 2
fmt.Print("Write ", i, " as ")
switch i {
case 1:
fmt.Println("one")
case 2:
fmt.Println("two")
case 3:
fmt.Println("three")
case 4:
fmt.Println("four")
case 5:
fmt.Println("five")
}
}
// 5 cases - 3 = 2

func main() {
fmt.Print("Go runs on ")
switch os := runtime.GOOS; os {
case "darwin":
fmt.Println("OS X.")
case "linux":
fmt.Println("Linux.")
case "webOS":
fmt.Println("WebOS.")
case "otherOS":
fmt.Println("otherOS.")
default:
// freebsd, openbsd,
// plan9, windows...
fmt.Printf("%s.\n", os)
}
}
// 4 cases - 3 = 1
func main() {
switch time.Now().Weekday() {
case time.Saturday:
fmt.Println("Today is Saturday.")
case time.Sunday:
fmt.Println("Today is Sunday.")
case time.Friday:
fmt.Println("Today is Friday.")
default:
fmt.Println("Today is a weekday.")
}
}
// There is 2 switch containing more than 3 cases
// so average is (2+1) / 2 (total switch) = 1.5 => rounded to 2
```

# **References**

<https://rules.sonarsource.com/go/RSPEC-1479>

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

[SEE FEATURES](https://www.castsoftware.com/products/highlight/outputs-analytics)

[HOW IT WORKS](https://www.castsoftware.com/products/highlight/how-it-works)
