import requests
from lxml import html

def find_stream_link(url, iframe_xpath, stream_xpath):
    # Fetch the HTML content from the URL
    response = requests.get(url)
    
    if response.status_code == 200:
        html_content = response.content
        tree = html.fromstring(html_content)
        print(tree)
        
        # Find the iframe element using the provided XPath
        iframes = tree.xpath(iframe_xpath)
        print(iframes)
        
        for iframe in iframes:
            iframe_src = iframe.get('src')
            if iframe_src:
                # Fetch the content of the iframe
                iframe_response = requests.get(iframe_src)
                if iframe_response.status_code == 200:
                    iframe_content = iframe_response.content
                    iframe_tree = html.fromstring(iframe_content)
                    
                    # Find the stream link using the provided XPath
                    stream_links = iframe_tree.xpath(stream_xpath)
                    if stream_links:
                        return stream_links[0]  # Return the first found link
    
    return None

# Example usage
try:
    url = "https://laine.surf/"
    iframe_xpath = "//iframe[contains(@src, 'ipcamlive')]"  # Modify this XPath to match the iframe structure in your HTML
    stream_xpath = "//a[contains(@href, 'https://s27.ipcamlive.com/streams') and contains(@href, 'stream.m3u8')]/@href"  # Modify this XPath to match the stream link
    stream_link = find_stream_link(url, iframe_xpath, stream_xpath)
    if stream_link:
        print(stream_link)
    else:
        raise Exception("Stream link not found")
except Exception as e:
    print(f"{e}, link was not found")
