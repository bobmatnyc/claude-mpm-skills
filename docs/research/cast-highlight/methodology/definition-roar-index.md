---
title: ROAR Index
url: https://doc.casthighlight.com/definition-roar-index/
slug: definition-roar-index
content_type: methodology
---

The ROAR (Ranking of Application Risks) index is a composite metric that takes into account the three main Highlight software health factors (Software Resiliency, Software Agility and Software Elegance) with a weighted average formula, balanced with the Business Impact of the application. And that’s probably the most important part of the formula here, since it mixes both technical and business assessment of each applications in a single metric.

> ROAR = (((100 – Resiliency) \* 7) + ((100 – Elegance) \* 2) + ((100 – Agility) \* 1))) / 10 \* Business Impact / 100

Theoretically, the ROAR index is ranged from 0 to 100.

**Score interpretation:**

- A high value means that the application is important to the business and presents a high level of risk (from a code quality standpoint) in the same time. Urgent to investigate.
- A low value means that the application is not very important to the business and presents relatively acceptable level of code quality. Investigation is low priority.
