---
layout: archive
title: "Proyectos de Investigación"
permalink: /projects/
author_profile: true
---

{% include base_path %}

<style>
.proj-year-section { margin-bottom: 2rem; }
.proj-year-header {
  font-size: 1rem;
  font-weight: 700;
  color: #444;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  border-bottom: 2px solid #e0e0e0;
  padding-bottom: 0.4rem;
  margin-bottom: 1.2rem;
  margin-top: 0.5rem;
}
.proj-item {
  margin-bottom: 1.1rem;
  padding-bottom: 1.1rem;
  border-bottom: 1px solid #f2f2f2;
  line-height: 1.5;
}
.proj-item:last-child { border-bottom: none; }
.proj-title {
  font-size: 0.85rem;
  font-weight: 600;
  color: #222;
  margin-bottom: 0.2rem;
}
.proj-meta {
  font-size: 0.80rem;
  color: #555;
  font-style: italic;
  margin-bottom: 0.05rem;
}
.proj-role {
  font-size: 0.78rem;
  color: #888;
}
.proj-status-active {
  display: inline-block;
  font-size: 0.68rem;
  font-weight: 600;
  color: #2a7a2a;
  background: #e8f5e9;
  border-radius: 3px;
  padding: 1px 6px;
  margin-left: 6px;
  vertical-align: middle;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}
</style>

{% assign sorted_projects = site.projects | sort: 'date' | reverse %}
{% assign current_year = "" %}

{% for post in sorted_projects %}
  {% assign proj_year = post.date | date: "%Y" %}
  {% if proj_year != current_year %}
    {% unless current_year == "" %}</div>{% endunless %}
    <div class="proj-year-section">
    <div class="proj-year-header">{{ proj_year }}</div>
    {% assign current_year = proj_year %}
  {% endif %}
  <div class="proj-item">
    <div class="proj-title">
      {{ post.title }}
      {% if post.status == "active" %}<span class="proj-status-active">Activo</span>{% endif %}
    </div>
    {% if post.years %}<div class="proj-meta">{{ post.years }}{% if post.funder %} · {{ post.funder }}{% endif %}</div>{% endif %}
    {% if post.role %}<div class="proj-role">Rol: {{ post.role }}</div>{% endif %}
  </div>
{% endfor %}
</div>
