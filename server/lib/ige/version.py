

major = 0
minor = 5
revision = 74
# status must be either empty string or must start with a dash
status = "-1"

assert not status or status.startswith("-"), "Status MUST start with dash if set"

version = {
    "major": major,
    "minor": minor,
    "revision": revision,
    "status": status,
}

versionString = "%(major)d.%(minor)d.%(revision)d%(status)s" % version

clientURLs = {
    "*": "https://github.com/ospaceteam/outerspace/archive/%(major)d.%(minor)d.%(revision)d%(status)s.tar.gz" % version,
}
