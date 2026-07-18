---
permalink: /
title: "Jorge E. Gaete Olivares"
excerpt: "Profesor Titular y Director del Centro ISME, Escuela de Educación, Universidad de los Andes."
author_profile: true
redirect_from:
  - /about/
  - /about.html
---

<style>
.about-section { margin-bottom: 1.8rem; }
.about-header {
  font-size: 0.9rem;
  font-weight: 700;
  color: #444;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  border-bottom: 2px solid #e0e0e0;
  padding-bottom: 0.4rem;
  margin-bottom: 1rem;
  margin-top: 0.5rem;
}
.about-body {
  font-size: 0.85rem;
  color: #333;
  line-height: 1.65;
}
.about-body a { color: #2a5db0; text-decoration: none; }
.about-body a:hover { text-decoration: underline; }
.about-list {
  font-size: 0.83rem;
  color: #444;
  line-height: 1.7;
  padding-left: 1.2em;
  margin: 0;
}
.about-list li { margin-bottom: 0.2rem; }
.about-list a { color: #2a5db0; text-decoration: none; }
.about-list a:hover { text-decoration: underline; }
.pub-counter-badge {
  display: inline-block;
  background: #f0f4fb;
  border: 1px solid #d0daf0;
  border-radius: 4px;
  padding: 1px 9px;
  font-size: 0.88rem;
  font-weight: 700;
  color: #2a5db0;
}
</style>

<div class="about-section">
<div class="about-body">
Soy <strong>Profesor Titular</strong> de la Escuela de Educación de la Universidad de los Andes (Chile) y <strong>Director del Centro de Investigación en Salud Mental Estudiantil (ISME)</strong>. Soy Médico Cirujano (Pontificia Universidad Católica de Chile), Magíster en Psicología Clínica Infanto-Juvenil (Universidad de Chile), Especialista en Psiquiatría de Adultos, Doctor en Epidemiología Psiquiátrica de la University of Bristol (Reino Unido), con un postdoctorado en el Centre for Global Mental Health de la London School of Hygiene and Tropical Medicine y un Clinical Research Fellowship en Psiquiatría Infantil y del Adolescente en King's College London.
</div>
</div>

<div class="about-section">
<div class="about-header">Líneas de investigación</div>
<div class="about-body">
Mi trabajo se orienta a identificar <strong>factores de riesgo y protectores</strong> para el desarrollo de problemas de salud mental, violencia escolar, suicidalidad y consumo de drogas en niños, adolescentes y adultos jóvenes. Además, evalúo la <strong>efectividad de intervenciones preventivas</strong> en estas mismas áreas, tanto universales como selectivas e indicadas, implementadas principalmente en contextos escolares y universitarios.
</div>
</div>

<div class="about-section">
<div class="about-header">Afiliaciones actuales</div>
<ul class="about-list">
<li>Director, <strong>Centro de Investigación en Salud Mental Estudiantil (ISME)</strong>, Universidad de los Andes — <a href="https://www.ismeuandes.cl">ismeuandes.cl</a></li>
<li>Profesor Titular, <strong>Escuela de Educación</strong>, Universidad de los Andes</li>
<li>Investigador, <strong>Center for the Well-Being and Development of Adolescents and Children in the Digital Age (BAND)</strong>, Santiago, Chile</li>
<li>Clinical Research Fellow (2025), <strong>Centre for Addiction and Mental Health (CAMH)</strong>, University of Toronto, Canadá</li>
</ul>
</div>

<div class="about-section">
<div class="about-header">Producción científica</div>
<div class="about-body">
A la fecha cuento con <span class="pub-counter-badge" id="orcid-pub-count">…</span> publicaciones en revistas científicas indexadas y he dirigido o participado como co-investigador en más de <strong>25 proyectos de investigación</strong> financiados por ANID y otras agencias nacionales e internacionales (Wellcome Trust, Academy of Finland, entre otras).
</div>
</div>

<div class="about-section">
<div class="about-header">Perfiles académicos</div>
<ul class="about-list">
<li><a href="https://orcid.org/0000-0002-6650-6018">ORCID</a></li>
<li><a href="https://scholar.google.es/citations?user=g99obcwAAAAJ&hl=es">Google Scholar</a></li>
<li><a href="https://www.scopus.com/authid/detail.uri?authorId=8652950300">Scopus</a></li>
<li><a href="https://investigadores.uandes.cl/es/persons/jorge-eduardo-gaete-olivares/">Portal de Investigadores UAndes</a></li>
</ul>
</div>

<div class="about-section">
<div class="about-header">Contacto</div>
<div class="about-body">
&#128231; <a href="mailto:jgaete@uandes.cl">jgaete@uandes.cl</a><br>
&#128205; Facultad de Educación, Universidad de los Andes, Monseñor Álvaro del Portillo 12455, Las Condes, Santiago, Chile.
</div>
</div>

<script>
(function() {
  fetch('https://pub.orcid.org/v3.0/0000-0002-6650-6018/works', {
    headers: { 'Accept': 'application/json' }
  })
  .then(function(r) { return r.json(); })
  .then(function(data) {
    var count = data.group ? data.group.length : null;
    var el = document.getElementById('orcid-pub-count');
    if (el && count !== null) el.textContent = count;
  })
  .catch(function() {});
})();
</script>
