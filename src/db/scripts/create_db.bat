echo on
title testing sql connection for PADification
:: hope this works.

PAUSE

SQLCMD -E -dmaster -i.\Generate-PADification-DB.sql
PAUSE
