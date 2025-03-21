#!/bin/bash
'atomsk.exe' --create fcc 4.05 Al Al.xsf
'atomsk.exe' Al.xsf -swap X Z Al_swap.xsf
'atomsk.exe' NiAl3-ortho.xsf -swap X Z NiAl3_swap.xsf
for ((i=0;i<=180;i+=1))
do 
    'atomsk.exe' --polycrystal Al_swap.xsf Al-$i.txt Al-$i.lmp;
    'atomsk.exe' Al-$i.lmp -select in box 50 50 50 150 150 150 -rmatom select Al-outbox-$i.lmp;
    'atomsk.exe' --polycrystal NiAl3_swap.xsf Al3Ni-$i.txt Al3Ni-$i.lmp;
    'atomsk.exe' Al3Ni-$i.lmp -select out box 50 50 50 150 150 150 -rmatom select NiAl3-inbox-$i.lmp;
    'atomsk.exe' --merge 2 Al-outbox-$i.lmp Al3Ni-inbox-$i.lmp Al-Al3Ni-$i.lmp;
done
