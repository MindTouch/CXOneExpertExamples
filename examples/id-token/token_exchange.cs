using System.Dynamic;
using System.Net.Http.Json;
using System.Text;

Console.WriteLine("Exchange an Identity Token for a session");
var identityToken = "REDACTED";
var httpClient = new HttpClient();
var request = new HttpRequestMessage(HttpMethod.Post, "https://customer.mindtouch.us/@app/auth/token/exchange") {
    Content = new StringContent(identityToken,
    Encoding.UTF8,
    "application/json")
};
var response = await httpClient.SendAsync(request);
dynamic userDynamic = await response.Content.ReadFromJsonAsync<ExpandoObject>();
var userJsonDict = new Dictionary<string, object>(userDynamic);
Console.WriteLine("Welcome " + userJsonDict["fullname"] + " where anonymous equals " + userJsonDict["@anonymous"]);