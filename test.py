import streamlit as st
def test():

    def clear_text():
        st.session_state.my_text = st.session_state.widget
        st.session_state.widget = ""

    st.text_input('Enter text here:', key='widget', on_change=clear_text)
    my_text = st.session_state.get('my_text', '')
    return my_text

