"""
Color Picker AI - Ekstraksi Warna Dominan dari Gambar
Praktikum Artificial Intelligence
Menggunakan algoritma K-Means Clustering untuk menemukan warna paling dominan.
"""

import streamlit as st
import numpy as np
from PIL import Image
from sklearn.cluster import KMeans
from collections import Counter
import webcolors

# ============================================================
# KONFIGURASI HALAMAN
# ============================================================
st.set_page_config(
    page_title="Color Picker AI",
    page_icon="🎨",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ============================================================
# CUSTOM CSS — Dreamy pastel aesthetic + animations
# ============================================================
st.markdown("""
<style>
    /* Reset & global */
    [data-testid="stSidebar"] { display: none; }
    [data-testid="collapsedControl"] { display: none; }
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    header[data-testid="stHeader"] { background: transparent; }
    
    /* ===== BACKGROUND: Mesh gradient yang bergerak ===== */
    .stApp {
        background: 
            radial-gradient(at 20% 30%, #FFD6E8 0px, transparent 50%),
            radial-gradient(at 80% 20%, #C8B6FF 0px, transparent 50%),
            radial-gradient(at 70% 80%, #B8E6FF 0px, transparent 50%),
            radial-gradient(at 30% 90%, #FFE5B4 0px, transparent 50%),
            radial-gradient(at 50% 50%, #FFF0F5 0px, transparent 50%),
            linear-gradient(135deg, #FDF4FF 0%, #F0F9FF 100%);
        background-size: 200% 200%, 200% 200%, 200% 200%, 200% 200%, 200% 200%, 100% 100%;
        animation: meshMove 25s ease infinite;
        min-height: 100vh;
    }
    
    @keyframes meshMove {
        0%, 100% {
            background-position: 0% 0%, 100% 0%, 100% 100%, 0% 100%, 50% 50%, 0% 0%;
        }
        50% {
            background-position: 100% 100%, 0% 100%, 0% 0%, 100% 0%, 50% 50%, 0% 0%;
        }
    }
    
    /* ===== FLOATING PARTICLES ===== */
    .particles {
        position: fixed;
        top: 0; left: 0;
        width: 100%; height: 100%;
        pointer-events: none;
        z-index: 0;
        overflow: hidden;
    }
    .particle {
        position: absolute;
        border-radius: 50%;
        opacity: 0.5;
        animation: float linear infinite;
    }
    
    @keyframes float {
        0% {
            transform: translateY(100vh) translateX(0) scale(0.5);
            opacity: 0;
        }
        10% { opacity: 0.6; }
        90% { opacity: 0.6; }
        100% {
            transform: translateY(-10vh) translateX(40px) scale(1);
            opacity: 0;
        }
    }
    
    /* Pastikan konten di atas particles */
    .block-container {
        position: relative;
        z-index: 1;
        padding-top: 2.5rem;
        padding-bottom: 2rem;
        max-width: 950px;
    }
    
    /* ===== JUDUL ===== */
    .main-title {
        font-size: 4rem;
        font-weight: 900;
        background: linear-gradient(90deg, #FF6FB5, #C77DFF, #7B9EFF, #6DD5FA, #FFB07C, #FF6FB5);
        background-size: 300% 300%;
        animation: gradientShift 6s ease infinite;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        letter-spacing: -2px;
        margin-bottom: 0.2rem;
        filter: drop-shadow(0 2px 20px rgba(199, 125, 255, 0.3));
        line-height: 1;
    }
    
    @keyframes gradientShift {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    .subtitle {
        text-align: center;
        color: #6b5b95;
        font-size: 1rem;
        margin-bottom: 2.5rem;
        font-weight: 500;
        letter-spacing: 0.5px;
    }
    
    /* ===== SLIDER STYLING ===== */
    .stSlider label {
        color: #5a4a7a !important;
        font-weight: 600 !important;
    }
    
    /* ===== UPLOAD AREA ===== */
    [data-testid="stFileUploader"] {
        background: rgba(255, 255, 255, 0.5);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        padding: 0.5rem;
        border: 2px dashed rgba(199, 125, 255, 0.4);
        transition: all 0.3s ease;
    }
    [data-testid="stFileUploader"]:hover {
        border-color: rgba(199, 125, 255, 0.7);
        background: rgba(255, 255, 255, 0.7);
    }
    
    /* ===== GAMBAR ===== */
    [data-testid="stImage"] img {
        border-radius: 20px;
        box-shadow: 
            0 10px 40px rgba(199, 125, 255, 0.2),
            0 4px 12px rgba(0, 0, 0, 0.05);
    }
    
    /* ===== SECTION HEADING ===== */
    .section-heading {
        font-size: 1.6rem;
        font-weight: 800;
        color: #5a4a7a;
        margin-top: 2rem;
        margin-bottom: 1rem;
        text-align: center;
        letter-spacing: -0.5px;
    }
    
    /* ===== COLOR GRID — flexbox auto-wrap ===== */
    .color-grid {
        display: flex;
        flex-wrap: wrap;
        gap: 18px;
        justify-content: center;
        margin-top: 1rem;
        perspective: 1000px;
    }
    
    /* ===== COLOR CARD — fancy with gradient border + glow ===== */
    .color-card {
        flex: 1 1 160px;
        min-width: 160px;
        max-width: 190px;
        position: relative;
        border-radius: 20px;
        overflow: hidden;
        background: white;
        transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275), 
                    box-shadow 0.4s ease;
        animation: cardFadeIn 0.7s ease backwards;
        transform-style: preserve-3d;
        box-shadow: 
            0 8px 24px rgba(199, 125, 255, 0.15),
            0 2px 6px rgba(0, 0, 0, 0.05);
    }
    
    /* Stagger animation tiap kartu */
    .color-card:nth-child(1) { animation-delay: 0.05s; }
    .color-card:nth-child(2) { animation-delay: 0.12s; }
    .color-card:nth-child(3) { animation-delay: 0.19s; }
    .color-card:nth-child(4) { animation-delay: 0.26s; }
    .color-card:nth-child(5) { animation-delay: 0.33s; }
    .color-card:nth-child(6) { animation-delay: 0.40s; }
    .color-card:nth-child(7) { animation-delay: 0.47s; }
    .color-card:nth-child(8) { animation-delay: 0.54s; }
    .color-card:nth-child(9) { animation-delay: 0.61s; }
    .color-card:nth-child(10) { animation-delay: 0.68s; }
    
    @keyframes cardFadeIn {
        from { opacity: 0; transform: translateY(30px) rotateX(-10deg); }
        to { opacity: 1; transform: translateY(0) rotateX(0); }
    }
    
    /* Gradient border using pseudo-element */
    .color-card::before {
        content: '';
        position: absolute;
        inset: 0;
        border-radius: 20px;
        padding: 2px;
        background: linear-gradient(135deg, #FF6FB5, #C77DFF, #7B9EFF, #6DD5FA);
        -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
        -webkit-mask-composite: xor;
        mask-composite: exclude;
        opacity: 0;
        transition: opacity 0.3s ease;
        pointer-events: none;
    }
    
    .color-card:hover {
        transform: translateY(-10px) rotateX(5deg) rotateY(-5deg) scale(1.03);
        box-shadow: 
            0 20px 40px rgba(199, 125, 255, 0.3),
            0 8px 16px rgba(0, 0, 0, 0.08);
    }
    
    .color-card:hover::before {
        opacity: 1;
    }
    
    /* Swatch dengan shimmer effect saat hover */
    .color-swatch {
        height: 110px;
        width: 100%;
        position: relative;
        overflow: hidden;
    }
    
    .color-swatch::after {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(
            90deg,
            transparent,
            rgba(255, 255, 255, 0.4),
            transparent
        );
        transition: left 0.6s ease;
    }
    
    .color-card:hover .color-swatch::after {
        left: 100%;
    }
    
    /* Info section */
    .color-info {
        padding: 14px 12px;
        text-align: center;
        background: white;
    }
    
    .color-name {
        font-size: 0.9rem;
        font-weight: 700;
        color: #5a4a7a;
        margin-bottom: 8px;
        text-transform: capitalize;
        letter-spacing: -0.2px;
    }
    
    .color-hex {
        font-family: 'Courier New', monospace;
        font-size: 0.95rem;
        font-weight: 800;
        color: #2d2438;
        margin-bottom: 4px;
        letter-spacing: 0.5px;
    }
    
    .color-rgb {
        font-family: 'Courier New', monospace;
        font-size: 0.72rem;
        color: #8a7ba3;
        margin-bottom: 8px;
    }
    
    .color-pct {
        display: inline-block;
        font-size: 0.78rem;
        font-weight: 700;
        color: white;
        background: linear-gradient(135deg, #C77DFF, #7B9EFF);
        border-radius: 12px;
        padding: 3px 12px;
        box-shadow: 0 2px 8px rgba(199, 125, 255, 0.3);
    }
    
    /* Info box (sebelum upload) */
    .stAlert {
        background: rgba(255, 255, 255, 0.7) !important;
        backdrop-filter: blur(10px);
        border-radius: 16px !important;
        border: 1px solid rgba(199, 125, 255, 0.2) !important;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        color: #8a7ba3;
        font-size: 0.85rem;
        margin-top: 3rem;
        padding-top: 1.5rem;
        border-top: 1px solid rgba(199, 125, 255, 0.15);
        font-weight: 500;
    }
</style>

<!-- ===== FLOATING PARTICLES (HTML) ===== -->
<div class="particles">
    <div class="particle" style="left: 5%;  width: 14px; height: 14px; background: #FFB7DE; animation-duration: 22s; animation-delay: 0s;"></div>
    <div class="particle" style="left: 12%; width: 10px; height: 10px; background: #C8B6FF; animation-duration: 28s; animation-delay: 3s;"></div>
    <div class="particle" style="left: 20%; width: 18px; height: 18px; background: #B8E6FF; animation-duration: 25s; animation-delay: 7s;"></div>
    <div class="particle" style="left: 28%; width: 8px;  height: 8px;  background: #FFE5B4; animation-duration: 30s; animation-delay: 1s;"></div>
    <div class="particle" style="left: 36%; width: 12px; height: 12px; background: #FFB7DE; animation-duration: 26s; animation-delay: 12s;"></div>
    <div class="particle" style="left: 45%; width: 16px; height: 16px; background: #C8B6FF; animation-duration: 24s; animation-delay: 5s;"></div>
    <div class="particle" style="left: 54%; width: 9px;  height: 9px;  background: #B8E6FF; animation-duration: 32s; animation-delay: 9s;"></div>
    <div class="particle" style="left: 63%; width: 14px; height: 14px; background: #FFE5B4; animation-duration: 27s; animation-delay: 2s;"></div>
    <div class="particle" style="left: 72%; width: 11px; height: 11px; background: #FFB7DE; animation-duration: 29s; animation-delay: 15s;"></div>
    <div class="particle" style="left: 80%; width: 15px; height: 15px; background: #C8B6FF; animation-duration: 23s; animation-delay: 6s;"></div>
    <div class="particle" style="left: 88%; width: 10px; height: 10px; background: #B8E6FF; animation-duration: 31s; animation-delay: 10s;"></div>
    <div class="particle" style="left: 95%; width: 13px; height: 13px; background: #FFE5B4; animation-duration: 26s; animation-delay: 4s;"></div>
</div>

<!-- ===== SCRIPT: 3D tilt effect untuk kartu warna ===== -->
<script>
(function() {
    function attachTilt() {
        const cards = document.querySelectorAll('.color-card');
        cards.forEach(card => {
            if (card.dataset.tilt) return;
            card.dataset.tilt = '1';
            
            card.addEventListener('mousemove', e => {
                const rect = card.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;
                const cx = rect.width / 2;
                const cy = rect.height / 2;
                const rotY = ((x - cx) / cx) * 8;
                const rotX = -((y - cy) / cy) * 8;
                card.style.transform = `translateY(-10px) rotateX(${rotX}deg) rotateY(${rotY}deg) scale(1.03)`;
            });
            
            card.addEventListener('mouseleave', () => {
                card.style.transform = '';
            });
        });
    }
    // Run berulang karena Streamlit re-render
    attachTilt();
    setInterval(attachTilt, 1000);
})();
</script>
""", unsafe_allow_html=True)

# ============================================================
# FUNGSI EKSTRAKSI WARNA DOMINAN (K-MEANS)
# ============================================================
def extract_dominant_colors(image, num_colors=5):
    """Ekstrak warna dominan dari gambar menggunakan K-Means Clustering."""
    image = image.copy()
    image.thumbnail((200, 200))
    
    img_array = np.array(image)
    
    if len(img_array.shape) == 2:
        img_array = np.stack([img_array]*3, axis=-1)
    elif img_array.shape[2] == 4:
        img_array = img_array[:, :, :3]
    
    pixels = img_array.reshape(-1, 3)
    
    kmeans = KMeans(n_clusters=num_colors, random_state=42, n_init=10)
    kmeans.fit(pixels)
    
    colors = kmeans.cluster_centers_.astype(int)
    labels = kmeans.labels_
    label_counts = Counter(labels)
    total = len(labels)
    percentages = [label_counts[i] / total * 100 for i in range(num_colors)]
    
    sorted_indices = np.argsort(percentages)[::-1]
    colors = [tuple(colors[i]) for i in sorted_indices]
    percentages = [percentages[i] for i in sorted_indices]
    
    return colors, percentages

# ============================================================
# HELPER
# ============================================================
def rgb_to_hex(rgb):
    return '#{:02X}{:02X}{:02X}'.format(int(rgb[0]), int(rgb[1]), int(rgb[2]))

def closest_color_name(rgb):
    """Cari nama warna CSS terdekat berdasarkan jarak Euclidean."""
    min_dist = float('inf')
    closest_name = "unknown"
    try:
        for name in webcolors.names("css3"):
            r, g, b = webcolors.name_to_rgb(name)
            dist = (r - rgb[0])**2 + (g - rgb[1])**2 + (b - rgb[2])**2
            if dist < min_dist:
                min_dist = dist
                closest_name = name
    except Exception:
        closest_name = "unknown"
    return closest_name

# ============================================================
# UI UTAMA
# ============================================================
st.markdown('<h1 class="main-title">Color Picker AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">✨ Ekstrak warna dominan dari gambar dengan K-Means Clustering ✨</p>', unsafe_allow_html=True)

num_colors = st.slider(
    "Jumlah warna dominan",
    min_value=3,
    max_value=10,
    value=5
)

uploaded_file = st.file_uploader(
    "Upload gambar (JPG, PNG, JPEG)",
    type=['jpg', 'jpeg', 'png']
)

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, use_container_width=True)
    
    with st.spinner('✨ Menganalisis warna dengan K-Means...'):
        colors, percentages = extract_dominant_colors(image, num_colors)
        names = [closest_color_name(c) for c in colors]
    
    st.markdown('<div class="section-heading">🎨 Warna Dominan</div>', unsafe_allow_html=True)
    cards_html = '<div class="color-grid">'
    for color, pct, name in zip(colors, percentages, names):
        hex_code = rgb_to_hex(color)
        rgb_str = f"RGB({color[0]}, {color[1]}, {color[2]})"
        cards_html += (
            f'<div class="color-card">'
            f'<div class="color-swatch" style="background-color: {hex_code};"></div>'
            f'<div class="color-info">'
            f'<div class="color-name">{name}</div>'
            f'<div class="color-hex">{hex_code}</div>'
            f'<div class="color-rgb">{rgb_str}</div>'
            f'<div class="color-pct">{pct:.1f}%</div>'
            f'</div>'
            f'</div>'
        )
    cards_html += '</div>'
    st.markdown(cards_html, unsafe_allow_html=True)

else:
    st.info("👆 Upload gambar untuk mulai mengekstrak warna dominan")

st.markdown('<div class="footer">Praktikum Artificial Intelligence • Made with Streamlit ✨</div>', unsafe_allow_html=True)