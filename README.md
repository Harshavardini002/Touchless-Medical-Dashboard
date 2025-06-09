# 🩺 Touchless Medical Dashboard using Hand Gestures

This project is a real-time **touchless medical dashboard** that uses **hand gestures** to interact with vital patient parameters. It leverages computer vision to allow healthcare professionals to view patient vitals without physical contact — ideal for sterile or restricted environments.

---

## 🚀 Features

- Real-time **hand gesture recognition** (1–5 fingers)
- Live **vital signs monitoring** from synthetic patient data
- Interactive **Streamlit dashboard** with:
  - Auto-refresh
  - Dynamic highlighting based on gesture
- Modular and extensible structure

---

## 📁 Folder Structure


---

## 📷 Gesture Mapping

| Fingers Shown | Vital Parameter        |
|---------------|------------------------|
| 1             | Heart Rate             |
| 2             | Blood Pressure         |
| 3             | Oxygen Saturation      |
| 4             | Temperature            |
| 5             | Medication             |

---

## 🧠 How It Works

- `gesture_listener.py` detects hand gestures using MediaPipe.
- The number of fingers is mapped to a vital sign.
- The selected parameter is highlighted in the Streamlit dashboard using JSON communication.
- The dashboard refreshes automatically every 2 seconds.

---

## ✅ To Do (Future Enhancements)

- [ ] Implement swipe gesture (e.g., open sidebar with left-to-right motion)
- [ ] Add gesture classification testing for accuracy metrics
- [ ] Improve lighting and angle robustness in gesture detection
- [ ] Add backend (Flask/FastAPI) for data integration
- [ ] Deploy on cloud (e.g., Streamlit Cloud / Heroku / Render)

---



---

## 🧾 Requirements

```bash
streamlit
opencv-python
mediapipe
pandas
altair
streamlit_autorefresh
