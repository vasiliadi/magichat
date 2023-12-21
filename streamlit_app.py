import streamlit as st
import random
import pandas as pd
from sqlalchemy import text

conn = st.connection("postgresql", type="sql")

try:
    pd.read_excel('db.xlsx', sheet_name='gifters').to_sql('gifters', conn.engine, index=False)
    pd.read_excel('db.xlsx', sheet_name='gifters').to_sql('resiviers', conn.engine, index=False)
    pd.read_excel('db.xlsx', sheet_name='results').to_sql('results', conn.engine, index=False)
except ValueError:
    pass

gifters = pd.read_sql_table('gifters', conn.engine)
resiviers = pd.read_sql_table('resiviers', conn.engine)
conn.engine.dispose()

st.title('Magic Hat 🎩')

name = st.selectbox(
    'Please select your name...',
    gifters['name'].sort_values(),
    index=None,
    placeholder='Please select your name...', 
    label_visibility='collapsed')

if name != None:
    st.text(f'Hi {name} 👋 ')
    st.text('Press the button to know who you are gifting to:')
    if st.button('Hocus Pocus 🪄', type='primary'):
        choice = random.choice(resiviers['name'])
        while (name == choice) or (gifters[gifters['name'] == name]['familyID'].isin(resiviers[resiviers['name'] == choice]['familyID']).iloc[0]):
            choice = random.choice(resiviers['name'])

        with conn.session as s:
            s.execute(text('DELETE FROM gifters WHERE name = :name'), {'name': name})
            s.execute(text('DELETE FROM resiviers WHERE name = :choice'), {'choice': choice})
            s.execute(text('INSERT INTO results VALUES (:result)'), {'result': f'{name} is gifting to {choice}'})
            s.commit()
            st.header(f'{name} is gifting to {choice}')

        st.balloons()
