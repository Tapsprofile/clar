namespace VirtualTryOn.Api.Models;

public sealed record Garment(
    string id,
    string name,
    string imageUrl,
    string? wooProductId
);

