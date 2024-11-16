from bs4 import BeautifulSoup

def extract_book_info(xml_text):
    soup = BeautifulSoup(xml_text, 'lxml-xml')  # Use 'lxml-xml' as the parser

    chapters = soup.find_all('content_item', {'component_type': 'chapter'})
    results = []

    for chapter in chapters:
        # Extract authors
        authors = []
        for person in chapter.find_all('person_name'):
            given_name = person.find('given_name').text
            surname = person.find('surname').text
            authors.append(f"{given_name} {surname}")
        authors_string = ', '.join(authors)

        # Extract titles
        title = chapter.find('title').text.strip() if chapter.find('title') else "Title not found"

        # Extract pages
        first_page = chapter.find('first_page').text if chapter.find('first_page') else "First page not found"
        last_page = chapter.find('last_page').text if chapter.find('last_page') else "Last page not found"
        pages = f"{first_page}-{last_page}" if first_page != "First page not found" and last_page != "Last page not found" else "Pages not found"

        # Extract DOI
        doi = chapter.find('doi').text if chapter.find('doi') else "DOI not found"

        # Prepare result for this chapter
        result = {
            'Chapter Title': title,
            'Authors': authors_string,
            'Page Range': pages,
            'DOI': doi
        }
        results.append(result)

    return results

def check_page_ranges(chapters):
    issues = []
    pages_seen = set()
    
    for idx, chapter in enumerate(chapters):
        first_page, last_page = map(int, chapter['Page Range'].split('-'))
        
        # Check for negative range (first page > last page)
        if first_page >= last_page:
            issues.append(f"Negative range in Chapter {idx + 1}: {chapter['Page Range']}")
        
        # Check for overlapping or nested ranges
        for page in range(first_page, last_page + 1):
            if page in pages_seen:
                issues.append(f"Repeated page {page} in Chapter {idx + 1}: {chapter['Page Range']}")
            pages_seen.add(page)
    
    return issues if issues else None  # Return list of issues or None if no issues found

def main():
    filename = input("Enter the XML file name (e.g., your_file.xml): ")
    
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            xml_text = file.read()
            
            book_info = extract_book_info(xml_text)
            
            # Check page ranges for issues
            issues = check_page_ranges(book_info)
            
            # Print issues if found
            if issues:
                for issue in issues:
                    print(issue)
            else:
                print("No issues found with page ranges.")
            
            # Print book information
            for idx, chapter_info in enumerate(book_info, start=1):
                print(f"Chapter {idx}:")
                print(f"  Title: {chapter_info['Chapter Title']}")
                print(f"  Authors: {chapter_info['Authors']}")
                print(f"  Page Range: {chapter_info['Page Range']}")
                print(f"  DOI: {chapter_info['DOI']}")
                print()

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")

if __name__ == "__main__":
    main()
