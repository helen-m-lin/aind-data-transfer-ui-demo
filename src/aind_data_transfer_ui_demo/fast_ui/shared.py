from fastui import AnyComponent
from fastui import components as c
from fastui.events import GoToEvent

# global configs/variables
APP_TITLE = "AIND Data Transfer Service"
APP_READTHEDOCS_URL = "https://aind-data-transfer-service.readthedocs.io"
APP_GITHUB_URL = (
    "https://github.com/AllenNeuralDynamics/aind-data-transfer-service"
)
AIND_METADATA_SERVICE_PROJECT_NAMES_URL = "http://aind-metadata-service/project_names"


def page(
    *components: AnyComponent, title: str | None = None
) -> list[AnyComponent]:
    """
    Displays a page that contains the provided components, along with the shared
    title, navbar, and footer.
    """
    # Render the shared components
    title_component = c.PageTitle(
        text=f"{APP_TITLE} — {title}" if title else APP_TITLE
    )
    navbar_component = c.Navbar(
        title=APP_TITLE,
        title_event=GoToEvent(url="/"),
        start_links=[
            c.Link(
                components=[c.Text(text="Submit Jobs")],
                # default to an option
                on_click=GoToEvent(url="/forms/login"),
                active="startswith:/forms",
            ),
            c.Link(
                components=[c.Text(text="Job Status")],
                on_click=GoToEvent(url="/users"),
                active="startswith:/users",
            ),
            c.Link(
                components=[c.Text(text="Job Submit Template")],
                on_click=GoToEvent(
                    url="/api/job_upload_template",
                    target="_blank",
                ),
            ),
            c.Link(
                components=[c.Text(text="Project Names")],
                on_click=GoToEvent(
                    url=AIND_METADATA_SERVICE_PROJECT_NAMES_URL,
                    target="_blank",
                ),
            ),
        ],
        end_links=[
            c.Link(
                components=[c.Text(text="Help")],
                on_click=GoToEvent(
                    url=APP_READTHEDOCS_URL,
                    target="_blank",
                ),
            ),
            c.Link(
                components=[c.Text(text="API Docs")],
                on_click=GoToEvent(
                    url="/docs",
                    target="_blank",
                ),
            ),
        ],
    )
    footer = c.Footer(
        extra_text=APP_TITLE,
        links=[
            c.Link(
                components=[c.Text(text="github")],
                on_click=GoToEvent(
                    url=APP_GITHUB_URL,
                    target="_blank",
                ),
            ),
            c.Link(
                components=[c.Text(text="readthedocs")],
                on_click=GoToEvent(
                    url=APP_READTHEDOCS_URL,
                    target="_blank",
                ),
            ),
        ],
    )
    # Render the page contents
    page_component = c.Page(
        components=[
            *((c.Heading(text=title),) if title else ()),
            *components,
        ],
    )
    return [title_component, navbar_component, page_component, footer]
