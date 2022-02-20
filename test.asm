
$MV(@R1,10)
$MV(@i, 1) // postavljamo varijablu i
$MV(@R0, 0) // postavljamo R0 na 0
$MV(@d, 1) // postavljamo varijablu d
$WHILE(@d) // dok varijabla d nije 0 radi  
{
$ADD(@R0, @R0, @i) // uvecaj R0 za i
$ADD(@i, @i, 1) // uvecaj i za 1
$SUB(@d, @R1, @i) // provjera
}