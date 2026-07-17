import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

STARTING_URL = "https://ollama.com/library"
HEADERS = {"User-Agent": "Mozilla/5.0"}

SESSION = requests.Session()
SESSION.headers.update(HEADERS)

# =========================================================
# GETTING STARTING URLS
# =========================================================

response = SESSION.get(STARTING_URL)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

list_items = soup.find_all(
    "li",
    class_="flex items-baseline border-b border-neutral-200 py-6"
)

url_results = []

for item in list_items:
    name = item.find("span", class_="group-hover:underline truncate").get_text(strip=True)
    url_results.append(f"{STARTING_URL}/{name}")

# =========================================================
# SCRAPE ONE MODEL FAMILY
# =========================================================

def scrape_family(url):
    response = SESSION.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    general_capabilities = soup.find_all("span", class_="inline-flex items-center rounded-md bg-indigo-50 px-2 py-0.5 text-xs font-medium text-indigo-600 sm:text-[13px]") 
    capabilities = [c.get_text(strip=True) for c in general_capabilities]  

    list_items = soup.find_all("div", class_="hidden group px-4 py-3 sm:grid sm:grid-cols-12 text-[13px]")

    results = []


    for item in list_items:
        full_name = item.find(
            "a",
            class_="block group-hover:underline text-sm font-medium text-neutral-800"
        ).get_text(strip=True)

        variant = None
        family, variant = full_name.split(":", 1)

        storage = None
        context = None
        modalities = []

        for p in item.find_all("p", class_="col-span-2 text-neutral-500"):
            text = p.get_text(strip=True)

            if text.endswith(("MB", "GB", "TB")):
                storage = text

            elif text.endswith(("K", "M")) or text.isdigit():
                context = text

            else:
                modalities.extend(
                    x.strip()
                    for x in text.split(",")
                )

        if context is not None and context.isdigit(): # That one 512 D:
            context += "K"

        result_dict = {
            "full_name": full_name,
            "family": family,
            "variant": variant,
            "storage": storage,
            "context": context,
            "capabilities": capabilities.copy()
        }

        results.append(result_dict)

    return results

# =========================================================
# SCRAPE EVERYTHING IN PARALLEL
# =========================================================

def threading_web_data():
    final_result = []

    with ThreadPoolExecutor(max_workers=10) as executor:
        for family_models in executor.map(scrape_family, url_results):
            final_result.extend(family_models)
    
    return final_result