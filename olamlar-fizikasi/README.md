# «Olamlar fizikasi» — kitob uchun rasmlar

Topshiriqdagi 19 ta rasm, kitobdagi raqamlanish bo‘yicha.

| Papka / fayl | Nima bor |
|---|---|
| `svg/rasm_X-Y.svg` | Vektor asl nusxa. Ikki qatlam: **rasm** va **yozuvlar** (yozuvlar tahrirlanadigan matn). |
| `png/rasm_X-Y.png` | 300 dpi rastr nusxa (to‘liq kenglik — 1323 px). |
| `olamlar_fizikasi_rasmlar_maket.pdf` | Har bir rasm A5 sahifada haqiqiy o‘lchamda, kitobdagi izohi bilan. |
| `olamlar_fizikasi_rasmlar_oq-qora.pdf` | O‘sha maket oq-qora ko‘rinishda — bosmani tekshirish uchun. |
| `generator/` | Rasmlarni chizgan dastur (Python + Chromium). |

## O‘lchamlar

| Rasm | O‘lcham (eni × bo‘yi) |
|---|---|
| 2.1, 4.1 | 112 × 50 mm |
| 2.2, 3.1, 4.4, 5.1, 5.3 | 112 × 70 mm |
| 3.2, 4.2, 6.3 | 112 × 60 mm |
| 6.2 | 112 × 55 mm |
| 6.1 | 112 × 112 mm (to‘liq kenglik, kvadrat) |
| 2.3, 3.3, 3.4, 4.3, 6.4 | 54 × 54 mm (yarim kenglik, kvadrat) |
| 2.4 | 54 × 76 mm (yarim kenglik, ikki qism ustma-ust) |
| 5.2 | 54 × 64 mm |

## Uslub

- Palitra: to‘q ko‘k `#1F3A5F`, oltinrang `#A67C2E`, och qaymoq `#F3EEE3`, kulrang tuslar.
  Yagona urg‘u rangi — terrakota `#B8553A` (barcha rasmlarda bir xil).
- Asosiy chiziq — 0,75 pt. Faqat to‘r va tekstura chiziqlari (setka, to‘lqin
  frontlari, Kalabi–Yau to‘ri) ingichkaroq, 0,4–0,5 pt.
- Shrift: Arial / Helvetica (8–9 pt). Yozuvlarda o‘, g‘ — kitob matnidagi kabi `‘` belgisi bilan.
- Hamma rasm oq-qora bosmada tekshirildi (`..._oq-qora.pdf`). 6.2 dagi rang shkalasi
  yorqinlik bo‘yicha bir tomonga o‘sadi: oq-qorada ham «sovuq — to‘q, issiq — och» bo‘lib qoladi.

## Topshiriqdan farqlar va izohlar

- **2.1** — asosiy 6 siluet orasida xira oraliq siluetlar bor: ular vaqt bo‘ylab uzluksiz «lenta» hosil qiladi.
- **2.3** — EHT suratidan nusxa ko‘chirilmagan, o‘z chizmamiz. Asl EHT suratini ishlatsangiz:
  CC BY 4.0, manba — «EHT Collaboration».
- **3.4** — «bir atom qalinlikda» yozuvini aniq ko‘rsatish uchun pastga varaqning yon tomondan
  ko‘rinishi (bir qator atom) qo‘shildi.
- **4.1** — uchlar soni «1 ta uch», «2 ta uch», … ko‘rinishida yozilgan. Tesseraktda 16 ta uch va
  32 ta qirra borligi dasturda tekshiriladi.
- **4.3** — kvintik Kalabi–Yau kesimi tenglamalardan (n = 5, 25 ta bo‘lak) hisoblab chizilgan;
  boshqa rasmdan ko‘chirilmagan.
- **5.1** — ixtiyoriy pastki lenta (10, 100, 10 000 elektron) qo‘shilgan. Ekrandagi yo‘llar
  va punktir «yorug‘ yo‘nalishlar» aniq yo‘l farqi bo‘yicha hisoblangan.
- **5.3** — «vaqt →» matn sifatida berilgan (tahrirlash oson bo‘lsin).
- **6.2** — tasodifiy izotrop maydon, Mollveyde proyeksiyasi; ESA Planck xaritasidan nusxa emas.
- Topshiriqda avval qora qalamda eskiz so‘ralgan edi. Bu yerda darhol rangli variantlar tayyorlandi;
  ilmiy aniqlikni tekshirib, izohlarni bering — tuzatish oson.

## Blender varianti (9 ta rasm)

Hajmli mavzudagi 9 ta rasm qo‘shimcha ravishda Blender’da (Cycles) ham yaratildi:
**2.2, 2.4, 3.2, 3.4, 4.1, 4.3, 4.4, 6.3, 6.4**.

| Papka / fayl | Nima bor |
|---|---|
| `blender/svg/` | Render rasm «rasm» qatlamida, yozuvlar alohida «yozuvlar» qatlamida (tahrirlanadigan matn). |
| `blender/png/` | Yozuvlari bilan, 300 dpi. |
| `blender/render/` | Yozuvsiz toza render, 300 dpi. |
| `blender/blend/` | Blender sahnalari — kamera, yorug‘lik va ranglarni o‘zingiz o‘zgartirishingiz mumkin. |
| `olamlar_fizikasi_rasmlar_maket_blender.pdf` | Maket: shu 9 rasm Blender variantida, qolgan 10 tasi vektor. |
| `olamlar_fizikasi_rasmlar_oq-qora_blender.pdf` | O‘sha maketning oq-qora ko‘rinishi. |

E’tiborga oling:
- Blender rasmlari rastr (300 dpi) va yumshoq soyali hajmli uslubda. Topshiriqdagi «tekis vektor
  uslubi» talabidan farq qiladi — qaysi variantni tanlash muallifning ixtiyorida.
- Qolgan 10 rasm (2.1, 2.3, 3.1, 3.3, 4.2, 5.1, 5.2, 5.3, 6.1, 6.2) mohiyatan tekis sxema yoki
  xarita, shuning uchun ular faqat vektor variantda. Masalan, 3.1 da figuralar «mutlaqo yassi» bo‘lishi shart.
- Unsplash ishlatilmadi: topshiriqning 6-bandi internetdagi rasmlarni, 3-bandi esa fotorealizmni taqiqlaydi.

Qayta yaratish: `pip install bpy` (Blender 5.3, Python 3.13), so‘ng
`cd blender && python3 bl_rasmlar.py 2-2 2-4 3-2 3-4 4-1 4-3 4-4 6-3 6-4`.

## Qayta yaratish

```bash
cd generator
pip install numpy scipy matplotlib pillow
for c in 2 3 4 5 6; do python3 rasm$c.py; done   # svg/
node render.js                                  # png/ (Playwright + Chromium)
node maket.js && node maket.js --oq-qora        # PDF maketlar
```
