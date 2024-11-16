import xml.etree.ElementTree as ET

def create_book_xml():
    # Book Metadata without namespace
    book = ET.Element('book', {'book_type': 'monograph'})
    book_metadata = ET.SubElement(book, 'book_metadata')
    
    # Contributors
    contributors = ET.SubElement(book_metadata, 'contributors')
    authors = []
    num_authors = int(input("Enter the number of authors for the book: "))
    for i in range(num_authors):
        person_name = ET.SubElement(contributors, 'person_name', {'sequence': 'first' if i == 0 else 'additional', 'contributor_role': 'author'})
        given_name = ET.SubElement(person_name, 'given_name')
        given_name_text = input(f"Enter given name of author {i+1}: ")
        given_name.text = given_name_text
        surname = ET.SubElement(person_name, 'surname')
        surname_text = input(f"Enter surname of author {i+1}: ")
        surname.text = surname_text
        authors.append((given_name_text, surname_text))
    
    # Edit authors check
    edit_authors = input("Do you want to edit any author's details? (y/n): ").strip().lower()
    while edit_authors == 'y':
        author_index = int(input(f"Enter the index of the author you want to edit (1-{num_authors}): ")) - 1
        given_name_text = input(f"Enter new given name of author {author_index+1}: ")
        surname_text = input(f"Enter new surname of author {author_index+1}: ")
        authors[author_index] = (given_name_text, surname_text)  # Update the authors list
        edit_authors = input("Do you want to edit another author's details? (y/n): ").strip().lower()

    # Titles
    titles = ET.SubElement(book_metadata, 'titles')
    title = ET.SubElement(titles, 'title')
    title.text = input("Enter the title of the book: ")

    # Abstract
    abstract_text = input("Enter the abstract of the book: ")
    abstract = ET.SubElement(book_metadata, 'jats:abstract', {'xml:lang': 'es'})
    abstract_p = ET.SubElement(abstract, 'jats:p')
    abstract_p.text = abstract_text

    # Edition Number
    edition_number = ET.SubElement(book_metadata, 'edition_number')
    edition_number.text = input("Enter the edition number: ")

    # Publication Date
    pub_day = input("Enter the publication day (DD): ")
    pub_month = input("Enter the publication month (MM): ")
    pub_year = input("Enter the publication year (YYYY): ")

    for media_type in ['print', 'online']:
        publication_date = ET.SubElement(book_metadata, 'publication_date', {'media_type': media_type})
        month = ET.SubElement(publication_date, 'month')
        month.text = pub_month
        day = ET.SubElement(publication_date, 'day')
        day.text = pub_day
        year = ET.SubElement(publication_date, 'year')
        year.text = pub_year

    # DOI Data
    book_doi_prefix = "10.xxxxx/"
    book_doi = input("Enter the DOI of the book (without prefix): ")
    
    # Derive ISBN from DOI
    isbn = ET.SubElement(book_metadata, 'isbn')
    isbn.text = book_doi.replace("-", "")
    
    doi_data = ET.SubElement(book_metadata, 'doi_data')
    doi = ET.SubElement(doi_data, 'doi')
    doi.text = book_doi_prefix + book_doi

    resource_url = input("Enter the resource URL: ")
    resource = ET.SubElement(doi_data, 'resource')
    resource.text = resource_url

    # Publisher
    publisher = ET.SubElement(book_metadata, 'publisher')
    publisher_name = ET.SubElement(publisher, 'publisher_name')
    publisher_name.text = input("Enter the name of the publisher: ")

    # Edit book metadata check
    edit_metadata = input("Do you want to edit any of the book metadata fields? (y/n): ").strip().lower()
    while edit_metadata == 'y':
        field_to_edit = input("Enter the field you want to edit (title/abstract/edition number/publication date/ISBN/publisher/DOI/resource URL): ").strip().lower()
        if field_to_edit == 'title':
            title.text = input("Enter the new title of the book: ")
        elif field_to_edit == 'abstract':
            abstract_p.text = input("Enter the new abstract of the book: ")
        elif field_to_edit == 'edition number':
            edition_number.text = input("Enter the new edition number: ")
        elif field_to_edit == 'publication date':
            pub_month = input("Enter the new publication month (MM): ")
            pub_day = input("Enter the new publication day (DD): ")
            pub_year = input("Enter the new publication year (YYYY): ")
            for publication_date in book_metadata.findall('publication_date'):
                month = publication_date.find('month')
                month.text = pub_month
                day = publication_date.find('day')
                day.text = pub_day
                year = publication_date.find('year')
                year.text = pub_year
        elif field_to_edit == 'isbn':
            isbn.text = input("Enter the new ISBN of the book: ")
        elif field_to_edit == 'publisher':
            publisher_name.text = input("Enter the new name of the publisher: ")
        elif field_to_edit == 'doi':
            doi.text = book_doi_prefix + input("Enter the new DOI of the book (without prefix): ")
        elif field_to_edit == 'resource url':
            resource.text = input("Enter the new resource URL: ")
        else:
            print("Invalid field. Please enter one of the specified fields.")
        
        edit_metadata = input("Do you want to edit another field? (y/n): ").strip().lower()

    # Add the separator comment
    separator = ET.Comment(' ============== ')
    book.append(separator)

    # Chapters
    num_chapters = int(input("Enter the number of chapters: "))
    for i in range(num_chapters):
        content_item = ET.SubElement(book, 'content_item', {'component_type': 'chapter'})
        chapter_contributors = ET.SubElement(content_item, 'contributors')
        num_chapter_authors = int(input(f"Enter the number of authors for chapter {i+1}: "))
        for j in range(num_chapter_authors):
            print(f"Choose an author for chapter {i+1} author {j+1}:")
            for idx, author in enumerate(authors, start=1):
                print(f"{idx}. {author[0]} {author[1]}")
            choice = int(input(f"Enter the number corresponding to the author for chapter {i+1} author {j+1} (or 0 to add a new author): "))
            if choice == 0:
                chapter_given_name_text = input(f"Enter given name of new author for chapter {i+1} author {j+1}: ")
                chapter_surname_text = input(f"Enter surname of new author for chapter {i+1} author {j+1}: ")
                authors.append((chapter_given_name_text, chapter_surname_text))
            else:
                chapter_given_name_text, chapter_surname_text = authors[choice-1]

            chapter_person_name = ET.SubElement(chapter_contributors, 'person_name', {'sequence': 'first' if j == 0 else 'additional', 'contributor_role': 'author'})
            chapter_given_name = ET.SubElement(chapter_person_name, 'given_name')
            chapter_given_name.text = chapter_given_name_text
            chapter_surname = ET.SubElement(chapter_person_name, 'surname')
            chapter_surname.text = chapter_surname_text

        chapter_titles = ET.SubElement(content_item, 'titles')
        chapter_title = ET.SubElement(chapter_titles, 'title')
        chapter_title.text = input(f"Enter the title of chapter {i+1}: ")

        chapter_abstract = ET.SubElement(content_item, 'jats:abstract', {'xml:lang': 'es'})
        chapter_abstract_p = ET.SubElement(chapter_abstract, 'jats:p')
        chapter_abstract_p.text = abstract_text

        for media_type in ['print', 'online']:
            chapter_publication_date = ET.SubElement(content_item, 'publication_date', {'media_type': media_type})
            chapter_month = ET.SubElement(chapter_publication_date, 'month')
            chapter_month.text = pub_month
            chapter_day = ET.SubElement(chapter_publication_date, 'day')
            chapter_day.text = pub_day
            chapter_year = ET.SubElement(chapter_publication_date, 'year')
            chapter_year.text = pub_year

        pages = ET.SubElement(content_item, 'pages')
        first_page = ET.SubElement(pages, 'first_page')
        first_page.text = input(f"Enter the first page of chapter {i+1}: ")
        last_page = ET.SubElement(pages, 'last_page')
        last_page.text = input(f"Enter the last page of chapter {i+1}: ")

        chapter_doi_data = ET.SubElement(content_item, 'doi_data')
        chapter_doi = ET.SubElement(chapter_doi_data, 'doi')
        chapter_doi.text = book_doi_prefix + book_doi + f"-CAP{i+1}"
        chapter_resource = ET.SubElement(chapter_doi_data, 'resource')
        chapter_resource.text = resource_url

            # Add the separator comment after each chapter except the last one
        if i < num_chapters - 1:
            book.append(separator)

    # Final edit chapter check
    edit_chapters = input("Do you want to edit any chapter details? (y/n): ").strip().lower()
    while edit_chapters == 'y':
        chapter_index = int(input(f"Enter the index of the chapter you want to edit (1-{num_chapters}): ")) - 1
        edit_field = input("Which item of the chapter do you want to edit? (authors/title/first page/last page): ").strip().lower()
        if edit_field == 'authors':
            num_chapter_authors = int(input(f"Enter the new number of authors for chapter {chapter_index + 1}: "))
            contributors = book.findall(f'content_item[{chapter_index + 1}]/contributors')[0]
            contributors.clear()
            for j in range(num_chapter_authors):
                print(f"Choose an author for chapter {chapter_index + 1} author {j + 1}:")
                for idx, author in enumerate(authors, start=1):
                    print(f"{idx}. {author[0]} {author[1]}")
                choice = int(input(f"Enter the number corresponding to the author for chapter {chapter_index + 1} author {j + 1} (or 0 to add a new author): "))
                if choice == 0:
                    chapter_given_name_text = input(f"Enter given name of new author for chapter {chapter_index + 1} author {j + 1}: ")
                    chapter_surname_text = input(f"Enter surname of new author for chapter {chapter_index + 1} author {j + 1}: ")
                    authors.append((chapter_given_name_text, chapter_surname_text))
                else:
                    chapter_given_name_text, chapter_surname_text = authors[choice - 1]

                chapter_person_name = ET.SubElement(contributors, 'person_name', {'sequence': 'first' if j == 0 else 'additional', 'contributor_role': 'author'})
                chapter_given_name = ET.SubElement(chapter_person_name, 'given_name')
                chapter_given_name.text = chapter_given_name_text
                chapter_surname = ET.SubElement(chapter_person_name, 'surname')
                chapter_surname.text = chapter_surname_text

        elif edit_field == 'title':
            chapter_title = book.findall(f'content_item[{chapter_index + 1}]/titles/title')[0]
            chapter_title.text = input(f"Enter the new title of chapter {chapter_index + 1}: ")

        elif edit_field == 'first page':
            first_page = book.findall(f'content_item[{chapter_index + 1}]/pages/first_page')[0]
            first_page.text = input(f"Enter the new first page of chapter {chapter_index + 1}: ")

        elif edit_field == 'last page':
            last_page = book.findall(f'content_item[{chapter_index + 1}]/pages/last_page')[0]
            last_page.text = input(f"Enter the new last page of chapter {chapter_index + 1}: ")

        else:
            print("Invalid field. Please enter one of the specified fields.")

        edit_chapters = input("Do you want to edit another chapter's details? (y/n): ").strip().lower()

    # Convert the ElementTree to a string
    xml_string = ET.tostring(book, encoding='unicode', method='xml')

    # Replace double quotes with single quotes in attributes
    xml_string = xml_string.replace('"', "'")

    # Remove the closing book tag
    xml_string = xml_string.replace("</book>", "")

    # Write the XML string to the file
    with open("output.xml", "w", encoding='utf-8') as fh:
        fh.write(xml_string)

if __name__ == "__main__":
    create_book_xml()
