using System.Net.Http.Headers;
using System.Text;
using System.Text.Json;

namespace VirtualTryOn.Api.Services;

// Minimal WooCommerce REST client (stub). Used for syncing products/images into "garments".
public sealed class WooCommerceClient
{
    private readonly HttpClient _http;
    private readonly IConfiguration _config;

    public WooCommerceClient(HttpClient http, IConfiguration config)
    {
        _http = http;
        _config = config;
    }

    public async Task<JsonDocument> GetProductsAsync(CancellationToken ct)
    {
        var baseUrl = _config["WooCommerce:BaseUrl"];
        var key = _config["WooCommerce:ConsumerKey"];
        var secret = _config["WooCommerce:ConsumerSecret"];

        if (string.IsNullOrWhiteSpace(baseUrl) || string.IsNullOrWhiteSpace(key) || string.IsNullOrWhiteSpace(secret))
        {
            throw new InvalidOperationException("WooCommerce credentials missing (WooCommerce:BaseUrl/ConsumerKey/ConsumerSecret).");
        }

        // Woo REST supports query params, but Basic Auth over HTTPS is common for server-to-server.
        var auth = Convert.ToBase64String(Encoding.UTF8.GetBytes($"{key}:{secret}"));
        var req = new HttpRequestMessage(HttpMethod.Get, new Uri(new Uri(baseUrl.TrimEnd('/') + "/"), "wp-json/wc/v3/products?per_page=100"));
        req.Headers.Authorization = new AuthenticationHeaderValue("Basic", auth);

        using var resp = await _http.SendAsync(req, ct);
        resp.EnsureSuccessStatusCode();

        await using var stream = await resp.Content.ReadAsStreamAsync(ct);
        return await JsonDocument.ParseAsync(stream, cancellationToken: ct);
    }
}

