Very small library for parsing AppEngine keys as urlsafes when outside the 
AppEngine env.

This was forked from the implementations that were spread out accross multiple
projects in the big `geekie` repository, and it is meant to be used like this

```lang=py
from glibs.ndbkeyparser import ndb


x = ndb.Key(urlsafe="ffafdasfadsfasdfasfas")
x.id()

# or, the reverse way

x = ndb.key("Kind", <id>)
x.urlsafe()
```
