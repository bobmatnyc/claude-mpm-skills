---
title: Open Source License Risk Profiles
url: https://doc.casthighlight.com/open-source-license-risk-profiles/
slug: open-source-license-risk-profiles
content_type: methodology
---

Using Open Source components makes your development team deliver software faster, but also comes with potential legal risks on license types that these OSS components use. Depending on your application context (distributed, mobile, embedded, etc.), some license types have more legal & operational consequences, while others are more flexible. CAST Highlight [detects 350+ Open Source licences](https://doc.casthighlight.com/oss-licenses-mined-detected-highlights-software-composition-analysis-feature/) comes with out-of-the-box and commonly adopted license risk profiles that help you quickly identify if your applications use risky license types. See below.

CAST Highlight comes with an out-of-the-box risk profile template that takes the different license constraints into account. However, if you have different views on specific licenses and the potential impact within your organization, you can build your own license risk profile. To do so, go to MANAGE PORTFOLIO > Manage License Profiles.

Our out-of-the-box license risk template follows these principles:

- If the license creates a risk of **custom proprietary source code disclosure**, it will fall under HIGH risk. This is when there is a risk to the organization’s IP. i.e. GPLv3: “Permissions of this strong copyleft license are conditioned on making available complete source code of licensed works and modifications, which include larger works using a licensed work, under the same license”. In short, if the app team makes modifications to the open source package, we have to disclose the source code of the whole application.
- If the license creates a risk of **library-modifications source code disclosure**, it will fall under MEDIUM risk. This is when there is a smaller risk to the organization’s IP, because only the potential modifications of the OSS package have to be disclosed. It limits the scope, but could also lead to significant IP being disclosed, if the developers have embedded business rules in the library edits. i.e. Mozilla Public License 2.0: “Permissions of this weak copyleft license are conditioned on making available source code of licensed files and modifications of those files under the same license (or in certain cases, one of the GNU licenses)”. In short, if the app team makes modifications to the open source package, we have to disclose the modified open source package.
- If none of these risks exist, it will fall under LOW risk

See <https://choosealicense.com/appendix/> for a summary of Permissions and Conditions for the major license types.

- [HIGH RISK](#1548092023597-a3ec38a2-f02e)
- [MEDIUM RISK](#1548092023610-e266d797-8c8a)
- [LOW RISK](#1548092154540-e43dce45-75c0)

#### [HIGH RISK](#1548092023597-a3ec38a2-f02e)

AGPL-3.0, EUPL-1.1, GPL-2.0, GPL-3.0, LGPL-2.1, LGPL-3.0

#### [MEDIUM RISK](#1548092023610-e266d797-8c8a)

EPL-1.0, MPL-2.0

#### [LOW RISK](#1548092154540-e43dce45-75c0)

Apache-2.0, BSD-2-Clause, BSD-3-Clause, BSL-1.0, MIT, Unlicense

**NOTE:** Some Open Source components use non-SPDX licenses detected by our license matching algorithm. You’ll see them under the ‘NOASSERTION’ tag.
