/* Generador y corrector de ejercicios de subneteo (guía y simulacro) */
(function(){
  if(window.Subneteo) return;
  function rnd(a,b){return a+Math.floor(Math.random()*(b-a+1));}
  function n2ip(n){return [n>>>24,(n>>>16)&255,(n>>>8)&255,n&255].join('.');}
  function mask(p){return p===0?0:(0xFFFFFFFF<<(32-p))>>>0;}
  function bin(n){var s=(n>>>0).toString(2);while(s.length<32)s='0'+s;return s.slice(0,8)+'.'+s.slice(8,16)+'.'+s.slice(16,24)+'.'+s.slice(24);}
  function miles(n){return String(n).replace(/\B(?=(\d{3})+(?!\d))/g,'.');}
  var DEF={A:8,B:16,C:24}, ORD=['primer','segundo','tercer','cuarto'];
  function claseAzar(pref){
    if(pref) return pref;
    var r=Math.random(); return r<0.45?'B':(r<0.85?'C':'A');
  }
  function primerOcteto(c){return c==='A'?rnd(1,126):(c==='B'?rnd(128,191):rnd(192,223));}
  function salto(p){var oi=Math.floor((p-1)/8), mv=(mask(p)>>>(24-8*oi))&255; return {oi:oi,mv:mv,s:256-mv};}

  /* ---- tipo 1: IP con prefijo ---- */
  function genIP(cl){
    var c=claseAzar(cl), d=DEF[c], p=rnd(d+1,Math.min(30,d+(c==='C'?6:12))), ip, m, net, bc;
    do{ ip=((primerOcteto(c)<<24)|(rnd(0,255)<<16)|(rnd(0,255)<<8)|rnd(0,255))>>>0;
        m=mask(p); net=(ip&m)>>>0; bc=(net|(~m>>>0))>>>0; }while(ip===net||ip===bc);
    var st=salto(p), oct=(ip>>>(24-8*st.oi))&255, base=Math.floor(oct/st.s)*st.s;
    return {tipo:'ip', clase:c, ip:ip, p:p,
      campos:[['red','Dirección de red'],['bc','Dirección de broadcast'],['h1','Primer host'],['hn','Último host'],['hosts','Cantidad de hosts utilizables']],
      sol:{red:n2ip(net), bc:n2ip(bc), h1:n2ip(net+1), hn:n2ip(bc-1), hosts:Math.pow(2,32-p)-2},
      pasos:[
        'Prefijo /'+p+' → máscara <b>'+n2ip(m)+'</b> ('+bin(m)+').',
        'El octeto "interesante" es el '+ORD[st.oi]+' (el que no es 255 ni 0, o el último 255 si el prefijo es múltiplo de 8): vale '+st.mv+', así que el <b>salto es 256 − '+st.mv+' = '+st.s+'</b> en ese octeto.',
        'En la IP ese octeto vale '+oct+'. El múltiplo de '+st.s+' que queda justo abajo es <b>'+base+'</b> → red <b>'+n2ip(net)+'</b>. La siguiente red empezaría en '+(base+st.s)+', y la dirección anterior es el broadcast: <b>'+n2ip(bc)+'</b>.',
        'Primer host = red + 1 = <b>'+n2ip(net+1)+'</b>. Último host = broadcast − 1 = <b>'+n2ip(bc-1)+'</b>.',
        'Bits de host: 32 − '+p+' = '+(32-p)+' → 2<sup>'+(32-p)+'</sup> − 2 = <b>'+miles(Math.pow(2,32-p)-2)+'</b> hosts.'
      ],
      enunciado:'Dada la dirección <b>'+n2ip(ip)+'/'+p+'</b>, calculá la dirección de red, la de broadcast, el primer y el último host de su subred, y la cantidad de hosts utilizables.'};
  }

  /* ---- tipo 2: subnetear una red con clase según requisitos ---- */
  function genReq(cl){
    var c=claseAzar(cl), d=DEF[c], maxN=c==='C'?5:(c==='B'?8:12), n=rnd(2,maxN), h=32-d-n, net;
    if(c==='A') net=(primerOcteto('A')<<24)>>>0;
    else if(c==='B') net=((primerOcteto('B')<<24)|(rnd(0,255)<<16))>>>0;
    else net=((primerOcteto('C')<<24)|(rnd(0,255)<<16)|(rnd(0,255)<<8))>>>0;
    var hostsMax=Math.pow(2,h)-2, porHosts=Math.random()<0.4, S, H, txt;
    if(porHosts){
      H=rnd(Math.pow(2,h-1)-1,hostsMax); if(H<2)H=2;
      txt='Se necesitan subredes de <b>al menos '+miles(H)+' hosts</b> cada una, y la <b>mayor cantidad de subredes</b> posible.';
    }else{
      S=rnd(Math.pow(2,n-1)+1,Math.pow(2,n));
      H=rnd(Math.max(2,Math.floor(hostsMax/3)),hostsMax);
      txt='Se necesitan <b>al menos '+S+' subredes</b> con <b>al menos '+miles(H)+' hosts</b> cada una (prestá la menor cantidad de bits posible).';
    }
    var p=d+n, m=mask(p), st=salto(p), tam=Math.pow(2,h), k=rnd(2,Math.min(4,Math.pow(2,n)));
    var red=(net+(k-1)*tam)>>>0, bc=(red+tam-1)>>>0, ult=(net+(Math.pow(2,n)-1)*tam)>>>0;
    var pasos=['Red clase '+c+': máscara por defecto /'+d+' ('+n2ip(mask(d))+'). Hay '+(32-d)+' bits de host para repartir.'];
    if(porHosts){
      pasos.push('Hosts: busco el menor M con 2<sup>M</sup> − 2 ≥ '+miles(H)+': 2<sup>'+(h-1)+'</sup> − 2 = '+miles(Math.pow(2,h-1)-2)+' no alcanza, 2<sup>'+h+'</sup> − 2 = <b>'+miles(hostsMax)+'</b> sí → M = '+h+' bits de host.');
      pasos.push('Bits prestados: N = '+(32-d)+' − '+h+' = <b>'+n+'</b> → 2<sup>'+n+'</sup> = <b>'+miles(Math.pow(2,n))+' subredes</b>.');
    }else{
      pasos.push('Subredes: busco el menor N con 2<sup>N</sup> ≥ '+S+': 2<sup>'+(n-1)+'</sup> = '+Math.pow(2,n-1)+' no alcanza, 2<sup>'+n+'</sup> = <b>'+miles(Math.pow(2,n))+'</b> sí → N = '+n+' bits prestados.');
      pasos.push('Verifico hosts: quedan M = '+(32-d)+' − '+n+' = '+h+' bits → 2<sup>'+h+'</sup> − 2 = <b>'+miles(hostsMax)+'</b> ≥ '+miles(H)+' ✔.');
    }
    pasos.push('Máscara nueva: /'+d+' + '+n+' = <b>/'+p+'</b> = <b>'+n2ip(m)+'</b> ('+bin(m)+').');
    pasos.push('Salto: 256 − '+st.mv+' = <b>'+st.s+'</b> en el '+ORD[st.oi]+' octeto. Las subredes empiezan en '+n2ip(net)+', '+n2ip(net+tam)+', '+n2ip(net+2*tam)+'…');
    pasos.push('Subred número '+k+' (la primera es la que empieza en '+n2ip(net)+'): '+n2ip(net)+' + '+(k-1)+(k===2?' salto':' saltos')+' de '+tam+' direcciones → red <b>'+n2ip(red)+'</b>, hosts de <b>'+n2ip(red+1)+'</b> a <b>'+n2ip(bc-1)+'</b>, broadcast <b>'+n2ip(bc)+'</b>.');
    pasos.push('Para controlar: la última subred empieza en '+n2ip(ult)+' y su broadcast es '+n2ip((ult+tam-1)>>>0)+' (el broadcast de toda la red original).');
    return {tipo:'req', clase:c, ip:net, p:d,
      campos:[['masc','Máscara de subred (decimal)'],['pref','Prefijo (/n)'],['nsub','Cantidad de subredes'],['hosts','Hosts utilizables por subred'],['salto','Salto (rango entre subredes)'],
              ['red','Subred n.º '+k+': dirección de red'],['h1','Subred n.º '+k+': primer host'],['hn','Subred n.º '+k+': último host'],['bc','Subred n.º '+k+': broadcast']],
      sol:{masc:n2ip(m), pref:p, nsub:Math.pow(2,n), hosts:hostsMax, salto:st.s, red:n2ip(red), h1:n2ip(red+1), hn:n2ip(bc-1), bc:n2ip(bc)},
      pasos:pasos,
      enunciado:'Te asignan la red <b>'+n2ip(net)+'/'+d+'</b> (clase '+c+'). '+txt+' Calculá la máscara, la cantidad de subredes, los hosts por subred, el salto y los datos de la <b>subred número '+k+'</b> (la primera es la que empieza en '+n2ip(net)+').'};
  }

  function norm(k,v){
    v=String(v||'').trim().replace(/\s+/g,'');
    if(k==='pref') return v.replace(/^\//,'');
    if(k==='hosts'||k==='nsub'||k==='salto') return v.replace(/[.,]/g,'');
    return v.replace(/^0+(\d)/,'$1').replace(/\.0+(\d)/g,'.$1');
  }
  function corregir(ex,ans){
    var r={}, ok=0;
    ex.campos.forEach(function(c){var k=c[0], b=norm(k,ans[k])===norm(k,ex.sol[k]); r[k]=b; if(b)ok++;});
    return {campos:r, ok:ok, total:ex.campos.length, todo:ok===ex.campos.length};
  }
  function fmtSol(k,v){return (k==='hosts'||k==='nsub')?miles(v):(k==='pref'?'/'+v:String(v));}
  function html(ex,ans,res,pref){
    ans=ans||{}; pref=pref||'sg';
    var h='<p class="sg-en">'+ex.enunciado+'</p><div class="sg-grid">';
    ex.campos.forEach(function(c){
      var k=c[0], st=res?(res.campos[k]?' ok':' bad'):'';
      h+='<label class="sg-f'+st+'"><span>'+c[1]+'</span><input data-k="'+k+'" autocomplete="off" spellcheck="false" inputmode="'+((k==='hosts'||k==='nsub'||k==='salto'||k==='pref')?'numeric':'decimal')+'" value="'+(ans[k]!==undefined?String(ans[k]).replace(/"/g,''):'')+'"'+(res?' disabled':'')+'>'+
        (res&&!res.campos[k]?'<em>Correcto: '+fmtSol(k,ex.sol[k])+'</em>':'')+'</label>';
    });
    h+='</div>';
    if(res){
      h+='<div class="sg-res '+(res.todo?'ok':'bad')+'"><b>'+(res.todo?'✓ Todo bien.':'✗ '+res.ok+' de '+res.total+' bien.')+'</b> Resolución paso a paso:<ol>';
      ex.pasos.forEach(function(p){h+='<li>'+p+'</li>';}); h+='</ol></div>';
    }
    return h;
  }
  function leer(el){var a={};el.querySelectorAll('input[data-k]').forEach(function(i){a[i.getAttribute('data-k')]=i.value;});return a;}
  function lleno(el){var ins=el.querySelectorAll('input[data-k]');if(!ins.length)return false;for(var i=0;i<ins.length;i++)if(!ins[i].value.trim())return false;return true;}

  var css='.sg-en{margin:6px 0 10px}.sg-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:10px 14px}'+
    '.sg-f{display:flex;flex-direction:column;gap:4px;font-size:13.5px;color:var(--mut)}.sg-f input{font:15px ui-monospace,Consolas,monospace;padding:8px 10px;border-radius:8px;border:1.5px solid var(--line);background:var(--bg);color:var(--ink);min-width:0}'+
    '.sg-f input:focus{outline:none;border-color:var(--acc)}.sg-f.ok input{border-color:var(--acc2);background:var(--okbg)}.sg-f.bad input{border-color:#dc2626}.sg-f em{font-style:normal;font:13px ui-monospace,Consolas,monospace;color:var(--acc2);font-weight:700}'+
    '.sg-res{margin-top:14px;padding:10px 14px;border-radius:0 8px 8px 0;border-left:4px solid var(--acc2);background:var(--okbg)}.sg-res.bad{border-color:var(--warn);background:var(--warnbg)}.sg-res ol{margin:6px 0 0;padding-left:20px}.sg-res li{margin:4px 0}'+
    '.subgen{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px 16px;margin:16px 0}.subgen .sg-opts{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:6px}'+
    '.subgen .sg-opts button,.subgen .sg-act button{font:inherit;font-size:14px;padding:6px 12px;border-radius:99px;border:1.5px solid var(--line);background:var(--bg);color:var(--ink);cursor:pointer}'+
    '.subgen .sg-opts button.on{border-color:var(--acc);background:var(--acc);color:var(--on-acc)}.subgen .sg-act{display:flex;gap:8px;margin-top:12px;flex-wrap:wrap}.subgen .sg-act button.p{background:var(--acc);border-color:var(--acc);color:var(--on-acc);font-weight:700}'+
    '.subgen .sg-cnt{font-size:13px;color:var(--mut);margin-left:auto;align-self:center}';
  var st=document.createElement('style');st.textContent=css;document.head.appendChild(st);

  /* ---- widget de práctica en la guía ---- */
  function montar(box){
    var tipo='ip', clase='', ex=null, hechos=0, bien=0;
    box.innerHTML='<div class="sg-opts" data-g="tipo"><button type="button" data-v="ip" class="on">IP/prefijo → red, broadcast, hosts</button><button type="button" data-v="req">Subnetear según requisitos</button></div>'+
      '<div class="sg-opts" data-g="clase"><button type="button" data-v="" class="on">Clase al azar</button><button type="button" data-v="A">Clase A</button><button type="button" data-v="B">Clase B</button><button type="button" data-v="C">Clase C</button></div>'+
      '<div class="sg-body"></div><div class="sg-act"><button type="button" class="p" data-a="corregir">Corregir</button><button type="button" data-a="ver">Ver la solución</button><button type="button" data-a="otro">Otro ejercicio</button><span class="sg-cnt"></span></div>';
    var body=box.querySelector('.sg-body'), cnt=box.querySelector('.sg-cnt');
    function nuevo(){ex=tipo==='ip'?genIP(clase):genReq(clase); body.innerHTML=html(ex); box.querySelector('[data-a="corregir"]').disabled=false;}
    function cont(){cnt.textContent=hechos?('Bien: '+bien+' de '+hechos):'';}
    box.addEventListener('click',function(e){
      var b=e.target.closest('button'); if(!b) return;
      var g=b.parentNode.getAttribute('data-g');
      if(g){b.parentNode.querySelectorAll('button').forEach(function(x){x.classList.toggle('on',x===b);});
        if(g==='tipo')tipo=b.getAttribute('data-v'); else clase=b.getAttribute('data-v'); nuevo(); return;}
      var a=b.getAttribute('data-a');
      if(a==='otro') nuevo();
      else if(a==='corregir'||a==='ver'){
        var ans=a==='ver'?{}:leer(body), r=corregir(ex,ans);
        if(a==='corregir'){hechos++; if(r.todo)bien++; cont();}
        body.innerHTML=html(ex,ans,r); box.querySelector('[data-a="corregir"]').disabled=true;
      }
    });
    body.addEventListener('keydown',function(e){if(e.key==='Enter'){var c=box.querySelector('[data-a="corregir"]');if(!c.disabled)c.click();}});
    nuevo();
  }
  window.Subneteo={genIP:genIP, genReq:genReq, corregir:corregir, html:html, leer:leer, lleno:lleno};
  function init(){document.querySelectorAll('.subgen').forEach(montar);}
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',init); else init();
})();
