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
Soy <strong>Profesor Titular</strong> de la Escuela de Educación de la <a href="https://www.uandes.cl/" target="_blank">Universidad de los Andes</a> (Chile) y <strong>Director del <a href="https://www.ismeuandes.cl/" target="_blank">Centro de Investigación en Salud Mental Estudiantil (ISME)</a></strong>. Soy Médico Cirujano (<a href="https://www.uc.cl/" target="_blank">Pontificia Universidad Católica de Chile</a>), Magíster en Psicología Clínica Infanto-Juvenil (<a href="https://www.uchile.cl/" target="_blank">Universidad de Chile</a>), Especialista en Psiquiatría de Adultos, Doctor en Epidemiología Psiquiátrica de la <a href="https://www.bristol.ac.uk/" target="_blank">University of Bristol</a> (Reino Unido), con un postdoctorado en el <a href="https://www.lshtm.ac.uk/" target="_blank">Centre for Global Mental Health de la London School of Hygiene and Tropical Medicine</a> y un Clinical Research Fellowship en Psiquiatría Infantil y del Adolescente en el <a href="https://www.kcl.ac.uk/" target="_blank">King's College London</a>.
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
<li>Director, <strong><a href="https://www.ismeuandes.cl/" target="_blank">Centro de Investigación en Salud Mental Estudiantil (ISME)</a></strong>, <a href="https://www.uandes.cl/" target="_blank">Universidad de los Andes</a></li>
<li>Profesor Titular, <strong>Escuela de Educación</strong>, <a href="https://www.uandes.cl/" target="_blank">Universidad de los Andes</a></li>
<li>Investigador, <strong>Center for the Well-Being and Development of Adolescents and Children in the Digital Age (BAND)</strong>, Santiago, Chile</li>
<li>Clinical Research Fellow (2025), <strong><a href="https://www.camh.ca/" target="_blank">Centre for Addiction and Mental Health (CAMH)</a></strong>, <a href="https://www.utoronto.ca/" target="_blank">University of Toronto</a>, Canadá</li>
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
<li><a href="https://orcid.org/0000-0002-6650-6018" target="_blank">ORCID</a></li>
<li><a href="https://scholar.google.es/citations?user=g99obcwAAAAJ&hl=es" target="_blank">Google Scholar</a></li>
<li><a href="https://www.scopus.com/authid/detail.uri?authorId=8652950300" target="_blank">Scopus</a></li>
<li><a href="https://investigadores.uandes.cl/es/persons/jorge-eduardo-gaete-olivares/" target="_blank">Portal de Investigadores UAndes</a></li>
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
