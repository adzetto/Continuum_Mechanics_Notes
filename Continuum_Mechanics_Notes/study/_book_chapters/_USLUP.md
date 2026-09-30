# Ders notu yazim sozlesmesi

Bu notlar Steigmann ve Shirani'nin *Principles of Continuum Mechanics*
kitabinin bastan sona islenmis halidir. Bolum 1-5 yazildi; sen bir bolumu
yaziyorsun. Cikti tek bir dosya: `C:\Users\lenovo\Desktop\A\body_chN.tex`.

**Once bunu yap:** `body_ch4.tex` ve `body_ch5.tex` dosyalarini bastan sona
oku. Uslup, yogunluk ve ses oradan ogrenilir; asagisi yalnizca kurallarin
ozeti.

---

## 1. Dosya bicimi

Dosya `\chapter{...}` ile baslar, `\begin{document}` ya da onsoz ICERMEZ:
`main.tex` onu `\input` ediyor. Bolum ayirici yorumlar 71 karakterlik `=`
satiridir, kaynak satirlari 72 sutunda sarilir.

```latex
%=======================================================================
\chapter{Balance Laws}
%=======================================================================

<giris paragrafi>

%=======================================================================
\section{Generic forms of the balance laws}\label{sec:genericbal}
%=======================================================================
```

Alt bolum `\subsection{...}\label{...}`, numarasiz ara baslik
`\subsection*{...}`. Kitabin kisim numaralari ve basliklari BIREBIR
korunur; `_book_chapters/chN.txt` icindeki yer imi listesi olcuttur.

## 2. Denklem numaralari

**Yalnizca kitapta numarali olan gosterimler numaralanir.**

```latex
\begin{equation}
   \dvg\bT+\rho\bb=\rho\dot\bv .
   \tag{6.24}\label{eq:6.24}
\end{equation}
```

Kitapta numarasiz olan her gosterim `\[ ... \]` ile yazilir ve numara
ALMAZ. Ara adimlar, cozumlerdeki hesaplar, kendi kurdugun yardimci
ifadeler: hepsi `\[ ... \]`. On sayfa "equation numbers match the book"
diyor; uydurma numara bu sozu bozar. `\tag*{}` KULLANMA, uretim hattinda
sirali numara aliyor.

Bir gosterime birden cok kitap numarasi dusuyorsa aralik yazilir:
`\tag{6.31--6.33}`. Aralik uyeleri `eq_aliases.tex` uzerinden zaten
cozuluyor.

## 3. Capraz basvuru

- Kitap denklemi: `\eqr{2.54}`. "(2.54)" basar ve o denklem belgede varsa
  baglanti olur, yoksa sessizce duz metne duser.
- Teorem, tanim, not, kisim, sekil: `Theorem~\ref{thm:div}`,
  `Section~\ref{sec:divvar}`.
- **Hedefi `_book_chapters/_REFERANS.md` icinde bulunmayan bir seye
  baglanma.** Kendi bolumunde tanimladigin etiketler elbette serbest;
  onlarin adi baska bolumle CAKISMAMALI (`sec:disc` bir kez bu yuzden
  catisti). Kendi etiketlerine bolum numarasi ekle: `sec:ch6bal`,
  `rem:ch6why`.

Onceki bolumlere bagli yazmak bu isin ana istegi. "Bolum 3'te gordugumuz
polar ayrisim", "Bolum 1'in yerelleştirme teoremi", "Bolum 5'in Reynolds
formulu" gibi baglar metnin dokusu olmali, susleme degil.

## 4. Ortamlar

`theorem, proposition, lemma, corollary, definition, remark, example`
ayni sayaci paylasir ve her bolumde sifirlanir; `\begin{remark}[kisa
baslik]\label{rem:...}` bicimi kullanilir. Kanit icin `proof`.

Problemler bolumu:

```latex
%=======================================================================
\setcounter{problemenv}{0}
\section{Problems}\label{sec:problems:c6}
%=======================================================================

\begin{problem}[Kisa tanitici baslik]
<kitaptaki problem ifadesi, kendi sozlerinle ama eksiksiz>
\end{problem}

\begin{solution}
<tam cozum>
\end{solution}
```

`\setcounter{problemenv}{0}` satirini UNUTMA; yoksa problemler onceki
bolumun numarasindan devam eder.

## 5. Sekiller

Kitabin sekline karsilik gelen: `\bookfig{n}` ile numarasi kitaba
sabitlenir.

```latex
\bookfig{2}\begin{figure}[htbp]\centering
\begin{tikzpicture}[scale=1.0, ar/.style={-{Stealth[length=2.2mm]},thick}]
...
\end{tikzpicture}
\caption{...}
\label{fig:ch6cauchy}
\end{figure}
```

Kitapta olmayan, senin anlatim icin ekledigin sekil harf alir:
`\renewcommand{\thefigure}{A}` (sonra B, C, ...) figure ortaminin
icinde, `\centering`den sonra.

Kullanilabilir tikz kutuphaneleri: `arrows.meta, calc, positioning,
angles, quotes, patterns`. Hazir stiller: `vec, thinvec, mapar, guide,
bodyline, configline, lbl` ve `\blob{...}` (cisim silueti).

**Her sekil derlenmek zorunda.** Yazdiktan sonra
`python latex/tikz_svg.py chN` calistir (repo kokunden); "BASARISIZ"
diyen sekli duzelt. Sekil sayisi az ama isini goren olsun: bir kavram bir
sekil. Bos yere sus yapma.

## 6. Anlatim

Bu bolumun asil istegi budur.

- **Uzun tire (—) KULLANMA.** Ara cumleyi virgul, iki nokta, noktali
  virgul ya da ayri cumle ile kur. `Piola--Nanson` gibi ozel ad
  birlestiren kisa tire serbest.
- "load-bearing", "pays for itself", "honest bookkeeping", "it is worth
  noting" gibi sus ifadeler yok. Dogrudan yaz.
- **Atlanan hesap birakma.** "Hence", "one finds", "a short computation
  gives" yazip gecme; ara adimlari goster. Olcut: okur kalem tutmadan
  takip edebilmeli. Ornek icin `body_ch4.tex` icindeki
  `(\ln\mu)^{\textstyle\cdot}=\ip\bm{\bD\bm}` turetimine bak: birim
  vektorun turevinin neden dik oldugu, W teriminin neden dustugu,
  bolmenin neden serbest oldugu, zincir kuralinin nasil isledigi tek tek
  yaziliyor.
- **Neden oyle yapildigini anlat.** Bir tanim neden o bicimde, bir secim
  neden o secim, yanlis okunursa ne bozulur. Bunlar `remark` olarak ya da
  metnin akisinda durur.
- Gosterim aciklanir: sapka referans betimlemesi, tilde uzamsal, ust
  nokta maddesel turev, us sabit yerde turev. Bolum 2'nin
  `\ref{rem:decorations}` notuna baglan.

## 7. Problemler

Kitabin o bolumdeki HER problemi cozulecek. Cozum:

- Sifirdan, tam. Sonucu yazip gecme.
- Onceki bolumlere bagla: hangi teorem, hangi denklem, hangi problem.
- Anahtar sonuc `\boxed{...}` icinde.
- Cozumun sonunda, yerine gore, sonucun ne anlama geldigi ya da nerede
  kullanilacagi bir iki cumle.

## 8. Makrolar

`main.tex` onsozunde tanimli; yenisini EKLEME (uretim hatti onsozu
okuyor, bolum icinde tanimlanan makro KaTeX'e gitmez ve sitede kirmizi
cikar). Varsa `main.tex`'i oku. Sik kullanilanlar:

```
\Et \hEt \Vt \hVt \Ept \Rn \En \Lin \Orth \Sym \Skw \tr
\grad \Grad \dvg \Dvg \crl \I \hI \Ob \hOb \shift
\ba \bb \bc \bd \be \bff \bg \bh \bk \bm \bn \bp \bq \br \bs \bt
\bu \bv \bw \bx \by \bz  (kucuk harf vektorler)
\bA \bB \bC \bD \bE \bF \bG \bH \bK \bL \bM \bN \bP \bQ \bR \bS
\bT \bU \bV \bW \bX \bY \bZ  (buyuk harf tensorler)
\bchi \bom \bOm \bnu \bkappa \bze \hbE \hER \hETh
\dd (delta) \eps (varepsilon) \dl (dik d) \tbox{}{}{} \ip{}{}
\rest{} \Proj{} \Refl{} \jump{}  (atlama: [[phi]])
\eqr{}  (kitap denklem numarasi)
```

Maddesel turev `\dot\bv`, `\dot\varphi`; uzun ifadelerde
`(\bA\bB)^{\textstyle\cdot}`.

## 9. Tuzaklar

1. **Bash heredoc KULLANMA.** Bu ortamda ters bolulari yiyor: `\ref`
   satir basi karakterine donuyor ve dosyayi sessizce bozuyor. Dosya
   yazarken Write aracini, toplu degistirme icin ayri bir `.py` dosyasini
   kullan.
2. Dosya CRLF satir sonlu. Python ile toplu degistirme yapacaksan arama
   kalibini bosluga duyarsiz kur (`\s+`).
3. `\tag*{}` yok.
4. Etiket adlari bolumler arasi essiz olmali.
5. Kitabin numarasiz gosterimlerine numara verme.

## 10. Bitirmeden once

Repo kokunden (`C:\Users\lenovo\Desktop\reading-library`):

```
python latex/tikz_svg.py chN          # sekiller derlensin
```

`C:\Users\lenovo\Desktop\A` icinden:

```
latexmk -pdf -interaction=nonstopmode main.tex
```

`main.log` icinde `^!` hatasi, "undefined reference" ve "multiply
defined" OLMAYACAK. (main.tex'e `\input{body_chN}` satirini koordinator
ekleyecek; sen yalnizca kendi dosyandan sorumlusun, ama derlemeyi
denetlemek icin gecici olarak ekleyip cikarabilirsin. Baska bolumun
dosyasina DOKUNMA.)

Kendi dosyan icin son denetim: her `\ref` hedefi var mi, her `\tag`
kitapta gercekten o numarayla mi geciyor, uzun tire kalmis mi.
