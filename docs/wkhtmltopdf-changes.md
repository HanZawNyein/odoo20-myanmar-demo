# wkhtmltopdf မှာ ဘာပြင်ထားသလဲ

Odoo module ထဲမှာ Unicode ကို PUA စာလုံးပြောင်းခြင်း၊ အစဉ်ပြန်စီခြင်း မလုပ်ပါ။ အဓိကပြင်ဆင်မှုက wkhtmltopdf သုံးနေတဲ့ patched Qt 4.8.7 ရဲ့ text shaping နဲ့ PDF writer ထဲမှာ ဖြစ်ပါတယ်။ wkhtmltopdf application `src/` ကို မပြင်ထားပါ။

## 1. Modern HarfBuzz Myanmar shaping

`qmyanmarharfbuzz.cpp` / `_p.h` အသစ်ထည့်ပြီး selected font ရဲ့ SFNT tables ကို modern HarfBuzz နဲ့ shape လုပ်ပါတယ်။ Myanmar script၊ `my` language၊ LTR direction၊ grapheme cluster mapping၊ QFixed advances/offsets နဲ့ font stretch ကို Qt ဆီ ပြန်ပို့ပါတယ်။ `mymr` tag ကို `mym2` လို့ အစားထိုးရုံ မဟုတ်ပါ။ Font ရဲ့ OpenType tables နဲ့ modern Myanmar shaper ကို အတူသုံးပါတယ်။

## 2. Myanmar text itemization and clusters

`qtextengine.cpp` က Myanmar marks၊ virama နောက်ဆက်တွဲ၊ ZWJ/ZWNJ တွေကို ဆက်စပ်တဲ့ shaping run ထဲမှာ ထိန်းထားပါတယ်။ Cluster maps / cursor stops နဲ့ existing line-break opportunities ကို ထိန်းထားပြီး long-run limits နဲ့ glyph/offset bounds ကို စစ်ထားပါတယ်။ Modern Myanmar word-breaking အပြည့်အစုံ ထည့်ထားခြင်း မဟုတ်ပါ။

## 3. Font fallback

`qfontdatabase_x11.cpp`, `qfontengine*.cpp/.h` က headless Linux Fontconfig path မှာ complete fallback faces ကို ရှာနိုင်အောင် ပြင်ထားပါတယ်။ Glyph တစ်လုံးချင်း မတူတဲ့ font တွေကနေ ဆွဲမယူဘဲ primary-shaper cluster တစ်ခုကို complete font တစ်ခုက ဖုံးလွှမ်းနိုင်အောင် ရွေးပါတယ်။ တူညီတဲ့ font သုံးထားတဲ့ အနီးကပ် clusters တွေကို အတူ shape လုပ်ပြီး context/kerning ကို ထိန်းပါတယ်။ Fallback indices က အများဆုံး 256 faces ဖြစ်ပါတယ်။

## 4. PDF Unicode extraction

`qpdf.cpp`, `qprintengine_pdf.cpp`, `qfontsubset*.cpp/.h`, `qtextlayout.cpp`, `FontQt.cpp` တို့မှာ original Unicode ကို cluster-level `ActualText` နဲ့ PDF ထဲ ထည့်ပေးပါတယ်။ Visible glyphs နဲ့ invisible semantic text carrier ကို သီးခြားထိန်းပြီး copy/search တွင် duplicated သို့မဟုတ် reordered text မဖြစ်အောင် လုပ်ထားပါတယ်။ Partial formatting/selection ranges နဲ့ shadow text ကို ထိန်းထားပါတယ်။ Opt-in ဖြစ်လျှင် PDF 1.5 သုံးပါတယ်။

## 5. Build / runtime dependency

`text.pri` မှာ Linux bridge sources / HarfBuzz linking ထည့်ပါတယ်။ Packaging မှာ `libharfbuzz-dev` build dependency၊ Jammy targets မှာ `libharfbuzz0b` runtime dependency၊ Docker Desktop platform handling ထည့်ထားပါတယ်။

## Enable

```dockerfile
ENV QT_MYANMAR_HARFBUZZ=1
```

Flag မပါလျှင် legacy rendering ဆက်သုံးပါတယ်။ Complete Unicode font (ဒီ demo မှာ Noto Sans Myanmar) နဲ့ original Unicode input ကို သုံးရပါတယ်။ Demo addon သည် renderer workaround မဟုတ်ဘဲ report fixture သာ ဖြစ်ပါတယ်။

## Exact source / patches

- [Qt commit 82ffe9ae](https://github.com/HanZawNyein/qt/commit/82ffe9ae) — 16 files, 503 additions / 54 deletions.
- [Application/workflow commit a1997bc](https://github.com/HanZawNyein/wkhtmltopdf/commit/a1997bc) — tests, scripts, documentation, Qt submodule reference.
- [Packaging commit 62ad22c](https://github.com/HanZawNyein/packaging/commit/62ad22c).
- [Complete Qt patch](qt-myanmar.patch) and [packaging patch](packaging-myanmar.patch), copied from those exact commits.

## Tested scope / remaining limits

Prior release validation passed, per architecture: 72 Qt shaping comparisons, seven fallback checks, 34 isolated Unicode PDF cases, nine layout cases and 43 extraction/search cases in each of MuPDF 1.26.7 and 1.28.2. ARM64 also passed an Odoo 20 two-page report. This repository separately verifies its running Odoo 20 / Noto demo.

Known limits remain: cluster boundaries initially derived from the primary face, context at font changes, 256-face fallback limit, incomplete broad font/style/bidi coverage, modern word-breaking, arbitrary PDF reading order/whitespace and other PDF readers. Normal GitHub release status is not a claim that those limits are solved.
