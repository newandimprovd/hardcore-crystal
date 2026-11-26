#!/bin/bash
# The single combined pass: builds the real ROM and every test ROM, runs every test, one summary line each.
# usage: verify_all.sh      logs in /home/claude/scratch/verify/, summary in /home/claude/scratch/verify/summary.txt
cd "$(dirname "$0")/../.."
export PATH=/home/claude/bin:$PATH
V=/home/claude/scratch/verify; mkdir -p $V; : > $V/summary.txt
TB=tools/hardcore/testbuild.sh
step() { # name, command...
  local n=$1; shift
  if "$@" > $V/$n.log 2>&1; then echo "ok    $n: $(tail -1 $V/$n.log | cut -c1-120)" >> $V/summary.txt
  else echo "FAIL  $n: $(tail -1 $V/$n.log | cut -c1-120)" >> $V/summary.txt; fi
}
step build_real make -j2 crystal11
step check_text python3 tools/hardcore/check_text.py
step check_names python3 tools/hardcore/check_names.py
step check_wild python3 tools/hardcore/check_wild.py
step battle_budget python3 tools/hardcore/battle_budget.py --quiet
step roster python3 tools/hardcore/test_roster.py pokecrystal11.gbc
step category python3 tools/hardcore/test_category.py pokecrystal11.gbc
step intro python3 tools/hardcore/test_intro.py pokecrystal11.gbc
step charms python3 tools/hardcore/test_charms.py pokecrystal11.gbc
step b_cr $TB cr
step credits python3 tools/hardcore/test_credits.py /home/claude/scratch/cr.gbc
step b_rv $TB rv TEST_MAP=CHERRYGROVE_CITY TEST_X=17 TEST_Y=5
step reveal python3 tools/hardcore/test_reveal.py /home/claude/scratch/rv.gbc
step b_vc $TB vc TEST_MAP=CHERRYGROVE_CITY TEST_X=17 TEST_Y=3 TEST_MON=CTHULUDON TEST_LEVEL=100 TEST_REVEALED=1
step cross python3 tools/hardcore/test_cross.py /home/claude/scratch/vc.gbc
step b_ui $TB ui TEST_MAP=CHERRYGROVE_CITY TEST_X=17 TEST_Y=8 TEST_MON=TOTODILE TEST_LEVEL=12 TEST_REVEALED=1
step battle_ui python3 tools/hardcore/test_battle_ui.py /home/claude/scratch/ui.gbc
step exp python3 tools/hardcore/test_exp.py /home/claude/scratch/ui.gbc
step b_nf $TB nf TEST_MAP=CHERRYGROVE_POKECENTER_1F TEST_X=3 TEST_Y=3 TEST_MON=TOTODILE TEST_LEVEL=12 TEST_REVEALED=1
step nurse_free python3 tools/hardcore/test_nurse.py /home/claude/scratch/nf.gbc free
step b_np $TB np TEST_MAP=TITHE_POKECENTER1 TEST_X=3 TEST_Y=3 TEST_MON=TOTODILE TEST_LEVEL=12 TEST_REVEALED=1
step nurse_paid python3 tools/hardcore/test_nurse.py /home/claude/scratch/np.gbc paid
step b_run $TB run1 TEST_MAP=TITHE_JUNCTION TEST_X=22 TEST_Y=8 TEST_MON=CTHULUDON TEST_LEVEL=100 TEST_REVEALED=1
step run python3 tools/hardcore/test_run.py /home/claude/scratch/run1.gbc
step b_cg1 $TB cg1 TEST_MAP=CHERRYGROVE_CITY TEST_X=17 TEST_Y=8 TEST_MON=CTHULUDON TEST_LEVEL=60 TEST_REVEALED=1 TEST_ITEMS=1
step whiteout python3 tools/hardcore/test_whiteout.py /home/claude/scratch/cg1.gbc
step worldmap python3 tools/hardcore/test_worldmap.py /home/claude/scratch/cg1.gbc /home/claude/scratch/map/shots 60
read -r WC WX WY <<< "$(python3 tools/hardcore/spawn.py TithePlaza1 grass)"
step b_wa1 $TB wa1 TEST_MAP=$WC TEST_X=$WX TEST_Y=$WY TEST_MON=CTHULUDON TEST_LEVEL=100 TEST_REVEALED=1 TEST_ITEMS=0
step wild python3 tools/hardcore/test_wild.py /home/claude/scratch/wa1.gbc TithePlaza1 40
step split python3 tools/hardcore/test_split.py /home/claude/scratch/wa1.gbc 400
read -r SC SX SY <<< "$(python3 tools/hardcore/spawn.py TithePlaza1 spawn)"
step b_stA $TB stA TEST_MAP=$SC TEST_X=$SX TEST_Y=$SY TEST_MON=CTHULUDON TEST_LEVEL=100 TEST_REVEALED=1
step milestone python3 tools/hardcore/test_story.py milestone /home/claude/scratch/stA.gbc
step hollow python3 tools/hardcore/test_hollow.py /home/claude/scratch/stA.gbc
step cork python3 tools/hardcore/test_cork.py /home/claude/scratch/stA.gbc
step b_stB $TB stB TEST_MAP=NEW_BARK_TOWN TEST_X=10 TEST_Y=10 TEST_MON=CTHULUDON TEST_LEVEL=100 TEST_REVEALED=1 TEST_STORY=2
step newbark python3 tools/hardcore/test_story.py newbark /home/claude/scratch/stB.gbc
step b_gt1 $TB gt1 TEST_MAP=TITHE_JUNCTION TEST_X=19 TEST_Y=20 TEST_MON=CTHULUDON TEST_LEVEL=100 TEST_REVEALED=1
step opening python3 tools/hardcore/test_opening.py /home/claude/scratch/gt1.gbc
step forced python3 tools/hardcore/test_forced.py
step gates_road python3 tools/hardcore/test_gates.py /home/claude/scratch/gt1.gbc road
step b_gt2 $TB gt2 TEST_MAP=TITHE_CATHEDRAL TEST_X=4 TEST_Y=6 TEST_MON=CTHULUDON TEST_LEVEL=100 TEST_REVEALED=1
step gates_area python3 tools/hardcore/test_gates.py /home/claude/scratch/gt2.gbc area
step named_block python3 tools/hardcore/test_named.py /home/claude/scratch/stA.gbc block
step named_rival python3 tools/hardcore/test_named.py /home/claude/scratch/gt1.gbc rival
step b_pg $TB pg TEST_MAP=TITHE_JUNCTION TEST_X=19 TEST_Y=20 TEST_MON=CTHULUDON TEST_LEVEL=100 TEST_REVEALED=1 TEST_ITEMS=1
step purg python3 tools/hardcore/test_purg.py /home/claude/scratch/pg.gbc
step b_stF $TB stF TEST_MAP=JUDECCA_CENTRE TEST_X=4 TEST_Y=17 TEST_MON=DEATHROLL TEST_LEVEL=100 TEST_REVEALED=1 TEST_STORY=2
step ending python3 tools/hardcore/test_story.py ending /home/claude/scratch/stF.gbc
read -r HC HX HY <<< "$(python3 tools/hardcore/hut_spawn.py)"
step b_hut $TB hut1 TEST_MAP=$HC TEST_X=$HX TEST_Y=$HY TEST_MON=CTHULUDON TEST_LEVEL=100 TEST_REVEALED=1 TEST_ITEMS=0
step hut python3 tools/hardcore/test_hut.py /home/claude/scratch/hut1.gbc
step b_endA $TB endA TEST_MAP=JUDECCA_CENTRE TEST_X=4 TEST_Y=17 TEST_MON=DEATHROLL TEST_LEVEL=100 TEST_REVEALED=1 TEST_STORY=2 TEST_FULLDEX=1 TEST_NAME=CHRIS
step fulldex python3 tools/hardcore/test_fulldex.py /home/claude/scratch/endA.gbc
step continuity python3 tools/hardcore/check_continuity.py
step variety python3 tools/hardcore/check_variety.py --quiet
echo "done" >> $V/summary.txt
