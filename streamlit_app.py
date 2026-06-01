# Import python packages
import streamlit as st
from streamlit.errors import StreamlitSecretNotFoundError
from snowflake.snowpark.functions import col
from pathlib import Path
import requests
import pandas as pd

try:
    import tomllib
except ModuleNotFoundError:
    try:
        import tomli as tomllib  # pip install tomli
    except ModuleNotFoundError:
        tomllib = None

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
    """
    Choose the fruits you want in your custom smoothie
    """
)


def get_snowflake_session():
    try:
        snowflake_config = st.secrets.get("snowflake", {})
    except StreamlitSecretNotFoundError:
        fallback_file = Path(__file__).parent / "secrets.toml"
        if fallback_file.exists() and tomllib is not None:
            with fallback_file.open("rb") as f:
                fallback_secrets = tomllib.load(f)
            snowflake_config = fallback_secrets.get("snowflake", {})
        else:
            snowflake_config = {}

    if not snowflake_config:
        st.error(
            "Snowflake connection is not configured. "
            "Add your connection details under [snowflake] in `.streamlit/secrets.toml` "
            "or configure them via Streamlit secrets/environment variables."
        )
        st.stop()

    try:
        cnx = st.connection("", type="snowflake", **snowflake_config)
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
    ingredients_string = ''
    # ingredients_string = " ".join(ingredients_list)
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
        st.subheader(fruit_chosen +" Nutrition Infomation")
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/{search_on}")  
        # smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")  
        # st.text(smoothiefroot_response.json())
        sf_df = st.dataframe(data=smoothiefroot_response.json(),use_container_width=True)

        my_df = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"),col("SEARCH_ON"))
        pd_df = my_df.to_pandas()
        st.dataframe(pd_df)
        # st.stop()
        
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

        
