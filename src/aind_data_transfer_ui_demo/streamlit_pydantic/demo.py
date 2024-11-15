import streamlit as st
import streamlit_pydantic as sp
from aind_data_transfer_models.core import (
    BasicUploadJobConfigs,
    ModalityConfigs,
    SubmitJobRequest,
)

from aind_data_transfer_ui_demo.models.modality_configs import ModalityConfigsStreamlit, ModalityConfigsFastUI
from aind_data_transfer_ui_demo.models.basic_upload_job_configs import BasicUploadJobConfigsStreamlit, BasicUploadJobConfigsFastUI, BasicUploadJobConfigsSimple
from aind_data_transfer_ui_demo.models.submit_job_request import SubmitJobRequestStreamlit, SubmitJobRequestFastUI, SubmitJobRequestSimple

# streamlit allows UI to group "optional" parameters into an expander
# this doesn't actually allow Optional type, just ones with default set already

# ___Streamlit models additionally remove optional fields but can render lists


# top level tabs
top_level_tabs = st.tabs(["Modality Configs", "Basic Upload Job Configs", "Submit Job Request"])

with top_level_tabs[0]:
    st.header("Modality Configs")
    modality_configs_tabs = st.tabs(['streamlit', 'fast_ui', 'full'])

    with modality_configs_tabs[0]:
        data = sp.pydantic_input(
            key="ModalityConfigsStreamlit",
            model=ModalityConfigsStreamlit,
            group_optional_fields="expander",
        )
        if data:
            st.json(data)
    
    with modality_configs_tabs[1]:
        data = sp.pydantic_input(
            key="ModalityConfigsFastUI",
            model=ModalityConfigsFastUI,
            group_optional_fields="expander",
        )
        if data:
            st.json(data)
    
    with modality_configs_tabs[2]:
        data = sp.pydantic_input(
            key="ModalityConfigs",
            model=ModalityConfigs,
            group_optional_fields="expander",
        )
        if data:
            st.json(data)

with top_level_tabs[1]:
    st.header("Basic Upload Job Configs")
    basic_upload_job_configs_tabs = st.tabs(['streamlit', 'fast_ui', 'simple','full'])

    with basic_upload_job_configs_tabs[0]:
        data = sp.pydantic_input(
            key="BasicUploadJobConfigsStreamlit",
            model=BasicUploadJobConfigsStreamlit,
            group_optional_fields="expander",
        )
        if data:
            st.json(data)

    with basic_upload_job_configs_tabs[1]:
        data = sp.pydantic_input(
            key="BasicUploadJobConfigsFastUI",
            model=BasicUploadJobConfigsFastUI,
            group_optional_fields="expander",
        )
        if data:
            st.json(data)
    
    with basic_upload_job_configs_tabs[2]:
        data = sp.pydantic_input(
            key="BasicUploadJobConfigsSimple",
            model=BasicUploadJobConfigsSimple,
            group_optional_fields="expander",
        )
        if data:
            st.json(data)
    
    with basic_upload_job_configs_tabs[3]:
        data = sp.pydantic_input(
            key="BasicUploadJobConfigs",
            model=BasicUploadJobConfigs,
            group_optional_fields="expander",
        )
        if data:
            st.json(data)

with top_level_tabs[2]:
    st.header("Submit Job Request")
    submit_job_request_tabs =  st.tabs(['streamlit', 'fast_ui', 'simple','full'])

    with submit_job_request_tabs[0]:
        data = sp.pydantic_input(
            key="SubmitJobRequestStreamlit",
            model=SubmitJobRequestStreamlit,
            group_optional_fields="expander",
        )
        if data:
            st.json(data)

    with submit_job_request_tabs[1]:
        data = sp.pydantic_input(
            key="SubmitJobRequestFastUI",
            model=SubmitJobRequestFastUI,
            group_optional_fields="expander",
        )
        if data:
            st.json(data)

    with submit_job_request_tabs[2]:
        data = sp.pydantic_input(
            key="SubmitJobRequestSimple",
            model=SubmitJobRequestSimple,
            group_optional_fields="expander",
        )
        if data:
            st.json(data)

    with submit_job_request_tabs[3]:
        data = sp.pydantic_input(
            key="SubmitJobRequest",
            model=SubmitJobRequest,
            group_optional_fields="expander",
        )
        if data:
            st.json(data)