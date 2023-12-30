# UFC-Fight-Analysis

Objective: The objective of this project is to derive an optimal strategy for placing bets on UFC fights. In order to derive an optimal strategy, fight statistics from ufcstats.com and betting odds from bestfightodds.com were collected and cleaned.

Next Steps: Complete further data transformations, complete EDA, and create a classifier model.

Current Files:

(1) Driver_File - This file calls functions from the other listed files. The file enables the user to create a dataset containing every UFC fight with fight statistics, fighter information, and fight odds. 

(2) Get_Event_Table -  This file contains the function “get_all_events.” The purpose of this function is to provide event information from ufcstats.com.

(3) Scrape_UFC_Stats__v4 - This file contains “scrape_ufc_stats.” The purpose of this function is to retrieve fight level details given the output of “get_all_events.” The user can adjust the starting_point and end_point parameters as needed to complete the scraping.

(4) Remove_Old_Fights - This file contains the function “remove_old_fights.” The purpose of this function is to remove fights that occurred before standardized 5 min rounds were implemented. 

(5) Fix_Failed_Connections_Duplicates_v2 - This file contains two functions: “fix_failed_connects” and “remove_duplicates.” The purpose of “fix_failed_connects” is to ensure that all entries in the dataset have complete information from ufcstats.com. Incomplete information can occur due to failed connections during the scraping process. The purpose of “remove_duplicates” is to remove duplicate entries that might have occurred during the scraping process.

(6) Fix_Other_Outcomes - This file contains the function fix_other_outcomes. The purpose of this function is to fix the dataset for fights that resulted in ties or no contests. The website structure on ufcstats.com is different for fights with these outcomes.

(7) Scrape_Fight_Odds_v3 - This file contains the function scrape_fight_odds. The purpose of this function is to provide the historic fight odds for each fight. Due to changes in the website’s security configurations, this function does not currently work as intended. In the driver file, fight odds are provided by merging the dataset with a previous output of this function (when the function was still working as intended). This is noted as a potential area of improvement if more data is determined to be needed for the analysis. 

(8) Consolidated_Cleaned_Merged.csv - This file contains the output from running the driver file. 
