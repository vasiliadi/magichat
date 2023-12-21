# Magic Hat for Secret Santa

## Initial members

`db.xlsx` used for initial databese creation. \
You **need to edit** with your participants. \
You can edit **only yellow rows**. \
If you want to gift family member or all participants from different families just type for all differeft number in `family` column.

## PostgreSQL configuration

Edit `secrets.toml` in `.streamlit` folder and modify with your data.

Example of config:

```
[connections.postgresql]
dialect = "postgresql"
host = "xxxxxx"
port = "5432"
database = "xxxxxx"
username = "xxxxxx"
password = "xxxxxx"
```

where `host`, `port`, `database`, `username` and `password` replace with yours.

Free PostgreSQL nodes avalible on
[neon.tech](https://neon.tech/) or [elephantsql.com](https://www.elephantsql.com/) or wherever you want.

## Deploy

To deploy you need [streamlit.io](https://streamlit.io/) account and your own [github.com](https://github.com/) repository. Just fork it and replace `db.xlsx` and `secrets.toml` with you own.