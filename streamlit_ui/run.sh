#!/bin/bash

# Run application under streamlit server
export STREAMLIT_SERVER_MAX_UPLOAD_SIZE=5000
export STREAMLIT_SSL_CONNECTION=0
export STREAMLIT_RUN_SERVER_LOCALHOST=0

export SHOW_LOGIN_WINDOW=1


# Run application
~/.local/bin/streamlit run app.py --server.port 8502
