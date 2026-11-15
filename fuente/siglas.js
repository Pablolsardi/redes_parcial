(function(){
  /* Siglas con flotante (v3.1). Los datos salen de la tabla del glosario (table.glo).
     Hover o foco: flotante con significado y qué es. Clic: abre la sigla en el glosario en otra pestaña.
     En pantallas táctiles, el primer toque muestra el flotante y el link va adentro. */
  var tabla=document.querySelector('table.glo'), root=document.getElementById('main');
  if(!tabla||!root) return;
  var EXCL='h1,h2,h3,h4,a,code,pre,svg,button,input,textarea,select,label,mark,.crumb,.ptoc,.pager,.mk,.vfq,.subgen,#historial,#homeMods,#homeStart,section[data-page="sglo"],.sg';
  var IGNORAR={'A':1};
  function nrm(s){return s.normalize('NFD').replace(/[̀-ͯ]/g,'').toLowerCase();}

  /* 1. diccionario: sigla -> filas del glosario */
  var dic={}, filas={};
  [].forEach.call(tabla.querySelectorAll('tr'),function(tr){
    var td=tr.querySelectorAll('td'); if(td.length<3) return;
    var crudo=td[0].textContent.trim(), id=tr.id;
    var flot=tr.getAttribute('data-flot')!=='no';
    if(!id){id='g-'+nrm(crudo).replace(/[^a-z0-9]+/g,'-').replace(/^-|-$/g,''); tr.id=id;}
    var nota=(crudo.match(/\(([^)]*)\)/)||[])[1]||'';
    var ver=td[3]&&td[3].querySelector('a');
    filas[id]={sigla:crudo.replace(/\s*\([^)]*\)/,''),nota:nota,sig:td[1].textContent.trim(),que:td[2].textContent.trim(),tema:ver?ver.textContent.trim():''};
    crudo.replace(/\s*\([^)]*\)/,'').split(/\s*[\/,]\s*/).forEach(function(t){
      t=t.trim(); if(!flot||t.length<2||IGNORAR[t]) return;
      (dic[t]=dic[t]||[]).indexOf(id)<0&&dic[t].push(id);
    });
  });
  var claves=Object.keys(dic).sort(function(a,b){return b.length-a.length;});
  if(!claves.length) return;
  var esc=function(s){return s.replace(/[.*+?^${}()|[\]\\]/g,'\\$&');};
  var RE=new RegExp('(^|[^A-Za-z0-9ÁÉÍÓÚáéíóúñÑ\\-])('+claves.map(esc).join('|')+')(s?)(?![A-Za-z0-9ÁÉÍÓÚáéíóúñÑ])','g');

  /* 2. marcar en el cuerpo: la primera aparición de cada sigla por bloque (párrafo, ítem, celda) */
  var puestas=[];
  function poner(){
    if(puestas.length) return;
    var w=document.createTreeWalker(root,NodeFilter.SHOW_TEXT,{acceptNode:function(n){
      var el=n.parentElement; if(!el||!n.nodeValue.trim()) return NodeFilter.FILTER_REJECT;
      return el.closest(EXCL)?NodeFilter.FILTER_REJECT:NodeFilter.FILTER_ACCEPT;}});
    var nodos=[],n; while((n=w.nextNode())) nodos.push(n);
    var vistos=new WeakMap();
    nodos.forEach(function(node){
      var t=node.nodeValue, m, hits=[]; RE.lastIndex=0;
      var blq=node.parentElement.closest('p,li,td,th,figcaption,summary,dd,.box,.card,div')||root;
      var set=vistos.get(blq); if(!set){set={}; vistos.set(blq,set);}
      while((m=RE.exec(t))){var k=m[2]; if(set[k]) continue; set[k]=1; hits.push([m.index+m[1].length,k,(m[3]||'').length]);}
      for(var i=hits.length-1;i>=0;i--){
        var ini=hits[i][0], k=hits[i][1], ids=dic[k];
        var cola=node.splitText(ini); cola.splitText(k.length+hits[i][2]);
        var a=document.createElement('a'); a.className='sg'; a.href='#'+ids[0]; a.target='_blank'; a.rel='noopener';
        a.setAttribute('data-sg',k); a.setAttribute('aria-describedby','sgPop');
        cola.parentNode.replaceChild(a,cola); a.appendChild(cola); puestas.push(a);
      }
    });
  }
  function quitar(){
    ocultar(true);
    puestas.forEach(function(a){var p=a.parentNode; if(!p) return; p.replaceChild(document.createTextNode(a.textContent),a); p.normalize();});
    puestas=[];
  }
  window.Siglas={poner:poner,quitar:quitar};

  /* 3. flotante */
  var pop=document.createElement('div'); pop.id='sgPop'; pop.className='sgpop'; pop.setAttribute('role','tooltip'); pop.hidden=true;
  document.body.appendChild(pop);
  var actual=null, tIn=0, tOut=0, tactil=false, desde=0;
  function e(s){return s.replace(/&/g,'&amp;').replace(/</g,'&lt;');}
  function llenar(a){
    var k=a.getAttribute('data-sg'), ids=dic[k]||[], h='';
    ids.forEach(function(id,i){var f=filas[id];
      h+='<div class="sgp-it">'+(i===0?'<b class="sgp-k">'+e(k)+'</b>':'')+(f.nota?'<span class="sgp-n">'+e(f.nota)+'</span>':'')
        +'<span class="sgp-s">'+e(f.sig)+'</span><p>'+e(f.que)+'</p>'+(ids.length>1&&f.tema?'<span class="sgp-t">'+e(f.tema)+'</span>':'')+'</div>';});
    var tema=ids.length===1?filas[ids[0]].tema:'';
    h+='<div class="sgp-f">'+(tactil?'<a href="#'+ids[0]+'" target="_blank" rel="noopener">Ver en el glosario ↗</a>':'<span>Clic: ver en el glosario ↗</span>')
      +(tema?'<span class="sgp-t">'+e(tema)+'</span>':'')+'</div>';
    pop.innerHTML=h;
  }
  function ubicar(a){
    var r=a.getBoundingClientRect(), vw=document.documentElement.clientWidth, vh=window.innerHeight;
    pop.style.left='0px'; pop.style.top='0px'; pop.classList.remove('arriba');
    var pw=pop.offsetWidth, ph=pop.offsetHeight, x=r.left+r.width/2-pw/2;
    x=Math.max(10,Math.min(x,vw-pw-10));
    var y=r.bottom+10, arriba=false;
    if(y+ph>vh-8&&r.top-ph-10>8){y=r.top-ph-10; arriba=true;}
    pop.style.left=Math.round(x+window.scrollX)+'px'; pop.style.top=Math.round(y+window.scrollY)+'px';
    pop.style.setProperty('--fx',Math.round(r.left+r.width/2-x)+'px');
    pop.classList.toggle('arriba',arriba);
  }
  function mostrar(a){
    clearTimeout(tOut); clearTimeout(tIn);
    if(actual&&actual!==a) actual.classList.remove('sg-on');
    if(actual!==a||pop.hidden) desde=Date.now();
    actual=a; a.classList.add('sg-on'); llenar(a); pop.hidden=false; ubicar(a);
    requestAnimationFrame(function(){pop.classList.add('on');});
  }
  function ocultar(ya){
    clearTimeout(tIn); clearTimeout(tOut);
    var fin=function(){pop.classList.remove('on'); pop.hidden=true; if(actual) actual.classList.remove('sg-on'); actual=null;};
    if(ya===true) fin(); else tOut=setTimeout(fin,160);
  }
  root.addEventListener('mouseover',function(ev){
    var a=ev.target.closest&&ev.target.closest('a.sg'); if(!a||tactil) return;
    clearTimeout(tOut); if(a===actual) return;
    clearTimeout(tIn); tIn=setTimeout(function(){mostrar(a);},actual?60:220);
  });
  root.addEventListener('mouseout',function(ev){
    var a=ev.target.closest&&ev.target.closest('a.sg'); if(!a||tactil) return;
    if(ev.relatedTarget&&(a.contains(ev.relatedTarget)||pop.contains(ev.relatedTarget))) return;
    clearTimeout(tIn); if(actual) ocultar();
  });
  pop.addEventListener('mouseenter',function(){clearTimeout(tOut);});
  pop.addEventListener('mouseleave',function(){if(!tactil) ocultar();});
  root.addEventListener('focusin',function(ev){var a=ev.target.closest&&ev.target.closest('a.sg'); if(a) mostrar(a);});
  root.addEventListener('focusout',function(ev){var a=ev.target.closest&&ev.target.closest('a.sg'); if(a&&!tactil) ocultar();});
  document.addEventListener('pointerdown',function(ev){
    tactil=ev.pointerType==='touch';
    if(actual&&!pop.contains(ev.target)&&!(ev.target.closest&&ev.target.closest('a.sg'))) ocultar(true);
  },true);
  root.addEventListener('click',function(ev){
    var a=ev.target.closest&&ev.target.closest('a.sg'); if(!a) return;
    if(tactil&&(actual!==a||pop.hidden||Date.now()-desde<450)){ev.preventDefault(); mostrar(a);}
    else ocultar(true);
  });
  document.addEventListener('keydown',function(ev){if(ev.key==='Escape'&&actual) ocultar(true);});
  window.addEventListener('scroll',function(){if(actual&&!tactil) ocultar(true); else if(actual) ubicar(actual);},{passive:true});
  window.addEventListener('resize',function(){if(actual) ocultar(true);});
  document.addEventListener('pagina:cambio',function(){ocultar(true);});

  /* 4. al llegar al glosario desde una sigla: resaltar la fila */
  function resaltar(){
    var h=location.hash.slice(1); if(!/^g-/.test(h)) return;
    var tr=document.getElementById(h); if(!tr||!tr.closest('table.glo')) return;
    tr.classList.remove('glo-hit'); void tr.offsetWidth; tr.classList.add('glo-hit');
  }
  window.addEventListener('hashchange',resaltar);

  (window.requestIdleCallback||function(f){setTimeout(f,1);})(function(){poner(); resaltar();});
})();
