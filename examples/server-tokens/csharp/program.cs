using System;
using System.IO;
using System.Security.Cryptography;
using System.Net.Http;

// Server API Token key and secret are available from API token management dashboard when Server API Token is generated
var key = "REDACTED";
var secret = "REDACTED";

// include username prefixed with '='
var user = "=admin";

// ...or include userid
user = "1";

// hash time, key, user with secret
var hash = "";
var epoch = (int)(DateTime.UtcNow - new DateTime(1970, 1, 1)).TotalSeconds;
using (var hmac = new HMACSHA256(Encoding.ASCII.GetBytes(secret)))
{
    var bytes = hmac.ComputeHash(Encoding.ASCII.GetBytes(string.Format("{0}_{1}_{2}", key, epoch, user)));
    hash = BitConverter.ToString(bytes).Replace("-", "");
}
var signature = string.Format("tkn_{0}_{1}_{2}_{3}", key, epoch, user, hash);

// send signature as X-Deki-Token HTTP header to MindTouch API (WebRequest is used in this example)
var client = new HttpClient();
client.DefaultRequestHeaders.Add("X-Deki-Token", signature);
var response = await client.GetAsync("https://success.mindtouch.com/@api/deki/users/current?dream.out.format=json");
var body = await response.Content.ReadAsStringAsync();
Console.WriteLine(body);
