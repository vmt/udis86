#!/usr/bin/env bash

objdump="otool -tV"
yasm=yasm
asmfile="ud_yasmtest.asm"
binfile="ud_yasmtest.bin"
Sfile="ud_yasmtest.S"
objfile="ud_yasmtest.o"

echo "[bits $1]" > $asmfile
echo $2 >> $asmfile 

$yasm -f bin -o $binfile $asmfile

if [ ! $? -eq 0 ]; then
    echo "error: failed to assemble"
    exit 1
fi

echo "-- hexdump --------------------------------------"
hexdump $binfile
echo

echo "-- objdump --------------------------------------"
hexdump -e '1/1 ".byte 0x%02x\n"' $binfile > $Sfile
gcc -c $Sfile -o $objfile
$objdump -d $objfile
echo

echo "-- udcli (intel) ---------------------------------"
../udcli/udcli -$1 $binfile
echo

echo "-- udcli (at&t) ----------------------------------"
../udcli/udcli -$1 -att $binfile
echo

exit 0
