All internal models imports should import directly from the specific file.

```
# in counties.py

from ..notifications import Notification
```


All external imports should import from "exports" module.

```
# in undyingkingdoms/__init__.py

from models.exports import User
```

> The one exception to this is the metadata package.
> It should import directly from needed file as though it was a module in the models folder.
