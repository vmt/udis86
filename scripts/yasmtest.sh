#!/usr/bin/env bash

objdump="otool -tV"
yasm=yasm
asmfile="ud_yasmtest.asm"
binfile="ud_yasmtest.bin"
elffile="ud_yasmtest.elf"

echo "[bits $1]" > $asmfile
echo $2 >> $asmfile 

$yasm -f bin -o $binfile $asmfile && \
$yasm -f elf -o $elffile $asmfile

if [ ! $? -eq 0 ]; then
    echo "error: failed to assemble"
    exit 1
fi

echo "-- hexdump --------------------------------------"
hexdump $binfile
echo

# echo "-- objdump --------------------------------------"
# $objdump -d $elffile
# echo

echo "-- udcli ----------------------------------------"
../udcli/udcli -$1 $binfile

exit 0
