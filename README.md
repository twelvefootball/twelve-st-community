
Twelve Visulisations in Streamlit
=================================

This is a set of tools for making Twelve visulaisations in Streamlit. We ask that when you use his tool, you acknowledge
the usage by leaving the Twelve logo on your visualisations
and follow the style as much as possible.

### Instructions

This is part of the Soccermatics Pro course. Please see

https://soccermatics.readthedocs.io/en/latest/lesson10/Streamlit.html

for instructions.

### Installation and usage.

You should then create a Python environment by first going in to Anaconda and opening a terminal. Then chnage directory to the *twelve-st-community* folder. And set up an environment by running:

    conda create --name streamlit_env
    conda activate streamlit_env
    conda install pip
    pip install -r requirements.txt

Now if you run

    streamlit run app.py

The app will appear.

### Twelve credentials

This Streamlit App won't work unless you have credentials for the Twelve API. We provide this access to people on the Soccermatics Pro course only. If you work for a football club and would like to trial this then please [contact us](mailto:hello@twelve.football).

You then need to make a folder called *.streamlit* and a file *secrets.toml* which contains the text

    TWELVE_USERNAME = PROVIDED TO YOU
    TWELVE_PASSWORD = PROVIDED TO YOU
    TWELVE_API = "https://api.twelve.football"
    TWELVE_BLOB = "https://twelve.blob.core.windows.net"

Having this access will allow you to build apps which run online directly through the Twelve API. We will soon publish details of how to do this.



