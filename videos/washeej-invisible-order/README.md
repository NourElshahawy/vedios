# وشيج — «الطلب الخفي» (The Invisible Order)

إعلان 9:16، بدقة 1080×1920 و30fps. الطريقة: مجاني بالكامل (FLUX + Wan 2.2 على Hugging Face، Blender، HTML/Playwright، ffmpeg).

## الحالة
| الجزء | الحالة |
|---|---|
| الهوية (شعار SVG، خطوط، ألوان من washeej.site) | ✅ `brand/` |
| الجرافيك العربي + لقطة الختام بالشعار | ✅ `gfx/` → `renders/` (معاينات في `renders/preview/`) |
| لقطات بشرية (Wan) | 🟡 3 من 12: S03A، S03C، S07B في `gen/clips/` (الحصة المجانية حوالي 3 في اليوم) |
| CGI (Blender) | 🟡 S04B و S00 جاهزين. S04A و S03D و S06 بيترندروا |
| التعليق الصوتي | ⚠️ `audio/vo_original.wav` **مش مطابق للنص المعتمد** (لهجة خليجية). شوف `docs/VO_CHECK.md` |
| الموسيقى | ❌ بقرار العميل: مفيش موسيقى، مؤثرات صوتية بس |
| المونتاج النهائي | ⏳ بعد اكتمال اللقطات |

## الملفات المهمة
- `docs/PRODUCTION_BIBLE.md`: الستوري بورد، التايملاين، برومبتات Higgsfield، الصوت، والمراجعة
- `docs/FREE_GENERATION_KIT.md`: برومبتات الأدوات المجانية وجدول التوليد
- `docs/VO_CHECK.md`: مقارنة التسجيل بالنص المعتمد
- `timeline.json`: مصدر الحقيقة للمونتاج

## إعادة البناء (الملفات التقيلة مش على git)
```bash
tools/render_all.sh                                    # الجرافيك → renders/*.mov
for c in gen/clips/*_t1.mp4; do id=$(basename $c _t1.mp4); tools/post_wan.sh $c shots/$id.mp4; done
./cgi/render_all.sh && for s in S00 S04A S04B S03D S06; do tools/post_cgi.sh cgi/$s.mp4 shots/$s.mp4; done
python3 tools/assemble.py --check && python3 tools/assemble.py
tools/qa.sh renders/WASHEEJ_InvisibleOrder_9x16_1080x1920_30fps.mp4
```
