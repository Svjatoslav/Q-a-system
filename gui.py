import streamlit as st
import requests
from SQlite.sqlite import *
from SQlite.vector_dbs import *
from urllib.parse import unquote
st.title("Q-A system")
from transliterate import translit
# with st.echo("below"):



def main():

    menu = ["Login", "SignUp"]
    choice = st.sidebar.selectbox("Menu", menu)


    if choice == "Login":


        username = st.sidebar.text_input("User Name")
        password = st.sidebar.text_input("Password", type='password')
        if st.sidebar.checkbox("Login"):

            create_usertable()
            hashed_pswd = make_hashes(password)

            result = login_user(username, check_hashes(password, hashed_pswd))
            if result:
                dbs = get_all_user_vec_db(username)
                choice = st.sidebar.selectbox("Menu", dbs)
                my_form = st.form(key="form1")
                question = my_form.text_input("Введи вопрос")
                if not question:
                    question = 'none'
                answers = my_form.text_area("Введи варианты ответа", height=100)
                if not answers:
                    answers = 'none'
                submit = my_form.form_submit_button('Submit')
                if submit:
                    params = {'question': question,
                              'answers': answers,
                              'choice': choice,
                              'username': username}
                    response = requests.post('http://127.0.0.1:8000/getanswer', params=params).json()
                    print(response)
                    st.write(f'Правильный ответ: {response[0]}')
                    # st.markdown(f'**Отрывок на основе которого дан ответ**\n: {response[1]["page_content"]}')

                selected_class = st.selectbox("Выбрать", ['Документ', 'Текст'])
                if selected_class == 'Документ':
                    uploaded_file = st.file_uploader("Прикрепить файл")
                    if uploaded_file is not None:
                        st.write('Отправка на бэк (заглушка)')
                        file_name = translit(uploaded_file.name, language_code='ru', reversed=True)

                        bytes_data = uploaded_file.getvalue()
                        files = {'file': bytes_data}
                        params = {'file_name':file_name, 'username': username}
                        print(requests.post('http://127.0.0.1:8000/file/upload-file', files=files, params=params).text)
                if selected_class == 'Текст':
                    my_form_text = st.form(key="form_text")
                    title = my_form_text.text_input("Введите название текста:")
                    text = my_form_text.text_area("Введите текст:")
                    params = {'content_name': title, 'content': text, 'username': username}
                    submit = my_form_text.form_submit_button('Submit')
                    if submit:
                        if title and text is not None:
                            print(requests.post('http://127.0.0.1:8000/text/upload-text', params=params).text)


            else:
                st.warning("Incorrect Username/Password")


    if choice == "SignUp":
        st.subheader("Create New Account")
        new_user = st.text_input("Username")
        new_password = st.text_input("Password", type='password')

        if st.button("Signup"):
            create_usertable()
            add_userdata(new_user, make_hashes(new_password))
            create_user_folder(new_user)
            st.success("You have successfully created a valid Account")
            st.info("Go to Login Menu to login")


def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
    if make_hashes(password) == hashed_text:
        return hashed_text
    return False


if __name__ == '__main__':
    main()
