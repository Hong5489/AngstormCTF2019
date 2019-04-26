# Paper Bin

Description:

defund accidentally deleted all of his math papers! Help recover them from his computer's [raw data](paper_bin.dat).

Author: defund

Doing some basic search for flag
```bash
root@2Real:~/Downloads/AngstromCTF2019/paper_bin# file paper_bin.dat 
paper_bin.dat: data

root@2Real:~/Downloads/AngstromCTF2019/paper_bin# strings paper_bin.dat | grep actf
root@2Real:~/Downloads/AngstromCTF2019/paper_bin#
```

Using `binwalk` we found some intersting thing:
```bash
root@2Real:~/Downloads/AngstromCTF2019/paper_bin# binwalk paper_bin.dat | grep PDF
222           0xDE            PDF document, version: "1.4"
352478        0x560DE         PDF document, version: "1.4"
708830        0xAD0DE         PDF document, version: "1.4"
1081566       0x1080DE        PDF document, version: "1.4"
1446110       0x1610DE        PDF document, version: "1.4"
1790174       0x1B50DE        PDF document, version: "1.4"
2171102       0x2120DE        PDF document, version: "1.4"
2531550       0x26A0DE        PDF document, version: "1.4"
2932958       0x2CC0DE        PDF document, version: "1.4"
3301598       0x3260DE        PDF document, version: "1.4"
3629278       0x3760DE        PDF document, version: "1.4"
4051166       0x3DD0DE        PDF document, version: "1.4"
4411614       0x4350DE        PDF document, version: "1.4"
4739294       0x4850DE        PDF document, version: "1.4"
5066974       0x4D50DE        PDF document, version: "1.4"
5415134       0x52A0DE        PDF document, version: "1.4"
5751006       0x57C0DE        PDF document, version: "1.4"
6082782       0x5CD0DE        PDF document, version: "1.5"
6385886       0x6170DE        PDF document, version: "1.4"
6770910       0x6750DE        PDF document, version: "1.4"
```
Extract using `foremost paper_bin.dat`:
```bash
root@2Real:~/Downloads/AngstromCTF2019/paper_bin# foremost paper_bin.dat 
Processing: paper_bin.dat
|*|
root@2Real:~/Downloads/AngstromCTF2019/paper_bin# ls
output  paper_bin.dat
root@2Real:~/Downloads/AngstromCTF2019/paper_bin# ls output
audit.txt  pdf
root@2Real:~/Downloads/AngstromCTF2019/paper_bin# ls output/pdf
00000000.pdf  00002112.pdf  00004240.pdf  00006448.pdf  00008616.pdf  00010576.pdf  00012472.pdf
00000688.pdf  00002824.pdf  00004944.pdf  00007088.pdf  00009256.pdf  00011232.pdf  00013224.pdf
00001384.pdf  00003496.pdf  00005728.pdf  00007912.pdf  00009896.pdf  00011880.pdf
```
Yay! We got something!

Using `pdftotext` and some bash script we can find the flag easily:
```bash
root@2Real:~/Downloads/AngstromCTF2019/paper_bin# for i in output/pdf/*;do pdftotext $i - | grep actf ;done
actf{proof by triviality}
```

## Flag
> actf{proof_by_triviality}