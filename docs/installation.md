<!--
   Copyright 2021 Modelyst LLC

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
 -->

# Installation

## Installing with pip

The easiest way to install pg4j is using pip. The name of the package on [pypi.com](https://pypi.org/project/pg4j/) is `pg4j`.

<div class="termy">
```Console
$ pip install pg4j
---> 100%
Successfully installed pg4j
```
</div>
One thing to note is that pg4j relies on a sqlalchemy's postgres dialect which uses the pyscopg2 driver. This means that postgresql-client tools must be installed on the machine installing pg4j.

On linux this can be achieved through the following command:

```Bash
brew install postgresql
```

On linux this can be achieved through the following command (note apt-get may need to be replaced by the specific linux distro's package manager):

```Bash
sudo apt-get install postgresql-client
```

## Installing using Git

```Bash
{!../docs_src/installation/git_installation.sh!}
```
