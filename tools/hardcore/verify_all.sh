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
step roster python3 tools/hardcore/test_roster.py pokecrystal11.gbc
step category python3 tools/hardcore/test_category.py pokecrystal11.gbc
step intro python3 tools/hardcore/test_intro.py pokecrystal11.gbc
step b_vc $TB vc TEST_MAP=CHERRYGROVE_CITY TEST_X=17 TEST_Y=3 TEST_MON=CTHULUDON TEST_LEVEL=100 TEST_REVEALED=1
step cross python3 tools/hardcore/test_cross.py /home/claude/scratch/vc.gbc
step b_cg1 $TB cg1 TEST_MAP=CHERRYGROVE_CITY TEST_X=17 TEST_Y=8 TEST_MON=CTHULUDON TEST_LEVEL=60 TEST_REVEALED=1 TEST_ITEMS=1
step whiteout python3 tools/hardcore/test_whiteout.py /home/claude/scratch/cg1.gbc
read -r WC WX WY <<< "$(python3 tools/hardcore/spawn.py TithePlaza1 grass)"
step b_wa1 $TB wa1 TEST_MAP=$WC TEST_X=$WX TEST_Y=$WY TEST_MON=CTHULUDON TEST_LEVEL=100 TEST_REVEALED=1 TEST_ITEMS=0
step wild python3 tools/hardcore/test_wild.py /home/claude/scratch/wa1.gbc TithePlaza1 40
step split python3 tools/hardcore/test_split.py /home/claude/scratch/wa1.gbc 400
read -r SC SX SY <<< "$(python3 tools/hardcore/spawn.py TithePlaza1 spawn)"
step b_stA $TB stA TEST_MAP=$SC TEST_X=$SX TEST_Y=$SY TEST_MON=CTHULUDON TEST_LEVEL=100 TEST_REVEALED=1
step milestone python3 tools/hardcore/test_story.py milestone /home/claude/scratch/stA.gbc
step b_stB $TB stB TEST_MAP=NEW_BARK_TOWN TEST_X=10 TEST_Y=10 TEST_MON=CTHULUDON TEST_LEVEL=100 TEST_REVEALED=1 TEST_STORY=2
step newbark python3 tools/hardcore/test_story.py newbark /home/claude/scratch/stB.gbc
step b_pg $TB pg TEST_MAP=TITHE_JUNCTION TEST_X=19 TEST_Y=20 TEST_MON=CTHULUDON TEST_LEVEL=100 TEST_REVEALED=1 TEST_ITEMS=1
step purg python3 tools/hardcore/test_purg.py /home/claude/scratch/pg.gbc
step b_stF $TB stF TEST_MAP=JUDECCA_CENTRE TEST_X=4 TEST_Y=17 TEST_MON=DEATHROLL TEST_LEVEL=100 TEST_REVEALED=1 TEST_STORY=2
step ending python3 tools/hardcore/test_story.py ending /home/claude/scratch/stF.gbc
echo "done" >> $V/summary.txt
