#  Improving Customer Satisfaction in Ride-Sharing: A Data-Driven Analysis of Uber Ride Behavior (2024)

## 📊 A Data Analytics Case Study

---

## 📌 Project Overview

Customer satisfaction is one of the most critical metrics in the ride-sharing industry. High wait times, inconsistent driver behavior, cancelled bookings, and inefficient vehicle assignment all contribute to poor customer experience.

This project analyzes **148,770 Uber ride bookings from 2024** to uncover the key factors influencing:

- ⭐ **Customer Satisfaction**
- 🚫 **Cancellations** (Customer & Driver)
- 🚕 **Vehicle performance**
- 💰 **Revenue and distance patterns**
- ⏱ **Operational efficiency** (VTAT & trip duration)

The goal is to help ride-sharing operations teams make data-driven decisions that increase user satisfaction, reduce cancellations, and improve overall service reliability.

---

## 🔍 Business Problem

Uber wants to understand:

- Why customers are cancelling rides
- Which factors drive poor ratings
- Which vehicle types underperform
- Where operational inefficiencies occur
- How to optimize customer experience at scale

This analysis provides the insights needed to improve CSAT, reduce churn, and increase trip completion rates.

---

## 🎯 Project Objectives

### Primary Objective
➡️ Identify the leading indicators of customer satisfaction and propose improvements.

### Secondary Objectives
- Analyze customer and driver cancellation patterns
- Understand operational metrics (pickup time, distance, trip duration)
- Evaluate vehicle-type performance
- Measure revenue impact of cancellations
- Build an interactive performance dashboard
- Make actionable business recommendations

---

## 🧾 Dataset Summary

| Metric | Value |
|--------|-------|
| **Total Bookings** | 148,770 |
| **Completed Rides** | 93,000 |
| **Overall Success Rate** | 65.96% |
| **Cancellation Rate** | 25% |
| • Customer cancellations | 19.15% |
| • Driver cancellations | 18.49% |

### Key Columns
- Booking Status
- Vehicle Type
- Pickup/Drop Location
- Avg VTAT (pickup wait time)
- Avg CTAT (trip duration)
- Booking Value
- Cancellation Reason
- Customer/Driver Ratings
- Payment Method

---

## 🛠️ Tools & Technologies

| Category | Tools |
|----------|-------|
| **Data Cleaning & Analysis** | Python (Pandas, NumPy) |
| **Visualization** | Matplotlib |
| **Notebook** | Jupyter Notebook |
| **Documentation** | Markdown, GitHub |

---

## 📥 Data Cleaning & Preparation

The following steps were completed:

1. Removed null and inconsistent values
2. Extracted hour of day & day of week

---

## 🔎 Exploratory Data Analysis (EDA)

### 1️⃣ Customer Satisfaction Analysis

**Correlation between Customer Rating and:**
- Pickup wait time (VTAT)
- Trip duration (CTAT)
- Vehicle type
- Cancellation history

**Key Insight:**  
*Higher VTAT (wait time) strongly correlates with lower customer rating.*

---

### 2️⃣ Cancellation Analysis

**Analysis includes:**
- Breakdown of customer vs driver cancellations
- Most common cancellation reasons
- Cancellations by time of day
- Vehicle types with highest cancellations
- Pickup locations with highest cancellation concentration

**Key Insight:**  
*Customer cancellations peak during morning and evening rush hours, often linked to long pickup times.*

---

### 3️⃣ Vehicle Type Performance

**Metrics analyzed:**
- Success rate
- Avg distance per trip
- Total distance covered
- Avg customer rating
- Avg booking value

**Key Insight:**  
*UberXL offers the highest success rate and stable ratings despite lower total bookings.*

---

### 4️⃣ Revenue & Distance Insights

**Analysis includes:**
- Revenue per vehicle category
- Revenue lost due to cancellations
- High-value routes
- Payment method trends


---

## 📁 Repository Structure

```
ride-bookings/
│
├── Rides           # Jupyter notebook with full analysis  
│
├── README.md              # This portfolio document
└── requirements.txt       # Libraries used
```

---

## 🚀 Getting Started

### Prerequisites
```bash
Python 3.8+
pandas
numpy
matplotlib
seaborn
jupyter
```

### Installation
```bash
# Clone the repository
git clone https://github.com/Loutimi/ride-bookings.git

# Install dependencies
pip install -r requirements.txt

# Launch Jupyter Notebook
jupyter notebook
```

---

## 📈 Results Summary

- Identified **pickup wait time** as the primary driver of customer dissatisfaction
- Discovered **25% cancellation rate** with actionable patterns by time and location
- **UberXL** demonstrates best performance metrics across categories
- Potential **12-18% improvement** in ratings through VTAT reduction

---

## ⭐ Conclusion

This project demonstrates:

- ✅ Strong analytical skills
- ✅ Ability to translate data into business-driven insights
- ✅ Understanding of customer experience metrics
- ✅ End-to-end project ownership

---

## 👤 Author

**Rotimi Musa**  
Data Analyst | Business Intelligence Specialist

- 📧 Email: [loutimi59@gmail.com]
- 🐱 GitHub: [@loutimi]

---

## 🙏 Acknowledgments

- Dataset source: [[Dataset](https://www.kaggle.com/datasets/yashdevladdha/uber-ride-analytics-dashboard/data)]
- Inspiration from real-world ride-sharing operational challenges
- Tools and libraries from the open-source community

---