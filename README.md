
# 💧 The Hidden Water Map

### How water stress intersects with the world's food production

**Women in Data Datathon 2026 — Query Queens**

---

## 🌍 The Problem

Food production depends heavily on reliable water systems. Yet high agricultural output today does not necessarily mean that the underlying water system is sustainable.

Our project asks:

> **Where is today's food production dependent on water systems under structural pressure?**

Rather than predicting immediate crop failure, we identify where significant food production is already occurring alongside high water stress and strong agricultural dependence on water withdrawals.

---

## 🔎 Our Key Finding

Water stress does not automatically correspond to low agricultural production.

Instead, some countries maintain substantial food production while operating under significant water pressure.

This creates a **resilience risk**:

> **Today's food output can mask tomorrow's water vulnerability.**

---

## 📊 What We Analysed

We combined:

- **FAOSTAT crop production data**
- **FAO AQUASTAT water-stress indicators**
- Agricultural water withdrawal data

### Analysis year

**2022**

### Focus crops

- Sugar cane
- Rice
- Wheat
- Potatoes
- Maize

---

## 🚨 Key Results

Among the five focus crops:

| Crop | Production exposed to severe water stress |
|---|---:|
| Sugar cane | 23.8% |
| Rice | 16.6% |
| Potatoes | 13.5% |
| Wheat | 12.6% |
| Maize | 3.9% |

Exposure means production occurring in countries where observed water stress was **≥50%**.

---

## 🇮🇳🇵🇰 Major Production Hotspots

India and Pakistan stand out because they combine:

- substantial food production,
- severe water stress,
- and high agricultural dependence on water withdrawals.

### India

- Water stress: **66.5%**
- Agricultural withdrawal share: **90.4%**

### Pakistan

- Water stress: **110.0%**
- Agricultural withdrawal share: **94.0%**

Together, India and Pakistan account for approximately:

- **21.6% of global sugar cane production**
- **15.3% of global rice production**
- **8.9% of global wheat production**
- **8.6% of global potato production**
- **2.5% of global maize production**

These figures highlight where food-system resilience may depend heavily on water systems already under pressure.

---

## 🧭 Our Risk Framework

We define a **high-pressure hotspot** as a country meeting both conditions:

### Water stress

**≥50%**

### Agricultural dependence

**≥75% of total water withdrawals**

These are **project analytical thresholds**, not official FAO risk categories.

---

## 📈 Dashboard

The interactive dashboard allows users to explore:

1. Global food production exposure
2. Water stress versus agricultural dependence
3. Major production hotspots
4. Country–crop exposure
5. Production shares and water indicators

---

## 💡 Why This Matters

The question is not simply:

> "Which countries produce the most food?"

It is:

> **"Which food production systems are most dependent on water systems under pressure?"**

This reframes water stress from an immediate production problem into a **food-system resilience challenge**.

Potential responses include:

- improving irrigation efficiency,
- increasing productivity per unit of water,
- adapting crop choices,
- improving water governance,
- and strengthening monitoring of agricultural water dependence.

---

## ⚠️ Important Caveats

- The analysis is based on **2022** data.
- Water-stress data coverage varies across countries and crops.
- Exposure does **not** mean that crop losses will occur.
- The analysis identifies structural associations and hotspots; it does not establish causality.
- Water stress values above 100% can occur under the SDG 6.4.2 methodology and should not automatically be treated as data errors.
- The ≥50% severe-stress threshold is an analytical choice made for this project.

---

## 🗂️ Data Sources

### FAO FAOSTAT
Crop production statistics.

### FAO AQUASTAT
Water stress and agricultural water indicators.

---

## 👥 Team

**Query Queens**

Women in Data Datathon 2026

---

## 🎯 Project Thesis

> **Water stress does not necessarily reduce today's food production — it can reveal how vulnerable tomorrow's food system may be.**

---

## 🛠️ Technologies

- Python
- Pandas
- Plotly
- Streamlit
- FAOSTAT
- AQUASTAT
- Data analysis and visualisation

---

## 📌 Disclaimer

This project is intended for exploratory data analysis and decision-support storytelling. The results should not be interpreted as forecasts of crop failure or official assessments of national food-security risk.
