using System.Text.Json;
using VirtualTryOn.Api.Models;
using VirtualTryOn.Api.Services;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddCors(o =>
{
    o.AddDefaultPolicy(p => p
        .AllowAnyHeader()
        .AllowAnyMethod()
        .AllowAnyOrigin());
});

builder.Services.AddHttpClient<TryOnEngineClient>();
builder.Services.AddHttpClient<WooCommerceClient>();

var app = builder.Build();

app.UseCors();
app.UseStaticFiles(); // serves wwwroot/results/*

app.MapGet("/api/health", () => Results.Ok(new { ok = true }));

// MVP garments list. In a real system this comes from DB or Woo sync.
app.MapGet("/api/garments", (HttpRequest req) =>
{
    var baseUrl = $"{req.Scheme}://{req.Host}";
    var garments = new List<Garment>
    {
        new("demo-1", "Demo Dress (Upload your own for best)", $"{baseUrl}/assets/demo-dress.svg", null),
    };
    return Results.Ok(garments);
});

// Main endpoint: upload person + dress images, return stored result URL.
app.MapPost("/api/tryon", async (HttpRequest req, TryOnEngineClient engine, CancellationToken ct) =>
{
    if (!req.HasFormContentType)
        return Results.BadRequest(new { error = "Expected multipart/form-data" });

    var form = await req.ReadFormAsync(ct);
    var person = form.Files.GetFile("personImage");
    var dress = form.Files.GetFile("dressImage");

    if (person is null || dress is null)
        return Results.BadRequest(new { error = "Both personImage and dressImage are required." });

    if (person.Length == 0 || dress.Length == 0)
        return Results.BadRequest(new { error = "Empty file uploaded." });

    await using var personStream = person.OpenReadStream();
    await using var dressStream = dress.OpenReadStream();

    byte[] resultBytes;
    try
    {
        resultBytes = await engine.GenerateAsync(personStream, person.FileName, dressStream, dress.FileName, ct);
    }
    catch (Exception ex)
    {
        return Results.Problem(
            title: "Try-on generation failed",
            detail: ex.Message,
            statusCode: StatusCodes.Status502BadGateway);
    }

    var jobId = Guid.NewGuid().ToString("N");
    var resultsDir = Path.Combine(app.Environment.WebRootPath ?? "wwwroot", "results");
    Directory.CreateDirectory(resultsDir);
    var relPath = $"/results/{jobId}.png";
    var absPath = Path.Combine(resultsDir, $"{jobId}.png");
    await File.WriteAllBytesAsync(absPath, resultBytes, ct);

    var baseUrl = $"{req.Scheme}://{req.Host}";
    return Results.Ok(new TryOnResponse(jobId, $"{baseUrl}{relPath}"));
});

// WooCommerce sync stub: returns raw product JSON for now (BA/dev: replace with mapping + persistence).
app.MapGet("/api/woocommerce/products", async (WooCommerceClient wc, CancellationToken ct) =>
{
    var doc = await wc.GetProductsAsync(ct);
    return Results.Text(doc.RootElement.GetRawText(), "application/json");
});

app.Run();

