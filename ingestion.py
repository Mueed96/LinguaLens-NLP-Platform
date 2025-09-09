# ingestion.py

# Import necessary libraries
import PyPDF2               # For reading PDF files
from newspaper import Article # For scraping web articles

# --- Function 1: Extract text from a URL ---
def get_text_from_url(url):
    """
    Fetches an article from a given URL, downloads it, parses it to find the main content,
    and returns the clean article text as a string.
    """
    try:
        # Create an Article object from the URL
        article = Article(url)

        # Download the HTML content of the web page
        article.download()

        # Parse the downloaded HTML to find the main article title and text
        article.parse()

        # Return the extracted article text
        return article.text
    except Exception as e:
        # If anything goes wrong (e.g., bad URL, network error, parsing failed)
        print(f"Error fetching URL content: {e}")
        return None # Return nothing to signal an error

# --- Function 2: Extract text from a PDF file ---
def get_text_from_pdf(pdf_file_object):
    """
    Reads an uploaded PDF file object, iterates through each page, extracts text,
    and returns all text combined as a single string.
    """
    try:
        # Create a PDF reader object from the file
        pdf_reader = PyPDF2.PdfReader(pdf_file_object)

        # Initialize an empty string to store all extracted text
        full_text = ""

        # Loop through every page in the PDF document
        for page in pdf_reader.pages:
            # Extract text from the current page and add it to our string
            full_text += page.extract_text()

        return full_text
    except Exception as e:
        print(f"Error reading PDF file: {e}")
        return None

# --- Function 3: Extract text from a TXT file ---
def get_text_from_txt(txt_file_object):
    """Reads an uploaded TXT file object and returns its content as a string."""
    try:
        # Read the file content and decode it using 'utf-8' standard encoding
        return txt_file_object.read().decode("utf-8")
    except Exception as e:
        print(f"Error reading TXT file: {e}")
        return None

# --- Self-Test Block ---
# This code block only runs if you execute this file directly (python ingestion.py)
# It's used for testing our functions without running the full web app.
if __name__ == '__main__':
    print("Testing Ingestion Module...")

    # Test Case 1: Fetching from a URL
    test_url = "https://www.bbc.com/news/articles/c75qlerp2e5o" # A working example article
    print(f"\n--- Testing URL: {test_url} ---")
    url_text = get_text_from_url(test_url)
    if url_text:
        print("Success! First 300 characters:")
        print(url_text[:300] + "...")
    else:
        print("Failed to fetch text from URL.")

    # Note: To test PDF and TXT functions, you would need to write more complex test code
    # to open local files. For now, we'll test them through the web interface later.

    # Add this new function to ingestion.py
import feedparser

def parse_rss_feed(feed_url):
    """Parses an RSS feed and returns a list of articles (title, link)."""
    try:
        feed = feedparser.parse(feed_url)
        # Check if the feed was parsed correctly
        if feed.bozo:
            raise Exception(feed.bozo_exception)
        # Create a list of dictionaries, one for each article
        return [{"title": entry.title, "link": entry.link} for entry in feed.entries]
    except Exception as e:
        print(f"Error parsing RSS feed: {e}")
        return [] # Return an empty list on failure