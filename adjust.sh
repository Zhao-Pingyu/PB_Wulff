#!/bin/bash
for i in 148 149 158 162 163 169 55 56 70 71 72 74 76 8 82 83 85 93
do 
	'atomsk.exe' --merge 2 Al-outbox-$i.lmp Al3Ni-inbox-$i-1.lmp Al-Al3Ni-$i.lmp;
done