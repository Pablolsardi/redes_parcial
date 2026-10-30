#!/usr/bin/env python3
"""Genera autoevaluacion.html (repaso), practica.html (corrección inmediata) y examen.html (definitivo)
a partir de fuente/preguntas.json. Uso: python3 fuente/build_autoevaluacion.py"""
import json, html, pathlib

RAIZ = pathlib.Path(__file__).resolve().parent.parent
DATA = json.loads((RAIZ / "fuente" / "preguntas.json").read_text(encoding="utf-8"))
TEMAS = {t["id"]: t["nombre"] for t in DATA["temas"]}
LETRAS = "abcd"
BUSCADOR_CSS = (RAIZ / "fuente" / "buscador.css").read_text(encoding="utf-8")
BUSCADOR_JS = (RAIZ / "fuente" / "buscador.js").read_text(encoding="utf-8")


def sbar(placeholder, root="main", excluir=""):
    ex = f' data-excluir="{excluir}"' if excluir else ""
    return (f'<div class="sbar" id="sbar" data-root="{root}"{ex}><label class="sbox">'
            '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>'
            f'<input id="sq" type="search" placeholder="{placeholder}" aria-label="Buscar" autocomplete="off"><kbd>/</kbd></label>'
            '<span class="scount" id="scount" aria-live="polite"></span>'
            '<button type="button" class="sbtn" id="sprev" aria-label="Resultado anterior">↑</button>'
            '<button type="button" class="sbtn" id="snext" aria-label="Resultado siguiente">↓</button>'
            '<button type="button" class="sbtn" id="sclear" aria-label="Borrar búsqueda">✕</button></div>\n')

CSS = r"""
:root{--bg:#f6f7f9;--card:#fff;--ink:#1c2430;--mut:#5b6675;--line:#dfe3ea;--acc:#1f5fbf;--acc2:#0e8a6a;--warn:#b45309;--warnbg:#fff6e5;--okbg:#e9f7f1;--infobg:#eaf1fc;--code:#f0f2f6;--on-acc:#fff;--bad:#c0392b;--badbg:#fdecea;--sel:#1f5fbf;--selbg:#e3edfc}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#12161c;--card:#1a2029;--ink:#e6eaf0;--mut:#9aa6b6;--line:#2c3542;--acc:#6ea8ff;--acc2:#4fd1a5;--warn:#f0b35a;--warnbg:#33290f;--okbg:#12302a;--infobg:#16263f;--code:#232b37;--on-acc:#0b1220;--bad:#ff7b6b;--badbg:#3a1b18;--sel:#6ea8ff;--selbg:#1b2c48}}
:root[data-theme="dark"]{--bg:#12161c;--card:#1a2029;--ink:#e6eaf0;--mut:#9aa6b6;--line:#2c3542;--acc:#6ea8ff;--acc2:#4fd1a5;--warn:#f0b35a;--warnbg:#33290f;--okbg:#12302a;--infobg:#16263f;--code:#232b37;--on-acc:#0b1220;--bad:#ff7b6b;--badbg:#3a1b18;--sel:#6ea8ff;--selbg:#1b2c48}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.6 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
a,a:visited{color:var(--acc)}
.top{position:sticky;top:0;z-index:40;background:var(--bg);border-bottom:1px solid var(--line)}
.top-in{max-width:900px;margin:0 auto;padding:10px 70px 10px 16px;display:flex;flex-wrap:wrap;gap:6px 16px;align-items:center;font-size:14px}
.top-in a{text-decoration:none;color:var(--mut);padding:4px 8px;border-radius:6px}
.top-in a:hover{background:var(--card);color:var(--acc)}
.top-in a.on{color:var(--acc);font-weight:700}
main{max-width:900px;margin:0 auto;padding:24px 16px 120px}
h1{font-size:28px;margin:8px 0 4px;line-height:1.25}
h2{font-size:21px;margin:40px 0 10px;padding-top:10px;border-top:3px solid var(--acc)}
.sub{color:var(--mut);margin-bottom:16px}
.box{border-left:4px solid var(--acc);background:var(--infobg);padding:10px 14px;border-radius:0 8px 8px 0;margin:12px 0}
.chips{display:flex;flex-wrap:wrap;gap:6px;margin:12px 0}
.chips a,.chips button{font:inherit;font-size:13px;padding:4px 10px;border-radius:99px;border:1px solid var(--line);background:var(--card);color:var(--ink);text-decoration:none;cursor:pointer}
.chips a:hover,.chips button:hover{border-color:var(--acc);color:var(--acc)}
.chips button.on{background:var(--acc);border-color:var(--acc);color:var(--on-acc)}
.q{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px 16px;margin:12px 0}
.qh{display:flex;gap:8px;align-items:center;margin-bottom:6px;flex-wrap:wrap}
.num{font-weight:700;color:var(--acc)}
.tipo{font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.04em;padding:2px 8px;border-radius:99px;background:var(--infobg);color:var(--acc)}
.tipo.vf{background:var(--okbg);color:var(--acc2)}
.enun{margin:0 0 10px;font-weight:500}
ol.ops{list-style:none;margin:0;padding:0;display:grid;gap:6px}
ol.ops li{padding:7px 12px;border:1px solid var(--line);border-radius:8px;display:flex;gap:10px}
.let{font-weight:700;color:var(--mut);min-width:18px}
details{margin-top:10px;border-top:1px dashed var(--line);padding-top:8px}
summary{cursor:pointer;font-weight:600;color:var(--acc)}
.resp{margin:8px 0 0;padding:10px 12px;border-radius:8px;background:var(--okbg)}
.resp b:first-child{color:var(--acc2)}
.resp.f{background:var(--badbg)}
.resp.f b:first-child{color:var(--bad)}
.opt{font:inherit;text-align:left;width:100%;padding:9px 12px;border:1.5px solid var(--line);border-radius:8px;background:var(--card);color:var(--ink);display:flex;gap:10px;align-items:flex-start;cursor:pointer;transition:border-color .12s,background .12s}
.opt:hover{border-color:var(--sel)}
.opt[aria-pressed="true"]{border-color:var(--sel);background:var(--selbg);font-weight:600}
.opt[aria-pressed="true"] .let{color:var(--sel)}
.opt:disabled{cursor:default}
.opt.ok{border-color:var(--acc2);background:var(--okbg)}
.opt.bad{border-color:var(--bad);background:var(--badbg)}
.mark{margin-left:auto;font-size:12px;font-weight:700;white-space:nowrap}
.opt.ok .mark{color:var(--acc2)}.opt.bad .mark{color:var(--bad)}
.hint{font-size:13px;color:var(--mut);margin-top:6px}
.q.res-ok{border-left:5px solid var(--acc2)}.q.res-bad{border-left:5px solid var(--bad)}.q.res-none{border-left:5px solid var(--warn)}
.estado{font-size:12px;font-weight:700;margin-left:auto}
.res-ok .estado{color:var(--acc2)}.res-bad .estado{color:var(--bad)}.res-none .estado{color:var(--warn)}
.bar{position:fixed;left:0;right:0;bottom:0;z-index:45;background:var(--card);border-top:1px solid var(--line);box-shadow:0 -4px 16px rgba(0,0,0,.08)}
.bar-in{max-width:900px;margin:0 auto;padding:10px 16px;display:flex;gap:12px;align-items:center;flex-wrap:wrap}
.prog{flex:1;min-width:160px}
.prog-txt{font-size:13px;color:var(--mut)}
.track{height:8px;border-radius:99px;background:var(--line);overflow:hidden;margin-top:4px}
.fill{height:100%;width:0;background:var(--acc);transition:width .2s}
.btn{font:inherit;font-weight:700;padding:9px 16px;border-radius:8px;border:1.5px solid var(--acc);background:var(--acc);color:var(--on-acc);cursor:pointer}
.btn.sec{background:transparent;color:var(--acc)}
.btn:hover{filter:brightness(1.08)}
.aviso{display:none;width:100%;background:var(--warnbg);border:1px solid var(--warn);border-radius:8px;padding:8px 12px;font-size:14px}
.aviso.on{display:flex;gap:10px;align-items:center;flex-wrap:wrap}
.score{display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:10px;margin:16px 0}
.score div{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:12px;text-align:center}
.score b{display:block;font-size:28px;line-height:1.2}
.score .k-ok b{color:var(--acc2)}.score .k-bad b{color:var(--bad)}.score .k-none b{color:var(--warn)}.score .k-nota b{color:var(--acc)}
.hidden{display:none!important}
::view-transition-old(root),::view-transition-new(root){animation-duration:.3s;animation-timing-function:ease}
[id]{scroll-margin-top:calc(var(--anch,0px) + 14px)}

.top ~ main .sbar{top:var(--toph,49px);padding-right:0;margin:0 -16px 6px;padding-left:16px;padding-right:16px}
.theme-btn{position:fixed;top:8px;right:14px;z-index:50;width:40px;height:40px;border-radius:50%;border:1px solid var(--line);background:var(--card);color:var(--ink);display:grid;place-items:center;cursor:pointer;box-shadow:0 2px 8px rgba(0,0,0,.12)}
.theme-btn:hover{color:var(--acc)}
.theme-btn svg{width:20px;height:20px}
.theme-btn .moon{display:none}
:root[data-theme="dark"] .theme-btn .sun{display:none}
:root[data-theme="dark"] .theme-btn .moon{display:block}
@media (max-width:600px){h1{font-size:23px}.bar-in{gap:8px}.btn{padding:8px 12px}}
"""

THEME_BTN = ('<button class="theme-btn" id="themeBtn" type="button" aria-label="Cambiar a modo oscuro" title="Cambiar modo claro / oscuro">'
  '<svg class="sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="4.5"/>'
  '<path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>'
  '<svg class="moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
  '<path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg></button>')

THEME_JS = r"""
(function(){function f(){var h=0;var t=document.querySelector('.top'),s=document.getElementById('sbar');if(t)h+=t.offsetHeight;if(s)h+=s.offsetHeight;document.documentElement.style.setProperty('--anch',h+'px');}f();window.addEventListener('resize',f);window.addEventListener('load',f);})();
(function(){var t=document.querySelector('.top');if(!t)return;function f(){document.documentElement.style.setProperty('--toph',t.offsetHeight+'px');}f();window.addEventListener('resize',f);})();
(function(){
  var root=document.documentElement, btn=document.getElementById('themeBtn');
  function current(){var t=root.getAttribute('data-theme');if(t)return t;
    return window.matchMedia&&window.matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light';}
  function apply(t){root.setAttribute('data-theme',t);btn.setAttribute('aria-label',t==='dark'?'Cambiar a modo claro':'Cambiar a modo oscuro');}
  var saved=null;try{saved=localStorage.getItem('redes-theme');}catch(e){}
  apply(saved==='dark'||saved==='light'?saved:current());
  btn.addEventListener('click',function(){var n=current()==='dark'?'light':'dark';if(document.startViewTransition&&!matchMedia('(prefers-reduced-motion: reduce)').matches){document.startViewTransition(function(){apply(n);});}else{apply(n);}try{localStorage.setItem('redes-theme',n);}catch(e){}});
})();
"""


def head(title, desc):
    return f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<style>{CSS}\n{BUSCADOR_CSS}</style>
</head>
<body>
{THEME_BTN}
"""


def topbar(actual):
    links = [("index.html", "← Guía de estudio"), ("autoevaluacion.html", "Repaso con respuestas"), ("practica.html", "Examen de práctica"), ("examen.html", "Examen definitivo")]
    a = "".join(f'<a href="{h}"{" class=\"on\"" if h == actual else ""}>{t}</a>' for h, t in links)
    return f'<header class="top"><div class="top-in">{a}</div></header>\n'


def letra(q, i):
    return "V" if q["tipo"] == "vf" and i == 0 else ("F" if q["tipo"] == "vf" else LETRAS[i] + ")")


def tipo_tag(q):
    return '<span class="tipo vf">Verdadero o falso</span>' if q["tipo"] == "vf" else '<span class="tipo">Opción múltiple</span>'


def pagina_repaso():
    n = len(DATA["preguntas"])
    out = [head("Autoevaluación · Repaso", "Preguntas de Redes de Datos con la respuesta en un desplegable."), topbar("autoevaluacion.html")]
    out.append('<main>\n' + sbar("Buscar en las preguntas (sin mostrar respuestas)…", "main", "details"))
    out.append(f'<h1>Autoevaluación: repaso con respuestas</h1>\n<div class="sub">Redes de Datos · UTN FRT · {n} preguntas de verdadero o falso y opción múltiple · versión {DATA["version"]}</div>\n')
    out.append('<div class="box">Leé la pregunta, elegí mentalmente tu respuesta y recién después abrí <b>Ver respuesta</b>. Si querés que te corrija, usá el <a href="practica.html">examen de práctica</a> (corrección inmediata) o el <a href="examen.html">examen definitivo</a> (con tiempo y nota al final).</div>\n')
    out.append('<div class="chips">' + "".join(f'<a href="#t-{t["id"]}">{html.escape(t["nombre"])}</a>' for t in DATA["temas"]) + "</div>\n")
    for t in DATA["temas"]:
        qs = [q for q in DATA["preguntas"] if q["tema"] == t["id"]]
        out.append(f'<h2 id="t-{t["id"]}">{html.escape(t["nombre"])} <span style="font-size:14px;color:var(--mut);font-weight:500">({len(qs)})</span></h2>\n')
        for q in qs:
            ops = "".join(f'<li><span class="let">{letra(q, i)}</span><span>{o}</span></li>' for i, o in enumerate(q["opciones"]))
            c = q["correcta"]
            resp = f'<b>{letra(q, c)} {q["opciones"][c]}.</b>' if q["tipo"] == "mc" else f'<b>{q["opciones"][c]}.</b>'
            if q["explicacion"]:
                resp += " " + q["explicacion"]
            out.append(f'<div class="q" id="p{q["id"]}"><div class="qh"><span class="num">{q["id"]}.</span>{tipo_tag(q)}</div>'
                       f'<p class="enun">{q["enunciado"]}</p><ol class="ops">{ops}</ol>'
                       f'<details><summary>Ver respuesta</summary><p class="resp{" f" if q["tipo"] == "vf" and c == 1 else ""}">{resp}</p></details></div>\n')
    out.append('</main>\n<script>' + THEME_JS + '</script>\n<script>' + BUSCADOR_JS + '</script>\n</body>\n</html>\n')
    return "".join(out)


EXAM_JS = (RAIZ / "fuente" / "examen_motor.js").read_text(encoding="utf-8")

EXAM_CSS = r"""
.ops{display:grid;gap:6px}
.panel{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:16px 18px;margin:16px 0}
.panel h3{margin:0 0 4px;font-size:16px}
.panel .sub{margin:0 0 8px;font-size:14px}
.lnk{font:inherit;background:none;border:0;color:var(--acc);text-decoration:underline;cursor:pointer;padding:0}
.big{font-size:17px;padding:12px 22px;margin-top:6px}
.otro{display:inline-flex;align-items:center;gap:6px;font-size:13px;margin-left:4px}
.otro input{width:64px;font:inherit;padding:4px 8px;border-radius:8px;border:1px solid var(--line);background:var(--card);color:var(--ink)}
.fb{margin:10px 0 0;padding:10px 12px;border-radius:8px;line-height:1.55}
.fb.ok{background:var(--okbg)}.fb.ok>b:first-child{color:var(--acc2)}
.fb.bad{background:var(--badbg)}.fb.bad>b:first-child{color:var(--bad)}
.fb .por{font-weight:700}
.fb .corr{color:var(--acc2)}
.repasar{font-size:13px;color:var(--mut);margin-top:8px}
.stats{display:flex;gap:6px 16px;flex-wrap:wrap;align-items:center;font-size:14px;flex:1;min-width:200px}
.stats .st{display:inline-flex;gap:5px;align-items:baseline;white-space:nowrap}
.stats .st b{font-size:16px}
.stats .st.ok b{color:var(--acc2)}.stats .st.bad b{color:var(--bad)}
.stats .st.tm.alerta b{color:var(--bad)}
.stats .track{width:100%;margin-top:2px}
.btn.pulso{animation:pulso 1.4s ease-in-out infinite}
@keyframes pulso{0%,100%{box-shadow:0 0 0 0 rgba(31,95,191,.45)}50%{box-shadow:0 0 0 7px rgba(31,95,191,0)}}
.score .k-tm b{color:var(--ink)}
ul.rep{list-style:none;padding:0;margin:0;display:grid;gap:6px}
ul.rep li{display:flex;flex-wrap:wrap;gap:4px 12px;justify-content:space-between;background:var(--card);border:1px solid var(--line);border-radius:8px;padding:8px 12px}
ul.rep li span{color:var(--mut);font-size:14px}
.todo-ok{font-weight:600;color:var(--acc2)}
.porTiempo{background:var(--warnbg);border:1px solid var(--warn);border-radius:8px;padding:8px 12px;margin:10px 0;font-weight:600}
@media (prefers-reduced-motion:reduce){.btn.pulso{animation:none}}
"""


def pagina_examen(modo):
    prac = modo == "practica"
    n = len(DATA["preguntas"])
    archivo = "practica.html" if prac else "examen.html"
    titulo = "Examen de práctica" if prac else "Examen definitivo"
    desc = ("Examen de Redes de Datos con corrección inmediata en cada pregunta." if prac
            else "Examen de Redes de Datos con tiempo, nota final y corrección.")
    intro = ("Cada respuesta se <b>corrige al instante</b>: cuando elegís una opción queda fija y ves si acertaste, con la explicación y la sección de la guía donde repasarla. Abajo vas viendo contestadas, correctas, incorrectas y el tiempo."
             if prac else
             "Como en el parcial: elegís, podés <b>cambiar</b> o <b>deseleccionar</b> cada respuesta, y la corrección aparece recién cuando enviás. Podés ponerle un tiempo límite; si se termina, el examen se envía solo.")
    tiempo_html = "" if prac else """<div class="panel"><h3>Tiempo</h3><div class="sub">Si se termina el tiempo, el examen se envía automáticamente. Sin límite, el reloj solo cuenta lo que tardás.</div>
<div class="chips" id="tiempos" style="margin-bottom:0"><button type="button" data-m="0" class="on">Sin límite</button><button type="button" data-m="10">10 min</button><button type="button" data-m="20">20 min</button><button type="button" data-m="30">30 min</button><button type="button" data-m="45">45 min</button><button type="button" data-m="60">60 min</button>
<label class="otro">Otro: <input id="tOtro" type="number" min="1" max="300" inputmode="numeric" placeholder="min"> min</label></div></div>"""
    stats_html = ("""<div class="stats"><span class="st"><span>Contestadas</span><b id="sResp">0 / 0</b></span><span class="st ok"><span>✓ Correctas</span><b id="sOk">0</b></span><span class="st bad"><span>✗ Incorrectas</span><b id="sBad">0</b></span><span class="st tm"><span>⏱</span><b id="sTiempo">00:00</b></span><div class="track"><div class="fill" id="progFill"></div></div></div>
<button type="button" class="btn" id="enviar">Terminar</button>"""
                  if prac else
                  """<div class="stats"><span class="st"><span>Respondidas</span><b id="sResp">0 / 0</b></span><span class="st tm"><span>⏱</span><b id="sTiempo">00:00</b></span><div class="track"><div class="fill" id="progFill"></div></div></div>
<button type="button" class="btn" id="enviar">Enviar respuestas</button>""")
    aviso_btn = "Terminar igual" if prac else "Enviar igual"
    out = [head(f"Autoevaluación · {titulo}", desc).replace("</style>", EXAM_CSS + "</style>"), topbar(archivo)]
    out.append(f"""<main>
<h1>Autoevaluación: {titulo.lower()}</h1>
<div class="sub">Redes de Datos · UTN FRT · {n} preguntas de verdadero o falso y opción múltiple · versión {DATA["version"]}</div>
<section id="setup">
<div class="box">{intro}</div>
<div class="panel" id="temasBox"><h3>Tema</h3><div class="sub">Hacelo completo o elegí un tema.</div><div class="chips" id="chips" style="margin-bottom:0"></div></div>
{tiempo_html}
<div class="panel"><div id="setupInfo"></div><button type="button" class="btn big" id="comenzar">Comenzar examen</button></div>
</section>
<section id="resultado" class="hidden">
<h2 style="margin-top:16px">Resultado · <span id="rTema"></span></h2>
<div class="porTiempo hidden" id="rPorTiempo">⏱ Se terminó el tiempo: el examen se envió automáticamente.</div>
<div class="score"><div class="k-nota"><b id="rNota">0%</b>Nota</div><div class="k-ok"><b id="rOk">0</b>Correctas</div><div class="k-bad"><b id="rBad">0</b>Incorrectas</div><div class="k-none"><b id="rNone">0</b>Sin responder</div><div class="k-tm"><b id="rTiempo">00:00</b>Tiempo</div></div>
<div style="display:flex;gap:10px;flex-wrap:wrap;margin:8px 0 4px"><button type="button" class="btn" id="reintentarInc">Reintentar solo las incorrectas</button><button type="button" class="btn sec" id="repetir">Repetir este examen</button><button type="button" class="btn sec" id="otroTema">Elegir otro tema{"" if prac else " o tiempo"}</button></div>
<h2>Qué repasar</h2>
<div id="rRepaso"></div>
<h2>Corrección</h2>
<div class="chips" id="filtros"><button type="button" data-f="todas" class="on">Ver todas</button><button type="button" data-f="bad">Solo incorrectas</button><button type="button" data-f="none">Solo sin responder</button><button type="button" data-f="ok">Solo correctas</button></div>
</section>
<section id="run" class="hidden"><h2 id="runTitulo" style="margin-top:8px"></h2><div id="lista"></div></section>
</main>
<div class="bar hidden" id="bar"><div class="bar-in">
{stats_html}
<div class="aviso" id="aviso"><span id="avisoTxt"></span><button type="button" class="btn" id="enviarIgual">{aviso_btn}</button><button type="button" class="btn sec" id="seguir">Seguir respondiendo</button></div>
</div></div>
<script>window.__DATA__={json.dumps(DATA, ensure_ascii=False)};window.__MODO__="{modo}";</script>
<script>{EXAM_JS}</script>
<script>{THEME_JS}</script>
</body>
</html>
""")
    return "".join(out)


idx = RAIZ / "index.html"
txt = idx.read_text(encoding="utf-8")
import re as _re
txt = _re.sub(r"/\*buscador-css\*/.*?/\*fin-buscador-css\*/", lambda m: "/*buscador-css*/\n" + BUSCADOR_CSS + "/*fin-buscador-css*/", txt, flags=_re.S)
txt = _re.sub(r"<script>/\*buscador-js\*/.*?</script>", lambda m: "<script>/*buscador-js*/\n" + BUSCADOR_JS + "</script>", txt, flags=_re.S)
idx.write_text(txt, encoding="utf-8")
_nav = _re.search(r"<nav>(.*?)</nav>", txt, flags=_re.S).group(1)
DATA["secciones"] = {m.group(1): _re.sub(r"<[^>]+>", "", m.group(2)).strip() for m in _re.finditer(r'<a href="#([^"]+)"[^>]*>(.*?)</a>', _nav)}
_faltan = {q["seccion"] for q in DATA["preguntas"]} - set(DATA["secciones"])
assert not _faltan, _faltan
(RAIZ / "autoevaluacion.html").write_text(pagina_repaso(), encoding="utf-8")
(RAIZ / "examen.html").write_text(pagina_examen("definitivo"), encoding="utf-8")
(RAIZ / "practica.html").write_text(pagina_examen("practica"), encoding="utf-8")
print("ok", len(DATA["preguntas"]), "preguntas")
