# Casa Dealu Negru — concept wellness

## Schema curentă: 7 compartimente

Varianta de lucru actuală vine din schița de mână cu 7 compartimente — BBQ,
piscină, fitness, hol, relaxare, saună și terasa cu jacuzzi. Analiza schiței,
suprafețele, problemele găsite și randările fotorealiste sunt în
[`renders_hf/README_compartimente.md`](renders_hf/README_compartimente.md).
Planul redesenat la scară: `renders/plan_compartimente.svg` și `.png`.
Modelul 3D: `model/zona_wellness_rev3.obj`, cu randări de masing în
`renders/3d/`.

```bash
python3 tools/plan_compartimente.py   # planul parterului, SVG + PNG
python3 tools/plan_combinat.py        # planul combinat demisol + parter
python3 tools/model_rev3.py           # modelul 3D, OBJ + MTL
python3 tools/render_rev3.py          # cele sase cadre din renders/3d/
```

## Studiul anterior

Randări ale modelului schematic de masing `model/concept_wellness.obj`.
Schema de mai jos e anterioară celei cu 7 compartimente și nu mai reflectă
împărțirea curentă.

## Ce conține modelul

| Volum | Amprentă | Înălțime streașină | Coamă | Material |
|---|---|---|---|---|
| Zona de distracție | 11,20 × 3,70 m — 41,4 m² | 3,00 m | 4,80 m | lemn deschis |
| SPA | 4,40 × 7,40 m — 32,6 m² | 3,40 m | 5,60 m | piatră |
| Garaj | 4,80 × 8,30 m — 39,8 m² | 3,20 m | 5,30 m | lemn închis |
| Casa existentă (context) | 11,90 × 7,70 m — 91,6 m² | 6,00 m | 8,40 m | volum transparent |

Amenajări: terasă 6,50 × 4,20 m (27,3 m²), piscină exterioară 2,60 × 4,20 m
(10,9 m²), alee pavată 13,45 × 2,20 m (29,6 m²).

Vitraje: bandă de 9,80 × 1,86 m pe fațada sud a zonei de distracție și
6,20 × 2,10 m pe fațada dinspre curte a SPA-ului.

Amprentă nouă construită: **113,8 m²**; împreună cu casa existentă: 205,4 m².

Cele trei corpuri noi se așază în jurul casei existente: zona de distracție
în sud, deschisă cu banda de vitraj spre terasă; SPA-ul în est, cu vitrajul
orientat spre curtea interioară în care stă piscina; garajul retras spre vest,
legat de casă prin aleea pavată.

## Randări

| Fișier | Cadru |
|---|---|
| `renders/01_ansamblu_sud_est.png` | ansamblu dinspre sud-est |
| `renders/02_ansamblu_nord_vest.png` | ansamblu dinspre nord-vest, cu garajul |
| `renders/03_terasa.png` | din grădină, spre terasă și zona de distracție |
| `renders/04_curte_piscina.png` | de pe aleea pavată, spre piscină și SPA |
| `renders/05_perspectiva_sud_est.png` | perspectivă de la nivelul ochiului |
| `renders/06_plan_de_situatie.png` | plan de situație |

## Cum se regenerează

```bash
python3 tools/render_obj.py
```

`tools/render_obj.py` este un renderer software scris de la zero, fără
dependențe în afara bibliotecii standard: proiecție perspectivă cu z-buffer,
decupare la planul apropiat, lumină directională plus cer emisferic, umbre
proiectate pe teren (înfășurătoarea convexă a fiecărui volum), ceață
atmosferică după adâncime și supraeșantionare 2×. Vegetația este generată
procedural în renderer și nu face parte din modelul OBJ.

Cadrele sunt definite în dicționarul `VIEWS`; cele marcate `fit=True` își
calculează singure distanța camerei astfel încât modelul să încapă în cadru.
