"""
Batch fetch best available images from Wikipedia/Wikimedia for all 45 analysis questions.
"""
import json, base64, io, os, sys, time, re, urllib.request, urllib.parse, urllib.error
from PIL import Image

TOPICS = [
    # Sensor Technology (subject index 0)
    {"id": 401, "sub":0, "q":"resistance_strain_gauge", "wiki":"Strain_gauge"},
    {"id": 402, "sub":0, "q":"thermocouple", "wiki":"Thermocouple"},
    {"id": 403, "sub":0, "q":"capacitive_sensor", "wiki":"Capacitive_sensing"},
    {"id": 404, "sub":0, "q":"piezoelectric_effect", "wiki":"Piezoelectricity"},
    {"id": 405, "sub":0, "q":"hall_effect_sensor", "wiki":"Hall_effect_sensor"},
    {"id": 406, "sub":0, "q":"wheatstone_bridge", "wiki":"Wheatstone_bridge"},
    {"id": 407, "sub":0, "q":"half_bridge_compensation", "wiki":"Wheatstone_bridge"},
    {"id": 408, "sub":0, "q":"lvdt", "wiki":"Linear_variable_differential_transformer"},
    {"id": 409, "sub":0, "q":"eddy_current_sensor", "wiki":"Eddy_current"},
    {"id": 410, "sub":0, "q":"pt100_rtd", "wiki":"Resistance_thermometer"},
    {"id": 411, "sub":0, "q":"piezoelectric_accelerometer", "wiki":"Accelerometer"},
    {"id": 412, "sub":0, "q":"eddy_current_displacement", "wiki":"Eddy_current"},
    {"id": 413, "sub":0, "q":"fiber_optic_sensor", "wiki":"Fiber-optic_sensor"},
    {"id": 414, "sub":0, "q":"gas_sensor", "wiki":"Gas_sensor"},
    {"id": 415, "sub":0, "q":"differential_pressure_flow", "wiki":"Flow_measurement"},
    # MCU Technology (subject index 1)
    {"id": 401, "sub":1, "q":"mcu_minimum_system", "wiki":"Intel_MCS-51"},
    {"id": 402, "sub":1, "q":"seven_segment_display", "wiki":"Seven-segment_display"},
    {"id": 403, "sub":1, "q":"matrix_keypad", "wiki":"Keyboard_matrix"},
    {"id": 404, "sub":1, "q":"uart_timing", "wiki":"Universal_asynchronous_receiver-transmitter"},
    {"id": 405, "sub":1, "q":"interrupt_response", "wiki":"Interrupt"},
    {"id": 406, "sub":1, "q":"mcu_block_diagram", "wiki":"Microcontroller"},
    {"id": 407, "sub":1, "q":"clock_circuit_timing", "wiki":"Clock_signal"},
    {"id": 408, "sub":1, "q":"reset_circuit", "wiki":"Reset_circuit"},
    {"id": 409, "sub":1, "q":"p0_port_structure", "wiki":"Intel_MCS-51"},
    {"id": 410, "sub":1, "q":"timer_mode1", "wiki":"Timer"},
    {"id": 411, "sub":1, "q":"timer_mode2", "wiki":"Timer"},
    {"id": 412, "sub":1, "q":"serial_mode1", "wiki":"Universal_asynchronous_receiver-transmitter"},
    {"id": 413, "sub":1, "q":"external_ram_expansion", "wiki":"Static_random-access_memory"},
    {"id": 414, "sub":1, "q":"external_rom_expansion", "wiki":"EPROM"},
    {"id": 415, "sub":1, "q":"ppi_8255a", "wiki":"Intel_8255"},
    # IoT System Design (subject index 2)
    {"id": 401, "sub":2, "q":"iot_three_layer", "wiki":"Internet_of_things"},
    {"id": 402, "sub":2, "q":"mqtt_pub_sub", "wiki":"MQTT"},
    {"id": 403, "sub":2, "q":"mqtt_qos", "wiki":"MQTT"},
    {"id": 404, "sub":2, "q":"smart_home_architecture", "wiki":"Home_automation"},
    {"id": 405, "sub":2, "q":"iot_gateway", "wiki":"Gateway_(telecommunications)"},
    {"id": 406, "sub":2, "q":"iot_four_layer", "wiki":"Internet_of_things"},
    {"id": 407, "sub":2, "q":"rfid_system", "wiki":"Radio-frequency_identification"},
    {"id": 408, "sub":2, "q":"zigbee_topology", "wiki":"Zigbee"},
    {"id": 409, "sub":2, "q":"wsn_node", "wiki":"Wireless_sensor_network"},
    {"id": 410, "sub":2, "q":"cloud_service_models", "wiki":"Cloud_computing"},
    {"id": 411, "sub":2, "q":"edge_cloud_architecture", "wiki":"Edge_computing"},
    {"id": 412, "sub":2, "q":"ble_protocol_stack", "wiki":"Bluetooth_Low_Energy"},
    {"id": 413, "sub":2, "q":"iot_data_flow", "wiki":"Internet_of_things"},
    {"id": 414, "sub":2, "q":"mes_system", "wiki":"Manufacturing_execution_system"},
    {"id": 415, "sub":2, "q":"nbiot_vs_lora", "wiki":"NB-IoT"},
]

WIKI_API = "https://en.wikipedia.org/w/api.php"

USER_AGENT = "Mozilla/5.0 (compatible; EduApp/1.0; +https://example.com)"

def wiki_request(params):
    params["format"] = "json"
    params["origin"] = "*"
    url = WIKI_API + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read())
    except Exception as e:
        print(f"  Wiki API error: {e}")
        return None

def get_page_image(wiki_title):
    """Get the best image for a Wikipedia page."""
    params = {
        "action": "query",
        "titles": wiki_title,
        "prop": "pageimages|images",
        "pithumbsize": 500,
        "piprop": "original|thumbnail",
        "format": "json"
    }
    data = wiki_request(params)
    if not data:
        return None
    
    pages = data.get("query", {}).get("pages", {})
    for pid, page in pages.items():
        if pid == "-1":
            continue
        # Try thumbnail first
        thumb = page.get("thumbnail")
        if thumb and thumb.get("source"):
            return thumb["source"]
        original = page.get("original")
        if original and original.get("source"):
            return original["source"]
        
        # Try to find the first image with category search
        img_params = {
            "action": "query",
            "titles": wiki_title,
            "prop": "images",
            "imlimit": 20,
            "format": "json"
        }
        img_data = wiki_request(img_params)
        if img_data:
            for pid2, p2 in img_data.get("query", {}).get("pages", {}).items():
                images = p2.get("images", [])
                for img in images:
                    title = img["title"]
                    if title.lower().startswith("file:"):
                        fn = title[5:]
                        # Skip icons, logos, small files
                        skip_words = ["icon", "logo", "wikidata", "flag", "Commons-logo", "Question_book"]
                        if any(s in fn.lower() for s in skip_words):
                            continue
                        # Get the image URL
                        url_params = {
                            "action": "query",
                            "titles": f"File:{fn}",
                            "prop": "imageinfo",
                            "iiprop": "url",
                            "iiurlwidth": 500,
                            "format": "json"
                        }
                        url_data = wiki_request(url_params)
                        if url_data:
                            for pid3, p3 in url_data.get("query", {}).get("pages", {}).items():
                                info = p3.get("imageinfo", [])
                                if info and info[0].get("thumburl"):
                                    return info[0]["thumburl"]
                                if info and info[0].get("url"):
                                    return info[0]["url"]
    return None

def download_and_convert(url, max_size_kb=150):
    """Download image and convert to base64, resize if too large."""
    try:
        dl_req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(dl_req, timeout=15) as resp:
            data = resp.read()
        
        if len(data) > max_size_kb * 1024:
            img = Image.open(io.BytesIO(data))
            # Resize if too large
            w, h = img.size
            if w > 500:
                ratio = 500.0 / w
                img = img.resize((500, int(h * ratio)), Image.LANCZOS)
            buf = io.BytesIO()
            img.save(buf, format="JPEG", quality=85)
            data = buf.getvalue()
        
        mime = "image/jpeg"
        if url.lower().endswith(".png"):
            mime = "image/png"
        elif url.lower().endswith(".gif"):
            mime = "image/gif"
        elif url.lower().endswith(".svg") or "svg" in url.lower():
            # SVG - try to get PNG thumbnail instead
            png_url = url.replace(".svg.png", ".png")
            if "thumb" in url:
                # Wikipedia thumb URLs end with {width}px-filename.png
                # We already have a PNG thumbnail
                pass
            return None  # Skip SVGs
        
        b64 = base64.b64encode(data).decode("ascii")
        return f"data:{mime};base64,{b64}"
    except Exception as e:
        print(f"  Download error: {e}")
        return None

def main():
    output = {}
    
    for topic in TOPICS:
        qid = topic["id"]
        sub = topic["sub"]
        wiki_title = topic["wiki"]
        sub_names = {0:"sensor", 1:"mcu", 2:"iot"}
        sn = sub_names[sub]
        key = f"{sn}_{qid}_{topic['q']}"
        print(f"[{key}] Searching '{wiki_title}'...")
        
        url = get_page_image(wiki_title)
        if url:
            print(f"  Found image: {url[:80]}...")
            b64 = download_and_convert(url)
            if b64:
                output[f"{sn}_{qid}"] = b64
                print(f"  ✓ Converted to base64 ({len(b64)//1024}KB)")
            else:
                print(f"  ✗ Failed to convert")
        else:
            print(f"  ✗ No image found")
        
        time.sleep(0.5)
    
    with open("/tmp/wiki_images.json", "w") as f:
        json.dump(output, f)
    
    print(f"\n=== Done! Got {len(output)}/{len(TOPICS)} images ===")
    print(f"Results saved to /tmp/wiki_images.json")

if __name__ == "__main__":
    main()
