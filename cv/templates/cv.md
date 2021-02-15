[Download PDF](./{{ base_name }}.pdf)

# {{ data.name }}

{{ data.summary }}

{{ data.contacts_line | join(' | ') }}

{% for section in data.sections %}
## {{ section.title }}

{% for entry in section.entries %}
**{{ entry.title }}**, {{ entry.rtitle }}{% if entry.subtitle %}\
*{{ entry.subtitle }}* {% if entry.rsubtitle %}*({{ entry.rsubtitle }})*{% endif %}{% endif %}


{% for line in entry.description %}
* {{ line | trim }}
{% endfor %}

{% endfor %}

{% endfor %}