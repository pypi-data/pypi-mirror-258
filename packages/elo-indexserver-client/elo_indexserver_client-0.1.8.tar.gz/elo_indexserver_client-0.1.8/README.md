# ELO indexserver client

Developed by [Treskon GmbH](https://treskon.at/) published on PyPI: https://pypi.org/project/elo-indexserver-client/

A client library for accessing Indexserver component of [ELO Digital Office GmbH](https://www.elo.com/de-at.html) via
REST API.

## Installation

```bash
pip install elo-indexserver-client
```

## Usage

First, init the Service with the baseurl, user and password of the Indexserver REST API.

```python
from eloservice.elo_service import EloService

rest_baseurl = "http://localhost::6056/ix-Archive/rest/"
rest_user = "elo"
rest_password = "elo"
elo_service = EloService(url=rest_baseurl, user=rest_user, password=rest_password)
```

Then you can use the service to access the Index server REST API.
Here are often examples:

```python
# Create Folder 
folder_id = elo_service.create_folder(path="¶Foodplaces", separator="¶")
# upload_file
file_id = elo_service.upload_file(sord_id=folder_id, file_path="test.jpg", file_name="ichiran_ramen.jpg")
# overwrite_mask_fields
elo_service.overwrite_mask_fields(sord_id=file_id, mask_name="Images", metadata={
    "LATITUDE": "35.73258119685775",
    "LONGITUDE": "139.71412884357233",
    "ITEMDOCDATE": "2023-12-26"
})
# search
search_result = elo_service.search(search_mask_fields={"LATITUDE": "35.73258119685775"}, max_results=1)
print(f"sordID of the found file: {search_result[0]}")
```

For more information visit the [Documentation](https://install.portrait.app/elo-indexserver-client/html/) or see the
docstrings in the code.

## License

Copyright 2024 Treskon GmbH

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.