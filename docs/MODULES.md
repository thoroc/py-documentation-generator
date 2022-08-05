# src

Empty DataFrame
Columns: []
Index: []


## commands

| name                              | path         | module   | functions                      | classes   |
|:----------------------------------|:-------------|:---------|:-------------------------------|:----------|
| generate_local_modules_listing.py | src/commands | commands | generate_local_modules_listing |           |
| generate_mailmap.py               | src/commands | commands | generate_mailmap               |           |


## generators

| name                       | path           | module     | functions   | classes                |
|:---------------------------|:---------------|:-----------|:------------|:-----------------------|
| documentation_generator.py | src/generators | generators |             | DocumentationGenerator |
| local_module_generator.py  | src/generators | generators |             | LocalModuleGenerator   |


## models

| name                    | path       | module   | functions   | classes                                                                                                      |
|:------------------------|:-----------|:---------|:------------|:-------------------------------------------------------------------------------------------------------------|
| \_\_init\_\_.py         | src/models | models   |             | WrongDataTypeException, MissingOutputFilenameException, MissingPackageException, MissingModuleFilesException |
| contributor_manager.py  | src/models | models   |             | ContributorManager                                                                                           |
| contributors.py         | src/models | models   |             | Contributor                                                                                                  |
| local_modules.py        | src/models | models   |             | LocalModule                                                                                                  |
| module_data_provider.py | src/models | models   |             | ModuleDataProvider                                                                                           |


