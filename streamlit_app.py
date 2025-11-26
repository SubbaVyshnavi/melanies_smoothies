# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col,when_matched
import requests
# Write directly to the app
st.title(f" :cup_with_straw: Customize Your Smoothie! :cup_with_straw: ")
st.write(
  """Choose the fruits you want in the custom Smoothie!
  """
)


title=st.text_input('Name of the title')
st.write('The name of the title is: ',title)
cnx=st.connection("snowflake")
session=cnx.session()

#session=get_active_session()
my_data=session.table("SMOOTHIES.PUBLIC.FRUIT_OPTIONS").select(col("fruit_name"))
#st.dataframe(data=my_data)
ing= st.multiselect("Choose upto 5 Fruits",my_data,max_selections=5)



if ing:
    #st.write(ing)

    #st.text(ing)

    in_str=''
    for food in ing:
        in_str += food + ' '
        st.subheader(food + "Nutrition Information")
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/"+food)
        st_df=st.dataframe(data=smoothiefroot_response.json())


    #st.write(in_str)

    ins_sta= """insert into SMOOTHIES.PUBLIC.ORDERS(name_on_order,ingredients)
    values('"""+in_str+"""','"""+title+"""')"""

    #st.write(ins_sta)
    time_but=st.button("Submit Order")

    if time_but:
        session.sql(ins_sta).collect()
        st.success("Your placed the Smoothie",icon="✅")


