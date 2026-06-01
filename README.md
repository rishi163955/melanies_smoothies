# melanies_smoothies
This is the web version of the smoothie order form.

## Snowflake configuration

This app uses a Snowflake connection, so you must configure your credentials before running it.

Create a file at `.streamlit/secrets.toml` with a Snowflake section like this:

```toml
[snowflake]
account = "<your_account>"
user = "<your_user>"
password = "<your_password>"
warehouse = "<your_warehouse>"
database = "<your_database>"
schema = "public"
role = "<your_role>"
```

Then run:

```bash
streamlit run streamlit_app.py
```

> Do not commit your real credentials to source control.
