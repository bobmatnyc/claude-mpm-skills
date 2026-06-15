---
title: URIs (URL & path) should not be hardcoded for testability purpose
url: https://doc.casthighlight.com/alt_hardcodedpaths-uris-url-path-not-hardcoded/
slug: alt_hardcodedpaths-uris-url-path-not-hardcoded
content_type: rule
languages: [swift]
category: Robustness
has_code_examples: true
---

[SOFTWARE RESILIENCY](https://doc.casthighlight.com/software-resiliency/)

[BEST PRACTICES](https://doc.casthighlight.com/category/product/indicators-methodology/code-insights/software-resiliency/best-practices/)

# **Why you should care**

Hard coding a URI makes it difficult to test a program: path literals are not always portable across operating systems, a given absolute path may not exist on a specific test environment, a specified Internet URL may not be available when executing the tests, production environment filesystems usually differ from the development environment, …etc. For all those reasons, a URI should never be hard coded. Instead, it should be replaced by customizable parameter.

Further even if the elements of a URI are obtained dynamically, portability can still be limited if the path-delimiters are hard-coded.

This code insight triggers only when URL or path delimiters are hard coded. URL security aspect is checked through Cloud Maturity patterns.

# **How we detect**

CAST Highlight counts one occurrence each time an URL or a path is hardcoded.

**Bad Code**

```
public class Foo {
    public func listUsers() -> [User] {
        var users:[User]
        let location = "/home/mylogin/Dev/users.txt"     // Non-Compliant
        let fileContent = NSString(contentsOfFile: location, encoding: NSUTF8StringEncoding, error: nil)
        users = parse(fileContent!)
        return users
    }
}
let url = URL(string: "https://www.apple.com")    // Non-Compliant
```

**Good Code**

```
public class Foo {
    // Configuration is a class that returns customizable properties: it can be mocked to be injected during tests.
    private var config:Configuration
    public init(myConfig:Configuration) {
        config = myConfig
    }
    public func listUsers() -> [User] {
        var users:[User]
        // Find here the way to get the correct folder, in this case using the Configuration object
        let location = config.getProperty("myApplication.listingFile")
        // and use this parameter instead of the hard coded path
        let fileContent = NSString(contentsOfFile: location, encoding: NSUTF8StringEncoding, error: nil)
        users = parse(fileContent!)
        return users
    }
}
```

# **References**

<https://wiki.sei.cmu.edu/confluence/pages/tinyurl.action?urlIdentifier=qQCHAQ>  
<https://rules.sonarsource.com/swift/RSPEC-1075>

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

[SEE FEATURES](https://www.castsoftware.com/products/highlight/outputs-analytics)

[HOW IT WORKS](https://www.castsoftware.com/products/highlight/how-it-works)
