(function(){
  var bar=document.getElementById('sbar'); if(!bar) return;
  var input=document.getElementById('sq'), cnt=document.getElementById('scount'),
      prev=document.getElementById('sprev'), next=document.getElementById('snext'), clr=document.getElementById('sclear');
  var root=document.querySelector(bar.getAttribute('data-root')||'main');
  var excl=bar.getAttribute('data-excluir')||'';
  var marks=[], cur=-1, timer=null;
  function nrm(s){return s.normalize('NFD').replace(/[̀-ͯ]/g,'').toLowerCase();}
  function limpiar(){
    marks.forEach(function(m){var p=m.parentNode;if(!p)return;p.replaceChild(document.createTextNode(m.textContent),m);p.normalize();});
    marks=[];cur=-1;
  }
  function excluido(n){
    var el=n.parentElement;
    if(!el||el.closest('script,style,#sbar,.theme-btn'))return true;
    return excl?!!el.closest(excl):false;
  }
  function buscar(q){
    limpiar();
    var nq=nrm(q.trim());
    if(nq.length<2){cnt.textContent='';bar.classList.remove('has');return;}
    bar.classList.add('has');
    var w=document.createTreeWalker(root,NodeFilter.SHOW_TEXT,null),nodos=[],n;
    while((n=w.nextNode())){if(n.nodeValue.trim()&&!excluido(n))nodos.push(n);}
    nodos.forEach(function(node){
      if(marks.length>=600)return;
      var t=node.nodeValue,s='',map=[];
      for(var i=0;i<t.length;i++){var c=nrm(t[i]);for(var j=0;j<c.length;j++){s+=c[j];map.push(i);}}
      var rs=[],k=s.indexOf(nq);
      while(k!==-1){rs.push([map[k],map[k+nq.length-1]+1]);k=s.indexOf(nq,k+nq.length);}
      if(!rs.length)return;
      var locales=[];
      for(var r=rs.length-1;r>=0;r--){
        var a=rs[r][0],b=rs[r][1];
        var tail=node.splitText(a);tail.splitText(b-a);
        var m=document.createElement('mark');m.className='sr';
        tail.parentNode.replaceChild(m,tail);m.appendChild(tail);
        locales.unshift(m);
      }
      marks=marks.concat(locales);
    });
    if(!marks.length){cnt.textContent='Sin resultados';return;}
    ir(0);
  }
  function ir(i){
    if(!marks.length)return;
    if(cur>=0&&marks[cur])marks[cur].classList.remove('cur');
    cur=(i+marks.length)%marks.length;
    var m=marks[cur];m.classList.add('cur');
    var d=m.closest('details');while(d){d.open=true;d=d.parentElement&&d.parentElement.closest('details');}
    m.scrollIntoView({block:'center',behavior:'instant'});
    cnt.textContent=(cur+1)+' de '+marks.length+(marks.length>=600?'+':'');
  }
  input.addEventListener('input',function(){clearTimeout(timer);timer=setTimeout(function(){buscar(input.value);},220);});
  input.addEventListener('keydown',function(e){
    if(e.key==='Enter'){e.preventDefault();clearTimeout(timer);
      if(!marks.length||nrm(input.value.trim())!==input.dataset.last)buscar(input.value);else ir(cur+(e.shiftKey?-1:1));
      input.dataset.last=nrm(input.value.trim());}
    if(e.key==='Escape'){input.value='';limpiar();cnt.textContent='';bar.classList.remove('has');}
  });
  input.addEventListener('input',function(){input.dataset.last=nrm(input.value.trim());});
  prev.addEventListener('click',function(){ir(cur-1);});
  next.addEventListener('click',function(){ir(cur+1);});
  clr.addEventListener('click',function(){input.value='';limpiar();cnt.textContent='';bar.classList.remove('has');input.focus();});
  document.addEventListener('keydown',function(e){
    var t=e.target.tagName;if(t==='INPUT'||t==='TEXTAREA')return;
    if(e.key==='/'||((e.ctrlKey||e.metaKey)&&e.key.toLowerCase()==='k')){e.preventDefault();input.focus();input.select();}
  });
})();
