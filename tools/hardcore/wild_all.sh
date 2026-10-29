#!/bin/bash
# Builds a test ROM per area (player on the plaza floor west of the east grass patch) and runs test_wild.py on it.
# usage: wild_all.sh [1 2 3 4 5]   logs: /home/claude/scratch/wildN.log, summary: /home/claude/scratch/wild_all.summary
cd "$(dirname "$0")/../.."
declare -A PL=([1]="TITHE_PLAZA1 TithePlaza1" [2]="GROVE_PLAZA4 GrovePlaza4" [3]="AXIOM_PLAZA4 AxiomPlaza4" [4]="LOTUS_PLAZA4 LotusPlaza4" [5]="DIS_PLAZA4 DisPlaza4")
for n in ${@:-1 2 3 4 5}; do
  read -r CONST NAME <<< "${PL[$n]}"
  ./tools/hardcore/testbuild.sh wa$n TEST_MAP=$CONST TEST_X=12 TEST_Y=12 TEST_MON=CTHULUDON TEST_LEVEL=100 TEST_REVEALED=1 TEST_ITEMS=0 > /home/claude/scratch/wild$n.log 2>&1
  python3 tools/hardcore/test_wild.py /home/claude/scratch/wa$n.gbc $NAME 40 >> /home/claude/scratch/wild$n.log 2>&1
  echo "area $n $NAME: $(tail -2 /home/claude/scratch/wild$n.log | tr '\n' ' ')" >> /home/claude/scratch/wild_all.summary
done
