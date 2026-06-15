---
title: "Transitive Dependencies: How much can you trust friends of your friends?"
url: https://doc.casthighlight.com/transitive-dependencies-much-can-trust-friends-friends/
slug: transitive-dependencies-much-can-trust-friends-friends
content_type: methodology
category: Security
---

***Friends of your friends are not necessarily your friends. In this post, we’ll see why it is important to get visibility on dependencies of the Open Source components your apps are using and how to manage security and license information of these transitive dependencies in CAST Highlight’s [Software Composition Analysis](https://www.castsoftware.com/products/highlight/software-composition-analysis) dashboards.***

In case you never watched the movie “[Project X](https://www.imdb.com/title/tt1636826/)“, just imagine that you organized a party for tonight with 3 or 4 of your best friends, planned to have a beer, watch a movie and eat some pizzas… and that’s it. But in reality, when your 4 best friends knock at your door, they didn’t tell you that each of them invited 5 to 10 of their own friends. You quickly lose control of the situation and the cops come in at this exact moment…

You generally trust your friends, right? But what do you really know about their friends you never met before tonight? Do you usually conduct background checks and verify security clearances for anyone coming into your house? This analogy fits perfectly with transitive dependencies. In a nutshell, transitive dependencies are the components that are necessary for the Open Source Software (OSS) your app uses to run, compile or be tested. These additional components have their own lifecycle, licenses and copyrights, bugs and vulnerabilities.

As a result, you can’t truly know in advance the complete degree of exposure to software risks when you decide to use component XYZ for your app. This is even more true when your app is built on top of 100, 200 or 300 OSS components which probably have multiple dependencies themselves.

As an example for Maven, on average, an Open Source component references around 60 dependencies. While 6% of them are for test purposes (Junit is dominating Maven-based OSS projects), 93% are needed for the compilation, 1% are only required at runtime, meaning that they’re executed with or by your software. Except for test dependencies, security is not something that can be ignored. As we say “a chain is only as strong as its weakest link”.

| Type | Distribution | Definition |
| --- | --- | --- |
| **TEST** | 6% | This scope indicates that the dependency is not required for normal use of the application, and is only available for the test compilation and execution phases. This scope is not transitive. |
| **COMPILE** | 90% | This is the default scope, used if none is specified. Compile dependencies are available in all classpaths of a project. Furthermore, these dependencies are propagated to dependent projects. |
| **PROVIDED** | 3% | This is much like compile, but indicates you expect the JDK or a container to provide the dependency at runtime. For example, when building a web application for the Java Enterprise Edition, you would set the dependency on the Servlet API and related Java EE APIs to scope “PROVIDED” because the web container provides these classes. This scope is only available on the compilation and test classpath, and is not transitive. |
| **RUNTIME** | 1% | This scope indicates that the dependency is not required for compilation, but is for execution. It is in the runtime and test classpaths, but not the compile classpath. |

*Table of the different types of dependencies and respective distribution, based on dependency crawling of Maven Central components (June 2019).*

One good real-life example to illustrate how a risk can be propagated through dependencies is [Apache ActiveMQ](https://activemq.apache.org/). The version 5.3.0 of this very popular Java-based messaging server is using [Spring-Beans 2.5.6](https://mvnrepository.com/artifact/org.springframework/spring-beans/usages)  from Spring framework, a dependency that allows [remote attackers to execute arbitrary code via an HTTP request](https://nvd.nist.gov/vuln/detail/CVE-2010-1622). How many times has ActiveMQ been downloaded in this version and implemented in business applications around the globe? Across your application portfolio?

Hence the need to get the visibility on what’s going on under the hood and have a sense of the security risk your application is accumulating across the multiple dependency layers.

# **What can I do to protect an app against transitive vulnerabilities?**

Realistically, I’m not saying you should fix all transitive vulnerabilities as you don’t manage this part of the equation. But at least you must know where they’re located and estimate a level of density and recurrence. In some cases, actions can be taken:

- If one of the direct OSS components is pulling critical transitive vulnerabilities in a specific version, consider upgrading it. The component team has probably fixed these CVEs by patching their own dependencies in an updated version.
- If one of the direct OSS components is pulling too many transitive vulnerabilities spread across multiple dependencies, and their number doesn’t seem to decrease over the version timeline, seriously consider finding an alternative to this component.

# **Transitive dependencies in CAST Highlight**

CAST has consolidated a unique database on Open Source made up of 94+ millions components, representing more than 9 billion distinct file fingerprints. Leveraging this unique knowledge base and some exclusive machine learning and crawling algorithms, Highlight recently started to resolve dependencies between these components. So far, more than 144 million links between OSS components have been identified and recorded into the SCA database.

**Supported OSS forges for component dependency calculation:**

- Maven
- NPM
- Nuget
- Packagist
- PyPi
- RubyGem

![8551](https://doc.casthighlight.com/wp-content/uploads/2019/05/CAST-Highlight-SCA-TransitiveDependencies-cropped.png)

- Transitive dependencies are available from the Software Composition dashboard by clicking on the magnifying glass of third-party components found in your application. On click, a modal opens and lists the component dependencies with their type (test, runtime, compile, etc.) and indicates:  
  the possible security vulnerabilities (a.k.a. CVEs) they may have and whether they are critical, high, medium or low from a severity standpoint
- their license type and if these comply with your license compliance policy

In case you want a thorough list of all identified transitive dependencies in your software, you can simply export the BOM (Bill of Material) and switch on the inclusion of transitive dependencies in the Excel report. They will be listed in a dedicated ‘Dependencies’ sheet along with CVE and license occurrences. If you have defined your own license compliance policy in Highlight, license cell colors will reflect the component dependency compliance.

That’s all folks!
