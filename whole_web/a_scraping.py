import requests
from bs4 import BeautifulSoup, Tag
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urljoin
from time import perf_counter

from constants import print_stats, print_breakline, ModelData


# =========================================================
# GETTING STARTING URLS
# =========================================================

def get_family_urls(session: requests.Session, starting_url: str, base_url: str) -> list[str]:
    response: requests.Response = session.get(starting_url)
    response.raise_for_status()

    soup: BeautifulSoup = BeautifulSoup(response.text, "html.parser")
    url_results: list[str] = []

    for item in soup.select('a[href^="/library/"]'):
        href: object = item.get("href")

        if not isinstance(href, str):
            continue

        url: str = urljoin(base_url, href)

        if url not in url_results:
            url_results.append(url)

    return url_results


# =========================================================
# SCRAPE ONE MODEL FAMILY
# =========================================================

def scrape_family(url: str) -> list[ModelData]:
    headers: dict[str, str] = {"User-Agent": "Mozilla/5.0"}

    session: requests.Session = requests.Session()
    session.headers.update(headers)

    response: requests.Response = session.get(url)
    response.raise_for_status()

    soup: BeautifulSoup = BeautifulSoup(response.text, "html.parser")

    # -----------------------------------------------------
    # GENERAL CAPABILITIES
    # -----------------------------------------------------

    general_capabilities: list[Tag] = soup.find_all("span", class_="inline-flex items-center rounded-md bg-indigo-50 px-2 py-0.5 text-xs font-medium text-indigo-600 sm:text-[13px]")

    capabilities: list[str] = [capability.get_text(strip=True) for capability in general_capabilities]

    # -----------------------------------------------------
    # FIND MODEL ENTRIES
    # -----------------------------------------------------

    list_items: list[Tag] = soup.find_all("div", class_="hidden group px-4 py-3 sm:grid sm:grid-cols-12 text-[13px]")

    results: list[ModelData] = []

    for item in list_items:
        name_element: Tag | None = item.find("a", class_="block group-hover:underline text-sm font-medium text-neutral-800")

        if name_element is None:
            continue

        full_name: str = name_element.get_text(strip=True)

        # -------------------------------------------------
        # FAMILY / VARIANT
        # -------------------------------------------------

        if ":" in full_name:
            family: str
            variant: str | None
            family, variant = full_name.split(":", 1)
        else:
            family = full_name
            variant = None

        # -------------------------------------------------
        # STORAGE / CONTEXT / MODALITIES
        # -------------------------------------------------

        storage: str | None = None
        context: str | None = None
        modalities: list[str] = []

        paragraphs: list[Tag] = item.find_all("p", class_="col-span-2 text-neutral-500")

        for paragraph in paragraphs:
            text: str = paragraph.get_text(strip=True)

            if text.endswith(("MB", "GB", "TB")):
                storage = text

            elif text.endswith(("K", "M")) or text.isdigit():
                context = text

            else:
                modalities.extend(part.strip() for part in text.split(",") if part.strip())

        # That one 512 D:
        if context is not None and context.isdigit():
            context += "K"

        # -------------------------------------------------
        # RESULT
        # -------------------------------------------------

        result_dict: ModelData = {
            "full_name": full_name,
            "family": family,
            "variant": variant,
            "storage": storage,
            "context": context,
            "capabilities": capabilities.copy(),
            "modalities": modalities,
        }

        results.append(result_dict)

    return results


# =========================================================
# SCRAPE EVERYTHING IN PARALLEL
# =========================================================

def scraping_main(scrape_debug: bool = False) -> list[ModelData]:
    base_url: str = "https://ollama.com"
    starting_url: str = f"{base_url}/library"
    headers: dict[str, str] = {"User-Agent": "Mozilla/5.0"}
    max_workers: int = 10

    start_time: float = perf_counter()

    session: requests.Session = requests.Session()
    session.headers.update(headers)

    family_urls: list[str] = get_family_urls(session, starting_url, base_url)
    final_result: list[ModelData] = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for family_models in executor.map(scrape_family, family_urls):
            final_result.extend(family_models)

    if scrape_debug:
        print_breakline(80)
        print_stats(f"Scraping duration: {perf_counter() - start_time:.2f} seconds")
        print_breakline(80)

    return final_result