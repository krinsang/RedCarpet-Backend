<h1>RedCarpet - Backend</h1>

<p>
This github repo contains the files needed to deploy the <b>Digital Ocean</b> Back-End entity that will handle requests from the <b>RedCarpet Mobile Application</b>.
</p>
<p>
The implemented files are as follows:
  <li><b>palette_server.py</b></li>
</p>

<h2>Palette Server</h2>
<p>This file contains the necessary request handlers to serve the reverse image searching. Users will upload a picture through the post method under the path <b>"/api/classify/"</b>. The corresponding picture will be piped into through the function <b>"goog_cloud_vision"</b>, which returns the top 10 labels and top 10 logos associated with the contents of the picture in a dictionary of strings. We are using the <b><i>Google Cloud Vision API</i></b> with our special API key to make this possible. This returned dictionary will then be passed in as an argument in to the function <b>"searchParses"</b> and  </p>
  
<title></title>
  
