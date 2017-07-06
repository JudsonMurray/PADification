echo on
title Drop PADification DB
:: hope this works.

PAUSE

SQLCMD -E -dmaster -i.\Drop-PADification-DB.sql
PAUSE