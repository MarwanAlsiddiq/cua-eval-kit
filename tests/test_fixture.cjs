// Execute the actual fixture script against a minimal event-capable DOM.
// Browser exports in evidence/ complement this fast recorder regression.
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const script = fs.readFileSync(path.join(__dirname,'../fixture/index.html'),'utf8').match(/<script>([\s\S]*?)<\/script>/)[1];
function fixture(){
  const nodes = new Map();
  function get(id){
    if(!nodes.has(id)) nodes.set(id,{id,value:id==='task'?'CUA-003':'',hidden:false,textContent:'',listeners:{},
      addEventListener(type,fn){(this.listeners[type]??=[]).push(fn)},
      fire(type){for(const fn of this.listeners[type]||[])fn()}});
    return nodes.get(id);
  }
  const document={getElementById:get,querySelectorAll(selector){
    if(selector==='main section')return ['home','jobs','detail','form','support','unavailable'].map(get);
    return [];
  }};
  vm.runInNewContext(script,{document});
  return {get,export(){get('export').onclick();return JSON.parse(get('trace').value)}};
}
test('input-only automation records both fields at export',()=>{
  const f=fixture();
  f.get('alias').value='Synthetic';f.get('alias').fire('input');
  f.get('draft').value='Synthetic draft';f.get('draft').fire('input');
  const trace=f.export();
  assert.equal(trace.final_state.form_filled,true);
  assert.deepEqual(trace.events,[{action:'fill',target:'alias'},{action:'fill',target:'draft'}]);
  assert.equal(JSON.stringify(trace).includes('Synthetic'),false);
});
test('change plus blur plus export does not triple-count an edit',()=>{
  const f=fixture();f.get('alias').value='Synthetic';f.get('alias').fire('input');
  f.get('alias').fire('change');f.get('alias').fire('blur');
  assert.equal(f.export().events.length,1);
  assert.equal(f.export().events.length,1);
});
test('reset clears pending edits and permits a fresh trial',()=>{
  const f=fixture();f.get('alias').value='Synthetic';f.get('alias').fire('input');
  f.get('reset').onclick();
  assert.deepEqual(f.export().events,[]);
  assert.equal(f.export().final_state.form_filled,false);
});
