from django.db import models

# This app is intentionally a thin composition + documentation layer only:
# it mounts each domain app's own API urls and hosts drf-spectacular's
# schema/docs views. No models belong here.
