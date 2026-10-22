#!/usr/bin/env python3
"""Genera autoevaluacion.html (repaso con desplegables) y examen.html (interactivo)
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
:root{--bg:#f6f7f9;--card:#fff;--ink:#1c2430;--mut:#5b6675;--line:#dfe3ea;--acc:#1f5fbf;--acc2:#0e8a6a;--warn:#b45309;--warnbg:#fff6e5;--okbg:#e9f7f1;--infobg:#eaf1fc;--code:#f0f2f6;--bad:#c0392b;--badbg:#fdecea;--sel:#1f5fbf;--selbg:#e3edfc}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#12161c;--card:#1a2029;--ink:#e6eaf0;--mut:#9aa6b6;--line:#2c3542;--acc:#6ea8ff;--acc2:#4fd1a5;--warn:#f0b35a;--warnbg:#33290f;--okbg:#12302a;--infobg:#16263f;--code:#232b37;--bad:#ff7b6b;--badbg:#3a1b18;--sel:#6ea8ff;--selbg:#1b2c48}}
:root[data-theme="dark"]{--bg:#12161c;--card:#1a2029;--ink:#e6eaf0;--mut:#9aa6b6;--line:#2c3542;--acc:#6ea8ff;--acc2:#4fd1a5;--warn:#f0b35a;--warnbg:#33290f;--okbg:#12302a;--infobg:#16263f;--code:#232b37;--bad:#ff7b6b;--badbg:#3a1b18;--sel:#6ea8ff;--selbg:#1b2c48}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.6 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
a{color:var(--acc)}
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
.chips button.on{background:var(--acc);border-color:var(--acc);color:#fff}
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
.btn{font:inherit;font-weight:700;padding:9px 16px;border-radius:8px;border:1.5px solid var(--acc);background:var(--acc);color:#fff;cursor:pointer}
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
    links = [("index.html", "← Guía de estudio"), ("autoevaluacion.html", "Repaso con respuestas"), ("examen.html", "Examen de práctica")]
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
    out.append('<div class="box">Leé la pregunta, elegí mentalmente tu respuesta y recién después abrí <b>Ver respuesta</b>. Si querés que te corrija y te dé un puntaje, usá el <a href="examen.html">examen de práctica</a>.</div>\n')
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


EXAM_JS = r"""
(function(){
  var D=window.__DATA__, KEY='redes-examen-'+D.version, L='abcd';
  var answers={}, tema='todos', submitted=false;
  try{var s=JSON.parse(localStorage.getItem(KEY)||'{}');if(s&&typeof s==='object'){answers=s.a||{};tema=s.t||'todos';}}catch(e){}
  var temaNombre={};D.temas.forEach(function(t){temaNombre[t.id]=t.nombre;});
  var list=document.getElementById('lista'), chips=document.getElementById('chips'),
      txt=document.getElementById('progTxt'), fill=document.getElementById('progFill'),
      aviso=document.getElementById('aviso'), avisoTxt=document.getElementById('avisoTxt'),
      res=document.getElementById('resultado'), bar=document.getElementById('bar'), filtros=document.getElementById('filtros');
  function save(){try{localStorage.setItem(KEY,JSON.stringify({a:answers,t:tema}));}catch(e){}}
  function visibles(){return D.preguntas.filter(function(q){return tema==='todos'||q.tema===tema;});}
  function let(q,i){return q.tipo==='vf'?(i===0?'V':'F'):L[i]+')';}
  function esc(s){var d=document.createElement('div');d.textContent=s;return d.innerHTML;}
  function renderChips(){
    var h='<button type="button" data-t="todos"'+(tema==='todos'?' class="on"':'')+'>Todos los temas ('+D.preguntas.length+')</button>';
    D.temas.forEach(function(t){var n=D.preguntas.filter(function(q){return q.tema===t.id;}).length;
      h+='<button type="button" data-t="'+t.id+'"'+(tema===t.id?' class="on"':'')+'>'+esc(t.nombre)+' ('+n+')</button>';});
    chips.innerHTML=h;
  }
  function render(){
    var qs=visibles(), h='', ultimo=null;
    qs.forEach(function(q,idx){
      if(tema==='todos'&&q.tema!==ultimo){h+='<h2>'+esc(temaNombre[q.tema])+'</h2>';ultimo=q.tema;}
      var a=answers[q.id], estado='', cls='q';
      if(submitted){
        if(a===undefined){cls+=' res-none';estado='Sin responder';}
        else if(a===q.correcta){cls+=' res-ok';estado='Correcta';}
        else{cls+=' res-bad';estado='Incorrecta';}
      }
      h+='<div class="'+cls+'" id="p'+q.id+'" data-estado="'+(submitted?(a===undefined?'none':(a===q.correcta?'ok':'bad')):'')+'">';
      h+='<div class="qh"><span class="num">'+(idx+1)+'.</span><span class="tipo'+(q.tipo==='vf'?' vf':'')+'">'+(q.tipo==='vf'?'Verdadero o falso':'Opción múltiple')+'</span>'+(estado?'<span class="estado">'+estado+'</span>':'')+'</div>';
      h+='<p class="enun">'+q.enunciado+'</p><div class="ops" style="display:grid;gap:6px">';
      q.opciones.forEach(function(o,i){
        var pressed=a===i, extra='', mark='';
        if(submitted){
          if(i===q.correcta){extra=' ok';mark='<span class="mark">'+(pressed?'✓ Tu respuesta':'✓ Correcta')+'</span>';}
          else if(pressed){extra=' bad';mark='<span class="mark">✗ Tu respuesta</span>';}
        }
        h+='<button type="button" class="opt'+extra+'" data-q="'+q.id+'" data-i="'+i+'" aria-pressed="'+pressed+'"'+(submitted?' disabled':'')+'><span class="let">'+let(q,i)+'</span><span>'+o+'</span>'+mark+'</button>';
      });
      h+='</div>';
      if(submitted){
        var c=q.correcta, r=(q.tipo==='mc'?let(q,c)+' ':'')+q.opciones[c]+'.';
        h+='<p class="resp'+(q.tipo==='vf'&&c===1?' f':'')+'"><b>'+r+'</b> '+(q.explicacion||'')+'</p>';
      }else if(a!==undefined){h+='<div class="hint">Tocá otra opción para cambiarla o la misma para deseleccionarla.</div>';}
      h+='</div>';
    });
    list.innerHTML=h; progreso();
  }
  function progreso(){
    var qs=visibles(), n=qs.filter(function(q){return answers[q.id]!==undefined;}).length;
    txt.textContent='Respondidas '+n+' de '+qs.length; fill.style.width=(qs.length?100*n/qs.length:0)+'%';
  }
  list.addEventListener('click',function(e){
    var b=e.target.closest('.opt'); if(!b||submitted) return;
    var id=b.getAttribute('data-q'), i=+b.getAttribute('data-i');
    if(answers[id]===i) delete answers[id]; else answers[id]=i;
    save(); aviso.classList.remove('on');
    var card=document.getElementById('p'+id);
    card.querySelectorAll('.opt').forEach(function(x){x.setAttribute('aria-pressed',String(answers[id]===+x.getAttribute('data-i')));});
    var hint=card.querySelector('.hint');
    if(answers[id]!==undefined&&!hint){var d=document.createElement('div');d.className='hint';d.textContent='Tocá otra opción para cambiarla o la misma para deseleccionarla.';card.appendChild(d);}
    if(answers[id]===undefined&&hint) hint.remove();
    progreso();
  });
  chips.addEventListener('click',function(e){
    var b=e.target.closest('button'); if(!b||submitted) return;
    tema=b.getAttribute('data-t'); save(); renderChips(); render(); aviso.classList.remove('on'); window.scrollTo({top:0,behavior:'instant'});
  });
  function enviar(){
    submitted=true; var qs=visibles(), ok=0, bad=0, none=0;
    qs.forEach(function(q){var a=answers[q.id];if(a===undefined)none++;else if(a===q.correcta)ok++;else bad++;});
    var nota=qs.length?Math.round(100*ok/qs.length):0;
    document.getElementById('rOk').textContent=ok;document.getElementById('rBad').textContent=bad;
    document.getElementById('rNone').textContent=none;document.getElementById('rNota').textContent=nota+'%';
    document.getElementById('rTema').textContent=tema==='todos'?'Todos los temas':temaNombre[tema];
    res.classList.remove('hidden'); bar.classList.add('hidden'); chips.classList.add('hidden');
    document.getElementById('intro').classList.add('hidden'); aviso.classList.remove('on');
    render(); filtrar('todas'); window.scrollTo({top:0,behavior:'instant'});
  }
  document.getElementById('enviar').addEventListener('click',function(){
    var qs=visibles(), faltan=qs.filter(function(q){return answers[q.id]===undefined;}).length;
    if(faltan>0){avisoTxt.textContent='Te '+(faltan===1?'falta 1 pregunta':'faltan '+faltan+' preguntas')+' sin responder. Las sin responder cuentan como no acertadas.';aviso.classList.add('on');}
    else enviar();
  });
  document.getElementById('enviarIgual').addEventListener('click',enviar);
  document.getElementById('seguir').addEventListener('click',function(){
    aviso.classList.remove('on');
    var q=visibles().find(function(q){return answers[q.id]===undefined;});
    if(q){var el=document.getElementById('p'+q.id);if(el)el.scrollIntoView({behavior:'smooth',block:'center'});}
  });
  function filtrar(f){
    filtros.querySelectorAll('button').forEach(function(b){b.classList.toggle('on',b.getAttribute('data-f')===f);});
    list.querySelectorAll('.q').forEach(function(c){var e=c.getAttribute('data-estado');c.classList.toggle('hidden',f!=='todas'&&e!==f);});
    list.querySelectorAll('h2').forEach(function(h){var n=h.nextElementSibling,vis=false;
      while(n&&n.tagName!=='H2'){if(!n.classList.contains('hidden'))vis=true;n=n.nextElementSibling;}h.classList.toggle('hidden',!vis);});
  }
  filtros.addEventListener('click',function(e){var b=e.target.closest('button');if(b)filtrar(b.getAttribute('data-f'));});
  document.getElementById('reintentar').addEventListener('click',function(){
    answers={}; submitted=false; save();
    res.classList.add('hidden'); bar.classList.remove('hidden'); chips.classList.remove('hidden');
    document.getElementById('intro').classList.remove('hidden'); render(); window.scrollTo(0,0);
  });
  document.getElementById('volverTema').addEventListener('click',function(){
    submitted=false; res.classList.add('hidden'); bar.classList.remove('hidden'); chips.classList.remove('hidden');
    document.getElementById('intro').classList.remove('hidden'); answers={}; tema='todos'; save(); renderChips(); render(); window.scrollTo(0,0);
  });
  renderChips(); render();
})();
"""


def pagina_examen():
    n = len(DATA["preguntas"])
    out = [head("Autoevaluación · Examen de práctica", "Examen interactivo de Redes de Datos con resultado final y corrección."), topbar("examen.html")]
    out.append(f'''<main>
<h1>Autoevaluación: examen de práctica</h1>
<div class="sub">Redes de Datos · UTN FRT · {n} preguntas de verdadero o falso y opción múltiple · versión {DATA["version"]}</div>
<div id="intro" class="box">Elegí una opción en cada pregunta. Podés <b>cambiarla</b> tocando otra o <b>deseleccionarla</b> tocando la misma. Cuando termines, tocá <b>Enviar respuestas</b> y vas a ver tu resultado con la corrección de cada pregunta. Si querés practicar un solo tema, elegilo abajo. Tus respuestas se guardan en este navegador por si cerrás la página.</div>
<div class="chips" id="chips"></div>
<section id="resultado" class="hidden">
<h2 style="margin-top:16px">Resultado · <span id="rTema"></span></h2>
<div class="score"><div class="k-nota"><b id="rNota">0%</b>Nota</div><div class="k-ok"><b id="rOk">0</b>Correctas</div><div class="k-bad"><b id="rBad">0</b>Incorrectas</div><div class="k-none"><b id="rNone">0</b>Sin responder</div></div>
<div class="chips" id="filtros"><button type="button" data-f="todas" class="on">Ver todas</button><button type="button" data-f="bad">Solo incorrectas</button><button type="button" data-f="none">Solo sin responder</button><button type="button" data-f="ok">Solo correctas</button></div>
<div style="display:flex;gap:10px;flex-wrap:wrap;margin:8px 0 4px"><button type="button" class="btn" id="reintentar">Volver a intentar</button><button type="button" class="btn sec" id="volverTema">Elegir otro tema</button></div>
</section>
<div id="lista"></div>
</main>
<div class="bar" id="bar"><div class="bar-in">
<div class="prog"><div class="prog-txt" id="progTxt">Respondidas 0 de {n}</div><div class="track"><div class="fill" id="progFill"></div></div></div>
<button type="button" class="btn" id="enviar">Enviar respuestas</button>
<div class="aviso" id="aviso"><span id="avisoTxt"></span><button type="button" class="btn" id="enviarIgual">Enviar igual</button><button type="button" class="btn sec" id="seguir">Seguir respondiendo</button></div>
</div></div>
<script>window.__DATA__={json.dumps(DATA, ensure_ascii=False)};</script>
<script>{EXAM_JS}</script>
<script>{THEME_JS}</script>
</body>
</html>
''')
    return "".join(out)


idx = RAIZ / "index.html"
txt = idx.read_text(encoding="utf-8")
import re as _re
txt = _re.sub(r"/\*buscador-css\*/.*?/\*fin-buscador-css\*/", lambda m: "/*buscador-css*/\n" + BUSCADOR_CSS + "/*fin-buscador-css*/", txt, flags=_re.S)
txt = _re.sub(r"<script>/\*buscador-js\*/.*?</script>", lambda m: "<script>/*buscador-js*/\n" + BUSCADOR_JS + "</script>", txt, flags=_re.S)
idx.write_text(txt, encoding="utf-8")
(RAIZ / "autoevaluacion.html").write_text(pagina_repaso(), encoding="utf-8")
(RAIZ / "examen.html").write_text(pagina_examen(), encoding="utf-8")
print("ok", len(DATA["preguntas"]), "preguntas")
