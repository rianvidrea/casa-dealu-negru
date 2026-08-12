# Zona wellness — analiză și randări

Cod de culoare folosit peste tot: roșu = ușă, bleu = vitraj retractabil,
albastru închis = vitraj fix, negru = perete plin.

---

# Revizia 3 — 8 compartimente, aripa subtiata

Bara est-vest de **19 × 6 m** (BBQ 10 m + piscină 9 m) lipită la capătul de est
de o aripă nord-sud de **6 × 12 m**. 19 + 6 = 25 m, lățimea totală cotată.
Terasa cu jacuzzi iese spre nord pe toată lățimea aripii.

| # | Compartiment | Dimensiuni | Suprafață |
|---|---|---|---|
| 1 | BBQ + bucătărie + masă | 10,0 × 6,0 | 60,0 m² |
| 2 | piscină | 9,0 × 6,0 | 54,0 m² |
| 3 | sala, în L în jurul saunei | 5,0 × 5,0 − sauna | 20,0 m² |
| 4 | hol | 1,0 × 12,0 | 12,0 m² |
| 5 | relaxare | 5,0 × 7,0 − baia | 28,2 m² |
| 6 | saună | 2,5 × 2,0 | 5,0 m² |
| 8 | băi: 2 dușuri, 2 WC, 2 chiuvete | 2,0 × 3,4 | 6,8 m² |
| 7 | terasă jacuzzi (exterior) | 6,0 × 3,0 | 18,0 m² |

Construit sub acoperiș: **186,0 m²** (bara 114 + aripa 72).

## Ce s-a schimbat față de revizia 2

- Bara crește de la 15 la 19 m: BBQ 7 → 10, piscină 8 → 9.
- Aripa se subțiază de la 10 la **6 m** lățime, deci totalul rămâne 25 m.
- Sauna devine o **cabină de 2,5 × 2 m** în colțul de sud-vest al zonei de jos,
  iar sala o înconjoară în L.
- **Sala capătă ușă din hol** — problema principală a reviziei 2, fitness-ul
  fără acces, e rezolvată.
- Jacuzzi-ul are **Ø 4,5 m**, scris cu galben pe schiță.

## Ce iese la verificare

1. **Cada de 4,5 m nu încape pe terasa de 3 m.** Îi trebuie minimum 5 m
   adâncime, plus o margine de circulație. Planul arată punctat subțire
   conturul de care ar fi nevoie. Alternativa e o cadă de Ø 2,4–2,8 m, care
   ține tot 6–8 persoane.
2. **Sala are 20 m² în formă de L** în jurul cabinei de saună. Banda de alergat
   intră pe brațul lung de lângă hol; restul aparatelor merg pe latura vitrată.
   Funcționează, dar e strâmt pentru cinci echipamente.
3. **Sauna de 2,5 × 2 = 5 m²** ține confortabil 4 persoane pe bănci în L, nu 5–6
   cum era cerința inițială. Pentru 6 ar trebui 2,5 × 2,5.
4. **Sauna dă direct în sală.** Ușa ei e pe hol, dar cabina e înconjurată de
   zona de fitness, deci aburul și temperatura ajung lângă aparate. Un mic
   antreu ar izola-o.
5. Rămân valabile: **holul de 1 m** pe 12 m cu cinci uși, **fâșia de 1 m din
   baie** care ține și chiuvetele și circulația, umiditatea piscinei peste
   bucătăria deschisă, lipsa deschiderilor operabile la 3 și 5, și lipsa
   luminii naturale pe hol.
6. **Sala a rămas fără vedere spre piscină** — cerința inițială. E în colțul de
   sud-est, la 14 m de bazin.

## Model 3D

`model/zona_wellness_rev3.obj` + `.mtl`, 1 unitate = 1 metru, construit de
`tools/model_rev3.py` care citeste geometria direct din `plan_compartimente`,
ca planul si modelul sa nu poata pleca unul de la celalalt. Contine pereti
plini si vitrati, compartimentarile interioare, cabina de sauna, acoperisul in
consola de 85 cm, bazinul, terasa cu cada de 4,5 m si mobilierul care face
programul lizibil de sus. Se deschide direct in Blender, SketchUp sau
Twinmotion.

Inaltimi: 3,20 m la streasina, 2,60 m compartimentarile, 2,20 m cabina de
sauna, placa de acoperis de 34 cm.

Randari de masing, cu acelasi renderer software fara dependente
(`python3 tools/render_rev3.py`, in `renders/3d/`):

| Fisier | Cadru |
|---|---|
| `01_aerian_sud_vest.png` | aerian trei sferturi dinspre sud-vest |
| `02_aerian_nord_est.png` | aerian trei sferturi dinspre nord-est |
| `03_de_sus.png` | vedere de sus, cu acoperisul |
| `04_dollhouse.png` | sectiune dollhouse, fara acoperis |
| `05_din_gradina.png` | din gradina, la nivelul ochiului, dinspre sud |
| `06_terasa_jacuzzi.png` | terasa cu jacuzzi, dinspre nord-vest |

Doua variante fotorealiste pornite din cadrul aerian, ca referinta de camera si
geometrie:

| Cadru | Link |
|---|---|
| Aerian sud-vest, dupa-amiaza | [png](https://d8j0ntlcm91z4.cloudfront.net/user_3GRvTxD20RDAOtHRKgeuej8yQei/hf_20260807_205534_1aba58c5-8fe5-429e-b2ee-aa2c60e60676.png) |
| Acelasi cadru, la ora albastra | [png](https://d8j0ntlcm91z4.cloudfront.net/user_3GRvTxD20RDAOtHRKgeuej8yQei/hf_20260807_205534_be835842-8df7-42b1-b81b-c39406305f64.png) |

## Randare

| Cadru | Link |
|---|---|
| Secțiune dollhouse strict de sus, toate cele 8 compartimente | [png](https://d8j0ntlcm91z4.cloudfront.net/user_3GRvTxD20RDAOtHRKgeuej8yQei/hf_20260807_202045_3096f165-98d7-48fc-b521-d48893409e03.png) |

Terasa e randată la 5 m adâncime, ca să încapă cada de 4,5 m.

Planul: `renders/plan_compartimente.svg` și `.png`, din
`tools/plan_compartimente.py`.

---

# Demisolul si planul combinat

Cotate de tine: **latura de 13 m** a camerei de depozitare si a cladirii
existente, cei **4 m** dintre usa camerei tehnice si hol, si diferenta de nivel
de **2,15 m**. Restul cotelor sunt scoase masurand schita fata de conturul
partii de sus si sunt punctate in plan.

CAM. D si casa sunt aliniate la est, pe x = 19 — acolo cade scara si acolo e
usa camerei tehnice.

| Zona | Dimensiuni | Suprafata |
|---|---|---|
| CAM. D — depozitare | 7,0 × 6,0 | 42,0 m² |
| CAM. J — joacă | 6,0 × 9,0 | 54,0 m² |
| fâșia de acces spre CAM. D, cu ușă de garaj | 3,5 × 6,0 | 21,0 m² |
| scara | 4,0 × 1,1 | 4,4 m² |
| clădirea existentă (adâncime estimată) | 13,0 × 6,9 | 89,7 m² |

Demisol, fără fâșia de acces: **96,0 m²**. Parter: 186,0 m².

CAM. D merge 3 m la stânga ușii roșii, deci are 7 m, și se oprește la est pe
x = 19, acolo unde cade scara. CAM. J are 6 × 9 m — stă sub hol, sub băi, sub
sală și sub saună — și atinge CAM. D pe peretele x = 19, deci poate primi ușă.
Casa rămâne la 13 m.

Traseul de iarnă merge casă → cameră tehnică → CAM. D → scară → capătul de sud
al holului de sus, tot pe interior.

## Ce iese la verificare

1. **A — gabaritul demisolului.** 2,15 m diferență de nivel minus 30 cm de
   placă lasă **1,85 m liberi**. O cameră de joacă cu biliard și ping-pong cere
   2,40 m. Soluția: se sapă cu încă 60 cm. Diferența devine 2,75 m, iar scara
   ajunge la 16 trepte de 17,2 cm cu treapta de 26,5 — adică 3,98 m de rampă,
   care încap fix în cei 4 m măsurați. Deasupra lui CAM. D e doar terasa, iar
   deasupra lui CAM. J doar aripa, deci coborârea nu schimbă nimic la parter:
   e numai săpătură.
2. **B — fâșia de acces trece 2,4 m pe sub bazin.** Fâșia e la x 15,1–18,6,
   bazinul la 11,5–17,5. Sub bazin rămân circa 40 cm. Bazinul se mută spre
   vest, la 10,3–16,3, și fâșia rămâne liberă pe toată lățimea.
3. **CAM. J la 54 m² ține toate cele patru funcții, dar la limită.** Biliardul
   cu spațiul de tac în jur cere circa 5,5 × 4,4 m, adică jumătate din cameră;
   ping-pongul încă vreo 15 m², iar canapeaua cu televizorul și fotbalul de
   masă restul. Se poate, dar fără loc de manevră.
4. **Scara iese prin placă în hol**, iar golul ei cade în colțul de nord-vest
   al lui CAM. J — de ținut minte la structură.
3. **Ușa de garaj e pe fațada de nord, la cota demisolului.** Terenul urcă spre
   nord, deci acolo cota naturală e la nivelul parterului — ușa ar fi îngropată
   2 m. Ori se face un decupaj în teren în fața ei, ori ușa e de fapt la cota
   parterului. De lămurit.
4. **Scara ajunge într-un hol de 1 m.** Ar trebui un podest cel puțin cât
   lățimea scării; holul are exact 1,0 m.
5. **Deasupra lui CAM. J stau băile, sauna și sala.** Hidroizolație pe toată
   placa și scurgerile băilor coborâte într-un tavan fals.
6. **Adâncimea clădirii existente (6,9 m) e estimată** din desen, nu cotată.

Planul combinat: `renders/plan_combinat.svg` și `.png`, din
`tools/plan_combinat.py`.

---

# Revizia 2 — 8 compartimente (istoric)

Ansamblul e în L: o bară est-vest de **15 × 6 m** (BBQ 7 m + piscină 8 m) lipită
la capătul de est de o aripă nord-sud de **10 × 12 m**. Terasa cu jacuzzi
iese 3 m spre nord din aripă. Lățimea totală: 25 m.

| # | Compartiment | Dimensiuni | Suprafață | Sursa cotei |
|---|---|---|---|---|
| 1 | BBQ + bucătărie + masă | 7,0 × 6,0 | 42,0 m² | scrisă pe schiță |
| 2 | piscină | 8,0 × 6,0 | 48,0 m² | scrisă pe schiță |
| 3 | fitness | 5,0 × 5,0 | 25,0 m² | 5 m cotat + scădere |
| 4 | hol | 1,0 × 12,0 | 12,0 m² | scrisă pe schiță |
| 5 | relaxare | 9,0 × 7,0 − baia | 56,2 m² | scădere din 12 − 5 |
| 6 | saună (cabină 2,5 × 2,0) | 4,0 × 5,0 | 20,0 m² | 2,5 + 1,5 cotate |
| 8 | băi: 2 dușuri, 2 WC, 2 chiuvete | 2,0 × 3,4 | 6,8 m² | 1 + 1 și 0,9+0,8+0,8+0,9 |
| 7 | terasă jacuzzi (exterior) | 6,0 × 3,0 | 18,0 m² | 6 m cotat |

Construit sub acoperiș: **210,0 m²** (bara 90 + aripa 120).

Baia 8: o fâșie de 1,0 m cu cele două chiuvete, plus patru cabine de 1,0 m
adâncime — duș 90, WC 80, WC 80, duș 90 cm — care dau cei 3,4 m pe lungime.

## Ce s-a schimbat față de revizia 1

- Bara scade de la 18 la 15 m; **fitness-ul iese din bară** și trece în colțul
  de sud-est al aripii. BBQ-ul crește de la 6 la 7 m.
- Aripa crește de la 7 × 12 la **10 × 12 m**; holul se îngustează de la 2 la 1 m.
- Apare **compartimentul 8**, baia, lipită de hol.
- **Piscina capătă ușă directă în hol** — legătura interioară care lipsea în
  revizia 1 e rezolvată. Nu mai trebuie să ieși pe afară ca să ajungi la saună.
- Jacuzzi-ul rămâne exterior, dar acum e la 6 × 3 m, în fața ușii de nord a
  holului.

## Ce iese la verificare

1. **3 nu are ușă desenată.** Fitness-ul e închis între peretele lui 5, peretele
   saunei, fațada de est vitrată fix și fațada de sud. Singurul acces posibil
   rămâne prin 6, adică prin zona umedă a saunei. O ușă din hol nu se poate:
   holul nu atinge fitness-ul. Fie o ușă în peretele dintre 5 și 3, fie holul se
   prelungește 4 m spre est pe latura de sud.
2. **Fitness-ul a pierdut vederea spre piscină**, care era cerința inițială.
   Acum e în colțul opus, la 12 m de bazin, cu vedere doar spre est și sud.
3. **Hol de 1 m** pe 12 m lungime, care deservește cinci uși și e singura
   legătură între piscină și zona umedă. Doi oameni nu se pot încrucișa, iar o
   ușă deschisă îl blochează complet. 1,2–1,4 m ar rezolva, luați din cei 9 m ai
   camerei de relaxare.
4. **Fâșia de 1,0 m din baie** ține chiuvetele *și* circulația spre cabine. La
   1 m, cine se spală pe mâini blochează trecerea. 1,6 m e minimul confortabil.
5. **5 are 56 m²** pentru paturi de relaxare — foarte mult. Din ea se pot lua
   cei 0,4 m pentru hol și cei 0,6 m pentru baie fără să se simtă.
6. **Sauna și jacuzzi-ul rămân la capete opuse**, 12 m de hol între ele.
7. Rămân valabile din revizia 1: umiditatea piscinei peste bucătăria deschisă
   (dezumidificare pe 2, hotă cu evacuare la exterior pe 1), lipsa deschiderilor
   operabile la 3 și 5, și lipsa luminii naturale pe hol.

## Randare

Un singur cadru, în aceeași cheie ca secțiunea dollhouse din revizia 1, cu
planul rev. 2 ca referință de geometrie. Model `nano_banana_pro` (servit ca
`nano_banana_2`), 4K, 3:2, 4 credite.

| Cadru | Link |
|---|---|
| Secțiune dollhouse strict de sus, toate cele 8 compartimente | [png](https://d8j0ntlcm91z4.cloudfront.net/user_3GRvTxD20RDAOtHRKgeuej8yQei/hf_20260807_200419_4c1ad4d8-4f64-4a08-a23a-fbe20eb80fc9.png) |

Planul rev. 2 nu mai e generat; scriptul produce acum rev. 3.

---

# Revizia 1 — 7 compartimente (istoric)

Bară de 18 × 6 m (BBQ 6 + piscină 8 + fitness 4) și aripă de 7 × 12 m (hol 2 m,
relaxare 5 × 7, saună 5 × 5), terasă jacuzzi 7 × 3,5 la nord. 192 m² sub
acoperiș. Fără baie.

Problema principală a acestei reviziei — piscina fără legătură interioară cu
holul — a fost rezolvată în revizia 2.

Zece cadre 4K, 3:2, cu aceeași paletă: stejar deschis, calcar cald, oțel negru
mat, micro-ciment antracit pe peretele de la grătar, tablă fălțuită grafit.

| # | Cadru | Link |
|---|---|---|
| 1 | Secțiune dollhouse, strict de sus | [png](https://d8j0ntlcm91z4.cloudfront.net/user_3GRvTxD20RDAOtHRKgeuej8yQei/hf_20260807_142330_fff3d5be-14da-455c-a4ea-eefc58e1d7c7.png) |
| 2 | Aerian trei sferturi dinspre sud-vest | [png](https://d8j0ntlcm91z4.cloudfront.net/user_3GRvTxD20RDAOtHRKgeuej8yQei/hf_20260807_141446_6b7d8caf-62e8-4f26-87e6-3ff60bc04673.png) |
| 3 | 1 — BBQ și bucătăria pe peretele plin | [png](https://d8j0ntlcm91z4.cloudfront.net/user_3GRvTxD20RDAOtHRKgeuej8yQei/hf_20260807_141446_5fe82261-cd68-4e2d-9576-abd846cfd324.png) |
| 4 | 2 — sala piscinei, vitrajele retrase | [png](https://d8j0ntlcm91z4.cloudfront.net/user_3GRvTxD20RDAOtHRKgeuej8yQei/hf_20260807_141446_82198f19-eaad-4ad2-8e3f-bdb38287a277.png) |
| 5 | 3 — fitness, spre piscină și spre pădure | [png](https://d8j0ntlcm91z4.cloudfront.net/user_3GRvTxD20RDAOtHRKgeuej8yQei/hf_20260807_141446_ec131776-b80f-4803-842c-dad9a52b82dd.png) |
| 6 | 4 — holul, spre terasa cu jacuzzi | [png](https://d8j0ntlcm91z4.cloudfront.net/user_3GRvTxD20RDAOtHRKgeuej8yQei/hf_20260807_141446_88b25bff-bf39-4de7-96d8-3cb0ddfd54c3.png) |
| 7 | 5 — camera de relaxare, colț vitrat | [png](https://d8j0ntlcm91z4.cloudfront.net/user_3GRvTxD20RDAOtHRKgeuej8yQei/hf_20260807_141446_6f108ed9-b43d-464f-a5e5-77405b772d42.png) |
| 8 | 6 — sauna uscată | [png](https://d8j0ntlcm91z4.cloudfront.net/user_3GRvTxD20RDAOtHRKgeuej8yQei/hf_20260807_141446_f350e8dd-02de-4116-9a27-adbff843e700.png) |
| 9 | 7 — jacuzzi-ul exterior la ora albastră | [png](https://d8j0ntlcm91z4.cloudfront.net/user_3GRvTxD20RDAOtHRKgeuej8yQei/hf_20260807_141446_45d45bf3-620e-4753-a26f-8e532b02fd84.png) |
| 10 | Ansamblul noaptea, dinspre grădină | [png](https://d8j0ntlcm91z4.cloudfront.net/user_3GRvTxD20RDAOtHRKgeuej8yQei/hf_20260807_141446_7c0fbc76-23eb-47a0-8095-4c461253077f.png) |

---

Imaginile nu sunt versionate în repo — hostul CDN al Higgsfield nu e accesibil
din sesiunea asta, deci nu au putut fi descărcate local. Link-urile sunt sursa;
se găsesc și în galeria de generări din contul Higgsfield.

Casa existentă nu apare în randări: nicio schiță nu arată unde stă față de zona
nouă.
