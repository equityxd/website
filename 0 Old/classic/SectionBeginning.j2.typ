== {{section_title}}
{% if entry_type in ["TextEntry", "EducationEntry", "ExperienceEntry"] %}
#grid(
  columns: (auto, auto),
  column-gutter: 2.5cm,
  align: top,
{% elif entry_type == "ReversedNumberedEntry" %}

#reversed-numbered-entries(
  [
{% endif %}
