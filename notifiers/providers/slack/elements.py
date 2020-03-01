from datetime import date
from enum import Enum
from typing import List
from typing import Union

from pydantic import constr
from pydantic import Field
from pydantic import HttpUrl
from pydantic import validator

from notifiers.models.provider import SchemaModel
from notifiers.providers.slack.common import _text_object_factory
from notifiers.providers.slack.common import SlackConfirmationDialog
from notifiers.providers.slack.common import SlackOption
from notifiers.providers.slack.common import SlackTextType


class SlackElementType(Enum):
    button = "button"
    checkboxes = "checkboxes"
    date_picker = "datepicker"
    image = "image"


class SlackBaseElementSchema(SchemaModel):
    type: SlackElementType = Field(..., description="The type of element")
    action_id: constr(max_length=255) = Field(
        ...,
        description="An identifier for this action. You can use this when you receive an interaction payload to "
        "identify the source of the action. Should be unique among all other action_ids used "
        "elsewhere by your app",
    )

    class Config:
        json_encoders = {SlackElementType: lambda v: v.value}


class SlackButtonElementStyle(Enum):
    primary = "primary"
    danger = "danger"
    default = None


class SlackButtonElement(SlackBaseElementSchema):
    """An interactive component that inserts a button.
     The button can be a trigger for anything from opening a simple link to starting a complex workflow."""

    type = SlackElementType.button
    text: _text_object_factory(type_=SlackTextType.plain_text, max_length=75)
    url: HttpUrl = Field(
        None,
        description="A URL to load in the user's browser when the button is clicked. "
        "Maximum length for this field is 3000 characters. If you're using url,"
        " you'll still receive an interaction payload and will need to send an acknowledgement response",
    )
    value: constr(max_length=2000) = Field(
        None,
        description="The value to send along with the interaction payload. "
        "Maximum length for this field is 2000 characters",
    )
    style: SlackButtonElementStyle = Field(
        None,
        description="Decorates buttons with alternative visual color schemes. Use this option with restraint",
    )
    confirm: SlackConfirmationDialog = Field(
        None,
        description="A confirm object that defines an optional confirmation dialog after the button is clicked.",
    )


class SlackCheckboxElement(SlackBaseElementSchema):
    """A checkbox group that allows a user to choose multiple items from a list of possible options"""

    type = SlackElementType.checkboxes
    options: List[SlackOption] = Field(..., description="An array of option objects")
    initial_options: List[SlackOption] = Field(
        ...,
        description="An array of option objects that exactly matches one or more of the options within options."
        " These options will be selected when the checkbox group initially loads",
    )
    confirm: SlackConfirmationDialog = Field(
        None,
        description="A confirm object that defines an optional confirmation dialog that appears after "
        "clicking one of the checkboxes in this element.",
    )


class SlackDatePickerElement(SlackBaseElementSchema):
    """An element which lets users easily select a date from a calendar style UI."""

    placeholder: _text_object_factory(
        type_=SlackTextType.plain_text, max_length=150
    ) = Field(
        None,
        description="A plain_text only text object that defines the placeholder text shown on the datepicker."
        " Maximum length for the text in this field is 150 characters",
    )
    initial_date: date = Field(
        None, description="The initial date that is selected when the element is loaded"
    )
    confirm: SlackConfirmationDialog = Field(
        None,
        description="A confirm object that defines an optional confirmation dialog that appears"
        " after a date is selected.",
    )

    @validator("initial_date")
    def format_date(cls, v: date):
        return str(v)


class SlackImageElement(SlackBaseElementSchema):
    """A plain-text summary of the image. This should not contain any markup"""

    type = SlackElementType.image
    image_url: HttpUrl = Field(..., description="The URL of the image to be displayed")
    alt_text: str = Field(
        ...,
        description="A plain-text summary of the image. This should not contain any markup",
    )


SlackElementTypes = Union[
    SlackButtonElement, SlackCheckboxElement, SlackDatePickerElement, SlackImageElement
]
