# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
    """
    Choose the fruits you want in your custom smoothie
    """
)


def get_snowflake_session():
    snowflake_config = st.secrets.get("snowflake", {})
    if not snowflake_config:
        st.error(
            "Snowflake connection is not configured. "
            "Add your connection details under [snowflake] in `.streamlit/secrets.toml` "
            "or configure them via Streamlit secrets/environment variables."
        )
        st.stop()

    try:
        cnx = st.connection("snowflake", **snowflake_config)
        return cnx.session()
    except Exception as err:
        st.error(f"Unable to connect to Snowflake: {err}")
        st.stop()


session = get_snowflake_session()
fruit_df = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"))
fruit_list = [row["FRUIT_NAME"] for row in fruit_df.collect()]

name_on_order = st.text_input("Name on smoothie:")
st.write("Name on your smoothie will be:")
st.write(name_on_order)

ingredients_list = st.multiselect(
    "Choose up to 5 fruits",
    fruit_list,
    max_selections=5,
)

if ingredients_list:
    ingredients_string = " ".join(ingredients_list)

    my_insert_stmt = (
        "insert into smoothies.public.orders (ingredients, name_on_order) "
        "values ('" + ingredients_string + "', '" + name_on_order + "')"
    )

    time_to_insert = st.button("Submit Order")
    if time_to_insert:
        try:
            session.sql(my_insert_stmt).collect()
            st.success("Your Smoothie is ordered!", icon="✅")
        except Exception as err:
            st.error(f"Failed to submit order: {err}")

        
