## A brief instruction for running the application.

In the attached archive, you can see two .py files. app.py is the program for binary annotation, and app_multiclass.py is for insect species annotation.


### To run the application, you need to:

1. Install the Streamlit library using:
    ```sh
    pip install streamlit
    ```
2. Start the application using the command:
    ```sh
    streamlit run <your_relative_path_to_app_multiclass.py>
    ```

    In my case, the command is:
    ```sh
    streamlit run TER2/data_app/app_multiclass.py
    ```

3. After launching the application, you need to specify the relative path to the folder with images and the path where the output file will be saved. In my case, it looks like this:

![Alt text](image.png)

4. Select the insect class. I have also added a back button to allow you to return to the previous image in case of an error.

![Alt text](image-1.png)

P.S. Some images may be too large and not fit on the web page along with the buttons. In my case, I reduced the page size to 50% on my monitor, and everything fit