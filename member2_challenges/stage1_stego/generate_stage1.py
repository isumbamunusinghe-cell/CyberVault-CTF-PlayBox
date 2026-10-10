#!/usr/bin/env python3
"""
Generates the Stage 1 challenge image.
Embeds the flag into EXIF UserComment metadata in standard ASCII format.
"""
import os
from PIL import Image, ImageDraw
import piexif

def create_challenge_image():
    # 1. Create a synthetic evidence badge / report image
    img = Image.new('RGB', (650, 320), color=(15, 23, 42))
    draw = ImageDraw.Draw(img)
    
    # Visual layout
    draw.text((25, 25), "CYBERVAULT SOLUTIONS - DIGITAL FORENSICS UNIT", fill=(56, 189, 248))
    draw.text((25, 55), "INCIDENT EVIDENCE ITEM: CV-2026-09A", fill=(203, 213, 225))
    draw.line([(25, 80), (620, 80)], fill=(51, 65, 85), width=2)
    
    draw.text((25, 100), "Asset: Recovered Workstation Cache Snapshot", fill=(148, 163, 184))
    draw.text((25, 125), "Custodian: Investigation Lead", fill=(148, 163, 184))
    draw.text((25, 150), "Hash Status: VERIFIED", fill=(34, 197, 94))
    
    draw.rectangle([(25, 190), (620, 280)], outline=(239, 68, 68), width=2)
    draw.text((45, 225), "[ CONFIDENTIAL AUDIT ARTIFACT - DO NOT DISTRIBUTE ]", fill=(239, 68, 68))

    # Output directory relative to script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, "evidence_photo.jpg")

    # 2. Build EXIF UserComment according to EXIF 2.2 standard:
    # 8-byte charset code ('ASCII\0\0\0') followed by the text
    flag_text = "CTF{hidden_message_found}"
    user_comment_bytes = b"ASCII\x00\x00\x00" + flag_text.encode("ascii")

    exif_dict = {
        "0th": {
            piexif.ImageIFD.Make: "CyberVault Security Cam",
            piexif.ImageIFD.Software: "AuditCapture v2.4"
        },
        "Exif": {
            piexif.ExifIFD.UserComment: user_comment_bytes
        }
    }
    
    exif_bytes = piexif.dump(exif_dict)
    img.save(output_path, "jpeg", exif=exif_bytes, quality=95)
    
    print(f"[+] Successfully generated: {output_path}")
    print(f"[+] Embedded Flag: {flag_text}")

if __name__ == "__main__":
    create_challenge_image()