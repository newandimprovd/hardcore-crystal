#!/bin/bash
# Build a test ROM with _TESTMODE in a scratch copy so the real tree stays untouched.
# usage: testbuild.sh NAME [TEST_MAP=NEW_BARK_TOWN] [TEST_X=6] [TEST_Y=8] [TEST_MON=QUILAVA] [TEST_LEVEL=30] [TEST_BEATEN=0] [TEST_REVEALED=0] [TEST_ITEMS=0] [TEST_STORY=0|1 flooded|2 crater|3 final boss fell]
set -e
NAME=${1:?name}; shift || true
SRC=$(cd "$(dirname "$0")/../.." && pwd)
OUT=${HC_SCRATCH:-/home/claude/scratch}
WORK=$OUT/tb_$NAME
export PATH=/home/claude/bin:$PATH
mkdir -p "$WORK"
tar -C "$SRC" --exclude=.git --exclude='*.gbc' --exclude='*.o' --exclude='*.sym' --exclude='*.map' -cf - . | tar -C "$WORK" -xf -
find "$WORK" -name '*.o' -delete
declare -A V=([TEST_MAP]=NEW_BARK_TOWN [TEST_X]=6 [TEST_Y]=8 [TEST_MON]=QUILAVA [TEST_LEVEL]=30 [TEST_BEATEN]=0 [TEST_REVEALED]=0 [TEST_ITEMS]=0 [TEST_STORY]=0)
for kv in "$@"; do V[${kv%%=*}]=${kv#*=}; done
: > "$WORK/test_config.asm"
for k in TEST_MON TEST_LEVEL TEST_BEATEN TEST_REVEALED TEST_ITEMS TEST_STORY; do echo "DEF $k EQU ${V[$k]}" >> "$WORK/test_config.asm"; done
echo "DEF TEST_SPAWN EQU SPAWN_DEBUG" >> "$WORK/test_config.asm"
printf 'MACRO TEST_SPAWN_ENTRY\n\tspawn %s, %s, %s\nENDM\n' "${V[TEST_MAP]}" "${V[TEST_X]}" "${V[TEST_Y]}" >> "$WORK/test_config.asm"
cd "$WORK"
RGBASMFLAGS="-Weverything -Wtruncation=1 -D _TESTMODE" make -j8 crystal11 > build.log 2>&1 || { tail -30 build.log; exit 1; }
cp pokecrystal11.gbc "$OUT/$NAME.gbc"; cp pokecrystal11.sym "$OUT/$NAME.sym"
echo "built $OUT/$NAME.gbc"
