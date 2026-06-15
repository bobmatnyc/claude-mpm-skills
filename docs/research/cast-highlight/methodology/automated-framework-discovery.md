---
title: Automated Dependency Discovery & Supported Package Managers
url: https://doc.casthighlight.com/automated-framework-discovery/
slug: automated-framework-discovery
content_type: methodology
---

During code scan of your applications, Highlight automatically detects application dependencies to aggregate this data into CAST Highlight’s [Software Composition](https://www.castsoftware.com/products/highlight/capabilities#Software-Composition-Analysis) dashboards. Find below the list of the dependency management tools we support so far.

## Dependency discovery through dependency files and package managers

CAST Highlight retrieves and references other framework and library dependencies through the analysis of dependency & requirement configuration files, such as pom.xml (Java/Maven), .json (Javascript), and .vcproj (C#).

Currently supported dependency management tools & files:

- Ant (build.xml)
- Cargo (Cargo.toml, Cargo.lock)
- CMake (CMakeLists.txt)
- Composer (composer.json, composer.lock)
- Ruby/Gemfile (gemfile.lock)
- Go (Go.mod, Go.sum)
- Gradle (build.gradle, dependencies.gradle, build.gradle.kts)
- Maven (pom.xml)
- NPM (package.json and package-lock.json v1, v2, v3)
- Swift (package.swift, package.resolved)
- Python (requirements.txt, setup.py, poetry.json, poetry.lock)
- R (require(), library())
- Ruby (Gemfile.lock)
- Visual Studio (.vcproj, .csproj)
- Yarn (yarn.lock)

| Package Manager | Technology | Supported Files | Detail |
| --- | --- | --- | --- |
| **Ant** | Java | build.xml | All dependencies are extracted |
| **Cargo** | Rust | Cargo.tom, Cargo.lock | All dependencies are extracted from Cargo.toml. If Cargo.lock is present during the scan, lock versions will be retained for the extracted dependencies from Cargo.toml. |
| **CMake** | C/C++ | CMakeLists.txt | Libraries are extracted when found in find\_package() of CMakeLists.txt files (recursively). |
| **Composer** | PHP | composer.json, composer.lock | All dependencies are extracted. If composer.lock is present during the scan, lock versions will be retained for the extracted dependencies from composer.json files |
| **Conan** | C/C++, Python | conan.lock, conan.txt, conanfile.py | All dependencies are extracted. If conan.lock is present during the scan, lock versions will be retained for the extracted dependencies from conan.txt or conanfile.py |
| **Gem** | Ruby | gemfile.lock | All dependencies are extracted |
| **Go Module** | Go | go.mod, go.sum | All dependencies are extracted from go.mod, except if go.sum is present during the scan. All dependencies are extracted from go.sum. |
| **Gradle** | Java, Kotlin, Groovy, Scala | build.gradle, dependencies.gradle, settings.gradle | All dependencies are extracted except ‘test’ dependencies. If versions of extracted components are defined in settings.gradle, these versions will be retained. |
| **Maven** | Java | pom.xml | All dependency scopes are extracted except ‘test’, ‘provied’, and ‘system’ dependencies. Dependencies from <dependencyManagement> are not taken into account. Component versions found within <dependencyManagement> are used to resolve versions of components found within <dependencies> |
| **NPM** | JavaScript | package.json, package-lock.json | Dependency extraction:  - devDependencies are not extracted - By default, node\_modules folders are excluded from the scan, except if the option –includeAllDependencies is passed - By default,only dependencies found in package.json are extracted. First level of dependencies found in package-lock.json will be extracted only if the option –includeAllDependencies is passed     Dependency version resolution:   - package.json: All dependencies except devDependencies are extracted. If package-lock.json or yarn.lock are present during the scan, yarn/lock versions will be retained for the extracted dependencies from package.json files. |
| **Python/Poetry** | Python | poetry.lock, pyproject.toml, requirements.txt, setup.py | If poetry.lock is included, requirements.txt and  setup.py files will be ignored.  When included, pyproject.toml file is used to extract first-level dependencies and exclude unused dependencies found in poetry.lock (e.g., test, development dependencies).  poetry.lock is used to resolve dependency versions and complete the OSS dependency map. |
| **R** | R | <code>  DESCRIPTION file | All dependencies are extracted |
| **Swift Packages** | Swift | Package.swift, Package.resolved | All dependencies are extracted |
| **Visual Studio** | VB/VB.Net, C# | .csproj, .vcproj, project.assets.json | All dependencies are extracted. For version resolution, CAST Highlight will retain the version specified in HintPath if present. |
| **Yarn** | JavaScript | yarn.lock | All dependencies are extracted (you’ll have to use the –includeAllDependencies option during the scan in order to extract all dependencies including transitive dependencies. Otherwise, only dependencies from package.json files will be taken into account). |
