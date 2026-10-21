// Dump Pokemon Showdown move data (via the @pkmn/dex npm package) for the Hardcore Crystal generators.
// usage: cd /home/claude/tools_src/sd && node /home/claude/pokecrystal/tools/hardcore/dump_showdown.js > tools/hardcore/showdown_moves.json
const { Dex } = require('@pkmn/dex');
const g = Dex.forGen(9);
const NEW = [
  'fairywind','drainingkiss','playrough','dazzlinggleam','moonblast','dragonpulse','earthpower','energyball','flashcannon',
  'ironhead','xscissor','bugbuzz','darkpulse','gunkshot','aurasphere','closecombat','bravebird','flareblitz','wildcharge',
  'stoneedge','powergem','scald','hypervoice','shadowclaw','nightslash','drainpunch','iceshard','vacuumwave','bulletpunch',
  'airslash','poisonjab','zenheadbutt','leafblade','seedbomb','aquatail',
  'dragonclaw','brickbreak','focusblast','shadowsneak','thunderfang','firefang','icefang','woodhammer','aquajet','psychocut','hurricane'
];
const out = {};
for (const m of g.moves.all()) {
  if (m.num > 251 && !NEW.includes(m.id)) continue;
  if (m.isNonstandard === 'CAP') continue;
  out[m.id] = {
    id: m.id, num: m.num, name: m.name, type: m.type, category: m.category,
    basePower: m.basePower, accuracy: m.accuracy === true ? 0 : m.accuracy, pp: m.pp,
    priority: m.priority, secondary: m.secondary ? (m.secondary.chance || 0) : 0,
    drain: m.drain || null, recoil: m.recoil || null, critRatio: m.critRatio || 1,
  };
}
console.log(JSON.stringify(out, null, 1));
