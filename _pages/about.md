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
.about-body { font-size: 0.85rem; line-height: 1.65; color: #333; }
.about-body h2 { font-size: 0.92rem; font-weight: 700; color: #444; text-transform: uppercase; letter-spacing: 0.10em; border-bottom: 2px solid #e0e0e0; padding-bottom: 0.3rem; margin-top: 1.6rem; margin-bottom: 0.8rem; }
.about-body p { margin-bottom: 0.8rem; }
.about-body ul { margin: 0.3rem 0 0.8rem 1.2rem; padding: 0; }
.about-body ul li { margin-bottom: 0.35rem; }
.about-body a { color: #2a5db0; text-decoration: none; }
.about-body a:hover { text-decoration: underline; }
.orcid-badge { display: inline-block; background: #f0f4fb; border: 1px solid #c5d3ea; border-radius: 4px; padding: 2px 8px; font-size: 0.78rem; color: #2a5db0; font-weight: 600; }
</style>

<div class="about-body">

<p><strong>Profesor Titular</strong> de la Escuela de Educación de la <a href="https://www.uandes.cl" target="_blank">Universidad de los Andes</a> (Chile) y <strong>Director del <a href="https://www.ismeuandes.cl" target="_blank">Centro de Investigación en Salud Mental Estudiantil (ISME)</a></strong>.</p>

<p>Médico Cirujano (<a href="https://www.uc.cl" target="_blank">Pontificia Universidad Católica de Chile</a>).</p>

<p>Magíster en Psicología Clínica Infanto-Juvenil (<a href="https://www.uchile.cl" target="_blank">Universidad de Chile</a>).</p>

<p>Especialista en Psiquiatría de Adultos (<a href="https://www.uchile.cl" target="_blank">Universidad de Chile</a>).</p>

<p>Doctor (PhD) en Epidemiología Psiquiátrica de la <a href="https://www.bristol.ac.uk" target="_blank">University of Bristol</a> (Reino Unido).</p>

<p>Postdoctorado en el <a href="https://www.lshtm.ac.uk" target="_blank">Centre for Global Mental Health de la London School of Hygiene and Tropical Medicine</a>.</p>

<p>Clinical Research Fellowship en Psiquiatría Infantil y del Adolescente en <a href="https://www.kcl.ac.uk" target="_blank">King's College London</a>.</p>

<p>Clinical Research Fellow, <a href="https://www.camh.ca" target="_blank">Centre for Addiction and Mental Health (CAMH)</a>, <a href="https://www.utoronto.ca" target="_blank">University of Toronto</a>, Canadá.</p>

<h2>Líneas de investigación</h2>

<p>Su investigación se organiza en torno a dos grandes ejes. El primero es <strong>epidemiológico</strong>: identificar factores de riesgo y protectores asociados al desarrollo de suicidalidad, depresión, conductas autolesivas, violencia escolar y consumo de sustancias en niños, adolescentes y adultos jóvenes. El segundo eje es de <strong>evaluación de intervenciones</strong>: examinar la eficacia y efectividad de programas preventivos —universales, selectivos e indicados— orientados a estas mismas problemáticas e implementados principalmente en entornos escolares y universitarios, incluyendo intervenciones basadas en terapia cognitivo-conductual y programas de salud mental escolar.</p>

<p>Transversalmente, su trabajo busca comprender la <strong>heterogeneidad en las trayectorias</strong> de síntomas a lo largo del tiempo, el papel de variables psicológicas como la inflexibilidad psicológica y el sentido de pertenencia, y los determinantes sociales y ambientales del bienestar mental en jóvenes.</p>

<h2>Producción científica</h2>

<p>Cuenta con más de <a href="/publications/" style="text-decoration:none;"><span class="orcid-badge"><span id="orcid-pub-count">95</span> publicaciones</span></a> en revistas científicas y ha dirigido o participado como co-investigador en más de <a href="/projects/" style="text-decoration:none;"><span class="orcid-badge"><span id="orcid-project-count">{{ site.projects | size }}</span> proyectos</span></a> de investigación financiados por la Agencia Nacional de Investigación y Desarrollo (ANID) y otras agencias nacionales e internacionales (Wellcome Trust, Academy of Finland, entre otras).</p>

<h2>Perfiles académicos</h2>

<ul>
<li><a href="https://orcid.org/0000-0002-6650-6018" target="_blank">ORCID</a></li>
<li><a href="https://scholar.google.es/citations?user=g99obcwAAAAJ&hl=es" target="_blank">Google Scholar</a></li>
<li><a href="https://www.scopus.com/authid/detail.uri?authorId=8652950300" target="_blank">Scopus</a></li>
<li><a href="https://investigadores.uandes.cl/es/persons/jorge-eduardo-gaete-olivares/" target="_blank">Portal de Investigadores UAndes</a></li>
</ul>

<h2>Contacto</h2>

<p><strong>Email:</strong> <a href="mailto:jgaete@uandes.cl">jgaete@uandes.cl</a><br>
<strong>Dirección Postal:</strong> Escuela de Educación, <a href="https://www.uandes.cl" target="_blank">Universidad de los Andes</a>, Monseñor Álvaro del Portillo 12455, Las Condes, Santiago, Chile.</p>

</div>

<script>
(function() {
fetch('https://pub.orcid.org/v3.0/0000-0002-6650-6018/works', {
headers: { 'Accept': 'application/json' },
cache: 'no-store'
})
.then(function(r) { return r.json(); })
.then(function(data) {
var count = data.group ? data.group.length : null;
var el = document.getElementById('orcid-pub-count');
if (el && count !== null) el.textContent = count;
})
.catch(function() {});

fetch('https://pub.orcid.org/v3.0/0000-0002-6650-6018/fundings', {
headers: { 'Accept': 'application/json' },
cache: 'no-store'
})
.then(function(r) { return r.json(); })
.then(function(data) {
var count = data.group ? data.group.length : null;
var el = document.getElementById('orcid-project-count');
if (el && count !== null) el.textContent = count;
})
.catch(function() {});
})();
</script>
