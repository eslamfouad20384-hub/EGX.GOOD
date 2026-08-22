# EGX AI PRO MAX — النسخة المعدلة

## أهم الإصلاحات
- Backtesting تاريخي event-driven: الإشارة على الشمعة الحالية والتنفيذ على Open الشمعة التالية، بدون look-ahead.
- Confirmed Swing High/Low مع تأكيد بعد 3 شموع.
- Fibonacci مبني على آخر Swing مؤكد بدل Rolling High/Low الحالي.
- Target Engine هيكلي فقط: Resistance / Confirmed Swing / Weekly / Monthly / Fibonacci Extensions. لا يتم اختراع TP بواسطة ATR عند غياب المستويات.
- منع ترتيب الأهداف العكسي، والأهداف غير المتاحة تظهر كـ NaN بدل أسعار مصطنعة.
- Liquidity مبنية على EGP turnover (Close × Volume) مقارنة بالـ median rolling turnover.
- Relative Strength مقارنة بعائد 20 يوم للـ EGX cross-sectional proxy.
- تحسين Pullback ليعتمد على مستويات دعم/سوينج/فيبوناتشي قريبة ومؤكدة.
- Breakout يعتمد على previous resistance فقط، مع حجم وBody وTrend.
- EMA200 لا يعتبر مكتملًا قبل 200 شمعة.

## التشغيل
```bash
pip install -r requirements.txt
streamlit run app.py
```

> البيانات تعتمد على Yahoo Finance من خلال yfinance، وتوفر البيانات تختلف حسب السهم والفترة.
