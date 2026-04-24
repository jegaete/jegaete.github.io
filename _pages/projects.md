---
layout: archive
title: "Proyectos de investigación"
permalink: /projects/
author_profile: true
---

{% include base_path %}

A continuación se listan los proyectos de investigación en los que he participado
como Investigador Principal (PI), Co-Investigador, Co-PI o Colaborador, desde
2009 hasta la fecha. En total son {{ site.projects | size }} proyectos.

## Proyectos activos

<ul>
{% assign active_projects = site.projects | where: "status", "active" | sort: "project_number" %}
{% for post in active_projects %}
  {% include archive-single.html %}
{% endfor %}
</ul>

## Proyectos finalizados

<ul>
{% assign finished_projects = site.projects | where: "status", "finished" | sort: "project_number" %}
{% for post in finished_projects %}
  {% include archive-single.html %}
{% endfor %}
</ul>
