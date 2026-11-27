# WASHEEJ — THE INVISIBLE ORDER
## كتاب الإنتاج (Production Bible) — إعلان سينمائي 9:16

> **حالة التنفيذ بصراحة:** كل عناصر الجرافيك والنصوص العربية والشعار وخط المونتاج النهائي **اتعملت واترندرت فعليًا** (موجودة في `renders/`). أما **اللقطات السينمائية الحية/CGI** (22 لقطة) **ما اتولّدتش**، لأن مفيش مولّد فيديو متاح في الجلسة دي (تفاصيل في القسم 10). البرومبتات تحت جاهزة للتنفيذ على Higgsfield، وأول ما اللقطات تتحط في `shots/` الأمر `python3 tools/assemble.py` يطلّع الماستر النهائي.

---

## 0. الهوية البصرية المستخرجة من washeej.site (مش من البريف)

| العنصر | القيمة الحقيقية من الموقع | الاستخدام في الفيلم |
|---|---|---|
| Burgundy | `#59171B` (`--burgundy`) | الخيط، خلفية الختام، حالة «جديد» |
| Burgundy deep | `#3F0F13` | تدرّج خلفية الختام |
| Peach | `#FED7B8` (`--peach`) | قلب الخيط المضيء، الشعار على الـBurgundy |
| Paper | `#FAF6F2` (`--paper`) | سطوح الـAct 1 الفاتحة |
| Ink | `#282828` | نصوص على الفاتح |
| خط عربي | **Readex Pro** (أوزان 160–700) | كل نصوص الواجهة والتايبوجرافي |
| خط لاتيني | **Cormorant Garamond** 600، تباعد 0.42em | «WASHEEJ» تحت الشعار و washeej.site |
| الشعار | كاليجرافي «وشيج» SVG أصلي (`brand/washeej_mark_*.svg`) + ذيل منحني (swash) + قناع كتابة يدوية أصلي | لقطة الختام بتكتبه بنفس ترتيب ضربات القلم في الموقع |
| موتيف الموقع | **ألياف/جذور حبر رفيعة** بلون الخوخ على ورق (صورة OG + `rootLayer` في الـSVG) | **الخيط = ليفة حبر، مش ليزر نيون**. ده اللي بيفرّق شكلنا عن الـcyberpunk |
| التاجلاين | «نصنع الرابط بين علامتك وعملائها» (مطابق لصورة OG حرفيًا) | الختام |

قرار إخراجي ناتج عن الاستخراج: الخيط في المشهد 06 والختام **ليفة حبر عضوية** (قلب خوخي + هالة Burgundy)، بتتصرّف كأنها خيط خياطة حقيقي: بتتشد، بتتعقد، بتترتق. ده اللي بيربطها بالشعار نفسه، لأن ذيل «وشيج» منحني بنفس الشكل.

---

## 1. القصة في سطرين
«كريم» صاحب محمصة «دار البُنّ» بيبني موقعه بنفسه بالذكاء الاصطناعي في ليلة. الموقع جميل فعلًا. «يوسف» يطلب من الموبايل، يشوف «تم الإرسال»، والطلب بيقف عند حاجز ما حدّش شايفه. وشيج بتمشي الرحلة كلها بخيطها، تلاقي العُقدة، تصلّحها، وتعيد الاختبار لحد ما الطلب يوصل.

> كريم هو نفسه اللي بيكتب البرومبت في المشهد 01. كده المشاهد بيفهم من غير شرح إن الموقع **اتبنى صح بصريًا** وإن المشكلة في الرحلة، مش في الأداة. ده بيخلّي الإعلان مش ضد الـAI.

## 2. الشخصيات والأماكن (Continuity Bible). تتثبّت قبل أي توليد

**C1 — يوسف (العميل).** راجل مصري، 27 سنة، شعر أسود كيرلي قصير، دقن خفيفة متظبطة، أوفرشيرت زيتوني على تيشيرت أبيض، ساعة فضي في الشمال. موبايل أسود جرافيت من غير جراب. المكان: صالة شقة في القاهرة، **ساعة الغروب الزرقاء**، أباجورة دافية على يمينه، بوكيه أنوار المدينة ورا الشباك.
`Soul ID / character ref: C1_youssef` (3 صور مرجعية: وش أمامي، 3/4، بروفايل. نفس اللبس).

**C2 — كريم (صاحب البيزنس).** راجل مصري، 40 سنة، دقن قصيرة رمادي وأسود، قميص فحمي بأكمام مطوية، **مريلة كانفاس Burgundy** بحزام جلد. لابتوب فضي 14" على كاونتر خشب. المكان: محمصة صغيرة متخصصة، حيطة طوب، **محمصة نحاس**، شكاير خيش، برطمانات بن. ليلًا (01، 05): ضوء تنجستن عملي + توهّج الشاشة. صباحًا (07، 08): ضوء شباك جانبي دافي.
`Soul ID: C2_karim`

**E1 — المتجر الرقمي (Act 1، الوهم).** نسخة معمارية مستحيلة من موقع «دار البُنّ»: معمار عاجي وخوخي طافي، رفوف زجاج، أكياس بن داكنة (نفس كيس «حَراز» اللي في الواجهة)، ضوء نهار ناعم 5600K، انعكاسات مصقولة، **من غير أي نص مقروء** (النصوص بتتركّب).

**E2 — نفق البيانات (Act 2، العطل).** أنبوب زجاج شفاف في فراغ جرافيتي، ضلوع زجاج رفيعة بتعدّي، كوستيكس باردة 4300K، خطوط ضوء عاجية رفيعة جدًا. **ممنوع:** كود طاير، جليتش زيادة، نيون سيان/ماجنتا.

**P1 — كبسولة الطلب (Hero prop، لازم تبقى متطابقة في كل لقطة).** كبسولة ناعمة بحجم قبضة اليد، قشرة زجاج عاجي شفاف، **قلب ضوء خوخي دافي**، جواها إيصال ورق مطوي باهت. ذيل ضوء قصير وراها.

**P2 — الحاجز الخفي.** مش مرئي لحد لحظة الاصطدام: بيبان بس من **تموّج الزجاج** حوالين نقطة التلامس وتشقّق ضوء الكبسولة. مفيش كلمة «Error» ولا لون أحمر في الصورة.

**T1 — خيط وشيج.** ليفة حبر عضوية، قلب `#FED7B8` مضيء، هالة `#59171B`، 6–9 شعيرات أرفع بتجري جنبها (زي صورة OG). بيتحرك بنيّة: يتشد، يتعقد، يترتق. مش ديكور.

**جدول الإضاءة حسب الفصل**
| الفصل | المشاهد | الحرارة | المزاج |
|---|---|---|---|
| ACT 1 الوهم | 01–03 | 5600K ناعم + أباجورة 3200K عند يوسف | مصقول، حلو، واثق |
| ACT 2 العطل | 00، 04، 05 | 4300K بارد، ريم لايت حاد، كوستيكس | توتر، صمت |
| ACT 3 الحل | 06–08 | 3200K دافي + Burgundy | وضوح، اعتمادية |

---

## 3. التايملاين المتزامن مع التعليق الصوتي (Master 58.5s)
> أوقات الجمل **تقديرية** لقراءة مصرية بإيقاع طبيعي، لأن ملف التعليق الصوتي ما اتسلّمش. بعد التسجيل: `python3 tools/measure_vo.py audio/vo.wav` بيطلّع الأوقات الحقيقية، تتحط في `timeline.json`، وحدود اللقطات تتزحزح معاها. **التعليق ما يتسرّعش أبدًا.**

| الوقت | اللقطة | الصوت (حرفيًا) | الصورة | الجرافيك |
|---|---|---|---|---|
| 0.00–0.90 | **S00** | (مفيش كلام) whoosh ← impact | FPV سريع جدًا في النفق، الكبسولة تخبط، تجميد، Crash Zoom | `GFX_00` لمحة «تم الإرسال» 0.55–0.80 |
| 0.90–1.20 | **S00R** | tape-rewind | ترجيع عنيف (S00 بالعكس 3×) + فلاش خوخي فريمين | — |
| 1.20–4.60 | S01A/B/C | «لو كلود بيعمل مواقع… وشيج لسه فاتحة ليه؟» | ماكرو كتابة ← Crash Zoom في الشاشة ← المتجر يتجسّد (أوربت) | `GFX_01` شاشة البرومبت |
| 4.60–12.60 | S02A/B | «سؤال في محلّه.» / «تقدر تفتح كلود دلوقتي…في نفس اليوم.» | المتجر بيتبني ← FPV جوّه ← خروج من شاشة موبايل حقيقي | — |
| 12.60–20.40 | S03A–D | «طب تخيّل معايا.» / «عميل دخل موقعك… ظهر له «تم الإرسال».» | يوسف بيتصفّح ← الإبهام ← **Bullet Time** ← الكبسولة تطلع | `GFX_03` على الشاشة، `GFX_00` على الكبسولة |
| 20.40–26.00 | S04A/B | «بس الطلب ما وصلكش.» ثم **صمت 22.2–24.0** | النفق كامل ← **الاصطدام (أقوى لحظة)** ← تجميد | `GFX_04` «تم الإرسال ≠ تم الاستلام» من 22.6 |
| 26.00–29.20 | S05A/B | «هو فاكر إنك هترد عليه. وإنت أصلًا ما تعرفش إنه دخل.» | يوسف مستني ← الكاميرا تعدّي حاجز زجاج ← كريم ولوحة فاضية | `GFX_05 empty` |
| 29.20–42.40 | **S06** (one-take) | «هنا بيبان شغلنا.» / «قبل ما الموقع ينزل…يوصلك.» / «ولو خطوة وقفت، بنصلّحها قبل ما أول عميل يجرّبها.» | الخيط يدخل ← يختبر كل محطة ← يتشد عند الخادم ← يترتق ← نبضة اختبار كاملة ← الطلب يوصل | `GFX_06` (عُقدة 38.3، إصلاح 39.6، إعادة اختبار 40.2، وصول 41.7) + `GFX_05 arrive` |
| 42.40–51.40 | S07A/B/C | «إنت عملت الموقع عشان يشيل عنك شغل.» / «لو كل يوم هتسيب شغلك…شغلانة.» | كريم شغّال ← النوافذ تحاصره + **Dolly Zoom** ← الفوضى ترجع لورا ← طلب يوصل | `GFX_07` ×6 كروت ثلاثية الأبعاد، `GFX_05 arrive` |
| 51.40–52.65 | S08A | (موسيقى) | Pull-out من المحمصة، الخيط يطلع ويعمل Wipe بالـBurgundy | — |
| 52.40–58.50 | **END** | «وشيج — نصنع الرابط بين علامتك وعملائها» (من 53.0) | الخيط يدخل ويكتب الشعار الأصلي بخط اليد (53.35–54.85) | `GFX_08` (مرندر نهائي) |

---

## 4. الستوري بورد لقطة بلقطة + برومبتات Higgsfield

**طريقة الشغل على Higgsfield (لكل لقطة):**
1. **صورة البداية** (وأحيانًا صورة النهاية): تتولّد بـ Higgsfield Soul (مع Soul ID للشخصية) أو أي موديل صور، **9:16**، ومن غير أي نص.
2. **فيديو:** Image-to-Video بصورة البداية (+ النهاية لو مكتوبة) على موديل بيدعم Start/End frame (Kling أو Seedance أو Veo أو DoP جوّه Higgsfield، حسب المتاح في حسابك). حركة الكاميرا من مكتبة Higgsfield Motion بالاسم الأقرب للمكتوب تحت.
3. **ولّد 5s** (أو 10s للـone-take)، وخد 3–4 تيكات لكل لقطة، واختار الأنضف. المونتاج بيستخدم جزء بس.
4. **ممنوع تطلب نص عربي من موديل الفيديو.** أي شاشة تتولّد بمحتوى فاضي ومضيء، ونستبدلها بملفات `renders/GFX_*`.

**Negative/Avoid (يتضاف لكل البرومبتات):** `no text, no letters, no logos, no watermark, no floating code, no matrix rain, no cyberpunk neon, no cyan-magenta palette, no heavy glitch, no extra fingers, no morphing faces, no warped hands, no lens-flare spam`

**اللاحقة الثابتة للستايل (تتضاف لكل البرومبتات):** `shot on ARRI Alexa 35, anamorphic 40mm look, natural film grain, shallow depth of field, cinematic color grade with ivory, warm peach and deep burgundy accents, graphite blacks, premium commercial, 9:16 vertical composition with subject in the central safe area`

---

### SCENE 00 — COLD OPEN (0.00–1.20)
> **تُصوَّر مع S04B نفسها:** الـCold Open لقطة من وسط الحكاية، فبتتولّد من نفس الإعداد (نفس النفق، نفس الكبسولة، نفس الحاجز) لكن بزاوية أقرب وأسرع. ولّد S04A/S04B الأول، واستخدم آخر فريم من S04A كصورة بداية لـS00.

**S00 — Impact teaser** · مدة في المونتاج 0.9s · توليد 5s · كاميرا: *FPV / Crash Zoom In*
- **Start frame:** POV ورا الكبسولة مباشرة جوّه نفق زجاج شفاف، ضلوع الزجاج متسحّبة من السرعة، الكبسولة مضيئة في الثلث اللي في النص.
- **End frame:** الكبسولة متجمّدة لحظة الاصطدام، تموّج دايري في هوا شفاف قدامها، شظايا ضوء خوخي معلّقة، الكاميرا قريبة جدًا (CU) من القشرة.
- **Prompt:** `Extreme-speed FPV tracking shot inside a transparent glass data tunnel floating in a graphite void, a fist-sized glowing ivory glass capsule with a warm peach light core races ahead of camera, thin glass ribs streak past, the capsule suddenly slams into an invisible wall, a circular ripple distorts the empty air like struck glass, peach light fractures into suspended shards, time freezes, violent but controlled crash zoom toward the frozen capsule, cool 4300K light with hard rim, glass caustics, tense, silent`
- **Continuity:** نفس P1/P2/E2 بالظبط زي S04B. الاصطدام عند ~0.55s من المقطع المستخدم.
- **Comp:** `GFX_00_capsule_label.mov` متتبّعة على الكبسولة، ظاهرة 8 فريمات بس (0.55–0.80). Chromatic aberration خفيف لحظة الـcrash zoom.

**S00R — Rewind** · 0.3s · **بيتعمل في المونتاج أوتوماتيك** (`assemble.py`: S00 بالعكس 3× + tmix smear + فلاش خوخي فريمين). بيقطع على أول فريم من S01A.

---

### SCENE 01 — THE QUESTION (1.20–4.60)
**S01A — Macro typing** · 1.4s · توليد 5s · كاميرا: *Macro, slow push-in*
- **Start:** ماكرو إكستريم على صوابع كريم على كيبورد لابتوب فضي، ليل، ضوء الشاشة على الصوابع، المريلة الـBurgundy باينة out of focus.
- **End:** نفس الكادر، الصباع بيدوس Enter، فوكس بيتنقل للشاشة.
- **Prompt:** `Extreme macro close-up of a man's fingers typing quickly on a silver laptop keyboard at night inside a small specialty coffee roastery, glow from the screen lighting the fingertips, a burgundy canvas apron softly out of focus, copper roaster bokeh in background, tungsten practicals, slow push-in, final key press then rack focus to the bright blank screen`
- **Comp:** `GFX_01_prompt_screen.mov` على الشاشة (لو ظاهرة). **مفيش أي لوجو أو واجهة لكلود.** الواجهة محايدة عن قصد.

**S01B — Dive through the screen** · 0.8s · توليد 5s · كاميرا: *Crash Zoom In / Through Object*
- **Start:** = آخر فريم S01A (الشاشة في الفوكس).
- **End:** الشاشة بقت بوابة ضوء عاجي، والكاميرا جوّه فراغ أبيض دافي.
- **Prompt:** `Violent crash zoom straight into a glowing laptop screen, the screen surface dissolves into soft ivory light as camera passes through it, pixels becoming luminous dust, seamless transition into a bright warm white space`

**S01C — The storefront materializes** · 1.2s · توليد 5s · كاميرا: *360 Orbit (slow)*
- **Start:** فراغ عاجي دافي فيه جزيئات ضوء.
- **End:** متجر قهوة ثلاثي الأبعاد كامل (E1) طافي، الكاميرا بتلف حواليه 40°.
- **Prompt:** `In a warm ivory void, floating architectural fragments rapidly assemble into an elegant three-dimensional coffee storefront, glass shelves, dark coffee bags with cream labels, peach and ivory surfaces, soft daylight, polished reflections, camera begins a smooth orbit around the structure, breathtaking and premium, no readable text`

### SCENE 02 — AI CAN BUILD (4.60–12.60)
**S02A — It really is impressive** · 3.8s · توليد 5s · كاميرا: *Crane up + Orbit*
- **Start:** = آخر فريم S01C.
- **End:** المتجر كامل بكل أقسامه، لافتات زجاج طافية (فاضية)، كروت منتجات بقت أكياس بن حقيقية على الرفوف.
- **Prompt:** `A stunning floating three-dimensional coffee shop built from ivory stone, glass and warm wood, product cards morph into real coffee bags that slide onto glass shelves, translucent navigation signs float into place, a checkout counter assembles itself, everything clicks together with satisfying precision, soft 5600K daylight, camera cranes up and orbits revealing the whole structure, it looks genuinely impressive and polished`
- **ملاحظة إخراج:** لازم يبان **جميل بجد**. الرسالة إن الـAI بيعمل حاجة تبهر. ممنوع أي إحساس بإن فيه حاجة غلط هنا.

**S02B — FPV flythrough → exit through a real phone** · 4.2s · توليد 10s (أو 5s+5s) · كاميرا: *FPV Drone*
- **Start:** = آخر فريم S02A.
- **End:** = **أول فريم S03A بالظبط** (لقطة Over-the-shoulder ليوسف ماسك الموبايل). ده **Match Cut** على مستطيل الشاشة.
- **Prompt:** `Seamless FPV drone flight through the aisles of a floating ivory digital coffee storefront, weaving between glass shelves and coffee bags, the camera dives toward a glowing rectangular portal at the end of the aisle, passes through it and emerges out of a real smartphone screen into a cozy Cairo living room at blue hour, revealing a young man holding the phone over his shoulder, warm lamp light, city bokeh through the window`
- **Continuity:** آخر 0.5s لازم تطابق S03A (نفس الأباجورة، نفس الكنبة، نفس اللبس C1).

### SCENE 03 — THE CUSTOMER (12.60–20.40)
**S03A — Browsing** · 2.8s · توليد 5s · كاميرا: *Slow push-in, over-the-shoulder*
- **Start/End:** يوسف قاعد على كنبة، بيتصفّح بإبهامه، شاشة مضيئة فاضية. End: بيوقف على منتج.
- **Prompt:** `Over-the-shoulder shot of a 27-year-old Egyptian man with short dark curly hair and a trimmed beard, olive overshirt over a white t-shirt, silver watch, sitting on a sofa in a cozy Cairo apartment at blue hour, scrolling on a graphite-black smartphone with his thumb, bright plain white screen, warm lamp on the right, city lights bokeh, slow push-in, natural relaxed acting`
- **Comp:** `GFX_03_phone_ui.mov` (0.0–1.6s) Screen Replacement + Tracking + انعكاس خفيف.

**S03B — The thumb** · 1.0s · توليد 5s · كاميرا: *Macro, rack focus*
- **Prompt:** `Macro close-up of a thumb approaching a smartphone screen to press a large button area near the bottom, rack focus from the thumb to the screen, warm lamp light, shallow depth of field, anticipation`
- **Comp:** `GFX_03` من 1.0s، بحيث التلامس يقع عند 2.0s من الجرافيك.

**S03C — BULLET TIME** · 2.8s · توليد 5s · كاميرا: *Bullet Time / 180° Orbit*
- **Start:** لحظة تلامس الإبهام بالشاشة، كل حاجة متجمّدة.
- **End:** الكاميرا لفّت 180° وبقت قدّام الموبايل، شايفة الشاشة ووش يوسف في الخلفية.
- **Prompt:** `Frozen moment: a thumb touching a smartphone screen, time completely stopped, dust particles and a tiny drop of light suspended in the air, the camera performs a smooth 180-degree bullet-time orbit around the hand and phone, the young man's face softly out of focus in background, warm lamp light wrapping around, matrix-style frozen time without any green tint`
- **Comp:** `GFX_03` متجمّد على 2.0s، وبعدين الـsuccess sheet (2.9–3.6) يشتغل **على الشاشة المتجمّدة** وينزل على «ظهر له تم الإرسال» حوالي 18.4.

**S03D — The capsule is born** · 1.2s · توليد 5s · كاميرا: *Tilt up + follow*
- **Start:** = آخر فريم S03C.
- **End:** الكبسولة (P1) طالعة من الشاشة لفوق، وبتصغر لحد ما تبقى نقطة ضوء.
- **Prompt:** `From the point where the thumb touches the phone screen, a fist-sized glowing ivory glass capsule with a warm peach core rises out of the screen like a drop of light, the camera tilts up and follows it as it accelerates away and shrinks into a bright pinpoint, seamless`
- **Comp:** `GFX_00_capsule_label.mov` متتبّعة على الكبسولة.

### SCENE 04 — THE INVISIBLE FAILURE (20.40–26.00) — **أقوى لحظة في الفيلم**
**S04A — The tunnel** · 2.0s · توليد 5s · كاميرا: *FPV tracking behind subject*
- **Start:** نقطة الضوء (آخر S03D) بتتفتح على النفق E2.
- **End:** نهاية النفق باينة: الأنبوب بيقف فجأة في فراغ.
- **Prompt:** `High-speed tracking shot following a glowing ivory glass capsule with a warm peach core through a long transparent glass tunnel suspended in a dark graphite void, glass ribs streaking past, cool caustic light, growing tension, the tunnel abruptly ends ahead in empty darkness`

**S04B — The barrier (full reveal of the cold open)** · 3.6s · توليد 5s · كاميرا: *Locked → very slow creep-in*
- **Start:** = آخر فريم S04A.
- **End:** الكبسولة متعلّقة في الهوا قدّام حاجز مش مرئي، تموّج ساكن، الضوء جواها بيخفت شوية. الكاميرا قرّبت ببطء شديد.
- **Prompt:** `The glowing capsule slams into an invisible barrier at the end of the glass tunnel, a circular ripple spreads through empty air like struck glass, peach light shards freeze mid-air, the capsule hangs suspended and motionless, its inner glow slowly dims, the camera creeps in very slowly, total stillness, cold rim light, lonely and silent, the strongest image of the film`
- **Comp:** `GFX_04_sent_ne_received.mov` من 22.6 («تم الإرسال» ← «≠» ← «تم الاستلام» باهت ← خط أحمر بيكسرها). **الموسيقى تقطع تمامًا 22.25–24.0.** يفضل بس الـimpact وroom tone منخفض.
- **التجميد هنا جزء من الأداء:** لازم ييجي من الفيديو المتولّد (جزيئات بتتحرك ببطء شديد، الكاميرا بتزحف). ممنوع فريم ثابت.

### SCENE 05 — TWO REALITIES (26.00–29.20)
**S05A — He's waiting** · 1.4s · توليد 5s · كاميرا: *Static-ish, gentle drift*
- **Prompt:** `The same young man sitting on the sofa at blue hour, glancing at his phone with a small satisfied smile, places it face-down on the cushion and leans back, waiting for a reply, warm lamp, quiet, natural subtle acting`

**S05B — Through the glass partition** · 1.8s · توليد 5s · كاميرا: *Lateral truck through glass*
- **Start:** يوسف على الشمال في الكادر.
- **End:** كريم في المحمصة بالليل، بيبص على اللابتوب (شاشة فاضية مضيئة) وبيقفل.
- **Prompt:** `Lateral dolly move: camera glides sideways from a man relaxing on a sofa through a tall cinematic glass partition that refracts the light, emerging on the other side in a small coffee roastery at night where a 40-year-old Egyptian man with a salt-and-pepper beard and a burgundy apron glances at his laptop on a wooden counter and starts closing up, two worlds side by side separated by glass, cool on one side warm on the other`
- **Comp:** `GFX_05_dashboard_empty.mov` على اللابتوب. **مفيش تمثيل زيادة**: نظرة عادية، ولا يعرف حاجة.

### SCENE 06 — THE WASHEEJ EFFECT (29.20–42.40) — One-take وهمي
> بيتبني من 3 توليدات متوصّلة بـ**hidden wipes** (عدّية عبر زجاج/ليفة خيط قريبة من العدسة). الإضاءة بتتحوّل من بارد لدافي على مدار اللقطة.

**S06A — The thread enters** (29.2–33.6) · توليد 5s · كاميرا: *Push into screen → FPV*
- **Start:** شاشة لابتوب كريم (لوحة فاضية).
- **End:** الكاميرا جوّه المتجر الرقمي (E1، أخفت دلوقتي)، والخيط T1 بيلف حوالين رف المنتج وبيتشد.
- **Prompt:** `The camera pushes into a glowing laptop screen and enters a dimmed version of an ivory floating coffee storefront, a single luminous organic thread with a warm peach core and a deep burgundy glow, made of fine ink-like fibres, enters from the darkness and wraps precisely around a coffee bag on a glass shelf, pulling taut, purposeful movement, camera follows the thread closely`

**S06B — Cart → submit → tunnel → snag** (33.6–39.0) · توليد 10s · كاميرا: *FPV following the thread*
- **End:** الخيط وصل لنهاية النفق، اتشد على الحاجز الخفي، وبيترعش.
- **Prompt:** `Continuous FPV shot following a luminous burgundy-and-peach fibrous thread as it travels from a shopping cart through a glowing button portal into a transparent glass tunnel, each junction it passes lights up warmly, the thread reaches the end of the tunnel where an invisible barrier holds a dimmed capsule, the thread snags against the invisible wall and trembles under tension, the barrier briefly reveals a hairline crack of light`

**S06C — Repair → full re-test → arrival** (39.0–42.4) · توليد 5s · كاميرا: *Orbit around knot → whip along thread → push out of screen*
- **End:** = أول فريم من لوحة الطلبات وفيها الطلب واصل (screen replace).
- **Prompt:** `The luminous fibrous thread stitches through the invisible barrier with precise sewing-like loops and ties a tight knot, the barrier dissolves into warm light, the capsule brightens and resumes its journey, a bright pulse runs along the entire thread from start to end, camera whips along with the pulse and exits through a laptop screen into a warm roastery, lighting turns warm 3200K`
- **Comp:** `GFX_06_journey.mov` (labels/HUD متزامن مع الصوت) من 29.4. آخر 0.7s: `GFX_05_dashboard_arrive.mov` (من 1.0s). Glow/bloom خفيف على الخيط من غير ما يغطي الوشوش.

### SCENE 07 — THE REAL BUSINESS VALUE (42.40–51.40)
**S07A — Working normally** · 2.6s · توليد 5s · كاميرا: *Smooth handheld / gimbal*
- **Prompt:** `Morning in a small specialty coffee roastery, warm window side light, the 40-year-old owner in a burgundy apron calmly pours freshly roasted beans from a copper roaster into a cooling tray, steam and dust in the light beams, relaxed and in control, smooth gimbal move`

**S07B — Pressure + DOLLY ZOOM** · 4.8s · توليد 5s · كاميرا: *Dolly Zoom (Vertigo)*
- **Start:** كريم في النص، مرتاح.
- **End:** حوالين كريم 6–8 ألواح زجاج مضيئة طافية (فاضية)، الخلفية اتمطّت بالدولي زوم، والرجل متوتر.
- **Prompt:** `Dolly zoom vertigo effect on the roastery owner standing at his counter, translucent frosted glass panels appear one by one and float around him at different depths, multiplying and closing in, the background stretches away while he stays the same size, he stops working and looks overwhelmed, light turns colder and harsher, claustrophobic`
- **Comp:** `GFX_07_window_1..6.png` على الألواح (Corner-pin/3D camera track)، ظهور متتابع مع «لو كل يوم هتسيب شغلك…». ترتيب الظهور: 1 ← 2 ← 4 ← 3 ← 6 ← 5.

**S07C — Reverse the chaos** · 1.6s · توليد 5s · كاميرا: *Reverse dolly zoom → settle*
- **Prompt:** `The floating glass panels fold away and get pulled into a single luminous burgundy fibrous thread that zips out of frame, the space relaxes back to normal, warm light returns, the owner exhales, glances at his laptop as a new order arrives, a small smile, returns to roasting`
- **Comp:** `GFX_05_dashboard_arrive.mov` (من 0.6s) على اللابتوب.

### SCENE 08 — FINAL BRAND REVEAL (51.40–58.50)
**S08A — Pull out + thread wipe** · 1.25s (شامل crossfade 0.25) · توليد 5s · كاميرا: *Pull-back / Crane out*
- **End:** الكادر كله بيغرق في Burgundy عميق عن طريق الخيط (يطلع من تحت يمين الكادر).
- **Prompt:** `Camera pulls back and up out through the roastery window, the luminous thread rises from the laptop, sweeps across the frame from bottom right and the image dissolves into a deep burgundy field with soft paper texture, elegant and calm`

**END — `GFX_08_endcard.mov` (جاهز ومرندر)** · 6.1s
الخيط بيدخل من تحت يمين ← بيكتب «وشيج» بالقناع الأصلي من الموقع ← WASHEEJ ← «نصنع الرابط بين علامتك وعملائها» ← washeej.site. حركة الشعار نفَس 3.5% بس، ومفيش حركة زيادة.

---

## 5. الأصول المطلوبة (Asset List)

| # | الأصل | الحالة | المسار |
|---|---|---|---|
| 1 | الشعار الأصلي (3 نسخ SVG) + أيقونة + OG + ورق الخوخ | ✅ مستخرج | `brand/` |
| 2 | الخطوط Readex Pro + Cormorant Garamond (من الموقع) | ✅ | `brand/fonts/` |
| 3 | GFX_00 ملصق الكبسولة «تم الإرسال» (alpha) | ✅ مرندر | `renders/GFX_00_capsule_label.mov` |
| 4 | GFX_01 شاشة البرومبت (محايدة) | ✅ | `renders/GFX_01_prompt_screen.mov` |
| 5 | GFX_03 واجهة موبايل «دار البُنّ» + الضغط + «تم الإرسال» | ✅ 1170×2532 | `renders/GFX_03_phone_ui.mov` |
| 6 | GFX_04 «تم الإرسال ≠ تم الاستلام» (alpha) | ✅ | `renders/GFX_04_sent_ne_received.mov` |
| 7 | GFX_05 لوحة الطلبات: فاضية / الطلب وصل | ✅ | `renders/GFX_05_dashboard_*.mov` |
| 8 | GFX_06 رحلة الخيط (labels، متزامنة مع الصوت، alpha) | ✅ 13s | `renders/GFX_06_journey.mov` |
| 9 | GFX_07 ست نوافذ مشاكل (PNG alpha @2x) | ✅ | `renders/GFX_07_window_1..6.png` |
| 10 | GFX_08 لقطة الختام بالشعار | ✅ 6.5s | `renders/GFX_08_endcard.mov` |
| 11 | 22 لقطة سينمائية (S00–S08A) | ⛔ محتاجة توليد | `shots/<ID>.mp4` |
| 12 | صور مرجعية للشخصيات C1/C2 (Soul ID) | ⛔ | `refs/` |
| 13 | التعليق الصوتي الأصلي | ⛔ ما اتسلّمش | `audio/vo.wav` أو `audio/vo/V1.wav…` |
| 14 | الموسيقى (مرخّصة) | ⛔ | `audio/music.wav` |
| 15 | المؤثرات الصوتية (23 cue، الأسماء في `timeline.json`) | ⛔ | `audio/sfx/*.wav` |

كل ملفات `.mov` بصيغة **ProRes 4444 بقناة ألفا** (للتراكب) أو ProRes 422 HQ (للشاشات). ومعاها نسخ معاينة H.264 في `renders/preview/`.

---

## 6. الكاميرا والانتقالات (لماذا كل حركة)

| الانتقال | النوع | المعنى |
|---|---|---|
| S00 ← S00R ← S01A | Freeze + Rewind عنيف | «استنى، هنرجع لأول الحكاية». بيزرع اللغز |
| S01A ← S01B | Crash Zoom في الشاشة | دخول عالم الموقع |
| S02B ← S03A | **Match cut** على مستطيل الشاشة (FPV يخرج من الموبايل) | الموقع الجميل ده هو اللي في إيد العميل دلوقتي |
| S03C | Bullet Time | اللحظة اللي العميل فيها «خلّص». بنوقف الزمن عشان نحس بثقلها |
| S03D ← S04A | الكبسولة تصغر لنقطة ← النقطة تتفتح نفق | Object transition |
| S04B | سكون + صمت | ده **سؤال الـCold Open بيتجاوب** |
| S05A ← S05B | Truck عبر زجاج | الحاجز بين الحقيقتين هو نفس زجاج النفق |
| S06 | One-take (3 توليدات، hidden wipes) | الاختبار رحلة واحدة متصلة، مش خطوات منفصلة |
| S07B | Dolly Zoom | الضغط النفسي: العالم بيتمط والراجل محبوس |
| S07C | Dolly Zoom بالعكس | الراحة |
| S08A ← END | الخيط يعمل Wipe بالـBurgundy ← نفس الخيط يكتب الشعار | الخيط اللي صلّح الرحلة هو نفسه «وشيج» |

---

## 7. الصوت والمونتاج

**الموسيقى (مخطط الأوتوميشن موجود في `timeline.json`):** تبدأ ناعمة (بيانو/أوتار ممسوحة) ← نبض خفيف من S03 ← توتر من S04A ← **قطع تام 22.25–24.0** ← عودة خافتة ومعلّقة في S05 ← دفء تدريجي من S06 (أوتار + بيس دافي) ← ثقة في S07C ← حلّ هادي على الشعار. Sidechain تحت التعليق (ratio 3:1) معمول في السكربت.

**Sound design (23 cue بالتوقيت في `timeline.json`):** whoosh النفق، impact زجاجي مكتوم (مش انفجار)، tape-rewind، crash-zoom whoosh، تجميع رقمي ناعم، FPV pass، نقرة UI، **time-freeze suck** للـBullet Time، chime نجاح، إطلاق الكبسولة، room tone منخفض في الصمت، مرور زجاج، **pluck وتر دافي** للخيط، **snag** (شدّة خيط)، **ربط عقدة**، صعود نبضة الاختبار، ding وصول الطلب، سرب إشعارات (S07B)، swoosh عكسي للتحرّر.

**قواعد:**
- التعليق صوته واضح دايمًا، والهدف ‑14 LUFS integrated و True Peak ≤ ‑1 dBTP (السكربت بيعملها two-pass loudnorm).
- الـCold Open قبل أول كلمة (التعليق يبدأ 1.20).
- كل قطع على كلمة أو نَفَس، مش في نص كلمة.
- Safe area للـReels/TikTok: أهم عنصر بين y=220 و y=1500، وولا نص في أسفل 380px أو في الـ120px على اليمين.

---

## 8. Workflow عملي (بالترتيب)

1. **سجّل التعليق** بالنص الحرفي (لا تعديل). `tools/measure_vo.py` ← حدّث `vo.lines` في `timeline.json`.
2. **ثبّت الشخصيات:** Soul ID لـC1 وC2 (3 صور لكل واحد). ثبّت P1 (الكبسولة) كصورة مرجعية واحدة تتكرر في كل برومبت.
3. **ولّد صور البداية/النهاية** لكل لقطة (9:16، من غير نص).
4. **ولّد بالترتيب ده:** S04A ← S04B ← S00 (من نفس الإعداد) ← S03 ← S02 ← S01 ← S05 ← S06 ← S07 ← S08A. نبدأ بأقوى لحظة عشان تحدد اللوك.
5. **Comp:** Screen replacement + tracking لـ S01A، S03A–C، S05B، S06C، S07B، S07C بملفات `renders/GFX_*`. احفظ النتيجة `shots/<ID>_comp.mp4` (السكربت بيفضّلها).
6. **Grade موحّد** (LUT واحد لكل فصل، الجدول في القسم 2).
7. `python3 tools/assemble.py --check` ← لازم يقول All shots present.
8. `python3 tools/assemble.py` ← الماستر في `renders/`.
9. `tools/qa.sh renders/WASHEEJ_InvisibleOrder_9x16_1080x1920_30fps.mp4` ← مراجعة (القسم 9).

---

## 9. مراجعة النتيجة النهائية (QA Checklist)

**المونتاج:** الـCold Open أقل من 1.25s ومن غير نص تعريفي؟ هل S04B بتكرر S00 بوضوح (نفس الكبسولة والزاوية)؟ هل في أي لقطة أطول من اللازم من غير ما تكشف معلومة جديدة؟
**الحركة:** كل حركة كاميرا ليها سبب (جدول القسم 6)؟ مفيش warping في الإيدين في S03B/C؟ الكبسولة نفس الشكل في S00/S03D/S04/S06؟
**التزامن:** «تم الإرسال» تظهر على «ظهر له تم الإرسال». الاصطدام بعد «ما وصلكش» مباشرة. العُقدة على «وقفت». الإصلاح على «بنصلّحها». الشعار بيتكتب على «وشيج».
**جودة الصورة:** مفيش نص AI مشوّه في أي كادر (كل النص عربي من الجرافيك بس)، مفيش flicker في الوشوش، الـgrain موحّد، الـtracking ثابت.
**آلي (`tools/qa.sh`):** مواصفات H.264 High 1080×1920 30fps yuv420p / AAC 48k، Loudness ‑14 LUFS، **freezedetect** (المسموح بس: S03C، S04B، hold الختام)، blackdetect، لوحة كادرات لكل ثانية.

**نتيجة اختبار خط الإنتاج** (اتعمل في الجلسة دي على نسخة اختبار بلقطات Slate وصوت صناعي، **وده مش الفيلم**): المواصفات طلعت H.264 High 1080×1920 30fps، AAC 48k stereo، المدة 58.5s، الـLoudness ‑14.0 LUFS. الطبقات اتركّبت فوق فيديو متحرك بالشفافية والتوقيت الصح، والـcrossfade للختام اشتغل. والسكربت بيرفض لقطة ناقصة أو قصيرة بدل ما يملاها بفريم ثابت.

---

## 10. اللي ما اتنفّذش وليه (بدون ادّعاء)

| المطلوب | الحالة | السبب / المطلوب منك |
|---|---|---|
| توليد اللقطات السينمائية | ❌ ما اتعملش | Higgsfield مش متاح كأداة في الجلسة. Figma Weave (فيه موديلات فيديو) **رافض لأن حساب Figma مش مربوط بـWeave**: افتح app.weavy.ai ← Settings ← Profile ← اربط Figma. بعدها أقدر أولّد اللقطات من هنا (بعد موافقتك على التكلفة لكل لقطة) |
| صور البداية/النهاية | ⏸ ممكن | أداة Figma `generate_image` متاحة لكنها **بتصرف كريديت Figma AI** وبتحتاج ملف Figma. محتاج موافقتك |
| التعليق الصوتي | ❌ | ما اتسلّمش ملف صوت. وما ينفعش أولّد صوت مصري بديل لأنك طالب «التعليق الأصلي» |
| موسيقى/مؤثرات | ❌ | محتاجة مكتبة مرخّصة (Artlist/Epidemic…)، والأسماء والتوقيتات جاهزة |
| الـMP4 النهائي | ⏸ | جاهز بأمر واحد أول ما اللقطات والصوت يتحطوا |
