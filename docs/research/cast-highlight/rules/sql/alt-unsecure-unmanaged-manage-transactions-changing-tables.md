---
title: Manage transactions when changing tables
url: https://doc.casthighlight.com/alt_unsecure-unmanaged-manage-transactions-changing-tables/
slug: alt_unsecure-unmanaged-manage-transactions-changing-tables
content_type: rule
languages: [sql]
category: Efficiency
has_code_examples: false
---

- [JSP](#1678173447076-3e1e0e09-d1f0)
- [SQL](#1678185388731-23b3a295-9871)

#### [JSP](#1678173447076-3e1e0e09-d1f0)

[Software Resiliency](https://doc.casthighlight.com/software-resiliency/)

[Code Reliability](https://doc.casthighlight.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# **Why you should care**

Every Servlet or JSP exposed to the Internet represents another attack surface and potential failure point. The best solution is to expose only what’s necessary under the most restrictive conditions that make sense.

It is common to think that internal web applications are deployed where they can only be accessed from trusted users. But in reality you can often find situations where the security policy needs to change, for example the ports or the source address to access to the web server might change or the mix of security policy and Network Address Translation policy open an unwanted address, port

A JSP application is not secured if the web.xml that doesn’t match the following conditions:  
\* Existence of node: security-constraint/web-resource-collection/url-pattern  
\* Existence of node: security-constraint/auth-constraint in the same node than the previous security-constraint node  
\* the url-pattern defined in security-constraint/web-resource-collection/url-pattern match at least one JSP page or a Servlet

# **CAST Recommendations**

# **References**

https://docs.oracle.com/cd/E19798-01/821-1841/bncbk/index.html

# **How we detect**

This code insight counts one occurrence if the web.xml file does not contain a <security-constraint> OR if this tag does not contain both following items :

a <web-resource-collection><url-pattern> node .  
an <auth-constraint> node.

Note : the web.xml file can contain several <security-constraint> tags. There is no violation for the rule if at least one of them is compliant with the above.

#### [SQL](#1678185388731-23b3a295-9871)

[Software Resiliency](https://doc.casthighlight.com/software-resiliency/)

[Code Reliability](https://doc.casthighlight.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# **Why you should care**

Transactions are vital in SQL as one of them is the representation of one or more changes to the database. For instance, anytime a record is created, updated or deleted in the database, a transaction is performed in that database.

Therefore, it is recommended to manage transactions as they ensure data integrity and handle database errors as well.

# **CAST Recommendations**

# **Business Impacts**

When involving transactions, it is important to note that the risks involved can hamper productivity since losing transactions is equivalent to losing records requiring the code to be rewritten. Loss of Productivity results in loss of time causing unsatisfactory work.

# **References**

https://www.tutorialspoint.com/sql/sql-transactions.htm

# **How we detect**

This code insight manages transactions with Functions and Procedures when a table is inserted, updated or deleted.

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
