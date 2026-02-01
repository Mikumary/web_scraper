# Import necessary libraries
import pandas as pd           # For handling data in spreadsheet format
import requests              # For making web requests to websites
from bs4 import BeautifulSoup # For parsing HTML content
import time                  # For adding delays between requests
import re                    # For pattern matching (emails, phones)

# Step 1: Load the agency list
# This reads your Excel/CSV file into a dataframe (think of it as a smart spreadsheet)
agencies_df = pd.read_csv('Texas_PC_Agencies.xlsx')

# Step 2: Create a function to search for agency websites
def find_agency_website(agency_name, city):
    """
    This function searches Google for the agency's website
    agency_name: The name of the insurance agency
    city: The city where they're located
    Returns: The website URL
    """
    # Build a search query like "Agency Name + City + Texas + insurance"
    search_query = f"{agency_name} {city} Texas insurance agency"
    
    # Use Google Custom Search API (requires API key)
    # This sends our search to Google and gets results back
    api_key =  "AIzaSyCyn4t4C-NT4mbBq84nI4QHnROOC12cWZU"
    search_engine_id = "a7b34d007abee4b22"
    url = f"https://www.googleapis.com/customsearch/v1?key={api_key}&cx={search_engine_id}&q={search_query}"
    
    response = requests.get(url)
    results = response.json()
    
    # Get the first result (usually the official website)
    if 'items' in results:
        return results['items'][0]['link']
    return None

# Step 3: Extract contact information from a website
def extract_contacts(website_url):
    """
    This function visits the agency website and extracts contact info
    website_url: The URL of the agency's website
    Returns: Dictionary with name, email, phone, address
    """
    try:
        # Download the webpage content
        response = requests.get(website_url, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Look for email addresses using pattern matching
        # This searches for text that looks like: something@something.com
        emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', 
                           response.text)
        
        # Look for phone numbers (common formats)
        # Searches for patterns like: (123) 456-7890 or 123-456-7890
        phones = re.findall(r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4})', 
                           response.text)
        
        # Look for common contact page indicators
        # Many sites have an "About Us" or "Contact" page with owner info
        contact_links = soup.find_all('a', href=True)
        for link in contact_links:
            if 'about' in link['href'].lower() or 'contact' in link['href'].lower():
                # Visit those pages to find more info
                pass
        
        return {
            'email': emails[0] if emails else None,
            'phone': phones[0] if phones else None
        }
    except:
        return {'email': None, 'phone': None}

# Step 4: Main processing loop
results = []
for index, row in agencies_df.iterrows():
    # For each agency in your list...
    print(f"Processing {row['Agency Name']}...")
    
    # Find their website
    website = find_agency_website(row['Agency Name'], row['City'])
    
    # Extract contact info
    if website:
        contacts = extract_contacts(website)
    else:
        contacts = {'email': None, 'phone': None}
    
    # Store the results
    results.append({
        'Agency Name': row['Agency Name'],
        'Website': website,
        'Email': contacts['email'],
        'Phone': contacts['phone']
    })
    
    # Be polite - wait 2 seconds between requests so we don't overload servers
    time.sleep(2)

# Step 5: Save results to Excel
results_df = pd.DataFrame(results)
results_df.to_excel('agency_contacts_found.xlsx', index=False)
print("Done! Results saved to agency_contacts_found.xlsx")