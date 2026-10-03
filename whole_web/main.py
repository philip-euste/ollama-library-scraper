from a_scraping import scraping_main
from b_cleaning import cleaning_main
from c_normalizing import normalizing_main
from e_visualizing import visualizing_main


# =========================================================
# CONFIGURATION
# =========================================================

DEBUG_SCRAPE: bool = True

DEBUG_CLEAN_ACCEPTED: bool = True
DEBUG_CLEAN_REJECTED: bool = True

DEBUG_NORMALIZE: bool = False

DEBUG_COMPARE: bool = False

VARIABLE_COUNT: int = 2  # 2 or 3

# =========================================================
# EXECUTION
# =========================================================

def main() -> None:
    scraped_data = scraping_main(scrape_debug = DEBUG_SCRAPE)
    cleaned_data = cleaning_main(scraped_data, debug_cleaned_accepted = DEBUG_CLEAN_ACCEPTED, debug_cleaned_rejected = DEBUG_CLEAN_REJECTED)
    normalized_data = normalizing_main(cleaned_data, normalize_debug = DEBUG_NORMALIZE)
    visualizing_main(normalized_data, variable_count = VARIABLE_COUNT, comparing_debug = DEBUG_COMPARE)


if __name__ == "__main__":
    main()