# Notların figürleri: ortak ev stili v3

Notların bütün bölüm figürleri (`figures/chN/`) buradaki tek stil ve tek
araç takımıyla çizilir. Görünüm, `figures/` altındaki ders figürlerinin
(fig01–fig10) Springer "Engineering Mechanics" görünümüdür. Ölçek **R10**:
10 pt Computer Modern etiketler, en fazla 100 mm genişlik. Nota
`\includegraphics[scale=1.728]` ile konur (not 17,28 pt). Figürlerdeki
bütün yazılar İngilizce; vektörler notun metniyle aynı biçimde
**alt-tilde** ile yazılır (`\FigVec`).

## 1. Dosyalar

```
figures/common/
├─ README.md
├─ figstyle.tex   palet, 1:2:4 çizgi kademesi, ok uçları, etiket stilleri
├─ fsgeom.py      geometri yardımcıları (nokta boşlukları, yaylar, \def yazıcı, ev kamerası)
├─ fscheck.py     PDF denetimi: etiket–çizgi ve etiket–etiket >= 1,5 pt, çıplak ok ucu, genişlik
└─ make.py        derleme: geometri -> sarmalayıcı -> pdflatex -> denetim -> png/ ve svg/

figures/chN/
├─ README.md               bölümün figür tablosu
├─ <ad>_body.tex           figür gövdesi (yorumsuz)
├─ <ad>_geom.py            geometri üreticisi -> <ad>_geom.tex (gerekiyorsa)
├─ <ad>.tex                sarmalayıcı (make.py yazar, elle düzenlemeyin)
├─ <ad>.pdf                TESLİM: vektör PDF, R10
├─ png/<ad>.png            300 dpi önizleme
└─ svg/<ad>.svg            web sürümü için SVG (glifler vektör yol)
```

Adlandırma: kitabın Şekil N.k'sine karşılık gelen figür `chN_fKK_<kısa-ad>`
(ör. `ch2_f05_twoinstants`), notun kendi eklediği harfli figür
`chN<harf>_<kısa-ad>` (ör. `ch9a_frames`).

## 2. Stil değerleri

Değerler ders figürlerinin (fig05–fig10) PDF'lerinden ölçüldü.

| Öğe | Değer |
|---|---|
| Çizgiler | ince 0,354 pt, orta 0,709 pt, kalın 1,417 pt; tarama 0,25 pt (%55 gri) |
| Gerilme, kuvvet, yük oku | kırmızı (255,0,0), gövde 0,709 pt, uç 9,3 × 4,2 pt (`fs stress`) |
| Eksen | mavi (0,0,255), 0,354 pt, küçük uç (`fs axis`); etiketi mavi |
| Açı, ölçü, birim normal | yeşil çizgi (0,176,0), yazı (0,140,0) |
| Geometri, vektör | siyah; vektör 0,709 pt, orta uç (`fs vec`) |
| Dolgular | cisim 0,90 gri, eleman 0,85, kesit yüzü 0,95; yasak/yük bölgesi pembe (255,226,226) |
| Gizli/ilk durum kenarı | 0,354 pt, kesikli 2,6 / 1,9 pt (`fs hidden`) |
| Formül kutusu | lavanta (199,196,226) (`fs formula`); notta `\boxed` da bu renkte |
| Nokta | içi boş daire, 2,8 pt, 0,354 pt kontur; ona değen çizgiler 0,3 pt boşlukla başlar |
| Panel harfleri | kalın mavi a, b, ... (`\FigPanel{(x,y)}{a}`) |

Renk anlamı: gerilme/kuvvet/yük kırmızı; eksenler mavi; ölçü, açı ve
normal n yeşil; geometri siyah. Etiket nesnesinin rengini alır.
Diferansiyel d dik yazılır (`\mathrm{d}`).

## 3. Stil anahtarları (figstyle.tex)

`fs` (ortam), `fs thin`, `fs med`, `fs heavy`, `fs body`, `fs hidden`,
`fs aux`, `fs axis`, `fs axlabel`, `fs stress`, `fs slabel`, `fs vec`,
`fs vec thin`, `fs vec aux`, `fs label`, `fs angle`, `fs angle plain`,
`fs anglabel`, `fs curve`, `fs point`, `fs hatch`, `fs wall`, `fs box`,
`fs formula`, `fs region`; komutlar `\FigVec`, `\FigTr`, `\FigPanel`.
Gövde `\begin{tikzpicture}[fs, x=1pt, y=1pt]` ile açılır; koordinatlar
sayfa noktasıdır ve `<ad>_geom.tex` içindeki `\def` makrolarından gelir.
Örnekler: `figures/ch9/*_body.tex` ve `*_geom.py`.

Kural: **Python geometriyi hesaplar, TeX yalnız stil verir; gövdede sihirli
koordinat yok.** Üretici, çizdiği şeyin doğruluğunu `assert` ile sınar
(ör. bir profilin sınır koşulları, bir açının değeri).

3-B figürler için `fsgeom.HOUSE` ev kamerasıdır (ortografik, az 35,0°,
el 20,4°; `page(P, scale)` model noktalarını sayfaya izdüşürür,
`faces_viewer(n)` bir yüzün görünür olup olmadığını söyler).

## 4. Derleme

Repo kökünden:

```bash
python figures/common/make.py ch9                 # bölümün bütün figürleri
python figures/common/make.py ch9 ch9a_frames     # yalnız seçilenler
python figures/common/make.py ch9 --dpi 600       # daha keskin önizleme
```

Gerekenler: `pdflatex`, `pdftocairo` (poppler-utils), Python 3 ile
`numpy scipy pillow pymupdf`. Bir figür derlenmezse ya da denetimden
geçmezse betik 1 koduyla çıkar; **CHECK FAILED görünen figür nota
konmaz.** Denetim mürekkep üzerinden yapılır: etiketler tek başına
1200 dpi'da basılır, çizgiler vektör yollarından gerçek kalınlıklarıyla
rasterleştirilir; fontun kutusu değil gerçek glif izi ölçülür. Kesir
çizgileri (0,4 pt TeX kuralı) etiketin parçası sayılır. Denetimden sonra
PNG önizlemesi gözle de kontrol edilir.

## 5. Nota koyma

```latex
\bookfig{5}\begin{figure}[htbp]\centering
\includegraphics[scale=1.728]{../../figures/ch2/ch2_f05_twoinstants.pdf}
\caption{...}
\label{fig:ch2twoinstants}
\end{figure}
```

Kitabın şekli `\bookfig{n}` ile kitabın numarasını alır; notun kendi
şekli `\renewcommand{\thefigure}{A}` (B, C, ...) ile harf alır. `width=`
kullanılmaz: etiketler metinden farklı boya çıkar.
