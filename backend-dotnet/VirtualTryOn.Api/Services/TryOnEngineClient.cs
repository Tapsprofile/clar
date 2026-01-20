using System.Net.Http.Headers;

namespace VirtualTryOn.Api.Services;

public sealed class TryOnEngineClient
{
    private readonly HttpClient _http;
    private readonly IConfiguration _config;

    public TryOnEngineClient(HttpClient http, IConfiguration config)
    {
        _http = http;
        _config = config;
    }

    public async Task<byte[]> GenerateAsync(Stream personImage, string personFileName, Stream dressImage, string dressFileName, CancellationToken ct)
    {
        var baseUrl = _config["TryOnEngine:BaseUrl"] ?? throw new InvalidOperationException("TryOnEngine:BaseUrl missing");
        var url = new Uri(new Uri(baseUrl.TrimEnd('/') + "/"), "tryon");

        using var form = new MultipartFormDataContent();

        var personContent = new StreamContent(personImage);
        personContent.Headers.ContentType = new MediaTypeHeaderValue("application/octet-stream");
        form.Add(personContent, "person_image", personFileName);

        var dressContent = new StreamContent(dressImage);
        dressContent.Headers.ContentType = new MediaTypeHeaderValue("application/octet-stream");
        form.Add(dressContent, "dress_image", dressFileName);

        using var resp = await _http.PostAsync(url, form, ct);
        resp.EnsureSuccessStatusCode();
        return await resp.Content.ReadAsByteArrayAsync(ct);
    }
}

