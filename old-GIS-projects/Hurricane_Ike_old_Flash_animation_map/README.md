# Hurricane Ike – Flash Animation Map (2011)

This project preserves a **Flash-based GIS animation** created in **2011** to visualize the path and impact of **Hurricane Ike (2008)**.  
The animation was originally built in Adobe Flash as part of early geospatial visualization work, and has now been restored using **Ruffle**, a modern Flash emulator that allows legacy `.swf` files to run safely in any browser.

This project is part of my **GIS portfolio archive**, showcasing my work in interactive mapping, temporal animation, and data‑driven geospatial storytelling.

---

## 🌐 View the Animation

Click below to watch the restored Hurricane Ike animation:

👉 **https://kmrw0101.github.io/KMR-portfolio/old-GIS-projects/Hurricane_Ike_old_Flash_animation_map/**

The animation loads directly in your browser using Ruffle — no plugins or downloads needed.

---

## 🧩 How the Animation Was Built (2011)

This project wasn’t just a simple Flash movie — it was a **data‑driven GIS visualization** built from scratch:

### **✔ Real storm center coordinates**
- The animation uses actual latitude/longitude points collected during Hurricane Ike’s progression.
- Each coordinate represents the storm’s center at a specific time.

### **✔ Animated storm track**
- The hurricane icon moves along the real storm path.
- The animation progresses through time, showing the storm’s movement across the Gulf of Mexico toward landfall.

### **✔ Spinning hurricane symbol tied to storm intensity**
- A custom hurricane icon rotates.
- The rotation speed increases or decreases based on the storm’s intensity at that point in time.
- This creates a visual cue for wind speed and storm strength.

### **✔ Geographic context**
- The storm track is overlaid on a Gulf Coast basemap.
- Coastlines, state outlines, and the Gulf of Mexico provide spatial reference.
- This helps viewers understand which areas were threatened as the storm approached land.

This was created before modern tools like Mapbox, Leaflet, or ArcGIS StoryMaps — everything was hand‑built using Flash timeline animation and coordinate‑based scripting.

---

## 📁 Project Structure

```
Hurricane_Ike_old_Flash_animation_map/
├── index.html                         # Webpage wrapper that loads the SWF via Ruffle
└── Real_Ike_RitterbuschComplete.swf   # Original Flash animation (2011)
```

---

## 🗺️ About the Visualization

The animation illustrates:

- Hurricane Ike’s storm track  
- Temporal progression of the storm  
- Changes in storm intensity  
- Spatial relationship to the Gulf Coast  
- Landfall movement and direction  

This project represents early work in **interactive geospatial storytelling**, combining real data, symbolic animation, and map‑based visualization.

---

## 📜 Notes

This project is part of a larger effort to **archive and preserve older GIS work** originally built in Flash.  
Using Ruffle ensures these animations remain viewable even after Flash’s end‑of‑life. RIP.


