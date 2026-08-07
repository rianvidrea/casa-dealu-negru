# Zona wellness cu 7 compartimente — analiză și randări

Schema de pornire este schița de mână cu 7 compartimente. Codul ei de culoare:
roșu = ușă, bleu = vitraj retractabil, albastru închis = vitraj fix, negru =
perete plin.

## Ce am citit din schiță

Ansamblul e în formă de T culcat: o bară lungă est-vest lipită, la capătul de
est, de o aripă nord-sud. Terasa cu jacuzzi stă la nord de aripă, în afara
volumului închis.

| # | Compartiment | Dimensiuni | Suprafață | Sursa cotei |
|---|---|---|---|---|
| 1 | BBQ + bucătărie + masă | 6,0 × 6,0 m | 36,0 m² | cotat pe schiță |
| 2 | piscină | 8,0 × 6,0 m | 48,0 m² | cotat pe schiță |
| 3 | fitness | 4,0 × 6,0 m | 24,0 m² | cotat pe schiță |
| 4 | hol | 2,0 × 12,0 m | 24,0 m² | citit la scară |
| 5 | relaxare | 5,0 × 7,0 m | 35,0 m² | citit la scară |
| 6 | saună | 5,0 × 5,0 m | 25,0 m² | citit la scară |
| 7 | terasă jacuzzi (exterior) | 7,0 × 3,5 m | 24,5 m² | citit la scară |

Construit sub acoperiș: **192,0 m²**. Bara lungă are 18,0 × 6,0 m, aripa
7,0 × 12,0 m.

Închideri, așa cum sunt colorate:

- **1 și 2** — vitraj retractabil pe ambele fațade lungi, nord și sud. Cele
  două compartimente sunt un singur spațiu, fără perete între ele.
- **Peretele de vest al lui 1** — plin. Aici merge gătitul: gratar, blat,
  hotă.
- **3** — vitraj fix pe fațada de nord (spre pădure) și vitraj fix pe peretele
  dinspre piscină. Fațada de sud e plină. Intrarea se face doar din hol.
- **5** — vitraj fix pe nord și pe est, colț vitrat. Fără deschideri operabile.
- **4 și 6** — pereți plini; holul are o ușă la capătul de nord spre terasa
  cu jacuzzi și una pe latura de vest, spre exterior.

Cele 7 uși marcate cu roșu: două din 1 și 2 spre grădină (sud), una la capătul
de nord al holului spre terasa cu jacuzzi, una din hol în fitness, una din hol
spre exterior (vest), una din hol în camera de relaxare, una din hol în saună.

Planul redesenat la scară: `renders/plan_compartimente.svg` și `.png`,
generate cu `tools/plan_compartimente.py`.

## Ce iese la verificare

1. **Piscina nu e legată de hol pe interior.** Peretele dintre 2 și 3 e vitraj
   fix, fără ușă, iar 3 comunică doar cu holul. Ca să ajungi de la piscină la
   saună trebuie să ieși pe ușa de sud a lui 2, să ocolești pe afară și să
   intri prin ușa de vest a holului. Iarna, ud, pe zăpadă. Trei ieșiri:
   o ușă de sticlă în peretele fix 2–3; sau un culoar de 1,5 m pe latura de sud
   a lui 3 (fitness-ul scade la 4,0 × 4,5 m); sau prelungirea holului spre vest
   pe sub aceeași streașină.
2. **Sauna și jacuzzi-ul sunt la capete opuse.** Circuitul obișnuit e saună →
   rece → relaxare → jacuzzi, iar acum sunt 12 m de hol între 6 și 7. Dacă 5 și
   6 se inversează, sauna ajunge lângă ușa de nord și circuitul se scurtează la
   câțiva pași.
3. **Umiditate.** 1 și 2 fiind un singur volum, aburul piscinei ajunge peste
   bucătărie și grăsimea de la grătar ajunge în aerul piscinei. Vara se rezolvă
   cu vitrajele deschise; iarna e nevoie de dezumidificare pe 2 și de hotă cu
   evacuare directă la exterior pe 1.
4. **Ventilație pe 3 și 5.** Ambele au numai vitraj fix, deci nicio deschidere.
   Un panou basculant pe fațada de nord la fiecare, sau ventilație mecanică.
5. **Holul nu are lumină naturală** pe 12 m, în afară de ușa de la capăt.
   Un luminator liniar pe toată lungimea rezolvă și lumina, și senzația de
   tunel la 2 m lățime.
6. **Sauna are nevoie de duș rece lângă ea.** Nu e figurat în schiță; încape
   în colțul lui 6, lângă ușă.
7. **Camera de relaxare are 35 m²** — mult pentru patru paturi. Ori se mai
   adaugă o zonă de ceai și lecturã, ori 1–2 m trec la saună.

Randările de mai jos arată schița exact așa cum e desenată, fără corecțiile de
mai sus.

## Randări

Model `nano_banana_pro`, servit ca `nano_banana_2`. Rezoluție 4K, raport 3:2,
4 credite/imagine — 40 în total. Cadrele 1 și 2 au primit planul la scară drept
referință de geometrie; restul sunt descrieri de spațiu.

Paletă comună întregului set: tavane cu lamele de stejar deschis, pardoseală de
gresie porțelanată gri-cald format mare, profile de oțel negru mat, micro-ciment
antracit pe peretele plin de la BBQ, calcar cald pe aripa de spa, tablă fălțuită
grafit pe acoperiș, accesorii alamă periată.

| # | Cadru | Link |
|---|---|---|
| 1 | Secțiune dollhouse, strict de sus, toate cele 7 compartimente | [png](https://d8j0ntlcm91z4.cloudfront.net/user_3GRvTxD20RDAOtHRKgeuej8yQei/hf_20260807_142330_fff3d5be-14da-455c-a4ea-eefc58e1d7c7.png) |
| 2 | Aerian trei sferturi dinspre sud-vest, cu acoperișul pus | [png](https://d8j0ntlcm91z4.cloudfront.net/user_3GRvTxD20RDAOtHRKgeuej8yQei/hf_20260807_141446_6b7d8caf-62e8-4f26-87e6-3ff60bc04673.png) |
| 3 | 1 — BBQ și bucătăria pe peretele plin, spre piscină | [png](https://d8j0ntlcm91z4.cloudfront.net/user_3GRvTxD20RDAOtHRKgeuej8yQei/hf_20260807_141446_5fe82261-cd68-4e2d-9576-abd846cfd324.png) |
| 4 | 2 — sala piscinei, vitraje retrase, spre fitness | [png](https://d8j0ntlcm91z4.cloudfront.net/user_3GRvTxD20RDAOtHRKgeuej8yQei/hf_20260807_141446_82198f19-eaad-4ad2-8e3f-bdb38287a277.png) |
| 5 | 3 — fitness, cu vedere spre piscină și spre pădure | [png](https://d8j0ntlcm91z4.cloudfront.net/user_3GRvTxD20RDAOtHRKgeuej8yQei/hf_20260807_141446_ec131776-b80f-4803-842c-dad9a52b82dd.png) |
| 6 | 4 — holul, spre ușa de nord și terasa cu jacuzzi | [png](https://d8j0ntlcm91z4.cloudfront.net/user_3GRvTxD20RDAOtHRKgeuej8yQei/hf_20260807_141446_88b25bff-bf39-4de7-96d8-3cb0ddfd54c3.png) |
| 7 | 5 — camera de relaxare, colț vitrat spre pădure | [png](https://d8j0ntlcm91z4.cloudfront.net/user_3GRvTxD20RDAOtHRKgeuej8yQei/hf_20260807_141446_6f108ed9-b43d-464f-a5e5-77405b772d42.png) |
| 8 | 6 — sauna uscată, cabină pentru șase | [png](https://d8j0ntlcm91z4.cloudfront.net/user_3GRvTxD20RDAOtHRKgeuej8yQei/hf_20260807_141446_f350e8dd-02de-4116-9a27-adbff843e700.png) |
| 9 | 7 — jacuzzi-ul exterior la ora albastră | [png](https://d8j0ntlcm91z4.cloudfront.net/user_3GRvTxD20RDAOtHRKgeuej8yQei/hf_20260807_141446_45d45bf3-620e-4753-a26f-8e532b02fd84.png) |
| 10 | Ansamblul noaptea, dinspre grădină, cu vitrajele deschise | [png](https://d8j0ntlcm91z4.cloudfront.net/user_3GRvTxD20RDAOtHRKgeuej8yQei/hf_20260807_141446_7c0fbc76-23eb-47a0-8095-4c461253077f.png) |

Imaginile nu sunt versionate în repo — hostul CDN al Higgsfield nu e accesibil
din sesiunea asta, deci nu au putut fi descărcate local. Link-urile de mai sus
sunt sursa.

Casa existentă nu apare în randări: schița nu arată unde stă față de zona nouă.
Odată fixată poziția ei, cadrele 2 și 10 merită regenerate cu casa în context.
