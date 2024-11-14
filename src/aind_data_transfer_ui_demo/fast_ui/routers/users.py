from datetime import date

from fastapi import APIRouter, HTTPException
from fastui import AnyComponent, FastUI
from fastui import components as c
from fastui.components.display import DisplayLookup, DisplayMode
from fastui.events import BackEvent, GoToEvent
from pydantic import BaseModel, Field

from aind_data_transfer_ui_demo.fast_ui.shared import page

router = APIRouter()


class User(BaseModel):
    id: int
    name: str
    dob: date = Field(title="Date of Birth")


# define some users
users = [
    User(id=1, name="John", dob=date(1990, 1, 1)),
    User(id=2, name="Jack", dob=date(1991, 1, 1)),
    User(id=3, name="Jill", dob=date(1992, 1, 1)),
    User(id=4, name="Jane", dob=date(1993, 1, 1)),
]


@router.get("", response_model=FastUI, response_model_exclude_none=True)
def users_table_page() -> list[AnyComponent]:
    """
    Users table page, the frontend will fetch this when the user visits `/users`.
    Connects to /users/{id}/ when a user clicks on a user's name.
    """
    print("users_table")
    return page(
        c.Table(
            data=users,
            # define two columns for the table
            columns=[
                # the first is the users, name rendered as a link to their profile
                DisplayLookup(
                    field="name", on_click=GoToEvent(url="/users/{id}/")
                ),
                # the second is the date of birth, rendered as a date
                DisplayLookup(field="dob", mode=DisplayMode.date),
            ],
        ),
        title="Users",
    )


@router.get(
    "/{user_id}/", response_model=FastUI, response_model_exclude_none=True
)
def user_profile_page(user_id: int) -> list[AnyComponent]:
    """
    User profile page, the frontend will fetch this when the user visits `/users/{id}/`.
    """
    try:
        user = next(u for u in users if u.id == user_id)
    except StopIteration:
        raise HTTPException(status_code=404, detail="User not found")
    return page(
        c.Link(components=[c.Text(text="Back")], on_click=BackEvent()),
        c.Details(data=user),
        title=f"User Profile: {user.name}",
    )
