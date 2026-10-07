import cv2
import numpy as np
from PIL import Image
from rembg import remove

def prep_portrait(input_path, output_path):
    src = Image.open(input_path).convert("RGB")
    src_np = np.array(src)
    
    # 1. Background removal using rembg
    cut = remove(src)
    alpha = np.array(cut.split()[-1]).astype(np.float32) / 255.0
    
    # Grayscale
    gray = cv2.cvtColor(src_np, cv2.COLOR_RGB2GRAY).astype(np.float32)
    
    # 2. Local contrast enhancement (CLAHE) on the subject
    clahe = cv2.createCLAHE(clipLimit=2.8, tileGridSize=(8, 8))
    g_uint8 = np.clip(gray, 0, 255).astype(np.uint8)
    enhanced = clahe.apply(g_uint8).astype(np.float32) / 255.0
    
    # 3. Tone scaling
    # Ensure facial highlights pop and shadows/features have depth
    mask_subj = alpha > 0.3
    lo, hi = np.percentile(enhanced[mask_subj], [2, 98])
    tone = np.clip((enhanced - lo) / max(hi - lo, 0.01), 0, 1)
    
    # 4. Feature edge extraction (DoG - Difference of Gaussians) for eye, nose, beard, curls
    fine = cv2.GaussianBlur(tone, (0, 0), 1.2)
    coarse = cv2.GaussianBlur(tone, (0, 0), 4.5)
    dog_edges = np.clip(fine - coarse, -1, 1)
    
    # Boost edges in the face and hair
    enhanced_features = np.clip(tone + 0.35 * dog_edges, 0, 1)
    
    # 5. Base silhouette & Rim: ensure hair, ear and t-shirt have a recognizable outline
    soft_mask = cv2.GaussianBlur(alpha, (0, 0), 1.2)
    edge_rim = np.clip(cv2.GaussianBlur(alpha, (0, 0), 3.0) - cv2.erode(alpha, np.ones((5, 5))), 0, 1)
    
    # Minimum floor for subject so t-shirt and hair don't completely vanish
    subject_layer = np.maximum(enhanced_features, 0.08) + 0.25 * edge_rim
    final_light = np.clip(subject_layer * soft_mask, 0, 1)
    
    # 6. Crop and center the subject nicely
    ys, xs = np.where(alpha > 0.15)
    h, w = final_light.shape
    pad = 30
    min_x, max_x = max(0, xs.min() - pad), min(w, xs.max() + pad)
    min_y, max_y = max(0, ys.min() - pad), min(h, ys.max() + pad)
    
    span = max(max_x - min_x, max_y - min_y)
    cx = (min_x + max_x) // 2
    cy = (min_y + max_y) // 2
    
    x0 = max(0, min(w - span, cx - span // 2))
    y0 = max(0, min(h - span, cy - span // 2))
    
    crop = final_light[y0:y0+span, x0:x0+span]
    
    res = Image.fromarray((crop * 255).astype(np.uint8), mode="L").resize((900, 900), Image.LANCZOS)
    res.save(output_path)
    print("Prepped portrait saved to", output_path)

if __name__ == "__main__":
    prep_portrait("assets/portrait-source.png", "assets/portrait-prepped.png")
