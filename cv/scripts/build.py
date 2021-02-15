#!/usr/bin/env python3

import os
import urllib.parse as up
from typing import Dict, Type, List, Optional

import click
import jinja2
import pydantic
import yaml


class Contact(pydantic.BaseModel):
    id: str

    def __str__(self):
        url = self.url()
        if url:
            return f'[{self.title()}]({url})'
        return self.title()

    def title(self) -> str:
        return self.id

    def url(self) -> Optional[str]:
        raise NotImplementedError


class URLTitleMixin:
    def url(self) -> str:
        raise NotImplementedError

    def title(self) -> str:
        parts = up.urlparse(self.url())
        return f'{parts.netloc}{parts.path}'


class Linkedin(URLTitleMixin, Contact):
    def url(self) -> Optional[str]:
        return f"https://linkedin.com/in/{self.id}"


class Github(URLTitleMixin, Contact):
    def url(self) -> Optional[str]:
        return f"https://github.com/{self.id}"


class Skype(URLTitleMixin, Contact):

    def title(self) -> str:
        return f"Skype: {self.id}"

    def url(self) -> Optional[str]:
        return f"skype:{self.id}?add"


class Email(Contact):
    def url(self) -> Optional[str]:
        return f"mailto:{self.id}"


class Location(Contact):

    def url(self) -> Optional[str]:
        return None


CONTACT_CLASSES: Dict[str, Type[Contact]] = {
    "email": Email,
    "skype": Skype,
    "linkedin": Linkedin,
    "github": Github,
    "location": Location,
}


class Entry(pydantic.BaseModel):
    title: pydantic.StrictStr
    subtitle: pydantic.StrictStr
    rtitle: pydantic.StrictStr = ""
    rsubtitle: pydantic.StrictStr = ""
    description: List[str]


class Section(pydantic.BaseModel):
    title: pydantic.StrictStr
    entries: List[Entry]


class CV(pydantic.BaseModel):
    name: pydantic.StrictStr
    summary: pydantic.StrictStr
    contacts: Dict[str, Contact]
    sections: List[Section]

    @pydantic.validator("contacts", pre=True)
    def _init_contacts(cls, data: Dict[str, str]) -> Dict[str, Type[Contact]]:
        return {key: CONTACT_CLASSES[key](id=id_) for key, id_ in data.items()}

    @property
    def first_name(self) -> str:
        return self.name.split()[0]

    @property
    def last_name(self) -> str:
        return self.name.split()[1]

    @property
    def contacts_line(self) -> List[Contact]:
        return [
            contact for key in ('location', 'email', 'skype', 'github', 'linkedin')
            if (contact := self.contacts.get(key)) is not None
        ]


@click.group()
def cli():
    pass


@cli.command("markdown")
@click.option("-i", "input_file", required=True, type=click.File("r"))
@click.option("-o", "output_file", required=True, type=click.File("w"))
@click.option("-t", "template_file", required=True, type=click.File("r"))
def main(input_file, output_file, template_file) -> int:
    raw = yaml.safe_load(input_file)
    data = CV.validate(raw)
    tpl_src = template_file.read()

    env = jinja2.Environment(
        keep_trailing_newline=True,
        trim_blocks=True,
        lstrip_blocks=True,
    )
    tpl = env.from_string(tpl_src)

    base_name, _ = os.path.splitext(output_file.name)
    output_file.write(tpl.render(data=data, base_name=base_name))

    return 0


if __name__ == "__main__":
    cli()
