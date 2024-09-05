import streamlit as st
import os
import glob
import json

from datetime import datetime

now = datetime.now()

current_time_str = now.strftime("%Y-%m-%d %H:%M:%S")

class_mapper = {'Rien': 0,
 'mellifera': 1,
 'Fourmis': 2,
 'Coleoptere': 3,
 'Petite abeille sauvage': 4,
 'Bourdon': 5,
 'Syrphe': 6,
 'Chenille': 7, 
 'Indéterminable': 8}

reversed_mapper = {class_mapper[k]:k for k in class_mapper}


def seconds_to_hms(seconds):

    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    
    return f"{hours:02}:{minutes:02}:{secs:02}"

def show_photos(main_directory, output_path):
    subdirs = [os.path.join(main_directory, o) for o in os.listdir(main_directory) if os.path.isdir(os.path.join(main_directory, o))]
    all_images = []
    for subdir in subdirs:
        images = glob.glob(os.path.join(subdir, '*.jpg')) + glob.glob(os.path.join(subdir, '*.png'))
        all_images.extend(images)

    if 'photo_index' not in st.session_state:
        st.session_state.photo_index = 0

    if 'user_responses' not in st.session_state:
        st.session_state.user_responses = {}

    if st.session_state.photo_index < len(all_images):

        

        img_path = all_images[st.session_state.photo_index]
        img_name = os.path.basename(img_path)

        st.header(f"le modele voit: {img_name.split('_')[-3]} a l'instant: {seconds_to_hms(int(img_name.split('_')[-1][:-4]))}")

        st.image(img_path, caption=img_name, use_column_width=True)

        # Layout for 3x3 button grid
        button_labels = [str(i) for i in range(9)]

        

        if st.button('prédiction correcte', key='button_correct'):
            st.session_state.user_responses[img_name] = class_mapper[img_name.split('_')[-3]]
            st.session_state.photo_index += 1
            st.rerun() # st.experimental_rerun()

        cols = st.columns(3)

        for i in range(3):
            for j in range(3):
                button_index = i * 3 + j
                if cols[j].button(reversed_mapper[button_index], key=f'button_{button_labels[button_index]}'):
                    st.session_state.user_responses[img_name] = button_labels[button_index]
                    st.session_state.photo_index += 1
                    st.rerun()

        if st.button('Back', key='back_button') and st.session_state.photo_index > 0:
            st.session_state.photo_index -= 1
            st.rerun()
    else:
        st.write("All photos reviewed!")
        inp_dir = st.session_state['selected_dir'].split('/')[-1]
        obs_nom = st.session_state['observateur_nom']
        path2json = f'responses_{inp_dir}_{current_time_str}_{obs_nom}.json'

        st.download_button(
              label="Download results",
              data=st.session_state.user_responses,
              file_name=path2json,
              mime='text/json',
        )
        with open(os.path.join(output_path, path2json), 'w') as json_file:
            json.dump(st.session_state.user_responses, json_file)
        st.write(f"Responses saved to {path2json}")

     

st.title("Image Annotation App")

if 'page' not in st.session_state:
    st.session_state.page = "Home"

page = st.session_state.page

if page == "Home":
    st.header("Select input and output paths")

    observateur_nom = st.text_input("What is your name?:")
    main_dir = st.text_input("Path to Main Directory")
    output_path = st.text_input("Path to output file")
    if st.button("Selected"):
        st.session_state['selected_dir'] = main_dir
        st.session_state['observateur_nom'] = observateur_nom
        st.session_state['output_path'] = output_path
        st.session_state.photo_index = 0
        st.session_state.page = "Positive - an insect is present on the flower, Negative - no insect is present"
        st.rerun()

if page == "Positive - an insect is present on the flower, Negative - no insect is present":
    if 'selected_dir' in st.session_state and os.path.isdir(st.session_state['selected_dir']):
        show_photos(st.session_state['selected_dir'], st.session_state['output_path'])
    else:
        st.write("Please select a valid main directory on the Home page.")

st.sidebar.header("Results")
if st.sidebar.button("Show Results"):
    st.sidebar.write(st.session_state.get('user_responses', {}))

st.markdown("""
    <style>
    div.stButton > button {
        font-size: 20px;
        padding: 10px 20px;
        width: 100%; 
        height: 60px;
    }
    </style>
""", unsafe_allow_html=True)

st.components.v1.html("""
    <script>
    document.addEventListener('keydown', function(event) {
        const key = event.key;
        if (key >= '1' && key <= '9') {
            const button = document.querySelector(`button[aria-label='button_${key}']`);
            if (button) {
                button.click();
            }
        }
    });
    </script>
""", height=0)
