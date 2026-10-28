#!/bin/bash
# Builds a god-mode test ROM per area and runs the full walker on it, one after the other (two CPUs only).
# usage: walk_all.sh [1 2 3 4 5]   logs: /home/claude/scratch/walkN.log, summary at the end of each
cd "$(dirname "$0")/../.."
declare -A START=([1]="TITHE_PLAZA1 6 4 TithePlaza1" [2]="GROVE_PLAZA1 3 4 GrovePlaza1" [3]="AXIOM_PLAZA1 3 4 AxiomPlaza1" [4]="LOTUS_PLAZA1 3 4 LotusPlaza1" [5]="DIS_PLAZA1 3 4 DisPlaza1")
for n in ${@:-1 2 3 4 5}; do
  read -r MAP X Y NAME <<< "${START[$n]}"
  ./tools/hardcore/testbuild.sh w$n TEST_MAP=$MAP TEST_X=$X TEST_Y=$Y TEST_MON=CTHULUDON TEST_LEVEL=100 TEST_REVEALED=1 TEST_ITEMS=0 > /home/claude/scratch/walk$n.log 2>&1
  WALK_GOD=1 SHOTS=/home/claude/scratch/walk$n python3 tools/hardcore/test_walk.py /home/claude/scratch/w$n.gbc auto:$NAME >> /home/claude/scratch/walk$n.log 2>&1
  echo "area $n: $(tail -2 /home/claude/scratch/walk$n.log | tr '\n' ' ')" >> /home/claude/scratch/walk_all.summary
done
