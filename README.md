# Blood Smear Slide Spreader

Ek 3D-printable jig jo blood smear banane ke kaam aata hai. Base slide (75 × 25 × 1 mm) ek recessed bed mein baithti hai. Carriage rails pe chalta hai aur glass spreader ko **45°** pe pakad ke rakhta hai. Carriage aage push karo, smear ban jaata hai.

Carriage base mein **captive** hai:
- **Uth nahi sakta:** carriage ke dovetail-T tongues rails ki undercut grooves mein phanse rehte hain.
- **Aage nahi nikal sakta:** groove aage se band hai (end stop).
- **Peeche nahi nikal sakta:** wahan ek removable pin lagta hai.

**Live viewer:** https://tanisheesh.github.io/smear-spreader/

## Files

| File | Kya hai |
|---|---|
| `spreader_model.py` | Parametric CadQuery model. Saare dimensions aur tolerances upar `PARAMETERS` section mein hain |
| `base.stl` | Base plate, print orientation mein |
| `carriage.stl` | Carriage, print orientation mein (side pe leta hua) |
| `params.json` | Viewer ke liye derived dimensions (script se auto-generate hota hai) |
| `index.html` | three.js viewer, phone pe bhi chalta hai |

## Model regenerate karna

```powershell
cd C:\Users\Tanish-Poddar\Downloads\smear-spreader
py -3.14 spreader_model.py
```

Script STL export karne se pehle yeh check karti hai:
- Min wall ≥ 1.6 mm
- Carriage, base, pins aur dono glass slides ke beech koi interference nahi, travel ke dono ends pe
- Captive fit: carriage upar uthane pe base se takraata hai, aur pin aur front stop dono ends pe carriage ko rokte hain
- Har part ek hi valid solid hai

Koi check fail ho to STL export nahi hoti.

CadQuery 2.8 global Python 3.14 (64-bit) mein installed hai, isliye `py -3.14` se chalao. Default `python` 3.15 32-bit hai aur uske liye CadQuery ka wheel nahi hai.

Important parameters:
- `SPREADER_ANGLE`: spreader ka angle (abhi 45)
- `SLIDE_L/W/T` aur `SPREADER_L/W/T`: base slide aur spreader slide ke size
- `CLR_SLIDE`: slide bed aur spreader slot ki clearance (0.3)
- `CLR_RAIL`: tongue aur groove ki clearance (0.25)
- `GROOVE_*`: groove ki shape
- `PIN_*`: stop pin ka size aur jagah
- `BASE_L/W`: base ka size

## Viewer locally chalana

```powershell
python -m http.server 8000
```

Phir browser mein **http://localhost:8000** kholo. `index.html` ko `file://` se mat kholna, warna STL load nahi hogi.

## Key dimensions

- **Base:** 100 × 44 × 9 mm.
  - Pehle 40 mm thi. Captive groove ke undercut ke saath dono taraf 1.6 mm wall rakhne ke liye 4 mm badhani padi.
  - Plate top z = 4 mm.
- **Rails:** 8.6 mm wide, plate se 5 mm unche.
- **Groove (dovetail-T):**
  - Upar 2.6 mm ka neck, 1.6 mm ka lip.
  - Lip ke neeche 45° pe 5.4 mm tak chaudi hoti hai. Total depth 3.0 mm.
  - Aage ke end pe 4 mm band hai (end stop).
- **Carriage tongue:** groove se har face pe 0.25 mm chhota. Lip ke neeche har taraf 0.8 mm phansa rehta hai. Upar uthane ki koshish karo to 0.35 mm ke baad atak jaata hai.
- **Stop pins:**
  - 1.75 mm filament ke do tukde, har ek ~11 mm lamba.
  - Peeche ke end se 4 mm pe groove floor mein Ø1.8 × 3 mm ke hole mein jaate hain.
  - Printed hole aam taur pe ~0.1 mm chhota banta hai, isliye pin halka daba ke andar jaata hai aur base ulta karne pe bhi nahi girta.
  - Pin rail ke upar ~5 mm bahar rehta hai, kheenchne ke liye.
- **Slide bed:**
  - 75.6 × 25.6 × 0.8 mm deep.
  - Slide plate se 0.2 mm upar rehti hai, taaki spreader glass pe chale.
  - Dono ends pe Ø12 mm finger notch hai, slide nikalne ke liye.
- **Spreader slot:** 45° pe, 25.6 × 1.6 mm. Spreader apne weight se neeche khisak ke base slide pe tikta hai. Slot ki dheel se angle lagbhag ±1.5° hil sakta hai.
- **Smear travel:** lagbhag 48 mm (contact X = 36 se 84.5 mm).

## Print settings

| Setting | Base | Carriage |
|---|---|---|
| Material | PLA ya PETG | PLA ya PETG |
| Layer height | 0.2 mm | 0.2 mm (tongue ki accuracy ke liye 0.16 behtar) |
| Walls / perimeters | 3 (1.2 mm) | 3 |
| Top / bottom layers | 5 / 4 | 5 / 4 |
| Infill | 20–25% gyroid | 25–30% gyroid (knob pe push force aata hai) |
| Supports | **Nahi chahiye** | **Nahi chahiye** |
| Orientation | Flat, bottom face bed pe (STL already aise hi hai) | Side pe leta hua, ek cheek bed pe (STL already aise hi hai) |
| Brim | Zaroori nahi | 3–5 mm brim recommended, kyunki part 44 mm ooncha hai |

Orientation ka reason:
- **Base:** groove ka undercut 45° overhang hai, isliye bina support print hota hai. Pin holes vertical hain.
- **Carriage:** side pe print karne se slot, knob aur tongue ki profile sab bed plane mein aa jaati hai. Tongue ke 45° faces bina support print hote hain, aur slot ki chhat sirf 1.6 mm ka bridge hai.

Material ke notes:
- **PLA:** sabse accurate aur aasaan.
- **PETG:** disinfectant wipe zyada achhe se sehta hai aur kam brittle hai. Lekin elephant-foot compensation (0.1–0.2 mm) on rakho, warna tongue groove mein tight ho sakta hai.

Fit tuning:
- Carriage tight chale to `CLR_RAIL` 0.3 karo.
- Spreader slot mein atke to `CLR_SLIDE` 0.35–0.4 karo.
- Phir script dobara chalao.

## Assembly

1. Base slide ko bed mein rakho.
2. Carriage ke tongues ko rails ke **peeche wale end** (jahan pin holes hain) se grooves mein daalo aur aage slide karo.
3. 1.75 mm filament ke do ~11 mm tukde kaato. Cutter se seedha kaato, taaki sira chapta rahe.
4. Har tukda pin hole mein seedha neeche dabao, jab tak hole ke floor tak na baith jaaye. Ungli se ho jaayega. Tight lage to pliers se pakad ke halka ghuma ke dabao.
   - Ab carriage na uth sakta hai, na kisi end se nikal sakta hai.
5. **Pins nikalna:**
   1. Spreader glass ko slot se upar nikaal lo.
   2. Carriage ko thoda aage khisakao, taaki pins ke paas jagah ho.
   3. Pin ka bahar nikla ~5 mm sira ungli, tweezer ya chhote pliers se pakdo.
   4. Halka ghuma ke seedha upar kheencho.
   - Phir carriage peeche se bahar slide ho jaayega. Pin dobara use ho sakta hai, ya naya tukda kaat lo, filament sasta hai.
6. **Agar hole bahut tight print hua** aur pin andar na jaaye:
   - Ek 1.8 mm drill bit hole mein haath se ghuma do.
   - Ya filament ke sire ko sandpaper se halka patla kar do.
   - Agar bahut dheela ho to pin daalne ke baad upar ka sira lighter se halka garam karke L ki shape mein mod do.

## Use kaise karein

1. Carriage ko peeche pin tak le jaao.
2. Spreader slide ko slot se upar nikaal lo.
3. Carriage ke aage wale edge ke theek neeche base slide pe blood drop rakho.
4. Spreader wapas slot mein daalo. Woh khud neeche khisak ke drop ke theek aage slide pe tikega, aur blood uske edge pe phail jaayega.
5. Knob se carriage ko ek smooth motion mein aage push karo.

> Lab safety: blood samples ke saath gloves pehno. Use ke baad parts aur glass ko lab protocol ke hisaab se disinfect karo.
