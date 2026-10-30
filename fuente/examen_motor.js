(function(){
  var D=window.__DATA__, MODO=window.__MODO__, L='abcd', PRAC=MODO==='practica';
  var temaNombre={};D.temas.forEach(function(t){temaNombre[t.id]=t.nombre;});
  var $=function(id){return document.getElementById(id);};
  var setup=$('setup'), run=$('run'), res=$('resultado'), list=$('lista'), chips=$('chips'), bar=$('bar'),
      aviso=$('aviso'), avisoTxt=$('avisoTxt'), filtros=$('filtros'), tiempos=$('tiempos');
  var tema='todos', limite=0, banco=null, qs=[], answers={}, done=false, t0=0, timer=null, ultimoTiempo=0, etiqueta='';
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
    $('temasBox').classList.toggle('hidden',!!banco);
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
  $('comenzar').addEventListener('click',comenzar);

  function comenzar(){
    qs=banco?banco.slice():delTema(); answers={}; done=false;
    etiqueta=banco?'Reintento de incorrectas':(tema==='todos'?'Todos los temas':temaNombre[tema]);
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
    var h='', ultimo=null, porTema=!banco&&tema==='todos';
    qs.forEach(function(q,idx){
      if(porTema&&q.tema!==ultimo){h+='<h2>'+esc(temaNombre[q.tema])+'</h2>';ultimo=q.tema;}
      h+=tarjeta(q,idx);
    });
    list.innerHTML=h;
  }
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
    return {ok:ok,bad:bad,resp:resp,none:qs.length-resp,total:qs.length};
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
    var c=cuenta(), nota=c.total?Math.round(100*c.ok/c.total):0;
    $('rNota').textContent=nota+'%'; $('rOk').textContent=c.ok; $('rBad').textContent=c.bad; $('rNone').textContent=c.none;
    $('rTiempo').textContent=fmt(ultimoTiempo); $('rTema').textContent=etiqueta;
    $('rPorTiempo').classList.toggle('hidden',!porTiempo);
    // qué repasar
    var grupos={}, orden=[];
    qs.forEach(function(q,idx){var a=answers[q.id]; if(a===q.correcta) return;
      if(!grupos[q.seccion]){grupos[q.seccion]=[];orden.push(q.seccion);} grupos[q.seccion].push(idx+1);});
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
    var rb=$('reintentarInc'); rb.classList.toggle('hidden',!inc.length);
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

  function aSetup(){
    clearInterval(timer); done=false; run.classList.add('hidden'); res.classList.add('hidden'); bar.classList.add('hidden');
    setup.classList.remove('hidden'); renderChips(); window.scrollTo({top:0,behavior:'instant'});
  }
  $('reintentarInc').addEventListener('click',function(){banco=this.__inc.slice(); aSetup();});
  $('repetir').addEventListener('click',function(){comenzar();});
  $('otroTema').addEventListener('click',function(){banco=null; aSetup();});

  renderChips();
})();
