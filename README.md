<h1>RedCarpet - Backend</h1>

<p>
This github repo contains the files needed to deploy the <b>Digital Ocean</b> Back-End entity that will handle requests from the <b>RedCarpet Mobile Application</b>.
</p>

<h2>Requirements</h2>
<p>In order to deploy the backend implementation, follow these steps:
 <li>Instantiate a cloud server of your choice that is running Ubuntu.</li>
  <li>Install Python3 and Python pip using:<p></p>
    <pre>sudo apt-get update<p></p>
    sudo apt-get install python3<p></p>
    sudo apt-get install python-pip</pre><p></p>
  </li></p>
  <li>Install the necessary Python Modules using pip. The modules are listed in the file <b>"pip_modules.txt"</b></li>
<p></p>
<p>
Currently, the implemented files are as follows:
 <p></p><h4><ol>
 <li>palette_server.py</li>
</ol><h4></p>

<h3>Palette Server</h3>
<p>This file contains the necessary request handlers to perform the reverse image searching. Users will upload a picture through the post method under the path <b>"/api/classify/"</b>. The corresponding picture will be piped into through the function <b>"goog_cloud_vision"</b>, which returns the top ten labels and top ten logos associated with the contents of the picture in a dictionary of strings. We are using the <b><i>Google Cloud Vision API</i></b> with our special API key to make this possible. This returned dictionary will then be passed in as an argument in to the function <b>"searchParses"</b>. This function takes the dictionary, and parses the keywords and returns the top five search results from Microsoft's <b><i>Bing Search Engine</i></b> via HTTPS request.</p>
