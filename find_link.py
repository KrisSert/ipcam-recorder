from playwright.sync_api import sync_playwright
import re


def find_stream_link(url, iframe_xpath):
    with sync_playwright() as p:
        # Launch the browser
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Open the desired webpage
        page.goto(url)

        # Navigate to the main element with the specified ID
        main_element = page.query_selector('#laine')
        main_element.wait_for_selector('div')
        if not main_element:
            print(f"Main element with id='{main_id}' not found")
            return
        
        main_element.wait_for_selector('div')
        # Print the main element's HTML content
        main_content = main_element.inner_html()

        
        # Look for the iframe using the provided XPath
        iframe_element_handle = page.query_selector(f'xpath={iframe_xpath}')

        if not iframe_element_handle:
            print(f"Iframe with XPath '{iframe_xpath}' not found")
            return
        
        # Get the iframe object from the element handle
        iframe = iframe_element_handle.content_frame()
        iframe.wait_for_selector('body')

        # Search for the JavaScript variables using regular expressions
        address_match = re.search(r'var\s+address\s*=\s*["\'](.*?)["\'];', iframe.content())
        streamid_match = re.search(r'var\s+streamid\s*=\s*["\'](.*?)["\'];', iframe.content())

        print(address_match)
        print(streamid_match)
        
        address = address_match.group(1) if address_match else "Not found"
        streamid = streamid_match.group(1) if streamid_match else "Not found"
        
        print(f"Address: {address}")
        print(f"Stream ID: {streamid}")
        
        stream_url = f"{address}streams/{streamid}/stream.m3u8"

        return stream_url

        # Close the browser
        browser.close()

"""
# Example usage
try:
    url = "https://laine.surf/"
    iframe_xpath = "//*[@id='laine']/div/div[2]/div/div/div/iframe"
    stream_link = find_stream_link(url, iframe_xpath)
    if stream_link:
        print(stream_link)
    else:
        raise Exception("Stream link not found")

except Exception as e:
    print(f"{e}, link was not found")
"""