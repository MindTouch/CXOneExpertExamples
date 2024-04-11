/**
 * Dynamically loads a JavaScript script into the HTML document.
 * @param {string} url - The URL of the script to load.
 */
const loadScript = (url) => {
  const script = document.createElement("script");
  script.type = "text/javascript";
  script.src = url;
  script.onload = () => console.log("Script loaded successfully.");
  script.onerror = () => console.error("Error loading the script.");
  document.body.appendChild(script);
};

/**
 * Appends a MindTouch embed script element to the document body and loads a script from a specified URL.
 * This function specifically handles MindTouch embeds which are used to integrate MindTouch content.
 *
 * @param {string} domain - The domain for the MindTouch embed, used to construct the script's source URL.
 * @param {string} id - The unique identifier for the MindTouch embed, used to construct the script's ID for URL.
 */
const appendTouchpointToBody = (domain, id) => {
  const script = document.createElement("script");
  script.type = "mindtouch/embed";
  script.id = `mindtouch-embed-${id}`;
  script.async = false;
  script.onload = (event) => {
    console.log("Touchpoint loaded successfully.");
    console.log(event);
  };
  document.body.appendChild(script);
  loadScript(`https://${domain}/@embed/${id}.js`);
};

// Example usage
appendTouchpointToBody(
  "spencersso.mindtouch.es",
  "a230965c9cd76ff4ac66dfdc4649d02f1e6bd0d26337282cadbae26d4ba7d7a2"
);

// Wait for search to be ready
document.addEventListener("mindtouch-web-widget:search:loaded", ({ data }) => {
  const embedId = data.embedId;

  // programmable widget interface contains properties and functions
  const widget = data.widget;

  console.log(widget);
  
  // perform a search
  widget.searchQuery = 'code';
});
