---
title: The code contains too many data contigus levels
url: https://doc.casthighlight.com/alt_contiguslevel-code-contains-many-data-contigus-levels/
slug: alt_contiguslevel-code-contains-many-data-contigus-levels
content_type: rule
has_code_examples: true
---

[SOFTWARE RESILIENCY](https://doc.casthighlight.com/software-resiliency/)

[BEST PRACTICES](https://doc.casthighlight.com/category/product/indicators-methodology/code-insights/software-resiliency/best-practices/)

# **Why you should care**

When creating a new data level, do not add 1 to the previous level. Having not contigus level is easier for inserting an intermediate level later, if needed.

# **How we detect**

CAST Highlight counts one occurrence each time two contiguus levels are detected.

**Bad Code**

```
000180 01 SALES-RECORD.
000190 02 BROKER-REGION PIC 9. 
000200 02 BROKER-CITY PIC X(19).
000210 02 BROKER-NAME PIC X(20).
```

**Good Code**

```
000180 01 SALES-RECORD.
000190 03 BROKER-REGION PIC 9. 
000200 03 BROKER-CITY PIC X(19).
000210 03 BROKER-NAME PIC X(20).
```

# **References**

Coming soon…

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

[SEE FEATURES](https://www.castsoftware.com/products/highlight/outputs-analytics)

[HOW IT WORKS](https://www.castsoftware.com/products/highlight/how-it-works)
