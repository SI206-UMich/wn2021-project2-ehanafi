from bs4 import BeautifulSoup
import requests
import re
import os
import csv
import unittest

# done
def get_titles_from_search_results(filename):
    """
    Write a function that creates a BeautifulSoup object on "search_results.htm". Parse
    through the object and return a list of tuples containing book titles (as printed on the Goodreads website) 
    and authors in the format given below. Make sure to strip() any newlines from the book titles and author names.

    [('Book title 1', 'Author 1'), ('Book title 2', 'Author 2')...]
    """

    # Open the file and get the file object
    source_dir = os.path.dirname(__file__) #<-- directory name
    full_path = os.path.join(source_dir, filename)
    infile = open(full_path,'r', encoding='utf-8')

    # Get a soup from a URL
    soup = BeautifulSoup(infile.read(), 'html.parser')

    # Extract info from the page
    # Get all tags of a certain type from the soup
    bookTitles = soup.find_all('a', class_='bookTitle')
    bookAuthors = soup.find_all('span', itemprop='author')

    # Collect info from the tags
    collect_info = []

    for i in range(len(bookTitles)):
        authors = bookAuthors[i].text.split(',')
        
        cleaned_authors = []

        for author in authors:
            cleaned_authors.append(author.strip())

        my_authors = ', '.join(cleaned_authors)

        collect_info.append((bookTitles[i].text.strip(), my_authors))

    return collect_info


# done
def get_search_links():
    """
    Write a function that creates a BeautifulSoup object after retrieving content from
    "https://www.goodreads.com/search?q=fantasy&qid=NwUsLiA2Nc". Parse through the object and return a list of
    URLs for each of the first ten books in the search using the following format:

    ['https://www.goodreads.com/book/show/84136.Fantasy_Lover?from_search=true&from_srp=true&qid=NwUsLiA2Nc&rank=1', ...]

    Notice that you should ONLY add URLs that start with "https://www.goodreads.com/book/show/" to 
    your list, and , and be sure to append the full path to the URL so that the url is in the format 
    “https://www.goodreads.com/book/show/kdkd".

    """

    # Get a soup from a URL
    url = 'https://www.goodreads.com/search?q=fantasy&qid=NwUsLiA2Nc'
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')

    # Extract info from the page
    # Get all tags of a certain type from the soup
    urls = soup.find_all('a', itemprop="url")
    
    # Collect info from the tags
    collect_info = []

    for url in urls:
        if "/book/show" in url['href'] and len(collect_info) < 10:
            collect_info.append('https://www.goodreads.com' + url['href'])
    
    return collect_info


# done
def get_book_summary(book_url):
    """
    Write a function that creates a BeautifulSoup object that extracts book
    information from a book's webpage, given the URL of the book. Parse through
    the BeautifulSoup object, and capture the book title, book author, and number 
    of pages. This function should return a tuple in the following format:

    ('Some book title', 'the book's author', number of pages)

    HINT: Using BeautifulSoup's find() method may help you here.
    You can easily capture CSS selectors with your browser's inspector window.
    Make sure to strip() any newlines from the book title and number of pages.
    """

    # Get a soup from a URL
    url = book_url
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')

    # Extract info from the page
    # Get all tags of a certain type from the soup
    bookTitle = soup.find_all('h1', id="bookTitle")
    bookAuthor = soup.find_all('span', itemprop="name")
    bookPages = soup.find_all('span', itemprop="numberOfPages")

    string = bookPages[0].text.strip()
    pages = string.split()

    return (
        bookTitle[0].text.strip(), 
        bookAuthor[0].text.strip(), 
        int(pages[0])
    )


# done
def summarize_best_books(filepath):
    """
    Write a function to get a list of categories, book title and URLs from the "BEST BOOKS OF 2020"
    page in "best_books_2020.htm". This function should create a BeautifulSoup object from a 
    filepath and return a list of (category, book title, URL) tuples.
    
    For example, if the best book in category "Fiction" is "The Testaments (The Handmaid's Tale, #2)", with URL
    https://www.goodreads.com/choiceawards/best-fiction-books-2020, then you should append 
    ("Fiction", "The Testaments (The Handmaid's Tale, #2)", "https://www.goodreads.com/choiceawards/best-fiction-books-2020") 
    to your list of tuples.
    """

    # Open the file and get the file object
    source_dir = os.path.dirname(__file__) #<-- directory name
    full_path = os.path.join(source_dir, filepath)
    infile = open(full_path,'r', encoding='utf-8')

    # Get a soup from a URL
    soup = BeautifulSoup(infile.read(), 'html.parser')

    # Extract info from the page
    # Get all tags of a certain type from the soup
    bookCategory = soup.find_all('h4', class_="category__copy")
    bookTitle = soup.find_all('img', class_='category__winnerImage')
    bookURL = soup.find_all('div', class_="category clearFix")

    # Collect info from the tags
    collect_info = []

    for i in range(len(bookCategory)):
        category = bookCategory[i].text.strip()
        title = bookTitle[i]['alt']
        url = bookURL[i].find('a')['href']

        collect_info.append((category, title, url))

    return collect_info


# done
def write_csv(data, filename):
    """
    Write a function that takes in a list of tuples (called data, i.e. the
    one that is returned by get_titles_from_search_results()), writes the data to a 
    csv file, and saves it to the passed filename.

    The first row of the csv should contain "Book Title" and "Author Name", and
    respectively as column headers. For each tuple in data, write a new
    row to the csv, placing each element of the tuple in the correct column.

    When you are done your CSV file should look like this:

    Book title,Author Name
    Book1,Author1
    Book2,Author2
    Book3,Author3
    ......

    This function should not return anything.
    """
    with open(filename, mode='w') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',')

        row1 = ["Book Title","Author Name"]
        csv_writer.writerow(row1)

        for row in data:
            csv_writer.writerow(row)


# def extra_credit(filepath):
#     """
#     EXTRA CREDIT

#     Please see the instructions document for more information on how to complete this function.
#     You do not have to write test cases for this function.
#     """
#     pass

class TestCases(unittest.TestCase):

    # call get_search_links() and save it to a static variable: search_urls
    search_urls = get_search_links()

    # done
    def test_get_titles_from_search_results(self):
        # call get_titles_from_search_results() on search_results.htm and save to a local variable
        results = get_titles_from_search_results("search_results.htm")

        # check that the number of titles extracted is correct (20 titles)
        self.assertEqual(20, len(results))

        # check that the variable you saved after calling the function is a list
        self.assertEqual(list, type(results))

        # check that each item in the list is a tuple
        self.assertEqual(tuple, type(results[0]))

        # check that the first book and author tuple is correct (open search_results.htm and find it)
        self.assertEqual(('Harry Potter and the Deathly Hallows (Harry Potter, #7)', 'J.K. Rowling'), results[0])

        # check that the last title is correct (open search_results.htm and find it)
        self.assertEqual(('Harry Potter: The Prequel (Harry Potter, #0.5)', 'J.K. Rowling'), results[-1])
        

    # done
    def test_get_search_links(self):
                
        # check that TestCases.search_urls is a list
        self.assertEqual(list, type(self.search_urls))

        # check that the length of TestCases.search_urls is correct (10 URLs)
        self.assertEqual(10, len(self.search_urls))

        # check that each URL in the TestCases.search_urls is a string
        self.assertEqual(str, type(self.search_urls[0]))
        self.assertEqual(str, type(self.search_urls[4]))
        self.assertEqual(str, type(self.search_urls[-1]))

        # check that each URL contains the correct url for Goodreads.com followed by /book/show/
        self.assertEqual('https://www.goodreads.com/book/show/84136.Fantasy_Lover?from_search=true&from_srp=true&qid=NwUsLiA2Nc&rank=1', self.search_urls[0])
        self.assertEqual('https://www.goodreads.com/book/show/42667807-die-vol-1?from_search=true&from_srp=true&qid=NwUsLiA2Nc&rank=10', self.search_urls[-1])


    # done
    def test_get_book_summary(self):
        # create a local variable – summaries – a list containing the results from get_book_summary()
        
        summaries = []

        for url in self.search_urls:
            summaries.append(get_book_summary(url))

        # for each URL in TestCases.search_urls (should be a list of tuples)
        self.assertEqual(list, type(summaries))
        self.assertEqual(tuple, type(summaries[0]))

        self.assertEqual(list, type(summaries))
        self.assertEqual(tuple, type(summaries[-1]))

        # check that the number of book summaries is correct (10)
        self.assertEqual(10, len(summaries))

        # check that each item in the list is a tuple
        self.assertEqual(tuple, type(summaries[0]))
        self.assertEqual(tuple, type(summaries[-1]))

        # check that each tuple has 3 elements
        self.assertEqual(3, len(summaries[0]))

        # check that the first two elements in the tuple are string
        self.assertEqual(str, type(summaries[0][0]))
        self.assertEqual(str, type(summaries[0][1]))

        # check that the third element in the tuple, i.e. pages is an int
        self.assertEqual(int, type(summaries[0][2]))

        # check that the first book in the search has 337 pages
        self.assertEqual(337, summaries[0][2])


    # done
    def test_summarize_best_books(self):
        # call summarize_best_books and save it to a variable
        filename = 'best_books_2020.htm'
        summarize = summarize_best_books(filename)

        # check that we have the right number of best books (20)
        self.assertEqual(20, len(summarize))

        # assert each item in the list of best books is a tuple
        self.assertEqual(tuple, type(summarize[0]))

        # check that each tuple has a length of 3
        self.assertEqual(3, len(summarize[0]))

        # check that the first tuple is made up of the following 3 strings:'Fiction', "The Midnight Library", 'https://www.goodreads.com/choiceawards/best-fiction-books-2020'
        self.assertEqual(('Fiction', "The Midnight Library", 'https://www.goodreads.com/choiceawards/best-fiction-books-2020'), summarize[0])

        # check that the last tuple is made up of the following 3 strings: 'Picture Books', 'Antiracist Baby', 'https://www.goodreads.com/choiceawards/best-picture-books-2020'
        self.assertEqual(('Picture Books', 'Antiracist Baby', 'https://www.goodreads.com/choiceawards/best-picture-books-2020'), summarize[-1])


    # done
    def test_write_csv(self):
        # call get_titles_from_search_results on search_results.htm and save the result to a variable
        filename = 'search_results.htm'
        data = get_titles_from_search_results(filename)

        # call write csv on the variable you saved and 'test.csv'
        write_csv(data, 'test.csv')

        # read in the csv that you wrote (create a variable csv_lines - a list containing all the lines in the csv you just wrote to above)
        with open('test.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')   
            csv_lines = []

            for line in csv_reader:
                csv_lines.append(line)

        # check that there are 21 lines in the csv
        self.assertEqual(21, len(csv_lines))

        # check that the header row is correct
        self.assertEqual(['Book Title', 'Author Name'], csv_lines[0])

        # check that the next row is 'Harry Potter and the Deathly Hallows (Harry Potter, #7)', 'J.K. Rowling'
        self.assertEqual(["Harry Potter and the Deathly Hallows (Harry Potter, #7)", 'J.K. Rowling'], csv_lines[1])

        # check that the last row is 'Harry Potter: The Prequel (Harry Potter, #0.5)', 'J.K. Rowling'
        self.assertEqual(["Harry Potter: The Prequel (Harry Potter, #0.5)", 'J.K. Rowling'], csv_lines[-1])

if __name__ == '__main__':
    #print(extra_credit("extra_credit.htm"))
    unittest.main(verbosity=2)

    # filename = 'search_results.htm'
    # titles = get_titles_from_search_results(filename)
    # print(titles)

    # print(get_search_links())

    # book_url = 'https://www.goodreads.com/book/show/4214.Life_of_Pi'
    # print(get_book_summary(book_url))

    # filename = 'best_books_2020.htm'
    # summarize = summarize_best_books(filename)
    # print(summarize)
    
    # csv = write_csv(titles, 'output.csv')
    # print(csv)