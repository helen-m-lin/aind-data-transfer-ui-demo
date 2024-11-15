from collections import defaultdict
from typing import Annotated, Literal, TypeAlias

import requests
from aind_data_transfer_models.core import (
    BasicUploadJobConfigs,
    SubmitJobRequest,
)
from fastapi import APIRouter, Request
from fastui import AnyComponent, FastUI
from fastui import components as c
from fastui.events import GoToEvent, PageEvent
from fastui.forms import SelectSearchResponse, fastui_form

from aind_data_transfer_ui_demo.fast_ui.shared import page
from aind_data_transfer_ui_demo.models.simple import LoginForm, SelectForm
from aind_data_transfer_ui_demo.models.modality_configs import ModalityConfigsFastUI
from aind_data_transfer_ui_demo.models.basic_upload_job_configs import BasicUploadJobConfigsFastUI
from aind_data_transfer_ui_demo.models.submit_job_request import SubmitJobRequestFastUI

## FORMS #######################
router = APIRouter()
FormType: TypeAlias = Literal[
    'login', 'select',
    # Attempt to render trimmed versions
    'ModalityConfigsFastUI',
    'BasicUploadJobConfigsFastUI', 'SubmitJobRequestFastUI',
    # Attempt to render full versions (unchanged from aind-data-transfer-models)
    'BasicUploadJobConfigs', 'SubmitJobRequest',
]

@router.get('/search', response_model=SelectSearchResponse)
async def search_view(request: Request, q: str) -> SelectSearchResponse:
    path_ends = f'name/{q}' if q else 'all'
    r = requests.get(
        url=f'https://restcountries.com/v3.1/{path_ends}',
    )
    if r.status_code == 404:
        options = []
    else:
        r.raise_for_status()
        data = r.json()
        if path_ends == 'all':
            # if we got all, filter to the 20 most populous countries
            data.sort(key=lambda x: x['population'], reverse=True)
            data = data[0:20]
            data.sort(key=lambda x: x['name']['common'])

        regions = defaultdict(list)
        for co in data:
            regions[co['region']].append({'value': co['cca3'], 'label': co['name']['common']})
        options = [{'label': k, 'options': v} for k, v in regions.items()]
    return SelectSearchResponse(options=options)

@router.get('/{form_type}', response_model=FastUI, response_model_exclude_none=True)
def forms_view(form_type: FormType) -> list[AnyComponent]:
    """Display the forms page as a tabbed view.
    """
    print(form_type)
    return page(
        c.LinkList(
            links=[
                c.Link(
                    components=[c.Text(text='Login Form')],
                    on_click=PageEvent(name='change-form', push_path='/forms/login', context={'form_type': 'login'}),
                    active='/forms/login',
                ),
                c.Link(
                    components=[c.Text(text='Select Form')],
                    on_click=PageEvent(name='change-form', push_path='/forms/select', context={'form_type': 'select'}),
                    active='/forms/select',
                ),
                # Attempt to render trimmed versions
                c.Link(
                    components=[c.Text(text='ModalityConfigsFastUI (min)')],
                    on_click=PageEvent(name='change-form', push_path='/forms/ModalityConfigsFastUI', context={'form_type': 'ModalityConfigsFastUI'}),
                    active='/forms/ModalityConfigsFastUI',
                ),
                c.Link(
                    components=[c.Text(text='BasicUploadJobConfigs (min)')],
                    on_click=PageEvent(name='change-form', push_path='/forms/BasicUploadJobConfigsFastUI', context={'form_type': 'BasicUploadJobConfigsFastUI'}),
                    active='/forms/BasicUploadJobConfigsFastUI',
                ),
                c.Link(
                    components=[c.Text(text='SubmitJobRequest (min)')],
                    on_click=PageEvent(name='change-form', push_path='/forms/SubmitJobRequestFastUI', context={'form_type': 'SubmitJobRequestFastUI'}),
                    active='/forms/SubmitJobRequestFastUI',
                ),
                # Attempt to render full versions (unchanged from aind-data-transfer-models)
                c.Link(
                    components=[c.Text(text='BasicUploadJobConfigs (full)')],
                    on_click=PageEvent(name='change-form', push_path='/forms/BasicUploadJobConfigs', context={'form_type': 'BasicUploadJobConfigs'}),
                    active='/forms/BasicUploadJobConfigs',
                ),
                c.Link(
                    components=[c.Text(text='Job Request Form (full)')],
                    on_click=PageEvent(name='change-form', push_path='/forms/SubmitJobRequest', context={'form_type': 'SubmitJobRequest'}),
                    active='/forms/SubmitJobRequest',
                ),
            ],
            mode='tabs',
            class_name='+ mb-4',
        ),
        c.ServerLoad(
            path='/forms/content/{form_type}',
            load_trigger=PageEvent(name='change-form'),
            components=form_content(form_type),
        ),
        title='Forms',
    )


@router.get('/content/{form_type}', response_model=FastUI, response_model_exclude_none=True)
def form_content(form_type: FormType):
    '''Return the form content for the given form_type.'''
    print(form_type)
    match form_type:
        case 'login':
            return [
                c.Heading(text='Login Form', level=2),
                c.Paragraph(text='Simple login form with email and password.'),
                c.ModelForm(model=LoginForm, display_mode='page', submit_url='/api/forms/login'),
            ]
        case 'select':
            return [
                c.Heading(text='Select Form', level=2),
                c.Paragraph(text='Form showing different ways of doing select.'),
                c.ModelForm(model=SelectForm, display_mode='page', submit_url='/api/forms/select'),
            ]
        # Attempt to render trimmed versions
        case 'ModalityConfigsFastUI':
            return [
                c.Heading(text='ModalityConfigs (min)', level=2),
                c.Paragraph(text='Form for creating modality configs (does not contain all fields in ModalityConfigs).'),
                c.ModelForm(model=ModalityConfigsFastUI, display_mode='page', submit_url='/api/forms/ModalityConfigsFastUI'),
            ]
        case 'BasicUploadJobConfigsFastUI':
            return [
                c.Heading(text='BasicUploadJobConfigs (min)', level=2),
                c.Paragraph(text='Form for creating basic upload job configs (does not contain all fields in BasicUploadJobConfigs).'),
                c.ModelForm(model=BasicUploadJobConfigsFastUI, display_mode='page', submit_url='/api/forms/BasicUploadJobConfigsFastUI'),
            ]
        case 'SubmitJobRequestFastUI':
            return [
                c.Heading(text='SubmitJobRequest (min)', level=2),
                c.Paragraph(text='Form for submitting a job request (does not contain all fields in SubmitJobRequest).'),
                c.ModelForm(model=SubmitJobRequestFastUI, display_mode='page', submit_url='/api/forms/SubmitJobRequestFastUI'),
            ]
        # Attempt to render full versions (unchanged from aind-data-transfer-models)
        case 'BasicUploadJobConfigs':
            return [
                c.Heading(text='BasicUploadJobConfigs (full)', level=2),
                c.Paragraph(text='Full model from aind-data-transfer-models.'),
                c.ModelForm(model=BasicUploadJobConfigs, display_mode='page', submit_url='/api/forms/BasicUploadJobConfigs'),
            ]
        case 'SubmitJobRequest':
            return [
                c.Heading(text='SubmitJobRequest (full)', level=2),
                c.Paragraph(text='Full model from aind-data-transfer-models.'),
                c.ModelForm(model=SubmitJobRequest, display_mode='page', submit_url='/api/forms/SubmitJobRequest'),
            ]
        case _:
            raise ValueError(f'Unknown form form_type: {form_type}')

# POST METHODS for Submit actions for each form ############################
@router.post('/login', response_model=FastUI, response_model_exclude_none=True)
async def login_form_post(form: Annotated[LoginForm, fastui_form(LoginForm)]):
    print(form)
    form_json = form.model_dump_json( indent=3)
    return display_submitted_form_data(form_json)

@router.post('/select', response_model=FastUI, response_model_exclude_none=True)
async def select_form_post(form: Annotated[SelectForm, fastui_form(SelectForm)]):
    print(form)
    form_json = form.model_dump_json( indent=3)
    return display_submitted_form_data(form_json)

# Attempt to submit trimmed versions (validates with full version from aind-data-transfer-models)
@router.post('/ModalityConfigsFastUI', response_model=FastUI, response_model_exclude_none=True)
async def modality_configs_fast_ui_form_post(form: Annotated[ModalityConfigsFastUI, fastui_form(ModalityConfigsFastUI)]):
    form_json = form.model_dump_json(indent=3)
    submit_json = None
    try:
        submit_json = form.process_and_validate_form_data()
    except Exception as e:
        print(repr(e))
    return display_submitted_form_data(form_json, submit_json)

@router.post('/BasicUploadJobConfigsFastUI', response_model=FastUI, response_model_exclude_none=True)
async def basic_upload_job_configs_fast_ui_form_post(form: Annotated[BasicUploadJobConfigsFastUI, fastui_form(BasicUploadJobConfigsFastUI)]):
    form_json = form.model_dump_json(indent=3)
    submit_json = None
    try:
        submit_json = form.process_and_validate_form_data()
    except Exception as e:
        print(repr(e))
    return display_submitted_form_data(form_json, submit_json)

@router.post('/SubmitJobRequestFastUI', response_model=FastUI, response_model_exclude_none=True)
async def submit_job_request_fast_ui_form_post(form: Annotated[SubmitJobRequestFastUI, fastui_form(SubmitJobRequestFastUI)]):
    form_json = form.model_dump_json(indent=3)
    submit_json = None
    try:
        submit_json = form.process_and_validate_form_data()
    except Exception as e:
        print(repr(e))
    return display_submitted_form_data(form_json, submit_json)

# Attempt to submit full versions (unchanged from aind-data-transfer-models)
@router.post('/BasicUploadJobConfigs', response_model=FastUI, response_model_exclude_none=True)
async def basic_upload_job_configs_form_post(form: Annotated[BasicUploadJobConfigs, fastui_form(BasicUploadJobConfigs)]):
    print(form)
    form_json = form.model_dump_json(indent=3)
    return display_submitted_form_data(form_json)

@router.post('/SubmitJobRequest', response_model=FastUI, response_model_exclude_none=True)
async def submit_job_request_form_post(form: Annotated[SubmitJobRequest, fastui_form(SubmitJobRequest)]):
    print(form)
    form_json = form.model_dump_json(indent=3)
    return display_submitted_form_data(form_json)

# Helper methods ###########################################################
def display_submitted_form_data(form_json: str, submit_json=None) -> list[AnyComponent]:
    """Displays the submitted form data back to user"""
    components = [
        c.Paragraph(text=f'Submitted form content!'),
        c.Heading(text='Form data:', level=3),
        c.Code(language='json', text=form_json),
    ]
    if submit_json is not None:
        components.extend([
            c.Heading(text='Submit to server (validated using aind-data-transfer-models):', level=3),
            c.Code(language='json', text=submit_json),
            # TODO: submit to aind-data-transfer-service
            c.Button(text='Submit', on_click=GoToEvent(url='/')),
        ])
    return components