# دليل عمل الفيديوهات (Handbook)

الدليل ده خلاصة اللي اتعلمناه في إعلان **وشيج «الطلب الخفي»**، علشان أي فيديو جاي يمشي أسرع ومن غير ما نعيد نفس التجارب.

> **لـ Claude في الجلسة الجاية:** اقرأ الملف ده الأول. وابدأ أي فيديو جديد بنسخ أدوات `videos/washeej-invisible-order/tools/` و`gfx/common.css` و`gfx/anim.js`.

---

## 1. تنظيم الـ Repository

```
videos/<اسم-الفيديو>/      ← كل فيديو في فولدر لوحده (ابدأ أي فيديو جديد هنا)
  README.md                ← حالة الفيديو + أوامر البناء
  docs/                    ← البريف، كتاب الإنتاج، كيت التوليد
  timeline.json            ← مصدر الحقيقة للمونتاج (لقطات، صوت، مؤثرات)
  brand/                   ← الشعار والخطوط والألوان المستخرجة من موقع العميل
  gfx/                     ← جرافيك HTML (نصوص عربية، واجهات، شعار)
  gen/                     ← توليد الفيديو بالـ AI (برومبتات + الكليبات الأصلية)
  cgi/                     ← مشاهد Blender
  tools/                   ← سكربتات الرندر والمونتاج والمراجعة
  audio/                   ← التعليق الصوتي + المؤثرات
  renders/preview/         ← معاينات خفيفة
project/ + output/         ← فيديو GD Tableware (القديم، متسابش زي ما هو)
```

**مش بيترفع على git** (تقيل وبيتعاد توليده بأمر واحد): `renders/*.mov` و`shots/` و`gen/post/` و`cgi/frames/`. الأوامر في README الفيديو.

---

## 2. خطوات أي فيديو (بالترتيب)

| # | الخطوة | الأداة | الناتج |
|---|---|---|---|
| 1 | قراءة البريف وتثبيت السكربت الصوتي حرفيًا | — | `docs/` |
| 2 | استخراج الهوية من موقع العميل | `curl` + Python (شوف §4) | `brand/` (SVG الشعار، الخطوط، الألوان) |
| 3 | ستوري بورد + تايملاين | `timeline.json` | لقطات بأوقات |
| 4 | الجرافيك والنصوص العربية | HTML + `tools/render.js` | ProRes بقناة شفافية |
| 5 | اللقطات الحية | FLUX + Wan (مجاني) أو Higgsfield (مدفوع) | `gen/clips/` |
| 6 | لقطات CGI | Blender (`cgi/scene.py`) | `cgi/*.mp4` |
| 7 | معالجة (رفع الدقة، 30fps، Bloom، تتبع الشاشات) | `tools/post_*.sh` و`screen_replace.py` | `shots/` |
| 8 | الصوت | تسجيل + `measure_vo.py` + Whisper | `audio/` |
| 9 | المونتاج النهائي | `tools/assemble.py` | MP4 |
| 10 | المراجعة | `tools/qa.sh` | تقرير + لوحة كادرات |

---

## 3. أوامر سريعة

```bash
# جرافيك: رندر كل عناصر HTML إلى ProRes (+ معاينات)
tools/render_all.sh
# فريم واحد للمراجعة
node tools/still.js gfx/X.html /tmp/x.png 1.5 1080 1920
# توليد مجاني (بيكمّل من مكان ما وقف، وبيقف لوحده عند انتهاء الحصة)
cd gen && python3 gen.py t1
# معالجة كليب Wan → 1080x1920 30fps
tools/post_wan.sh gen/clips/S03A_t1.mp4 shots/S03A.mp4
# Blender (مستمر في الخلفية، يكمّل من آخر فريم)
./cgi/render_all.sh
tools/post_cgi.sh cgi/S04B.mp4 shots/S04B.mp4
# تتبع شاشة واستبدالها
python3 tools/screen_replace.py shots/S03A.mp4 renders/GFX_03_phone_ui.mov shots/S03A_comp.mp4 --corners "x1,y1 x2,y2 x3,y3 x4,y4"
# تتبع شاشة عليها صوابع (الواجهة تتحط على الأجزاء البيضا بس) + تأخير ظهورها
python3 tools/screen_replace.py shots/S03C.mp4 renders/GFX_03_phone_ui.mov shots/S03C_comp.mp4 --corners "..." --insert-from 2.0 --delay 2.34 --luma-key 165
# كروت UI طايرة حوالين شخص (نوافذ مشاكل، إشعارات)
python3 tools/float_cards.py shots/S07B.mp4 shots/S07B_comp.mp4 gfx/S07B_cards.json
# مؤثرات صوتية مولّدة برمجيًا (من غير تراخيص)
python3 tools/make_sfx.py
# مونتاج
python3 tools/assemble.py --check
python3 tools/assemble.py            # النهائي
python3 tools/assemble.py --slates   # نسخة مراجعة توقيت (ممنوع تتنشر)
tools/qa.sh renders/<master>.mp4
```

---

## 4. إعداد البيئة (Claude Code على الويب)

**النطاقات المسموحة** (اللي احتجناها، وكلها مجانية):
`washeej.site` (موقع العميل) · `huggingface.co` · `linoyts-wan2-2-i2v-rcm.hf.space` (فيديو) · `black-forest-labs-flux-1-schnell.hf.space` (صور) · `cas-server.xethub.hf.co` و`cas-bridge.xethub.hf.co` و`transfer.xethub.hf.co` و`us.aws.cdn.hf.co` (تحميل موديلات مثل Whisper)

**Token لـ Hugging Face:** حساب مجاني و token قراءة، محفوظ كـ network secret **على نطاق كل Space** (مش على huggingface.co).

**مكتبات:**
```bash
pip install gradio_client opencv-python-headless faster-whisper
pip install bpy        # Blender 5.3 كمكتبة Python (لازم Python 3.13)
```
Playwright و Chromium موجودين جاهزين، و ffmpeg و ImageMagick كمان.

---

## 5. دروس اتعلمناها (هتوفّر ساعات)

**توليد الفيديو المجاني (Hugging Face Spaces):**
- **كلّم الـ Space بعنوانه المباشر** `Client("https://<space>.hf.space")` مش بالاسم `owner/space`. الاسم بيعدّي على `huggingface.co/api` من غير token، والـ IP المشترك بيتحظر بسرعة (429).
- الحصة المجانية لـ ZeroGPU **حوالي 3 كليبات في اليوم** (كل كليب Wan حوالي 70 ثانية GPU). الحصة بتتجدد بعد 24 ساعة، فجدول الاستكمال.
- Wan 2.2 (rCM) بيطلّع **480×832 بـ 16fps**، ودايمًا بيتعالج بـ `post_wan.sh`.
- Wan كويس في: ناس طبيعيين، حركة هادية، Push-in. **ضعيف في:** Bullet Time، Dolly Zoom، حركات معقدة. اعمل الحركات دي في Blender، أو اكسب الإحساس بالبطء (slow-mo بالـ interpolation).
- FLUX schnell ممتاز لصور البداية (7 ثواني). كرّر **نفس وصف الشخصية حرفيًا** في كل برومبت عشان الشكل يثبت.

**Blender على المعالج:**
- Blender 5 غيّر الـ API: `action.fcurves` مش موجودة. استخدم الدالة `fcurves()` اللي في `cgi/scene.py` (Slotted Actions / channelbags).
- **السرعة:** 540p، و14 عينة، و adaptive sampling، و**رندر فريم وسيب فريم** (`--step 2`)، وبعدين `minterpolate` لـ 30fps. كده الفريم بياخد حوالي 7–15 ثانية.
- الـ Volume (الضباب) بيبطّأ جدًا، فبلاش منه. والإضاءة النقطية جوه الزجاج بتعمل كتلة محروقة، فخلي التوهج Emission وحافة Fresnel.
- التوهج (Bloom) يتعمل في ffmpeg (`post_cgi.sh`)، أسرع وأنضف من الكمبوزيتور.
- **ما تشغّلش رندر طويل بـ `nohup … &`** لأن العملية بتموت مع الـ shell. شغّله كـ background task متتبَّع. والسكربت بيكمّل من آخر فريم (`use_overwrite=False`).

**الجرافيك والنص العربي:**
- **ممنوع أي نص عربي من موديلات الـ AI.** كل النصوص HTML بخط العميل، وبتترندر فريم بفريم بـ Playwright (`window.seek(t)` ثابت ومحدد).
- اتأكد إن أبعاد الفيديو زوجية (H.264 بيرفض 1179 مثلًا).
- صوّر الشعار من SVG الموقع نفسه، ولو الموقع فيه قناع كتابة (writing mask)، أعد استخدامه في لقطة الختام.

**التتبع (`screen_replace.py`):**
- الشاشة الفاضية مفيهاش ملامح، فبنتتبع **حلقة حوالين الشاشة**.
- `qualityLevel=0.001`، لأن زوايا الشاشة البيضا بتغطي على باقي الملامح.
- الهوموجرافي يتحسب **من الفريم المرجعي** (مش تراكمي). اتختبر بخطأ حوالي بكسل واحد.

**الصوت:**
- **أول ما يوصل التسجيل فرّغه بـ Whisper وقارنه بالنص المعتمد**. في وشيج التسجيل وصل بلهجة خليجية، وكان لازم يتعمل قرار من العميل (`docs/VO_CHECK.md`).
- لو البريف طالب صمت بعد جملة معينة والتسجيل مفيهوش، زوّد صمت في الملف (ffmpeg concat) من غير ما تلمس الكلام.
- من غير موسيقى، المؤثرات الصوتية بتشيل الإيقاع كله. `make_sfx.py` بيولّد whoosh وضربة زجاج ووتر (Karplus-Strong) وأجراس، مجانًا ومن غير تراخيص.
- السكربت الصوتي ما يتغيرش ولا حرف. وبعد التسجيل اتأكد منه بـ Whisper (`faster-whisper` موديل `small`، والصوت يتقري كـ PCM بـ ffmpeg).
- `measure_vo.py` بيطلّع أماكن الجمل، فحدّث `timeline.json` وحرّك حدود اللقطات معاها.

**المونتاج:**
- `assemble.py` **بيرفض** اللقطة الناقصة أو القصيرة، وما بيملاش بفريم ثابت أو Zoom على صورة.
- الصوت النهائي -14 LUFS / True Peak ‑1 (two-pass loudnorm).

---

## 6. المجاني والمدفوع (أسعار نوفمبر 2026 تقريبًا)

| | مجاني (اللي استخدمناه) | مدفوع |
|---|---|---|
| صور البداية | FLUX schnell على HF | Higgsfield Soul / Nano Banana |
| فيديو بشري | Wan 2.2 على HF: حوالي 3 في اليوم، 480p | Higgsfield (Kling/Veo/Seedance): حوالي 1,700 كريديت للإعلان كامل (باقة Ultra) |
| CGI | Blender على المعالج | — |
| جرافيك ونص عربي | HTML + Playwright | — |
| صوت | تسجيل + Whisper للتأكد | — |

---

## 7. قالب طلب فيديو جديد (انسخه لـ Claude)

```
فيديو جديد: <اسم>
العميل والموقع: <رابط>
السكربت الصوتي (حرفيًا، ممنوع تعديله): <النص>
المقاس: 9:16 1080x1920 30fps (أو غيره)
الميزانية: مجاني فقط / مسموح بـ <...>
اقرأ HANDBOOK.md الأول، واعمل الفيديو في videos/<slug>/ بنفس هيكل وشيج.
```
