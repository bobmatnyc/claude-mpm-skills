---
title: Software Resiliency
url: https://doc.casthighlight.com/software-resiliency/
slug: software-resiliency
content_type: rule
languages: [php]
category: Robustness
has_code_examples: false
---

## **Definition**

Software Resiliency indicates programming best practices that make software bullet-proof, more robust and secure. This index is derived from technology-specific code analysis which searches for the presence of code patterns and bad programming practices which may compromise the reliability of the software in the short term. Higher the Software Resiliency, lower is the likelihood of defects to occur in production.

## **Thresholds**

Thresholds used for Software Resiliency categories:

- **Low/Red:** below 65.0
- **Medium/Orange:** from 65.0 to 87.0
- **High/Green:** above 87.0

## **Code Insights**

Find below some code insight examples which contribute to the Software Resiliency index.

##### Use of ‘return’ statement is not recommended

[Read more](https://doc.casthighlight.com/alt_badreturn/ "Read more about Use of ‘return’ statement is not recommended")

##### Do not compare to null

[Read more](https://doc.casthighlight.com/alt_comparetonull/ "Read more about Do not compare to null")

##### phpinfo() should not be used in production

[Read more](https://doc.casthighlight.com/alt_debug-phpinfo-not-used-production/ "Read more about phpinfo() should not be used in production")

##### The code contains too many PHP4 deprecated constructor naming.

[Read more](https://doc.casthighlight.com/alt_constructornaming-code-contains-many-php4-deprecated-constructor-naming-since-php5-constructor-named-__construct/ "Read more about The code contains too many PHP4 deprecated constructor naming.")

##### The code contains too many final artifacts in final classes

[Read more](https://doc.casthighlight.com/alt_finalmodifier-code-contains-many-final-artifacts-final-classes/ "Read more about The code contains too many final artifacts in final classes")

##### The code contains too many classes that declare \_\_get() without declaring \_\_set()

[Read more](https://doc.casthighlight.com/alt_missingsetter-code-contains-many-classes-declare-__get-without-declaring-__set/ "Read more about The code contains too many classes that declare __get() without declaring __set()")

##### Force casts should not be used

[Read more](https://doc.casthighlight.com/alt_dangerouscast-force-casts-not-used/ "Read more about Force casts should not be used")

##### Avoid abstract classes without abstract or concrete methods

[Read more](https://doc.casthighlight.com/alt_badabstractclass-avoid-abstract-classes-without-abstract-concrete-methods/ "Read more about Avoid abstract classes without abstract or concrete methods")

##### Variables should be declared with ‘let’ or ‘const’

[Read more](https://doc.casthighlight.com/alt_variabledeclaration-variables-declared-let-const/ "Read more about Variables should be declared with ‘let’ or ‘const’")

##### Multiline string literals should not be used

[Read more](https://doc.casthighlight.com/alt_badlinecontinuation-multiline-string-literals-not-used/ "Read more about Multiline string literals should not be used")

##### Logical OR should not be used in switch cases

[Read more](https://doc.casthighlight.com/alt_caseexpression-logical-not-used-switch-cases/ "Read more about Logical OR should not be used in switch cases")

##### Avoid caching selector for long time

[Read more](https://doc.casthighlight.com/alt_greedydataaccess-avoid-caching-selector-long-time/ "Read more about Avoid caching selector for long time")

##### URIs (URL & path) should not be hardcoded for testability purpose

[Read more](https://doc.casthighlight.com/alt_hardcodedpaths-uris-url-path-not-hardcoded/ "Read more about URIs (URL & path) should not be hardcoded for testability purpose")

##### try! should not be used

[Read more](https://doc.casthighlight.com/alt_dangeroustry-try-not-used/ "Read more about try! should not be used")

##### Avoid generic catch

[Read more](https://doc.casthighlight.com/alt_genericcatches-avoid-generic-catch/ "Read more about Avoid generic catch")

##### Avoid undefined type on data or routines declaration

[Read more](https://doc.casthighlight.com/alt_dynamictype-avoid-undefined-type-data-routines-declaration/ "Read more about Avoid undefined type on data or routines declaration")

##### Avoid to update static fields from instance methods

[Read more](https://doc.casthighlight.com/alt_assignmenttostaticfieldfrominstancemethod-avoid-update-static-fields-instance-methods/ "Read more about Avoid to update static fields from instance methods")

##### Avoid Public finalize() methods

[Read more](https://doc.casthighlight.com/alt_publicfinalizemethod-avoid-public-finalize-methods/ "Read more about Avoid Public finalize() methods")

##### Avoid confusing initialization for variables declared on the same line

[Read more](https://doc.casthighlight.com/alt_suspiciousdestructuringassignment-avoid-confusing-initialization-variables-declared-line/ "Read more about Avoid confusing initialization for variables declared on the same line")

##### The code contains too many unnecessary COMPUTE

[Read more](https://doc.casthighlight.com/alt_simplecompute-the-code-contains-too-many-unnecessary-compute/ "Read more about The code contains too many unnecessary COMPUTE")
