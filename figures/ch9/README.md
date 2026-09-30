# Bölüm 9 (Viscous Fluids) figürleri: ev stili v3

Notların 9. bölümündeki sekiz figür (A–H), `figures/` altındaki ders
figürlerinin (fig01–fig10) Springer "Engineering Mechanics" görünümüyle
çizildi. Ölçek **R10**: 10 pt gövde metni, en fazla 100 mm genişlik,
etiketler 10 pt Computer Modern. Nota `scale=1.728` ile konur (not 17,28 pt).
Figürlerdeki bütün yazılar İngilizce. Vektörler, notun metniyle aynı
biçimde **alt-tilde** ile yazılır (`\FigVec`).

## 1. Dosyalar

```
figures/ch9/
├─ README.md
├─ figstyle9.tex          ev stili v3: palet, 1:2:4 çizgi kademesi, ok uçları, etiket stilleri
├─ fs9geom.py             ortak geometri yardımcıları (nokta boşlukları, yaylar, \def yazıcı)
├─ fscheck9.py            PDF denetimi: etiket–çizgi ve etiket–etiket >= 1,5 pt, çıplak ok ucu, genişlik
├─ make_ch9.py            derleme: geometri -> sarmalayıcı -> pdflatex -> denetim -> png/ ve svg/
├─ ch9X_body.tex          figür gövdesi (yorumsuz)
├─ ch9X_geom.py           geometri üreticisi -> ch9X_geom.tex (B dışında hepsi)
├─ ch9X.tex               sarmalayıcı (make_ch9.py yazar, elle düzenlemeyin)
├─ ch9X.pdf               TESLİM: vektör PDF, R10
├─ png/ch9X.png           300 dpi önizleme
└─ svg/ch9X.svg           web sürümü için SVG (glifler vektör yol)
```

## 2. Stil değerleri

`style/v3/` bu repoda olmadığı için değerler `fig05`–`fig10` PDF'lerinden
ölçülerek `figstyle9.tex` içine yeniden kuruldu:

| Öğe | Değer |
|---|---|
| Çizgiler | ince 0,354 pt, orta 0,709 pt, kalın 1,417 pt; tarama 0,25 pt (%55 gri) |
| Gerilme/kuvvet oku | kırmızı (255,0,0), gövde 0,709 pt, uç çekirdeği 8,29 × 3,84 pt, uç konturu 0,354 pt |
| Eksen | mavi (0,0,255), 0,354 pt, uç çekirdeği 4,59 × 2,15 pt |
| Açı, ölçü etiketi | yeşil çizgi (0,176,0), yazı (0,140,0) |
| Geometri, vektör | siyah; eleman dolgusu 0,85, cisim dolgusu 0,90 |
| Gizli/ilk durum kenarı | 0,354 pt, kesikli 2,6 / 1,9 pt |
| Yasak bölge dolgusu | pembe (255,226,226) |
| Formül kutusu | lavanta (199,196,226) |
| Nokta | içi boş daire, 2,8 pt, 0,354 pt kontur; ona değen çizgiler 0,3 pt boşlukla başlar |

## 3. Derleme

```bash
cd figures/ch9
python make_ch9.py                    # sekiz figür, denetim, 300 dpi PNG, SVG
python make_ch9.py ch9a_frames        # yalnız seçilen figür
python make_ch9.py --dpi 600          # daha keskin önizleme
```

Gerekenler: `pdflatex`, `pdftocairo` (poppler-utils), Python 3 ile
`numpy scipy pillow pymupdf`. Bir figür derlenmez ya da denetimden geçmezse
betik 1 koduyla çıkar. Son derleme 0 koduyla bitti: 8 PDF'in 8'i geçti, en
küçük etiket boşluğu 1,59 pt (ch9h).

Denetim mürekkep üzerinden yapılır: etiketler tek başına 1200 dpi'da
basılır (çizgiler sayfadan silinerek), çizgiler vektör yollarından gerçek
kalınlıklarıyla rasterleştirilir; fontun kutusu değil, gerçek glif izi
ölçülür. Kesir çizgileri (0,4 pt TeX kuralı) etiketin parçası sayılır.

## 4. Figürler

| Figür | Dosya | İçerik | R10 boyutu (mm) |
|---|---|---|---|
| A | `ch9a_frames` | x⁺, x₁, x₂: O⁺'nın uzayında iki yerleşim (a), O'nun uzayında iki okuma (b) | 91,3 × 43,8 |
| B | `ch9b_hinge` | (9.9)–(9.10) diyagramı: O⁺ menteşe, alt ok Ψ = Φ₂⁻¹∘Φ₁ | 95,6 × 67,5 |
| C | `ch9c_spin` | (9.18)–(9.20): dönen çerçeve spini siler, gerinme hızını değil | 97,6 × 37,7 |
| D | `ch9d_coaxial` | D ile G(D) aynı asal eksenlerde; asal yüzlerde kayma yok | 95,1 × 29,2 |
| E | `ch9e_rays` | (9.64)–(9.68) ve (9.71)–(9.72): "her w için" ve "her D için" | 97,9 × 36,8 |
| F | `ch9f_viscosity` | Hacimsel ve kayma deney hareketleri, κ ve μ | 74,8 × 38,3 |
| G | `ch9g_couette` | Problem 6(a): Couette–Poiseuille profilleri, Π = −2, 0, 2, 4 | 57,3 × 39,4 |
| H | `ch9h_annulus` | Problem 8: halka kesiti (a) ve v_θ(r) profilleri (b) | 97,6 × 45,8 |
