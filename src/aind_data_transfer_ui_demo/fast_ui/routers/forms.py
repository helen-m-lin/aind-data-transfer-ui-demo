from collections import defaultdict
from typing import Annotated, Literal, TypeAlias

import requests
from fastapi import APIRouter, Request
from fastui import AnyComponent, FastUI
from fastui import components as c
from fastui.events import PageEvent
from fastui.forms import SelectSearchResponse, fastui_form
from aind_data_transfer_ui_demo.fast_ui.shared import page
from aind_data_transfer_ui_demo.models.simple import LoginForm, SelectForm


## FORMS #######################
router = APIRouter()
FormType: TypeAlias = Literal[
    'login', 'select',
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
        case _:
            raise ValueError(f'Unknown form form_type: {form_type}')

# Submit actions for each form
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

def display_submitted_form_data(form_json: str, extra_json=None) -> list[AnyComponent]:
    """Displays the submitted form data back to user"""
    return [
        c.Paragraph(text=f'Submitted form content!'),
        c.Heading(text='Form Data:', level=3),
        c.Code(language='json', text=form_json),
        c.Code(language='json', text=extra_json or ''),
    ]