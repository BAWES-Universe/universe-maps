'use strict';
(() => {
 const cards=[...document.querySelectorAll('.map-card')];
 const controls=['search','family','feature','role'].map(id=>document.getElementById(id));
 const count=document.getElementById('result-count');
 const filter=()=>{
  const [q,g,f,r]=controls.map(c=>c.value.trim().toLowerCase()); let shown=0;
  for(const c of cards){const ok=(!q||c.dataset.search.includes(q))&&(!g||c.dataset.group===g)&&(!f||c.dataset.tags.split(' ').includes(f))&&(!r||c.dataset.role.toLowerCase()===r);c.hidden=!ok;shown+=Number(ok);}
  for(const group of document.querySelectorAll('.family'))group.hidden=![...group.querySelectorAll('.map-card')].some(c=>!c.hidden);
  count.textContent=`${shown} of ${cards.length} candidates`;
  document.getElementById('no-results').hidden=shown!==0;
 };
 controls.forEach(c=>c.addEventListener(c.tagName==='INPUT'?'input':'change',filter));
 document.getElementById('reset').addEventListener('click',()=>{controls.forEach(c=>c.value='');filter();});
 let toastTimer;const say=text=>{const toast=document.getElementById('toast');toast.textContent=text;toast.classList.add('show');clearTimeout(toastTimer);toastTimer=setTimeout(()=>toast.classList.remove('show'),3200);};
 document.querySelectorAll('[data-copy]').forEach(b=>b.addEventListener('click',async()=>{
  const value=b.dataset.copy;
  try{await navigator.clipboard.writeText(value);say('Import URL copied. Paste it into the custom-map field.');}
  catch{const input=document.createElement('textarea');input.value=value;input.readOnly=true;input.setAttribute('aria-label','Import URL to copy');input.style.cssText='position:fixed;left:10px;bottom:10px;width:90vw;height:70px;z-index:20';document.body.append(input);input.focus();input.select();let ok=false;try{ok=document.execCommand('copy');}catch{}if(ok){input.remove();say('Import URL copied.');}else{say('Copy the selected URL, then press Escape.');input.addEventListener('keydown',e=>{if(e.key==='Escape'){input.remove();b.focus();}});input.addEventListener('blur',()=>setTimeout(()=>input.remove(),1000),{once:true});}}
 }));
 const revealHash=()=>{const id=decodeURIComponent(location.hash.slice(1));const card=document.getElementById(id);if(card?.classList.contains('map-card')){controls.forEach(c=>c.value='');filter();card.querySelector('details').open=true;setTimeout(()=>card.scrollIntoView({block:'start'}),40);}};
 window.addEventListener('hashchange',revealHash);revealHash();
 if (typeof fetch === 'function') fetch('publication-status.json', {cache:'no-cache'}).then(r=>{if(!r.ok)throw new Error('status unavailable');return r.json();}).then(s=>{
  if(!Array.isArray(s.verified_runtime_ids)||s.packages_total!==80)return;
  const verified=new Set(s.verified_runtime_ids);
  const status=document.getElementById('public-status');
  status.textContent=`Public file checks: ${s.packages_verified} of 80 packages verified (${s.original_files_verified} of 596 files). ${s.packages_verified===80?'HTTP / hash checks complete; live gameplay remains open.':'Remaining checks are in progress.'}`;
  const receipt=document.createElement('a');receipt.href='publication-status.json';receipt.textContent=' Verification status';status.append(receipt);
  document.querySelectorAll('[data-integrity-id]').forEach(el=>el.textContent=verified.has(el.dataset.integrityId)?'Public files: HTTP / hash verified':'Public files: verification in progress');
 }).catch(()=>{});
})();
