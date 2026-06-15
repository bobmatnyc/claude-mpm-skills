---
title: How OSS licenses are mined and detected in Highlight’s Software Composition Analysis feature
url: https://doc.casthighlight.com/oss-licenses-mined-detected-highlights-software-composition-analysis-feature/
slug: oss-licenses-mined-detected-highlights-software-composition-analysis-feature
content_type: rule
languages: [python, java, javascript]
category: CloudReady
has_code_examples: false
---

**CAST has developed unique algorithms to mine and detect licenses from Open Source components to let you get a (more accurate) sense of IP and legal impacts your software is exposed to. Here is how it works.**

Very often in open source forges, the license information at the project level is not available, or not totally accurate. While a repository owner can pick one main license from a list, different licenses can apply on sub-modules or just give the opportunity to the user to decide whether it will be under MIT and/or Apache 2.0 license… what we commonly call dual-licensed projects. At the end of the day, you never really know the exact licenses of the project you use and the related legal and operational constraints, until you checked manually.

In addition, the different forges are not equal in that regard. On a sample made of 13 million of projects in our Open Source database, only 17% of Github-hosted repos were found with a license, while NPM and Maven had respectively 90% and 71%. Still for Github, 21% of the repos found with at least one license had a “NOASSERTION” tag (i.e. not sure what the exact license is).

![8514](https://doc.casthighlight.com/wp-content/uploads/2019/02/LicenseDistributionOpenSource.png)

In order to increase the accuracy of license resolutions and to make your team save a huge amount of time, Highlight has developed a license mining algorithm (mixing semantic and statistical analysis algorithms such as [Ngram](https://en.wikipedia.org/wiki/N-gram), [TD-IDF](https://en.wikipedia.org/wiki/Tf%E2%80%93idf)…) to automatically detect the right license(s) and retro feed this data in our Open Source database.

This “license matcher” is continuously running in our Cloud back-end and go after projects hosted on the different forges we support (Github, Maven, NuGet, NPM, PyPi, GitLab…) to extract license texts from dependency files (e.g., pom.xml’s license section), forges’ APIs or typical license files such as license.txt, readme.md, COPYING-LESSER… and verify more than 350 license types based on [SPDX data](https://spdx.org/) in a few milliseconds with pretty decent results: 99% accurate. From the most frequently used licenses such as MIT (representing ~39% of Open Source projects), Apache 2.0 (~11%), GPL 2.0 (~10%) … to the most funny ones like [WTFPL](https://spdx.org/licenses/WTFPL) (~0.3%).

DO WHAT THE F\*\*\* YOU WANT TO PUBLIC LICENSE  
Version 2, December 2004

Copyright (C) 2004 Sam Hocevar <sam@hocevar.net>

Everyone is permitted to copy and distribute verbatim or modified  
copies of this license document, and changing it is allowed as long  
as the name is changed.

DO WHAT THE F\*\*\* YOU WANT TO PUBLIC LICENSE  
TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION

0. You just DO WHAT THE F\*\*\* YOU WANT TO.

## How CAST License Risk Profile determined?

The license risk out-of-the-box profile in CAST Highlight has been inspired by a combination of different sources of information on this topic:

- [Choosealicense.com](https://choosealicense.com/appendix/) matrix that details the different constraints/conditions and permissions for the most popular licenses
- White papers, research papers
- Views from the main players of the Software Composition Analysis market

More importantly, in case you or your legal team have different views on license risks, CAST Highlight allows portfolio managers to define their own license risk profile.
