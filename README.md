# Blood Smear Slide Spreader

Ek 3D-printable jig jo blood smear banane ke kaam aata hai. Base slide (75 × 25 × 1 mm) ek recessed bed mein baithti hai. Carriage rails pe chalta hai aur glass spreader ko 30° pe pakad ke rakhta hai. Carriage aage push karo, smear ban jaata hai.

## Files

| File | Kya hai |
|---|---|
| `spreader_model.py` | Parametric CadQuery model. Saare dimensions aur tolerances upar `PARAMETERS` section mein hain |
| `base.stl` | Base plate, print orientation mein |
| `carriage.stl` | Carriage, print orientation mein (side pe leta hua) |
| `params.json` | Viewer ke liye derived dimensions (script se auto-generate hota hai) |
| `index.html` | three.js viewer |

## Model regenerate karna

```powershell
cd C:\Users\Tanish-Poddar\Downloads\smear-spreader
py -3.14 spreader_model.py
```

Script yeh cheezein check karti hai:
- Min wall ≥ 1.6 mm
- Carriage, base aur dono glass slides ke beech koi interference nahi, travel ke dono ends pe
- Har part ek hi valid solid hai

Koi check fail ho to STL export nahi hoti. CadQuery 2.8 global Python 3.14 (64-bit) mein installed hai, isliye `py -3.14` se chalao. Default `python` 3.15 32-bit hai aur uske liye CadQuery ka wheel nahi hai.

Important parameters:
- `SPREADER_ANGLE`: spreader ka angle
- `SLIDE_L/W/T` aur `SPREADER_L/W/T`: base slide aur spreader slide ke size
- `CLR_SLIDE`: slide bed aur spreader slot ki clearance (0.3)
- `CLR_RAIL`: carriage tongue aur rail groove ki clearance (0.25)
- `BASE_L/W`: base ka size
- `CARRIAGE_H`: carriage ki height

## Viewer

```powershell
cd C:\Users\Tanish-Poddar\Downloads\smear-spreader
python -m http.server 8000
```

Phir browser mein **http://localhost:8000** kholo. `index.html` ko double-click karke `file://` se mat kholna, warna STL load nahi hogi.

## Key dimensions

- **Base:** 100 × 40 × 9 mm. Plate top z = 4 mm. Rails 6.6 mm wide aur 5 mm unche, top pe 45° V-groove (3.0 mm wide, 1.0 mm deep)
- **Slide bed:** 75.6 × 25.6 × 0.8 mm deep. Slide plate se 0.2 mm upar rehti hai taaki spreader glass pe chale. Dono ends pe Ø12 mm finger notch hai, slide nikalne ke liye
- **Carriage:** 37 × 40 mm footprint, rails ke upar 14 mm ka body. 45° V-tongues grooves mein chalte hain, 0.25 mm normal clearance ke saath
- **Spreader slot:** 30° pe, 25.6 × 1.6 mm. Spreader apne weight se slot mein neeche khisak ke base slide pe tikta hai
- **Smear travel:** lagbhag 50 mm (contact X = 34 se 84 mm tak)

## Print settings

| Setting | Base | Carriage |
|---|---|---|
| Material | PLA ya PETG | PLA ya PETG |
| Layer height | 0.2 mm | 0.2 mm (slot/tongue ki accuracy ke liye 0.16 bhi chalega) |
| Walls / perimeters | 3 (1.2 mm) | 3 |
| Top / bottom layers | 5 / 4 | 5 / 4 |
| Infill | 20–25% gyroid | 25–30% gyroid (knob pe push force aata hai) |
| Supports | **Nahi chahiye** | **Nahi chahiye** |
| Orientation | Flat, bottom face bed pe (STL already aise hi hai) | Side pe leta hua, ek cheek bed pe (STL already aise hi hai) |
| Brim | Zaroori nahi | 3–5 mm brim recommended, kyunki part 40 mm ooncha hai |

Orientation ka reason:
- **Base:** groove, slide bed aur notches sab upar ki taraf khule hain, isliye flat print pe koi overhang nahi.
- **Carriage:** side pe print karne se slot, knob aur 30° slope sab bed plane mein aa jaate hain. Tongues ki 45° walls bina support print hoti hain, aur slot ki chhat sirf 1.6 mm ka bridge hai.

Material ke notes:
- **PLA:** sabse accurate aur aasaan.
- **PETG:** alcohol/disinfectant wipe zyada achhe se sehta hai aur kam brittle hai. Lekin thoda zyada ooze karta hai, isliye elephant-foot compensation (0.1–0.2 mm) on rakho, warna groove/tongue tight ho sakte hain.

Fit tuning:
- Carriage tight chale to `CLR_RAIL` 0.3 karo.
- Spreader slot mein atke to `CLR_SLIDE` 0.35–0.4 karo.
- Phir script dobara chalao.

## Use kaise karein

1. Base slide ko bed mein rakho.
2. Carriage ko rail ke pichhle end se slide karke andar daalo.
3. Spreader slide ko slot mein upar se daalo. Woh khud neeche khisak ke base slide pe tik jaayega.
4. Blood drop spreader ke peeche wale wedge mein rakho. Drop ko spreader edge pe phailne do.
5. Knob se carriage ko ek smooth motion mein aage push karo.

> Lab safety: blood samples ke saath gloves pehno. Use ke baad parts aur glass ko lab protocol ke hisaab se disinfect karo.
