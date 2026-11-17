(function(){
  var D=window.__DATA__, MODO=window.__MODO__, L='abcd', PRAC=MODO==='practica';
  var temaNombre={};D.temas.forEach(function(t){temaNombre[t.id]=t.nombre;});
  var $=function(id){return document.getElementById(id);};
  var setup=$('setup'), run=$('run'), res=$('resultado'), list=$('lista'), chips=$('chips'), bar=$('bar'),
      aviso=$('aviso'), avisoTxt=$('avisoTxt'), filtros=$('filtros'), tiempos=$('tiempos');
  var tema='todos', limite=0, banco=null, qs=[], answers={}, done=false, t0=0, timer=null, ultimoTiempo=0, etiqueta='';
  var sim=false, simOn=false, ex=null, subAns={}, subRes=null, modos=$('modos'), viendo=null, porTiempoUlt=false;
  var porId={}; D.preguntas.forEach(function(q){porId[q.id]=q;});
  function mezclar(a){a=a.slice();for(var i=a.length-1;i>0;i--){var j=Math.floor(Math.random()*(i+1)),t=a[i];a[i]=a[j];a[j]=t;}return a;}
  function esc(s){var d=document.createElement('div');d.textContent=s;return d.innerHTML;}
  function let(q,i){return q.tipo==='vf'?(i===0?'V':'F'):L[i]+')';}
  function fmt(sec){sec=Math.max(0,Math.round(sec));var m=Math.floor(sec/60),s=sec%60;return (m<10?'0':'')+m+':'+(s<10?'0':'')+s;}
  function delTema(){return D.preguntas.filter(function(q){return tema==='todos'||q.tema===tema;});}
  function secLink(id){var s=D.secciones[id];return s?'<a href="index.html#'+id+'" target="_blank" rel="noopener">'+esc(s)+'</a>':'';}

  /* ---------- pantalla inicial ---------- */
  function renderChips(){
    var h='<button type="button" data-t="todos"'+(tema==='todos'?' class="on"':'')+'>Todos los temas ('+D.preguntas.length+')</button>';
    D.temas.forEach(function(t){var n=D.preguntas.filter(function(q){return q.tema===t.id;}).length;
      h+='<button type="button" data-t="'+t.id+'"'+(tema===t.id?' class="on"':'')+'>'+esc(t.nombre)+' ('+n+')</button>';});
    chips.innerHTML=h; resumenSetup();
  }
  function resumenSetup(){
    var n=banco?banco.length:delTema().length;
    $('setupInfo').innerHTML=banco
      ? 'Vas a reintentar <b>'+n+'</b> pregunta'+(n===1?'':'s')+' que respondiste mal. <button type="button" class="lnk" id="salirReintento">Volver a elegir tema</button>'
      : '<b>'+n+'</b> preguntas · '+(tema==='todos'?'todos los temas':esc(temaNombre[tema]));
    if(!banco&&sim) $('setupInfo').innerHTML='<b>Simulacro del parcial:</b> 19 preguntas de verdadero o falso al azar de todos los temas + 1 ejercicio de subneteo. Cada incorrecta descuenta medio punto.';
    $('temasBox').classList.toggle('hidden',!!banco||sim);
    var s=$('salirReintento'); if(s) s.addEventListener('click',function(){banco=null;renderChips();});
  }
  chips.addEventListener('click',function(e){var b=e.target.closest('button');if(!b)return;tema=b.getAttribute('data-t');renderChips();});
  if(tiempos){
    tiempos.addEventListener('click',function(e){var b=e.target.closest('button');if(!b)return;
      limite=+b.getAttribute('data-m')*60; $('tOtro').value='';
      tiempos.querySelectorAll('button').forEach(function(x){x.classList.toggle('on',x===b);});});
    $('tOtro').addEventListener('input',function(){var v=parseInt(this.value,10);
      tiempos.querySelectorAll('button').forEach(function(x){x.classList.remove('on');});
      if(v>0){limite=Math.min(v,300)*60;}else{limite=0;tiempos.querySelector('[data-m="0"]').classList.add('on');}});
  }
  if(modos){
    modos.addEventListener('click',function(e){var b=e.target.closest('button');if(!b)return;
      sim=b.getAttribute('data-sim')==='1'; modos.querySelectorAll('button').forEach(function(x){x.classList.toggle('on',x===b);});
      if(tiempos){var m=tiempos.querySelector('[data-m="'+(sim?60:0)+'"]'); if(m) m.click();}
      resumenSetup();});
  }
  $('comenzar').addEventListener('click',comenzar);

  function comenzar(){
    simOn=!banco&&sim&&!!window.Subneteo; subAns={}; subRes=null;
    if(simOn){
      /* 14 V/F difíciles (estilo parcial: largas, con un detalle que las cambia) + 5 del resto */
      var vfs=D.preguntas.filter(function(q){return q.tipo==='vf';});
      var dif=mezclar(vfs.filter(function(q){return q.dificil;})).slice(0,14);
      var resto=mezclar(vfs.filter(function(q){return !q.dificil;})).slice(0,19-dif.length);
      qs=mezclar(dif.concat(resto));
      var r=Math.random(); ex=Subneteo.genReq(r<0.6?'B':(r<0.85?'C':'A'));
    }else qs=banco?banco.slice():delTema();
    answers={}; done=false; viendo=null;
    etiqueta=simOn?'Simulacro del parcial':(banco?'Reintento de incorrectas':(tema==='todos'?'Todos los temas':temaNombre[tema]));
    setup.classList.add('hidden'); res.classList.add('hidden'); run.classList.remove('hidden'); bar.classList.remove('hidden');
    aviso.classList.remove('on'); $('runTitulo').textContent=etiqueta;
    render(); t0=Date.now(); clearInterval(timer); timer=setInterval(tick,500); tick(); stats();
    window.scrollTo({top:0,behavior:'instant'});
  }

  /* ---------- tiempo ---------- */
  function tick(){
    var el=(Date.now()-t0)/1000, box=$('sTiempo');
    if(!PRAC&&limite>0){
      var rest=limite-el; box.textContent=fmt(rest)+' restantes';
      box.parentNode.classList.toggle('alerta',rest<=60);
      if(rest<=0){terminar(true);}
    }else{box.textContent=fmt(el);}
  }

  /* ---------- preguntas ---------- */
  function tarjeta(q,idx){
    var a=answers[q.id], cls='q', estado='', st='';
    var corregir=PRAC?(a!==undefined):done;
    if(corregir){
      if(a===undefined){cls+=' res-none';estado='Sin responder';st='none';}
      else if(a===q.correcta){cls+=' res-ok';estado='Correcta';st='ok';}
      else{cls+=' res-bad';estado='Incorrecta';st='bad';}
    }
    var h='<div class="'+cls+'" id="p'+q.id+'" data-estado="'+st+'">';
    h+='<div class="qh"><span class="num">'+(idx+1)+'.</span><span class="tipo'+(q.tipo==='vf'?' vf':'')+'">'+(q.tipo==='vf'?'Verdadero o falso':'Opción múltiple')+'</span>'+(estado?'<span class="estado">'+estado+'</span>':'')+'</div>';
    h+='<p class="enun">'+q.enunciado+'</p><div class="ops">';
    var bloqueada=corregir||done;
    q.opciones.forEach(function(o,i){
      var pressed=a===i, extra='', mark='';
      if(corregir){
        if(i===q.correcta){extra=' ok';mark='<span class="mark">'+(pressed?'✓ Tu respuesta':'✓ Correcta')+'</span>';}
        else if(pressed){extra=' bad';mark='<span class="mark">✗ Tu respuesta</span>';}
      }
      h+='<button type="button" class="opt'+extra+'" data-q="'+q.id+'" data-i="'+i+'" aria-pressed="'+pressed+'"'+(bloqueada?' disabled':'')+'><span class="let">'+let(q,i)+'</span><span>'+o+'</span>'+mark+'</button>';
    });
    h+='</div>';
    if(corregir){
      var c=q.correcta, r=(q.tipo==='mc'?let(q,c)+' ':'')+q.opciones[c];
      if(a===c){
        h+='<div class="fb ok"><b>✓ ¡Correcto!</b> <span class="por">Por qué:</span> '+q.explicacion+'</div>';
      }else{
        h+='<div class="fb bad"><b>'+(a===undefined?'Sin responder.':'✗ Incorrecto.')+'</b> La respuesta correcta es <b class="corr">'+r+'</b>. '+q.explicacion+'</div>';
      }
      if(q.seccion) h+='<div class="repasar">📖 Para repasar: '+secLink(q.seccion)+'</div>';
    }else if(!PRAC&&a!==undefined&&!done){
      h+='<div class="hint">Tocá otra opción para cambiarla o la misma para deseleccionarla.</div>';
    }
    return h+'</div>';
  }
  function render(){
    var h='', ultimo=null, porTema=!banco&&tema==='todos'&&!simOn;
    qs.forEach(function(q,idx){
      if(porTema&&q.tema!==ultimo){h+='<h2>'+esc(temaNombre[q.tema])+'</h2>';ultimo=q.tema;}
      h+=tarjeta(q,idx);
    });
    if(simOn) h+=tarjetaSub();
    list.innerHTML=h;
  }
  function tarjetaSub(){
    var st=done?(subRes.todo?'ok':'bad'):'', cls='q sub'+(done?(subRes.todo?' res-ok':' res-bad'):'');
    return '<div class="'+cls+'" id="psub" data-estado="'+st+'"><div class="qh"><span class="num">20.</span><span class="tipo">Ejercicio de subneteo</span>'+(done?'<span class="estado">'+(subRes.todo?'Bien':'Con errores')+'</span>':'')+'</div>'+
      Subneteo.html(ex,subAns,done?subRes:null)+
      (done?'<div class="repasar">📖 Para repasar: '+secLink('sej')+'</div>':'<div class="hint">Escribí las direcciones con puntos (ej.: 172.16.32.0) y los números sin puntos de miles.</div>')+'</div>';
  }
  list.addEventListener('input',function(e){var i=e.target.closest('#psub input');if(!i)return;subAns[i.getAttribute('data-k')]=i.value;stats();});
  function reemplazar(q){
    var el=$('p'+q.id); if(!el) return;
    var tmp=document.createElement('div'); tmp.innerHTML=tarjeta(q,qs.indexOf(q)); el.replaceWith(tmp.firstChild);
  }
  list.addEventListener('click',function(e){
    var b=e.target.closest('.opt'); if(!b||b.disabled||done) return;
    var id=+b.getAttribute('data-q'), i=+b.getAttribute('data-i'), q=qs.find(function(x){return x.id===id;});
    if(PRAC){ if(answers[id]!==undefined) return; answers[id]=i; }
    else{ if(answers[id]===i) delete answers[id]; else answers[id]=i; }
    reemplazar(q); stats(); aviso.classList.remove('on');
  });

  /* ---------- estadísticas en vivo ---------- */
  function cuenta(){
    var ok=0,bad=0,resp=0; qs.forEach(function(q){var a=answers[q.id];if(a===undefined)return;resp++;if(a===q.correcta)ok++;else bad++;});
    var tot=qs.length;
    if(simOn){tot++; var ps=$('psub'); if(ps&&Subneteo.lleno(ps)) resp++;}
    return {ok:ok,bad:bad,resp:resp,none:tot-resp,total:tot};
  }
  function stats(){
    var c=cuenta();
    $('sResp').textContent=c.resp+' / '+c.total; $('progFill').style.width=(c.total?100*c.resp/c.total:0)+'%';
    if(PRAC){
      $('sOk').textContent=c.ok; $('sBad').textContent=c.bad;
      var btn=$('enviar'); var fin=c.resp===c.total;
      btn.textContent=fin?'Ver resultado':'Terminar'; btn.classList.toggle('pulso',fin);
    }
  }

  /* ---------- terminar ---------- */
  $('enviar').addEventListener('click',function(){
    var c=cuenta();
    if(c.none>0){
      avisoTxt.textContent=(c.none===1?'Te falta 1 pregunta':'Te faltan '+c.none+' preguntas')+'. Las que no respondas cuentan como no acertadas.';
      aviso.classList.add('on');
    }else terminar(false);
  });
  $('enviarIgual').addEventListener('click',function(){terminar(false);});
  $('seguir').addEventListener('click',function(){
    aviso.classList.remove('on');
    var q=qs.find(function(q){return answers[q.id]===undefined;});
    if(q){var el=$('p'+q.id);if(el)el.scrollIntoView({behavior:'smooth',block:'center'});}
  });

  function terminar(porTiempo){
    if(done) return; done=true; clearInterval(timer); ultimoTiempo=(Date.now()-t0)/1000;
    if(!PRAC&&limite>0) ultimoTiempo=Math.min(ultimoTiempo,limite);
    if(simOn) subRes=Subneteo.corregir(ex,subAns);
    mostrar(porTiempo);
    guardar(porTiempo);
  }
  function mostrar(porTiempo){
    var c=cuenta(), nota=c.total?Math.round(100*c.ok/c.total):0;
    var rl=$('rLog'); rl.classList.toggle('hidden',!viendo);
    if(viendo) rl.innerHTML='📋 Estás viendo un intento del historial: <b>'+esc(viendo.etiqueta)+'</b> · '+fechaLarga(viendo.fecha)+'. <button type="button" class="lnk" id="rLogVolver">Volver al historial</button>';
    $('repetir').classList.toggle('hidden',!!viendo);
    $('otroTema').textContent=viendo?'Volver al historial':(PRAC?'Elegir otro tema':'Elegir otro tema o tiempo');
    $('rNota').textContent=nota+'%'; $('rNotaLbl').textContent='Nota'; var rs=$('rSim'); rs.classList.add('hidden');
    if(simOn){
      var pts=c.ok-0.5*c.bad, f=function(x){return String(x).replace('.',',');};
      $('rNota').textContent=f(pts)+' / 19'; $('rNotaLbl').textContent='Puntaje V/F';
      $('rNone').textContent=qs.length-c.ok-c.bad;
      rs.innerHTML='<p><b>Cuenta del puntaje:</b> '+c.ok+' correctas × 1 − '+c.bad+' incorrectas × 0,5 = <b>'+f(pts)+'</b> sobre 19. Las que dejaste sin responder no suman ni restan.</p>'+
        (subRes.todo?'<p class="sim-ok">✓ <b>Ejercicio de subneteo bien resuelto.</b> En el parcial es condición para aprobar.</p>'
                    :'<p class="sim-bad">✗ <b>Ejercicio de subneteo con errores ('+subRes.ok+' de '+subRes.total+' campos bien).</b> En el parcial tiene que estar bien para aprobar: mirá la resolución paso a paso en la pregunta 20.</p>');
      rs.classList.remove('hidden');
    } $('rOk').textContent=c.ok; $('rBad').textContent=c.bad; $('rNone').textContent=c.none;
    $('rTiempo').textContent=fmt(ultimoTiempo); $('rTema').textContent=etiqueta;
    $('rPorTiempo').classList.toggle('hidden',!porTiempo);
    // qué repasar
    var grupos={}, orden=[];
    qs.forEach(function(q,idx){var a=answers[q.id]; if(a===q.correcta) return;
      if(!grupos[q.seccion]){grupos[q.seccion]=[];orden.push(q.seccion);} grupos[q.seccion].push(idx+1);});
    if(simOn&&!subRes.todo){if(!grupos.sej){grupos.sej=[];orden.push('sej');}grupos.sej.push(20);}
    var keys=Object.keys(D.secciones);
    orden.sort(function(x,y){return keys.indexOf(x)-keys.indexOf(y);});
    var h='';
    if(!orden.length){h='<p class="todo-ok">🎉 No hay nada que repasar: respondiste todo bien.</p>';}
    else{
      h='<p class="sub" style="margin:0 0 8px">Secciones de la guía donde están los temas de las preguntas que no acertaste:</p><ul class="rep">';
      orden.forEach(function(s){var n=grupos[s];
        h+='<li>'+secLink(s)+'<span>'+(n.length===1?'pregunta ':'preguntas ')+n.join(', ')+'</span></li>';});
      h+='</ul>';
    }
    $('rRepaso').innerHTML=h;
    var inc=qs.filter(function(q){var a=answers[q.id];return a!==undefined&&a!==q.correcta;});
    var rb=$('reintentarInc'); rb.classList.toggle('hidden',!inc.length||!!viendo);
    rb.textContent='Reintentar solo las incorrectas ('+inc.length+')'; rb.__inc=inc;
    run.classList.remove('hidden'); res.classList.remove('hidden'); bar.classList.add('hidden'); aviso.classList.remove('on');
    render(); filtrar('todas'); window.scrollTo({top:0,behavior:'instant'});
  }
  function filtrar(f){
    filtros.querySelectorAll('button').forEach(function(b){b.classList.toggle('on',b.getAttribute('data-f')===f);});
    list.querySelectorAll('.q').forEach(function(c){var e=c.getAttribute('data-estado');c.classList.toggle('hidden',f!=='todas'&&e!==f);});
    list.querySelectorAll('h2').forEach(function(h){var n=h.nextElementSibling,vis=false;
      while(n&&n.tagName!=='H2'){if(!n.classList.contains('hidden'))vis=true;n=n.nextElementSibling;}h.classList.toggle('hidden',!vis);});
  }
  filtros.addEventListener('click',function(e){var b=e.target.closest('button');if(b)filtrar(b.getAttribute('data-f'));});

  /* ---------- historial de intentos (en este navegador) ---------- */
  var KEY='redes-intentos', MAX=60;
  function leer(){try{var v=JSON.parse(localStorage.getItem(KEY)||'[]');return Array.isArray(v)?v:[];}catch(e){return [];}}
  function escribir(v){try{localStorage.setItem(KEY,JSON.stringify(v.slice(0,MAX)));return true;}catch(e){return false;}}
  function guardar(porTiempo){
    var c=cuenta(), reg={id:Date.now(), fecha:new Date().toISOString(), pagina:MODO, sim:simOn, banco:!!banco, tema:simOn?'':tema,
      etiqueta:etiqueta, dur:Math.round(ultimoTiempo), limite:PRAC?0:limite, porTiempo:!!porTiempo,
      ok:c.ok, bad:c.bad, none:c.none, total:c.total, nota:c.total?Math.round(100*c.ok/c.total):0,
      q:qs.map(function(q){return q.id;}), a:answers};
    if(simOn){reg.pts=c.ok-0.5*c.bad; reg.ex=ex; reg.subAns=subAns; reg.subOk=!!subRes.todo; reg.subCampos=subRes.ok+'/'+subRes.total;}
    var v=leer(); v.unshift(reg); escribir(v); pintarHist();
  }
  function tipoDe(r){return r.sim?'Simulacro':(r.pagina==='practica'?'Práctica':'Examen');}
  function fechaCorta(iso){var d=new Date(iso);return d.toLocaleDateString('es-AR',{day:'2-digit',month:'2-digit'})+' '+d.toLocaleTimeString('es-AR',{hour:'2-digit',minute:'2-digit',hour12:false});}
  function fechaLarga(iso){var d=new Date(iso);return d.toLocaleDateString('es-AR',{weekday:'long',day:'numeric',month:'long'})+', '+d.toLocaleTimeString('es-AR',{hour:'2-digit',minute:'2-digit',hour12:false})+' h';}
  function coma(x){return String(Math.round(x*10)/10).replace('.',',');}
  function resultadoDe(r){
    if(r.sim) return '<b>'+coma(r.pts)+'</b> / 19 · subneteo '+(r.subOk?'<span class="h-ok">✓ bien</span>':'<span class="h-bad">✗ con errores</span>');
    return '<b>'+r.nota+'%</b> · '+r.ok+' bien, '+r.bad+' mal'+(r.none?', '+r.none+' sin responder':'');
  }
  /* ---------- insights: cómo venís para el parcial ---------- */
  function pct(a,b){return b?Math.round(100*a/b):0;}
  function pintarInsights(v){
    var box=$('ins'); if(!box) return;
    var base=v.filter(function(r){return !r.banco;});
    if(!base.length){box.innerHTML='<p class="h-vacio">Cuando termines tu primer intento, acá vas a ver cómo venís: tendencia, temas flojos y hábitos que te restan puntos. Lo más útil es hacer <b>simulacros</b>.</p>';return;}
    var tot={ok:0,bad:0,none:0}, porSec={}, vf={V:{ok:0,n:0},F:{ok:0,n:0}}, dif={d:{ok:0,n:0},n:{ok:0,n:0}};
    base.forEach(function(r){r.q.forEach(function(id){var q=porId[id]; if(!q) return; var a=r.a?r.a[id]:undefined;
      var st=a===undefined?'none':(a===q.correcta?'ok':'bad'); tot[st]++;
      var s_=porSec[q.seccion]=porSec[q.seccion]||{ok:0,bad:0,none:0}; s_[st]++;
      if(a!==undefined){ if(q.tipo==='vf'){var k=q.correcta===0?'V':'F'; vf[k].n++; if(st==='ok') vf[k].ok++;}
        var g=q.dificil?dif.d:dif.n; g.n++; if(st==='ok') g.ok++; }
    });});
    base.forEach(function(r){if(!r.sim) return; var s_=porSec.sej=porSec.sej||{ok:0,bad:0,none:0}; s_[r.subOk?'ok':'bad']++;});
    var sims=base.filter(function(r){return r.sim;}).slice().reverse();
    var ult=sims.slice(-3), h='';
    // veredicto
    if(sims.length){
      var prom=ult.reduce(function(t,r){return t+r.pts;},0)/ult.length, p100=Math.round(100*prom/19), subB=ult.filter(function(r){return r.subOk;}).length;
      var nivel=(p100>=75&&subB===ult.length)?['ok','Vas bien']:((p100>=55&&subB>=Math.ceil(ult.length/2))?['mid','Cerca, falta afinar']:['bad','A reforzar']);
      h+='<div class="i-ver i-'+nivel[0]+'"><b>'+nivel[1]+'</b><span>En tus últimos '+(ult.length===1?'simulacro':ult.length+' simulacros')+' promediaste <b>'+coma(prom)+' de 19</b> en las V/F ('+p100+'%) y resolviste bien el subneteo '+(ult.length===1?(subB?'':'no '):subB+' de '+ult.length+' veces')+'. '
        +(subB<ult.length?'Ojo: el subneteo tiene que estar bien para aprobar. ':'')+'Es una referencia orientativa, no una predicción de la nota.</span></div>';
    }else{
      h+='<div class="i-ver i-mid"><b>Sin simulacros todavía</b><span>Tenés intentos de práctica, pero para saber cómo venís para el parcial hacé un <b>simulacro</b>: 19 V/F con descuento + el ejercicio de subneteo, en 60 minutos.</span></div>';
    }
    // kpis
    var resp=tot.ok+tot.bad, tpq=sims.length?sims.reduce(function(t,r){return t+r.dur/20;},0)/sims.length:0;
    h+='<div class="h-kpis"><div><b>'+base.length+'</b><span>intento'+(base.length===1?'':'s')+' ('+sims.length+' simulacro'+(sims.length===1?'':'s')+')</span></div>'
      +'<div><b>'+pct(tot.ok,resp)+'%</b><span>de acierto en lo que respondiste</span></div>'
      +'<div><b>'+(tot.ok+tot.bad+tot.none)+'</b><span>preguntas vistas</span></div>'
      +(sims.length?'<div><b>'+fmt(tpq)+'</b><span>por pregunta en simulacro (el parcial da 3:00)</span></div>':'')+'</div>';
    // tendencia
    if(sims.length>=2){
      var u=sims.slice(-10); h+='<h4 class="i-h">Tendencia en los simulacros</h4><div class="i-tend">';
      u.forEach(function(r,i){var al=Math.max(4,Math.round(100*Math.max(0,r.pts)/19));
        h+='<div class="i-col" title="'+fechaCorta(r.fecha)+': '+coma(r.pts)+' / 19"><span>'+coma(r.pts)+'</span><i style="height:'+al+'%" class="'+(r.subOk?'':'nosub')+'"></i><small>'+(i+1)+'</small></div>';});
      var d=u[u.length-1].pts-u[0].pts;
      h+='</div><p class="i-nota">'+(d>0.25?'📈 Mejoraste '+coma(d)+' puntos desde el primero de esta serie.':(d<-0.25?'📉 Bajaste '+coma(-d)+' puntos desde el primero de esta serie.':'➖ Estás estable.'))+' Las barras rayadas son simulacros con el subneteo mal.</p>';
    }
    // temas flojos
    var secs=Object.keys(porSec).map(function(k){var x=porSec[k];return {k:k,n:x.ok+x.bad+x.none,mal:x.bad+x.none,acc:pct(x.ok,x.ok+x.bad+x.none)};})
      .filter(function(x){return x.n>=2&&x.mal>0;}).sort(function(a,b){return a.acc-b.acc||b.mal-a.mal;}).slice(0,6);
    if(secs.length){
      h+='<h4 class="i-h">Dónde más fallás</h4><ul class="i-temas">';
      secs.forEach(function(x){h+='<li><span class="i-nom">'+secLink(x.k)+'</span><span class="i-bar"><i style="width:'+x.acc+'%"></i></span><span class="i-num">'+x.acc+'% · '+x.mal+' de '+x.n+' sin acertar</span></li>';});
      h+='</ul>';
    }
    // hábitos
    var tips=[];
    var simB=sims.reduce(function(t,r){return t+r.bad;},0), simN=sims.reduce(function(t,r){return t+r.none;},0);
    if(sims.length){
      var malPorSim=simB/sims.length, accSim=pct(sims.reduce(function(t,r){return t+r.ok;},0),sims.reduce(function(t,r){return t+r.ok+r.bad;},0));
      if(malPorSim>=4&&accSim<70) tips.push('Contestás mucho con poca seguridad: <b>'+coma(malPorSim)+' incorrectas por simulacro</b> te restan '+coma(malPorSim/2)+' puntos. Si dudás entre V y F sin ninguna pista, dejarla en blanco no resta.');
      else if(simN/sims.length>=4&&accSim>=80) tips.push('Dejás muchas en blanco (<b>'+coma(simN/sims.length)+' por simulacro</b>) y cuando contestás acertás el '+accSim+'%. Con ese nivel conviene arriesgar más: si tenés más de 1 chance en 3, contestar suma en promedio.');
      if(tpq>180) tips.push('Vas lento: <b>'+fmt(tpq)+' por pregunta</b> y el parcial da 3:00 (60 minutos para 20). Dejá el subneteo con tiempo de sobra.');
    }
    if(vf.V.n>=5&&vf.F.n>=5){var aV=pct(vf.V.ok,vf.V.n), aF=pct(vf.F.ok,vf.F.n);
      if(aV-aF>=12) tips.push('Te equivocás más en las <b>falsas</b> ('+aF+'% contra '+aV+'% en las verdaderas): leé cada afirmación hasta el final, la trampa suele estar en un solo detalle.');
      else if(aF-aV>=12) tips.push('Te equivocás más en las <b>verdaderas</b> ('+aV+'% contra '+aF+'% en las falsas): estás desconfiando de más. Si no encontrás el detalle que la rompe, probablemente sea verdadera.');}
    if(dif.d.n>=5&&dif.n.n>=5){var aD=pct(dif.d.ok,dif.d.n), aN=pct(dif.n.ok,dif.n.n);
      if(aN-aD>=15) tips.push('En las V/F <b>difíciles</b> (las de estilo parcial) acertás el '+aD+'% y en el resto el '+aN+'%. Practicá con el simulacro, que trae 14 de esas.');}
    if(tips.length) h+='<h4 class="i-h">Hábitos que te están restando</h4><ul class="i-tips">'+tips.map(function(t){return '<li>'+t+'</li>';}).join('')+'</ul>';
    box.innerHTML=h;
  }

  var confirmando=false;
  function pintarHist(){
    var box=$('hist'); if(!box) return; var v=leer(); pintarInsights(v);
    var del=$('histBorrar');
    if(!v.length){box.innerHTML='<p class="h-vacio">Todavía no hay intentos. Cuando termines un simulacro, un examen o una práctica, va a aparecer acá con su tiempo y su resultado.</p>'; del.innerHTML=''; return;}
    var h='';
    h+='<div class="h-tabla"><table><thead><tr><th>Fecha</th><th>Tipo</th><th>De qué</th><th>Duración</th><th>Resultado</th><th></th></tr></thead><tbody>';
    v.forEach(function(r){
      h+='<tr><td>'+fechaCorta(r.fecha)+'</td><td><span class="h-tipo h-'+(r.sim?'sim':r.pagina)+'">'+tipoDe(r)+'</span></td><td>'+esc(r.etiqueta)+'</td>'
        +'<td>'+fmt(r.dur)+(r.porTiempo?' <span class="h-bad" title="Se terminó el tiempo">⏱</span>':'')+'</td><td>'+resultadoDe(r)+'</td>'
        +'<td><button type="button" class="btn sec h-ver" data-id="'+r.id+'">Ver resumen</button></td></tr>';
    });
    box.innerHTML=h+'</tbody></table></div>';
    del.innerHTML=confirmando?'¿Borrar los '+v.length+' intentos? <button type="button" class="lnk" data-b="si">Sí, borrar</button> · <button type="button" class="lnk" data-b="no">Cancelar</button>'
      :'<button type="button" class="lnk" data-b="pedir">Borrar historial</button>';
  }
  if($('histBorrar')) $('histBorrar').addEventListener('click',function(e){var b=e.target.closest('[data-b]');if(!b)return;var k=b.getAttribute('data-b');
    if(k==='pedir') confirmando=true; else{ if(k==='si') escribir([]); confirmando=false;} pintarHist();});
  if($('hist')) $('hist').addEventListener('click',function(e){var b=e.target.closest('.h-ver');if(!b)return;
    var r=leer().find(function(x){return String(x.id)===b.getAttribute('data-id');}); if(r) ver(r);});
  function ver(r){
    viendo=r; simOn=!!r.sim&&!!window.Subneteo; banco=null; tema=r.tema||'todos';
    qs=r.q.map(function(id){return porId[id];}).filter(Boolean);
    answers={}; Object.keys(r.a||{}).forEach(function(k){if(porId[k]) answers[k]=r.a[k];});
    ex=r.ex||null; subAns=r.subAns||{}; subRes=simOn&&ex?Subneteo.corregir(ex,subAns):null;
    if(simOn&&!subRes) simOn=false;
    etiqueta=r.etiqueta; ultimoTiempo=r.dur; done=true; clearInterval(timer);
    setup.classList.add('hidden'); $('runTitulo').textContent=etiqueta;
    mostrar(r.porTiempo);
  }
  document.addEventListener('click',function(e){if(e.target&&e.target.id==='rLogVolver'){aSetup(true);}});

  function aSetup(alHist){
    clearInterval(timer); done=false; run.classList.add('hidden'); res.classList.add('hidden'); bar.classList.add('hidden');
    setup.classList.remove('hidden'); renderChips(); pintarHist();
    var hb=$('histBox'); if(alHist&&hb) hb.scrollIntoView({behavior:'instant',block:'start'}); else window.scrollTo({top:0,behavior:'instant'});
    viendo=null;
  }
  $('reintentarInc').addEventListener('click',function(){banco=this.__inc.slice(); aSetup();});
  $('repetir').addEventListener('click',function(){comenzar();});
  $('otroTema').addEventListener('click',function(){var h=!!viendo; banco=null; aSetup(h);});

  renderChips(); pintarHist();
})();
