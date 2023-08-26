import streamlit as st
from bardapi import Bard
import time
import re
import os
from dotenv import load_dotenv 

token = st.secrets["token"]



bard = Bard(token=token,  timeout = 60)

# methods

def search_params(filename, restaurant_name, location_name):
    content = st.secrets["prompt"]
    content = content.replace('{restaurant}', restaurant_name)
    content = content.replace('{location}', location_name)
    
    return content


def create_second_prompt(filename, initial_output):
    content = st.secrets["filterprompt"]
    content = content.replace('{intial_output}', initial_output)

    return content



# Streamlit

st.title("Restaurant Reviewer")
st.write("Enter a restaurant and a location to get a review.")

restaurant_name = st.text_input("Restaurant name:")
location_name = st.text_input("Location name:")

if st.button("Generate Review"):
    
    #first call
    prompt = search_params('prompt.txt', restaurant_name, location_name)
    initial_result = bard.get_answer(prompt)['content']
    
    time.sleep(10)
    
    # second call
    secondary_prompt = create_second_prompt('filterprompt.txt', initial_result)  
    
    time.sleep(10)
    final_result = bard.get_answer(secondary_prompt)['content']
    
    time.sleep(10)
    
    
    final_result = re.sub(r"^.*?(\*\*Overview\*\*)", r"\1", final_result, flags=re.DOTALL).strip()

    st.markdown(final_result)


